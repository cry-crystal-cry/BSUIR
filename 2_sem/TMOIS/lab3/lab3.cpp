#include <iostream>
#include <vector>
#include <utility>


typedef std::vector<std::pair<int, int>> graphic;

graphic createGraphic() {
    using namespace std;
    graphic A;
    cout << "Введите мощность графика:"; //Пользователь задаёт мощность графика A
    int count;
    cin >> count;
    cout << "Вводите пары графика:";
    for (int i = 0; i < count; i++) {    //Пользователь вводит пары графика A
        int el1, el2;
        cin >> el1;
        cin >> el2;
        A.push_back(make_pair(el1, el2));
    }
    return A;
}

graphic unite(const graphic A, const graphic B) {
    graphic D;  //Создаём пустой график D
    D = A;      //Каждый элемент графика A переносим в график D
    int counterD,counterB;
    std::pair<int, int> pairD, pairB;

    counterB = 0;//Возьмём первую пару графика В
    pairB = B[counterB];

    p3_4:
    counterD = 0;//Возьмём первую пару графика D
    pairD = D[counterD];

    p3_5:       //Проверим, не равны ли пары
    if (pairB.first != pairD.first)    goto p3_7;   //Если первый элемент взятой пары графика В не равен первому элементу взятой пары графика D, переходим к пункту 3.7
    if (pairB.second != pairD.second)  goto p3_7;   //Если второй элемент взятой пары графика В не равен второму элементу взятой пары графика D, переходим к пункту 3.7
    goto p3_11; //Переходим к пункту 3.11

    p3_7:
    if (counterD == (D.size() - 1)) goto p3_10;    //Если взятая пара графика D – последняя, переходим к пункту 3.10

    pairD = D[++counterD];  //Возьмём следующую пару графика D
    goto p3_5;              //Перейдём к пункту 3.5

    p3_10:
    D.push_back(pairB); //Добавим взятую пару графика B в график D

    p3_11:
    if (counterB == (B.size() - 1)) return D;  //Если взятая пара графика В – последняя, то переходим к пункту 14

    pairB = B[++counterB];  //Возьмём следующую пару графика В
    goto p3_4;              //Перейдём к пункту 3.4
}

graphic intersect(const graphic A, const graphic B) {
    graphic D;      //Создадим новый пустой график D
    int counterA, counterB;
    std::pair<int, int> pairA, pairB;

    counterA = 0;   //Возьмём первую пару графика A
    pairA = A[counterA];

    p4_3:
    counterB = 0;   //Возьмём первую пару графика В
    pairB = B[counterB];

    p4_4:           //Проверим неравны ли пары
    if (pairA.first != pairB.first)   goto p4_7;    //Если первый элемент взятой пары графика А не равен первому элементу взятой пары графика В, то переходим к пункту 4.7
    if (pairA.second != pairB.second) goto p4_7;    //Если второй элемент взятой пары графика А не равен второму элементу взятой пары графика В, то переходим к пункту 4.7
    D.push_back(pairA); //Добавляем взятую пару графика А в график D
    goto p4_10;         //Переходим к пункту 4.10

    p4_7:
    if (counterB == (B.size() - 1)) goto p4_10;    //Если взятая пара графика В – последняя, то переходим к пункту 4.10

    pairB = B[++counterB];  //Возьмём следующий элемент графика В
    goto p4_4;              //Перейдём к пункту 4.4

    p4_10:
    if (counterA == (A.size() - 1)) return D;  //Если взятая пара графика А – последняя, то переходим к пункту 14

    pairA = A[++counterA];  //Возьмём следующую пару графика А
    goto p4_3;              //Перейдём к пункту 4.3
}

