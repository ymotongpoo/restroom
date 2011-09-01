#include "circularly_linked_list.h"

using std::cerr; using std::endl;

int main() {
	CircularlyLinkedList* cll = new CircularlyLinkedList();

	for (int i = 1; i < 10; i++) {
		cll->insert_cell(i);
	}
	cll->insert_cell(4);
	cll->insert_cell(-1);
	cll->insert_cell(-100);

	cll->delete_cell(5);
	cll->print_all();

	return 0;
}
