#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/time.h>
#include <time.h>

void print_time() {
time_t now = time(NULL);
    struct tm *tm_struct = localtime(&now);
    struct timeval t;
    gettimeofday(&t, NULL);
    printf("время: %d:%d:%d:%ld\n", tm_struct->tm_hour, tm_struct->tm_min, tm_struct->tm_sec, t.tv_usec/1000);
}

int main() {
    pid_t child1, child2;
    
    printf("Родительский процесс: pid=%d <-- ppid=%d, ", getpid(), getppid());
    print_time();
    
    child1 = fork();
    if(child1==0){
        printf("Дочерний процесс 1: pid=%d <-- ppid=%d, ", getpid(), getppid());
        print_time();
        exit(0);
        } else if(child1==-1) {
        perror("Ошибка вызова fork() для 1 дочернего процесса");
        exit(1);
      } else{
      wait(NULL);  
      }
      
    child2 = fork();
    if(child2==0){
        printf("Дочерний процесс 2: pid=%d <-- ppid=%d, ", getpid(), getppid());
        print_time();
        exit(0);
        } else if(child2==-1){
        perror("Ошибка вызова fork() для 2 дочернего процесса");
        exit(1);
      } else{
      wait(NULL);  
      }      
      system("ps -x");
    return 0;
    }
