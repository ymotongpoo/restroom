#include "doubly_linked_list.h"

int main() {
	HashList* hl = new HashList();

	std::string data1 = "hoge";
	std::string data2 = "piyo";
	std::string data3 = "fuga";

	hl->insert_data(data1);
	hl->insert_data(data2);
	hl->insert_data(data3);
	
	hl->print_all();

	hl->delete_data(data2);

	hl->print_all();
	
	return 0;
}
