typedef struct Node {
	void *data;
	struct Node *next;
}Node;

void fromFileToList(Node **head, FILE *f, int quantity);
void add(Node **head, int data);
void writeToFile(Node *head);
void *pop_front(Node **head);
void *pop_back(Node **head);
void copy(Node *head, Node **new_head);
Node *reverse(Node *head);
int main_function(FILE *f);
void printAll(Node *head);
int compare(const void* element1, const void* element2);
void sort(Node** head, int (*comparator)(const void *, const void *));
void sorted_insert(Node **head, Node *element, int (*comparator)(const void *, const void *));
void insert(Node **head, Node *element, Node *before);
