//Написать программу формирования ОПЗ и расчета полученного выражения.
//Разработать удобный интерфейс ввода исходных данных и вывода результатов.
//Работу программы проверить на конкретном примере.
//       Выражение			  a		  b		  c		  d		  e	   Результат
// |a / (b * (c + d))– e|	|8.5|	|0.3|	|2.4|	|7.9|	|1.6|	|1.151|	

#include <iostream>


struct Stack
{
	char info;			// Символ операции
	Stack* next;
};

struct Dstack
{
	double info;
	Dstack* next;
};
int  Prior(char);
Stack* InS(Stack*, char);
Dstack* InS(Dstack*, double);
Stack* OutS(Stack*, char&);
Dstack* OutS(Dstack*, double&);
void Rezult(char*, Dstack*);

int main()
{
	Stack* t, * Op = NULL;        // Стек операций Op – пуст
	char a, In[81], Out[81];
	// In – входная (S), Out – выходная (B) строки
	int   k = 0, l = 0;
	// Текущие индексы для строк
	std::cout << " Input formula : ";
	std::cin >> In;
	// Анализируем символы строки In 	
	while (In[k] != '\0')
	{
		//  1. Если символ – буква, заносим ее в Out 
		if (In[k] >= 'a' && In[k] <= 'z')
			Out[l++] = In[k];
		//  2. Если «(», записываем ее в стек 
		else
			if (In[k] == '(')
				Op = InS(Op, In[k]);
		/* 3. Если «)», извлекаем из стека в строку Out все операции до открывающей скобки */
			else
				if (In[k] == ')') {
					while ((Op->info) != '(') {
						// Считываем элемент a из стека 
						Op = OutS(Op, a);
						if (!Op) a = '\0';
						// и записываем его в строку Out.
						Out[l++] = a;
					}
					// Удаляем из стека открывающую скобку
					t = Op;
					Op = Op->next;
					delete t;
				}
		/* 4. Если операция, извлекаем из стека в Out операции с большим или равным приоритетом */
				else
					if (In[k] == '+' || In[k] == '-' || In[k] == '*' || In[k] == '/') {
						while (Op != NULL && Prior(Op->info) >= Prior(In[k]))
						{
							Op = OutS(Op, a);
							Out[l++] = a;
						}
						// Текущий символ – в стек
						Op = InS(Op, In[k]);
					}
		k++;
	}		// Конец цикла анализа входной строки
	/* 5. Если стек не пуст, переписываем все операции в выходную строку  */
	while (Op != NULL) {
		Op = OutS(Op, a);
		Out[l++] = a;
	}
	Out[l] = '\0';
	std::cout << "\n Polish = " << Out << std::endl;
	Dstack* b = NULL;
	Rezult(Out, b);
}

int  Prior(char a) {
	switch (a) {
	case '*': 	case '/': 	return 3;
	case '-': 	case '+': 	return 2;
	case '(':   return 1;
	}
	return 0;
}

Stack* InS(Stack* p, char s)
{
	Stack* t = new Stack;
	t->info = s;
	t->next = p;
	return t;
}

Dstack* InS(Dstack* p, double s)
{
	Dstack* t = new Dstack;
	t->info = s;
	t->next = p;
	return t;
}
Stack* OutS(Stack* p, char& s)
{
	Stack* t = p;
	s = p->info;
	p = p->next;
	delete t;
	return p;
}

Dstack* OutS(Dstack* p, double& s)
{
	Dstack* t = p;
	s = p->info;
	p = p->next;
	delete t;
	return p;
}

void View(Dstack* t)
{
	while (t != NULL) {
		std::cout << t->info << std::endl;
		t = t->next;
	}
}
void Rezult(char* Str, Dstack* b)
{
	int i = 0, k = 0;
	double v1, v2;
	double mas[140];
	do
	{
		if (Str[i] >= 'a' && Str[i] <= 'z')
		{
			std::cout << Str[i] << ":";
			std::cin >> mas[int(Str[i])];
			b = InS(b, mas[int(Str[i])]);
		}
		else
		{

			switch (Str[i])
			{
			case '+':
				b = OutS(b, v1);
				b = OutS(b, v2);
				b = InS(b, v1 + v2);
				break;
			case'-':
				b = OutS(b, v1);
				b = OutS(b, v2);
				b = InS(b, v2 - v1);
				break;
			case'*':
				b = OutS(b, v1);
				b = OutS(b, v2);
				b = InS(b, v1 * v2);
				break;
			case'/':
				b = OutS(b, v1);
				b = OutS(b, v2);
				b = InS(b, v2 / v1);
				break;
			}
		}
		i++;
	} while (Str[i] != '\0');
	std::cout << "rezult:";
	View(b);
	delete b;
}
