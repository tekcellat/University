#include <stdio.h>
#include <windows.h>

#define READERS 5
#define WRITERS 4
#define ITER 10

HANDLE single_mut, event_read, event_write;
HANDLE reader_Threads[READERS], writer_Threads[WRITERS];

int writersID[WRITERS], readersID[READERS];
unsigned int read_count = 0, writ_count = 0;
int value = 0;

volatile LONG active_readers = 0, waiting_readers = 0, waiting_writers = 0;
//CatchProcessMutex  WaitForSingleObject(single_mut, INFINITE);
//ReleaseProcessMutex ReleaseMutex(single_mut);

void StartWrite() {
	InterlockedIncrement(&waiting_writers);
	WaitForSingleObject(single_mut, INFINITE); //catch proc mut
	ResetEvent(event_read);
	++writ_count;
	ReleaseMutex(single_mut);

	WaitForSingleObject(event_write, INFINITE);
	WaitForSingleObject(single_mut, INFINITE);
	InterlockedDecrement(&waiting_writers);
}

void StartRead() {
	InterlockedIncrement(&waiting_readers);
	WaitForSingleObject(event_read, INFINITE);

	WaitForSingleObject(single_mut, INFINITE);
	ResetEvent(event_write);
	++read_count;
	ReleaseMutex(single_mut);
	WaitForSingleObject(single_mut, INFINITE);
	InterlockedDecrement(&waiting_readers);
	InterlockedIncrement(&active_readers);


}

void StopWrite() {
	InterlockedIncrement(&waiting_writers);
	if (!--writ_count) SetEvent(event_read);
	ReleaseMutex(single_mut);
}

void StopRead() {
	InterlockedDecrement(&active_readers);
	if (--read_count == 0) SetEvent(event_write);
	ReleaseMutex(single_mut);
}

DWORD WINAPI Reader(LPVOID param) {
	int num = *(int *)param;

	for (int i = 0; i < ITER; ++i) {
		StartRead();
		printf("Reader %d read %d!\n", num, value);
		StopRead();
		Sleep(500);
	}
	return 0;
}

DWORD WINAPI Writer(LPVOID param) {
	int num = *(int *)param;

	for (int i = 0; i < ITER; ++i) {
		StartWrite();
		printf("Writer %d write %d!\n", num, ++value);
		StopWrite();
		Sleep(1000);
	}
	return 0;
}

void Handles_go() {
	single_mut = CreateMutex(NULL, FALSE, NULL);
	event_read = CreateEvent(NULL, TRUE, TRUE, NULL);
	event_write = CreateEvent(NULL, TRUE, TRUE, NULL);
}

void Create_Threads(void) {
	for (int i = 0; i < WRITERS; ++i) {
		writersID[i] = i;
		writer_Threads[i] = CreateThread(NULL, 0, Writer, (writersID + i), 0, NULL);
	}

	for (int i = 0; i < READERS; ++i) {
		readersID[i] = i;
		reader_Threads[i] = CreateThread(NULL, 0, Reader, (readersID + i), 0, NULL);
	}
}

int main() {
	Handles_go();
	Create_Threads();

	WaitForMultipleObjects(WRITERS, writer_Threads, TRUE, INFINITE);
	WaitForMultipleObjects(READERS, reader_Threads, TRUE, INFINITE);
	return 0;
}