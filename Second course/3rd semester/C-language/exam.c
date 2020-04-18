#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

//Это +- то, что я запомнил с экзамена. Я если честно уже ХЗ что оно должно делать. Но компилится! Это важнее :))

struct TList{
   int value;
   struct TList* next;
};
struct TList* Push(struct TList** list, int value){
   struct TList* node = (struct TList*) malloc(sizeof(struct TList));
   node->value = value;
   node->next = *list;
   //t->Prev=NULL;
   *list = node;
   return *list;
}
void Print(struct TList* list){
   printf("Linked list: ");
   while (list){
      fprintf(stdout, "%d ", list->value);
      list = list->next;
   }
}
bool Load(const char* fname, struct TList** list){
   FILE* f = fopen(fname, "r");
   if (f == NULL) {return false;}
   int value = 0;
   while (feof(f) == false){
      if (fscanf(f, "%d", &value) == 1) {Push(list, value);}
   }
   fclose(f);
   return true;
}

float Average(struct TList* list){
   if (!list) 
         return -1; 
   int count = 0, sum = 0; // Initialize count  
   float avg = 0.0; 
   struct TList* current = list; // Initialize current 
      while (current != NULL) { 
         count++; 
         sum += current->value; 
         current = current->next; 
      } 
      avg = (double)sum / count; 
      printf("\nAverage: %f", avg);
}

/*
void DelMaxMid(TList* list){  //Удалить из списка все элементы, большие среднего арифметического
   TList*key=NULL;
   t=node;
   while(t!=NULL){
      t=node;
      while(t!=NULL){  //иду по списку, пока не найду тот эл-т, который больше s_ar;   //среднее арифметическое
         if(t->info>avg){
            key=t;
            break;
         }
         t=t->Next;
      }
      if(key!=NULL){   //cамо удаление из списка
         if(key==node){  //если элемент расположен в начале
            node=node->Next;
            node->Prev=NULL;
         }
         else{
            if(key==end){    //если он в конце   
               end=end->Prev;
               end->Next=NULL;
               }
            else{   //или в "теле"
               (key->Prev)->Next=key->Next;
               (key->Next)->Prev=key->Prev;
            }
         }
         free(key);  //затираю память
         key=NULL;
      }   
      else t=t->Next;
   }   
}
*/

int main(int argc, const char* argv[])
{
   if (argc != 2){
      fprintf(stderr, "Example: program.exe file_name.txt\n");
      return EXIT_FAILURE;
   }
   struct TList* list = NULL;
   if (Load(argv[1], &list) == false){
      fprintf(stderr, "Error: file '%s' not load ...\n", argv[1]);
      return EXIT_FAILURE;
   }
   Print(list);
   Average(list);
   return EXIT_SUCCESS;
}
