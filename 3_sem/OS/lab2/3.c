#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

int main(){
	//1 процесс
	printf("Создан 1 процесс: pid=%d <-- ppid=%d\n", getpid(), getppid());
	
	//2 процесс
	if(fork()==0){
		printf("Создан 2 процесс: pid=%d <-- ppid=%d\n", getpid(), getppid());
		//3 процесс
		if(fork()==0){
			printf("Создан 3 процесс: pid=%d <-- ppid=%d\n", getpid(), getppid());
			//5 процесс
			if(fork()==0){
				printf("Создан 5 процесс: pid=%d <-- ppid=%d\n", getpid(), getppid());
				//7 процесс
				if(fork()==0){
					printf("Создан 7 процесс: pid=%d <-- ppid=%d\n", getpid(), getppid());
				}		
			}
		}
		else{		
			//4 процесс
			if(fork()==0){
				printf("Создан 4 процесс: pid=%d <-- ppid=%d\n", getpid(), getppid());
				//6 процесс
				if(fork()==0){
					printf("Создан 6 процесс: pid=%d <-- ppid=%d\n", getpid(), getppid());
				}
			}
		}
	}
	else{
		while (wait(NULL)>0);
		printf("Запуск указанной проограммы вместо 1 процесса <-- ppid=%d\n", getpid());
		system("pwd");
	}
	
while (wait(NULL)>0);
printf("Завершается процесс: pid=%d <-- ppid=%d\n", getpid(), getppid());

return 0;	
}
