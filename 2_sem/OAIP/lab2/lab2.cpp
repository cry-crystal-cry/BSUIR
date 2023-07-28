#define _CRT_SECURE_NO_WARNINGS
#include <iostream>



struct member {
    char first_name[20], second_name[20], middle_name[20], comand[30], country[30];
    double age, high, weight;
    int number;
}*arr;

void segmentation(member* &a,int l,int r) {

    int i = l, j = r, x = a[(l + r) / 2].age;
    while (i <= j) {
        while (a[i].age < x)  i++;
        while (a[j].age > x)  j--;
        if (i <= j) {
            member r = a[i];
            a[i] = a[j];
            a[j] = r;
            i++; 		j--;
        }
    }
    if (l < j) segmentation(a, l, j);
    if (r > i) segmentation(a, i, r);
}


void quicksort(member*& a, int size) {
    segmentation(a, 0, size-1);
}

void straightsort(member*& a, int n) {
    for (int i = 0; i < n - 1; i++)
        for (int j = i + 1; j < n; j++)
            if (a[i].age > a[j].age) {
                member r = a[i];
                a[i] = a[j];
                a[j] = r;
            }
}

void read(member*& arr, int n) {
    std::cout << "enter the path to the file\n";
    char path[50];
    std::cin >> path;
    FILE* in = fopen(path, "r");
    if (!in) {
        std::cout << "error\n";
        read(arr, n);
    }
    else for (int i = 0; i < n; i++) 
        fscanf(in, "%s %s %s %d %lf %lf %lf %s %s", &(arr[i].first_name), &(arr[i].second_name), &(arr[i].middle_name), &(arr[i].number), &(arr[i].age), &(arr[i].high), &(arr[i].weight), &(arr[i].country), &(arr[i].comand));
    
    fclose(in);
}

void show(member* arr,int n) {
    FILE* out = fopen("2.txt", "w");
    for (int i = 0; i < n; i++){
        fprintf(out, "%s %s %s %d %lf %lf %lf %s %s\n", arr[i].first_name, arr[i].second_name, arr[i].middle_name, arr[i].number, arr[i].age, arr[i].high, arr[i].weight, arr[i].country, arr[i].comand);
        printf("%s %s %s %d %lf %lf %lf %s %s\n", arr[i].first_name, arr[i].second_name, arr[i].middle_name, arr[i].number, arr[i].age, arr[i].high, arr[i].weight, arr[i].country, arr[i].comand);
    }
    fclose(out);
}

void show(member arr) {
    FILE* out = fopen("2.txt", "w");
    fprintf(out, "%s %s %s %d %lf %lf %lf %s %s\n", arr.first_name, arr.second_name, arr.middle_name, arr.number, arr.age, arr.high, arr.weight, arr.country, arr.comand);
    printf("%s %s %s %d %lf %lf %lf %s %s\n", arr.first_name, arr.second_name, arr.middle_name, arr.number, arr.age, arr.high, arr.weight, arr.country, arr.comand);
}

void choose(int n) {
    int count;
    printf("\n\tenter 1 for quicksort\n\t2 for straightsort ");
    scanf("%d", &count);
    if (count == 1) {
        quicksort(arr, n);
        show(arr, n);
    }
    else if (count == 2){
        straightsort(arr, n);
        show(arr, n);
    }
    else choose(n);
}
bool compare(char* a, char* b) {
    int lena = 0, lenb = 0;
    while (a[lena] != '\0')lena++;
    while (b[lenb] != '\0')lenb++;
    if (lena == lenb) {
        bool add = true;
        for (int i = 0; (i < lena) && add; i++)
            if (a[i] != b[i]) add = false;
        return add;
    }
    else return false;
}
void youngest(member*& a, int n) {
    char** com = new char*[n];

    for (int i = 0; i < n; i++) 
        com[i] = new char[30]{'e'};

    int s = 0;
    bool add;

    for (int i = 0; i < n; i++) {
        add = true;
        for (int j = 0; ((j < s) && add); j++) {
            if (compare(a[i].comand, com[j]))
            {
                add = false;
            }
        }

        if (add) 
            com[s++] = a[i].comand;
        
    }
    
    int* uses = new int[s]{0};
    double* average = new double[s]{0};
    for (int i = 0; i < s; i++)
        for (int j = 0; j < n; j++)
            if (compare(com[i], a[j].comand))  
            {
                uses[i]++;
                average[i] += a[j].age;
            }
        
    double min=average[0];
    int index=-1;
    for (int i = 0; i < s; i++)
    {
        average[i] /= uses[i];
        if (average[i] <= min) {
            min = average[i];
            index = i;
        }
    }

    for (int i = 0; i < n; i++)
        if (compare(com[index], a[i].comand))
            show(a[i]);

   

    /*for (int i = 0; i < s; i++)
        delete[] com[i];*/
    

    delete[] com;

    delete[] uses;

}

int main() {
    setlocale(LC_ALL, "Russian");
    int n;
    std::cout << "enter the quantity of members\n";
    std::cin >> n;
    arr = new member[n];
    read(arr, n);
    show(arr, n);

    choose(n);

    printf("\n\n\n THE YOUNGEST TEAM\n\n");
    youngest(arr,n);
       
    delete[] arr;
    return 0;
}

