#include <iostream>
#include <cmath>


struct passenger
{
    char surname[20];
    int score;
    int seat;
} *list;

void sv_dvh(int seat, int m, int* H)
{
    int i = abs(seat % m);
    int c = 1 + (seat % (m - 2));
    if (H[i] != -1)
    {
        while (true)
        {
            int k = i - c;
            if (H[k] == -1)
            {
                H[k] = seat;
                break;
            }
            i++;
        }
    }
    else H[i] = seat;

}
int sv_search(int seat, int m, int* H)
{
    int i = abs(seat % m);
    while (H[i] != -1)
    {
        if (H[i] == seat) return i;
        i++;
        if (i == m) i = 0;
    }
    return -1;
}

int main()
{
    int n = 0;
    std::cout << "enter the quantity of passengers(<15)\n";
    std::cin >> n;


    std::cout << "\nenter data:\n";
    list = new passenger[n];
    for (int i = 0; i < n; i++)
    {
        std::cout << "\nenter passenger surname\n";
        std::cin >> list[i].surname;

        std::cout << "enter passenger score\n";
        std::cin >> list[i].score;

        std::cout << "enter passenger seat\n";
        std::cin >> list[i].seat;

    }
    std::cout << "\ntable:\n";
    for (int i = 0; i < n; i++)
    {
        std::cout << "surname " << list[i].surname << "\tscore " << list[i].score << "\tseat " << list[i].seat << std::endl;
    }

    const int m = 15; // Число элементов в хеш-таблице
    int H[m];
    for (int i = 0; i < m; i++)
        H[i] = -1; // Все позиции не заняты
    for (int i = 0; i < n; i++) sv_dvh(list[i].seat, m, H);

    int seat;
    std::cout << "enter seat to search\n";
    std::cin >> seat;


    std::cout << "\nhash-table:\n";
    for (int i = 0; i < m; i++)
    {
        std::cout << H[i] << std::endl;
    }
    std::cout << "the seat found\n";
    int k = sv_search(seat, m, H);
    if (k == -1) 
        std::cout << "there is no such seat\n";
    int s = sv_search(seat, m, H);
    for (int i = 0; i < n; i++)
    {
        if (list[i].seat == s) 
            std::cout << "surname " << list[i].surname << "\tscore " << list[i].score << "\tseat " << list[i].seat << std::endl;

    }
}