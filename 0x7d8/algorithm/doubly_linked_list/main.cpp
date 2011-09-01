#include "doubly_linked_list.h"

int main() {
	DoublyLinkedList* dll = new DoublyLinkedList();
	for (int i = 1; i < 10; i++) {
		dll->insert_cell(i);
	}
	dll->insert_cell(4);
	dll->insert_cell(-1);
	dll->insert_cell(-100);

	dll->delete_cell(5);
	dll->print_all();
	
	return 0;
}
