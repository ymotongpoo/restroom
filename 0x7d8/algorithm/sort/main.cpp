#include <iostream>
#include <cstdlib>
#include <vector>
#include "mysort.h"

const int DIVIDER = 100;

int main() {
	std::vector<int> source;
	std::srand((unsigned) time(NULL));
	for (int i = 0; i < 20; i++) {
		source.push_back(rand() % DIVIDER);
	}

	std::cerr << "----- source -----" << std::endl;
	for (int i = 0; i < 20; i++) {
		std::cerr << source[i] << std::endl;
	}

	//Sort::bubble_sort(source);
	//Sort::selection_sort(source);
	//Sort::insertion_sort(source);
	//Sort::shell_sort(source, Sort::SHELL_SORT_INTERVAL);
	Sort::quick_sort(source);
	//Sort::merge_sort(source);

	std::cerr << "----- result -----" << std::endl;
	for (int i = 0; i < 20; i++) {
		std::cerr << source[i] << std::endl;
	}
}
