# agent_service.py
import asyncio
from typing import List, AsyncGenerator
from functools import partial

from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_classic.chains.llm_math.base import LLMMathChain
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import Tool
from langchain_ollama import ChatOllama

from services.document_service import DocumentService
from tools.library_tools import get_available_book_count_by_author, get_book_info, get_last_book_from_author, \
    get_book_author
from tools.weather_tool import get_weather

class AgentService:
    def __init__(self, document_service: DocumentService, llm_weight: float = 0.7,
                 ):
        self.document_service = document_service
        self.llm_weight = llm_weight
        self.document_service = document_service

        self.llm = ChatOllama(
            model="llama3.2",
            temperature=0.3,
            num_ctx=4096,
            streaming=True
        )

        math_chain = LLMMathChain.from_llm(llm=self.llm)

        self.base_tools = [
            Tool(
                name="WeatherAPI",
                func=get_weather,
                description="Retrieves current weather for a specified city. Use only this tool to answer questions about weather."
            ),
            Tool(
                name="MathCalculator",
                func=math_chain.run,
                description="Calculates mathematical expressions. Use only this tool for math problems."
            ),
            get_available_book_count_by_author,
            get_book_info,
            get_last_book_from_author,
            get_book_author,
        ]

        self.prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=(
                        "Ты — полезный помощник. "
                        "Отвечай только на русском языке. "
                        "Используй инструменты только при необходимости и строго по их назначению:\n"
                        "- WeatherAPI: только для вопросов о погоде в городах.\n"
                        "- MathCalculator: только для математических выражений и задач.\n"
                        "- Инструменты библиотеки (книги, авторы): использовать только если вопрос явно касается литературы.\n"
                        "- Для всех остальных вопросов используй RAG-контекст и свои знания.\n"
                        "Не вызывай лишние инструменты, если они не относятся к вопросу. "
                        "Если можно ответить напрямую — отвечай без инструментов."
                        "Ты — агент с доступом к инструментам. "
                        "Если вопрос требует вызова инструмента — вызывай его напрямую, не описывай. "
                        "Не объясняй, как использовать инструмент — просто вызови его! "
                        "Ты работаешь в среде, где инструменты доступны и будут выполнены!"
                    )
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

    def _get_agent_executor(self, chat_id: int) -> AgentExecutor:
        all_tools = self.base_tools
        agent = create_tool_calling_agent(
            self.llm,
            all_tools,
            self.prompt,
        )

        return AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=all_tools,
            verbose=True,
            handle_parsing_errors=True,
            return_intermediate_steps=True

        )

    async def get_rag_context(self, chat_id: int, query: str) -> str:
        """
        Возвращает объединенный текст всех релевантных документов,
        отфильтрованных по комбинированной оценке LLM + векторной.
        """
        results = await self.document_service.search(chat_id, query, top_k=20)

        # Сортируем по score
        sorted_results = sorted(results, key=lambda r: r["score"], reverse=True)

        topn = sorted_results[:10]

        # Логируем кратко: score + начало текста
        print("[RAG LOG] Найдено чанков:", len(topn))
        for idx, r in enumerate(topn, 1):
            snippet = r["text"][:80].replace("\n", " ")  # первые 80 символов
            print(f"  {idx}. score={r['score']:.3f}, text='{snippet}...'")

        # Возвращаем текст
        top5_texts = [r["text"] for r in topn]
        return "\n".join(top5_texts)

    async def arun_agent_stream(
            self,
            chat_id: int,
            input_query: str,
            history_messages: List[BaseMessage]
    ) -> AsyncGenerator[str, None]:

        rag_context = await self.get_rag_context(chat_id, input_query)
        full_input = f"[RAG контекст]:\n{rag_context}\n\n[Вопрос]: {input_query}" if rag_context else input_query

        agent_executor = self._get_agent_executor(chat_id)
        input_data = {
            "input": full_input,
            "chat_history": history_messages
        }

        used_tools = set()
        streamed_output = False

        try:
            async for chunk in agent_executor.astream(input_data):
                # Если есть результат инструмента — вставляем его
                if "intermediate_steps" in chunk and chunk["intermediate_steps"]:
                    for action, result in chunk["intermediate_steps"]:
                        tool_name = getattr(action, "tool", None)
                        if tool_name:
                            used_tools.add(tool_name)
                            if result:
                                yield f"[{tool_name}] → {str(result).strip()}\n"

                # Если есть финальный текст — стримим его
                if "output" in chunk:
                    token = chunk["output"]
                    if token and not token.strip().startswith("[{"):
                        streamed_output = True
                        yield token

            # Вставляем инфо об инструментах
            if used_tools:
                tools_list = ", ".join(sorted(used_tools))
                yield f"\nДля ответа использованы инструменты: {tools_list}"


        except Exception as e:
            yield f"\n[ОШИБКА ГЕНЕРАЦИИ ОТВЕТА АГЕНТОМ]: {e}"

