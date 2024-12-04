#include <sys/ipc.h>
#include <sys/shm.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define SHM_SIZE 1024

int shmgen(int id)
{
    key_t key = ftok("shmfile", id);
    return shmget(key, SHM_SIZE, 0666 | IPC_CREAT);
}

void shmwrite(int shmid, char *str)
{

    char *stored = (char *)shmat(shmid, NULL, 0);
    stored = strcpy(stored, str);
    shmdt(stored);
}

char *shmread(int shmid)
{
    char *stored = (char *)shmat(shmid, NULL, 0);
    char *str = (char *)malloc(SHM_SIZE);
    str = strcpy(str, stored);
    shmdt(stored);
    return str;
}

int shmremove(int shmid)
{
    char *stored = (char *)shmat(shmid, NULL, 0);
    return shmctl(shmid, IPC_RMID, NULL);
}