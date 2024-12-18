#include <iostream>
#include <ctime>
#include <cmath>
#include <cstring>



const int ALPHABET_CARDINALITY = 26;

char get_char(int number)
{
    if (number < ALPHABET_CARDINALITY)
        return 'A' + number;
    else
        return 'a' + (number - ALPHABET_CARDINALITY);
}

int get_char_index(char c)
{
    if (c >= 'A' && c <= 'Z')
        return c - 'A';
    else
        return c - 'a' + ALPHABET_CARDINALITY;
}

void generate_password(char* password, int* frequencies, int length)
{
    for (int i = 0; i < length; i++)
    {
        int index = std::rand() % (ALPHABET_CARDINALITY * 2);
        frequencies[index]++;
        password[i] = get_char(index);
    }
    password[length] = '\0';
}

void increase_string(char* string, int length, int index = 0)
{
    if (index == length)
        return;

    if (string[index] == 'z')
    {
        string[index] = 'A';
        increase_string(string, length, index + 1);
    }
    else
    {
        string[index] = get_char(get_char_index(string[index]) + 1);
    }
}

char* find_password(const char* target_password, int length)
{
    char* found_password = new char[length + 1];
    std::fill(found_password, found_password + length, 'A');
    found_password[length] = '\0';

    do
    {
        if (std::strcmp(found_password, target_password) == 0)
            return found_password;

        increase_string(found_password, length);
    } while (found_password[length - 1] != 'z');

    delete[] found_password;
    return nullptr;
}

int main()
{
    setlocale(LC_ALL, ""); 
    std::srand(static_cast<unsigned>(std::time(0)));

    std::cout << "Введите длину пароля:\n";
    int length;
    std::cin >> length;

    if (length <= 0)
    {
        std::cerr << "Недопустимая длина пароля." << std::endl;
        return 1;
    }

    char* password = new char[length + 1];
    int frequencies[ALPHABET_CARDINALITY * 2] = { 0 };

    generate_password(password, frequencies, length);

    std::cout << "Пароль: " << password << std::endl << "Частотное распределение:" << std::endl;
    for (int i = 0; i < ALPHABET_CARDINALITY * 2; i++)
        std::cout << get_char(i) << '\t' << frequencies[i] << std::endl;

    time_t start_time = std::time(0);
    char* found_password = find_password(password, length);
    time_t finding_time = std::time(0) - start_time;    

    if (found_password != nullptr)
    {
        std::cout << "Время подбора пароля " << found_password << ": " << finding_time << " сек." << std::endl;
        delete[] found_password;
    }
    else
    {
        std::cout << "Пароль не найден." << std::endl;
    }

    delete[] password;
    return 0;
}   