graphic diff(const graphic A, const graphic B) {
    graphic D;      //Создадим новый пустой график D
    int counterA, counterB;
    std::pair<int, int> pairA, pairB;

    counterA = 0;   //Возьмём первую пару графика A
    pairA = A[counterA];

    p5_3:
    counterB = 0;   //Возьмём первую пару графика В
    pairB = B[counterB];

    p5_4:   //Проверим равны ли графики
    if (pairA.first != pairB.first)   goto p5_5;    //Если первый элемент взятой пары графика А не равен первому элементу взятой пары графика В, перейдём к пункту 5.5
    if (pairA.second == pairB.second) goto p5_9;    //Если второй элемент взятой пары графика А равен второму элементу взятой пары графика В, перейдём к пункту 5.9

    p5_5:
    if (counterB == (B.size() - 1)) goto p5_8;     //Если взятая пара графика В является последней, перейдём к пункту 5.8

    pairB = B[++counterB];  //Возьмём следующую пару графика В
    goto p5_4;              //Перейдём к пункту 5.4

    p5_8:
    D.push_back(pairA); //Добавляем взятую пару графика А в график D.

    p5_9:
    if (counterA == (A.size() - 1)) return D;  //Если взятая пара графика А является последней, перейдём к пункту 14

    pairA = A[++counterA];  //Возьмём следующую пару графика А
    goto p5_3;              //Перейдём к пункту 5.3

    
}

graphic sym_diff(const graphic A, const graphic B) {
    return unite(diff(A,B), diff(B,A));
}

graphic universum() {
    graphic U;
    int x, y;

    x = 1;  //Присвоим значение x = 1
    y = 0;  //Присвоим значение y = 0

p8_1_3:
    if (y >= 100) goto p8_1_5;  //Если значение y больше или равно 100, перейдём к пункту 8.1.5

    goto p8_1_8;    //Перейдём к пункту 8.1.8

p8_1_5:
    x++;    //x = x + 1

    if (x > 100) return U;  //Если значение x больше 100, перейдём к пункту 8.2
    y = 0;                  //y = 0

p8_1_8:
    y++;    //y = y + 1

    std::pair<int, int> f = std::make_pair(x, y); //Создадим пару f, где первая компонента будет равна x, а вторая компонента будет равна y
    U.push_back(f); //Добавим созданную пару в график U
    goto p8_1_3;    //Перейдём к пункту 8.1.3
}

graphic complement(const graphic A) {
    return diff(universum(), A);
}

graphic inverse(const graphic A) {
    graphic D;  //Создадим пустой график D
    int counterA;
    std::pair<int, int> pairA, f;

    counterA = 0;   //Возьмём первую пару графика A
    pairA = A[counterA];

    p10_3:
    f = std::make_pair(pairA.second, pairA.first);   //Создадим пару f, где первая компонента будет равна второй компоненте взятой пары графика А, 
                                                     //а вторая компонента будет равна первой компоненте взятой пары графика А
    D.push_back(f); //Добавляем пару f в график D

    if (counterA == (A.size() - 1)) return D;   //Если взятая пара графика А является последней, переходим к пункту 14
    pairA = A[++counterA];  //Выбираем следующая пару графика А
    goto p10_3; //Переходим к пункту 10.3
}

