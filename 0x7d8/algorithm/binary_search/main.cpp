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

	dll->init_addressv();

	dll->print_all();
	
	int length = dll->list_length();
	Cell* ret = dll->binary_search(7, 0, length);
	if (ret != NULL)
		std::cerr << "found -> " << ret->get_data() << std::endl;
	else
		std::cerr << "not found" << std::endl;
	
	return 0;
}
