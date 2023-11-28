#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <dirent.h>
#include <errno.h>
#include <semaphore.h>

void copyFile(const char *src, const char *dest) {
    int sourceFile, destFile, bytesRead;
    char buffer[4096];

    sourceFile = open(src, O_RDONLY);
    if (sourceFile == -1) {
        perror("Ошибка открытия файла для чтения");
        exit(EXIT_FAILURE);
    }

    destFile = open(dest, O_WRONLY | O_CREAT, S_IRUSR | S_IWUSR);
    if (destFile == -1) {
        perror("Ошибка открытия/создания файла для записи");
        close(sourceFile);
        exit(EXIT_FAILURE);
    }

    while ((bytesRead = read(sourceFile, buffer, sizeof(buffer))) > 0) {
        if (write(destFile, buffer, bytesRead) != bytesRead) {
            perror("Ошибка записи файла");
            close(sourceFile);
            close(destFile);
            exit(EXIT_FAILURE);
        }
    }

    close(sourceFile);
    close(destFile);
}

int main(int argc, char *argv[]) {
    if (argc < 4) {
        fprintf(stderr, "Использование: %s <Dir1> <Dir2> <N>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    char *dir1 = argv[1];
    char *dir2 = argv[2];
    int numProcesses = atoi(argv[3]);

    struct dirent *entry;
    DIR *dir = opendir(dir1);

    if (dir == NULL) {
        perror("Ошибка открытия директории Dir1");
        exit(EXIT_FAILURE);
    }

    sem_t semaphore;
    sem_init(&semaphore, 0, numProcesses);

    while ((entry = readdir(dir)) != NULL) {
        if (entry->d_type != DT_REG) continue; // Пропускаем не файлы
        char srcPath[256], destPath[256];
        snprintf(srcPath, sizeof(srcPath), "%s/%s", dir1, entry->d_name);
        snprintf(destPath, sizeof(destPath), "%s/%s", dir2, entry->d_name);

        pid_t pid = fork();

        if (pid == 0) {
            sem_wait(&semaphore); // Уменьшаем значение семафора на 1
            printf("PID %d: Копирование файла %s в %s\n", getpid(), srcPath, destPath);
            copyFile(srcPath, destPath);
            printf("PID %d: Файл %s скопирован\n", getpid(), entry->d_name);
            sem_post(&semaphore); // Увеличиваем значение семафора на 1
            exit(0);
        }
    }

    for (int i = 0; i < numProcesses; i++) {
        wait(NULL); // Ожидаем завершения всех процессов
    }

    sem_destroy(&semaphore);
    closedir(dir);
    return 0;
}
