#include "linked_list.h"

int main() {
	LinkedList* ll = new LinkedList();
	for (int i = 1; i < 10; i++) {
		ll->insert_cell(i);
	}
	ll->insert_cell(4);
	ll->insert_cell(-1);
	ll->insert_cell(-100);

	ll->delete_cell(5);
	ll->print_all();
	
	return 0;
}