graphic compose(const graphic A, const graphic B) {
    graphic D;
    std::pair<int, int> pairA, pairB, f, pairD;
    int counterA, counterB, counterD;

    counterA = 0;   //Возьмём первую пару графика A
    pairA = A[counterA];

    p12_3:
    counterB = 0;   //Возьмём первую пару графика В
    pairB = B[counterB];

    p12_4:
    if (pairA.second != pairB.first) goto p12_7;    //Если вторая компонента взятой пары графика А не равна первой компоненте взятой пары графика В, переходим к пункту 12.7
    
    f = std::make_pair(pairA.first, pairB.second);  //Создадим пару f, где первая компонента будет равна первой компоненте взятой пары графика А, 
                                                    //а вторая компонента будет равна второй компоненте взятой пары графика В

    //Проверим не повторится ли пара f в графике D
    if (D.empty()) goto p12_6_9;    //Если график D – пустой, переходим к пункту 12.6.9

    counterD = 0;   //Возьмём первую пару графика D
    pairD = D[counterD];

    p12_6_3:
    if (pairD.first != f.first)   goto p12_6_6;     //Если первый элемент взятой пары графика D не равен первому элементу пары f, переходим к пункту 12.6.6
    if (pairD.second != f.second) goto p12_6_6;     //Если второй элемент взятой пары графика D не равен второму элементу пары f, переходим к пункту 12.6.6
    goto p12_7; //Переходим к пункту 12.7
    
    p12_6_6:
    if (counterD == (D.size() - 1)) goto p12_6_9;   //Если взятая пара графика D является последней, переходим к пункту 12.6.9
    
    pairD = D[++counterD];  //Выбираем следующую пару графика D
    goto p12_6_3;   //Переходим к пункту 12.6.3
    
    p12_6_9:
    D.push_back(f); //Добавим пару f в график D

    p12_7:
    if (counterB == (B.size() - 1)) goto p12_10; //Если выбранная пара графика B является последней, переходим к пункту 12.10
    
    pairB = B[++counterB];  //Выбираем следующую пару графика В
    goto p12_4;             //Переходим к пункту 12.4
    
    p12_10:
    if (counterA == (A.size() - 1)) return D;    //Если выбранная пара графика А является последней, переходим к пункту 14
    
    pairA = A[++counterA];  //Выбираем следующую пару графика А
    goto p12_3;             //Переходим к пункту 12.3
}

void show(graphic A) {
    using namespace std;
    cout << "\nГрафик D = { ";
    for (int i = 0; i < A.size(); i++) {
        cout << "<" << A[i].first << "," << A[i].second << ">, ";
    }
    if (A.size()) cout<<"\b";
    cout << "\b }\n\n";
}



int main()
{
    using namespace std;
    setlocale(LC_ALL, "rus");
    graphic A, B, D;
    A = createGraphic();   //Пользователь задает график A
    B = createGraphic();   //Пользователь задает график В

    START:
    //Пользователь задает операцию над графиками А и В
    cout << "Выберите операцию над графиками:\n" 
        "\t1. Объединение графиков А и В\n"
        "\t2. Пересечение графиков А и В\n"
        "\t3. Разность графиков А и В\n"
        "\t4. Разность графиков В и А\n"
        "\t5. Симметрическая разность графиков А и В\n"
        "\t6. Дополнение графика А\n"
        "\t7. Дополнение графика В\n"
        "\t8. Инверсия графика А\n"
        "\t9. Инверсия графика В\n"
        "\t10. Композиция графиков А и В\n"
        "\t11. Композиция графиков В и А\n"
        "Ваш выбор: ";
    int choose;
    cin >> choose;

    switch (choose) {
        case 1:{
            D = unite(A, B);
            break;
        }
        case 2: {
            D = intersect(A, B);
            break;
        }
        case 3: {
            D = diff(A, B);
            break;
        }
        case 4: {
            D = diff(B, A);
            break;
        }
        case 5: {
            D = sym_diff(A, B);
            break;
        }
        case 6: {
            D = complement(A);
            break;
        }
        case 7: {
            D = complement(B);
            break;
        }
        case 8: {
            D = inverse(A);
            break;
        }
        case 9: {
            D = inverse(B);
            break;
        }
        case 10: {
            D = compose(A, B);
            break;
        }
        case 11: {
            D = compose(B, A);
            break;
        }
    }

    show(D);    //Выведем на экран полученный график D

    //Предлагаем пользователю повторно выполнить одну из операций или завершить работу
    cout<< "Для того, чтобы повторно выполнить одну из операций нажмите \"1\" \t Для завершения работы нажмите \"2\" \n";
    cin >> choose;
    if (choose == 1) goto START;    //Если пользователь нажал "1", возвращаем его к выбору операции

    return 0;	//Завершаем работу программы по требованию пользователя
}//Ilysha molodec
