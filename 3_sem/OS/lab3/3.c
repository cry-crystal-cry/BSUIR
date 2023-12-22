#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <curl/curl.h>

// Файл для записи логов
FILE *logFile;

// Структура для передачи аргументов в поток
typedef struct {
    char *imageURL;
    int threadIndex;
} ThreadArgs;

// Мьютекс для синхронизации доступа к операции загрузки
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

// Функция, выполняемая в каждом потоке
void *downloadImage(void *arg) {
    ThreadArgs *threadArgs = (ThreadArgs *)arg;
    char *imageURL = threadArgs->imageURL;
    int threadIndex = threadArgs->threadIndex;
    
    // Захват мьютекса
    pthread_mutex_lock(&mutex);

    // Запись операции в лог файл
    fprintf(logFile, "Thread %d: Downloading image: %s\n", threadIndex, imageURL);
    
    fclose(logFile);
    // Открытие лог файла
    logFile = fopen("log.txt", "a+");

    // Парсинг имени файла из URL-адреса
    char *ptr = strrchr(imageURL, '/');
    char imageName[100];
    if (ptr) {
        strcpy(imageName, ptr + 1);
    } else {
        fprintf(logFile, "Thread %d: Invalid image URL: %s\n", threadIndex, imageURL);
         // Освобождение мьютекса
        pthread_mutex_unlock(&mutex);
        pthread_exit(NULL);
    }
    
    // Создание папки 'images' при необходимости
    struct stat st = {0};
    if (stat("images", &st) == -1) {
        if (mkdir("images", 0777) != 0) {
            fprintf(logFile, "Thread %d: Unable to create 'images' folder: %s\n", threadIndex, strerror(errno));
             // Освобождение мьютекса
            pthread_mutex_unlock(&mutex);
            pthread_exit(NULL);
        }
    }

    // Формирование пути к сохраняемому файлу
    char imageSavePath[200];
    snprintf(imageSavePath, sizeof(imageSavePath), "./images/%s", imageName);

    // Инициализация сеанса cURL
    CURL *curl = curl_easy_init();
    if (curl) {
        FILE *imageFile = fopen(imageSavePath, "ab");
        if (imageFile) {
            // Настройка cURL URL
            curl_easy_setopt(curl, CURLOPT_URL, imageURL);
            // Настройка файла для добавления данных
            curl_easy_setopt(curl, CURLOPT_WRITEDATA, imageFile);
            
            // Выполнение запроса и скачивание файла
            CURLcode res = curl_easy_perform(curl);
            if (res != CURLE_OK) {
                fprintf(logFile, "Thread %d: Failed to download image: %s\n", threadIndex, curl_easy_strerror(res));
            } else {
                // Получение текущей позиции в файле для определения количества скачанных байт
                off_t fileSize = ftello(imageFile);
                fprintf(logFile, "Thread %d: Downloaded %lld bytes\n", threadIndex, (long long int)fileSize);
            }
            
            fclose(imageFile);
        } else {
            fprintf(logFile, "Thread %d: Failed to create image file: %s\n", threadIndex, strerror(errno));
        }
        
        // Освобождение ресурсов cURL
        curl_easy_cleanup(curl);
    } else {
        fprintf(logFile, "Thread %d: Failed to initialize cURL session.\n", threadIndex);
    }
     // Освобождение мьютекса
    pthread_mutex_unlock(&mutex);
    
    pthread_exit(NULL);
}

int main() {
    // Открытие лог файла для записи
    logFile = fopen("log.txt", "a+");
    if (logFile == NULL) {
        printf("Unable to open log file.\n");
        exit(1);
    }

    // Путь к изображению
    char imageURL[200];
    
    // Ввод URL-адреса изображения
    printf("Enter the image URL: ");
    scanf("%s", imageURL);
    
    // Инициализация библиотеки cURL
    CURLcode res = curl_global_init(CURL_GLOBAL_DEFAULT);
    if (res != CURLE_OK) {
        fprintf(logFile, "Failed to initialize cURL: %s\n", curl_easy_strerror(res));
        exit(1);
    }

    // Создание потоков
    pthread_t threads[4];
    ThreadArgs threadArgs[4];
    for (int i = 0; i < 4; ++i) {
        threadArgs[i].imageURL = imageURL;
        threadArgs[i].threadIndex = i + 1;
        int result = pthread_create(&threads[i], NULL, downloadImage, (void *)&threadArgs[i]);
        if (result != 0) {
                    fprintf(logFile, "Thread creation failed.\n");
            exit(1);
        }
    }
    
    // Ожидание завершения потоков
    for (int i = 0; i < 4; ++i) {
        pthread_join(threads[i], NULL);
    }

    // Закрытие лог файла
    fclose(logFile);
    
    // Очистка ресурсов библиотеки cURL
    curl_global_cleanup();
    
    return 0;
}