#include "open_address.h"

int main() {
	OpenAddress* oa = new OpenAddress();
	std::cerr << "----- inserting data" << std::endl;
	oa->insert_data("hoge");
	oa->insert_data("piyo");
	oa->insert_data("fuga");

	oa->print_all();

	std::cerr << "----- deleting data" << std::endl;
	oa->delete_data("fuga");

	oa->print_all();

	return 0;
}
