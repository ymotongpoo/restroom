#ifndef MYSORT_H
#define MYSORT_H

#include <iostream>
#include <vector>

class Sort {
public:
	static const int SHELL_SORT_INTERVAL = 3;

	static void bubble_sort(std::vector<int>& _source);
	static void selection_sort(std::vector<int>& _source);
	static void insertion_sort(std::vector<int>& _source);
	static void shell_sort(std::vector<int>& _source, int _interval);
	static void merge_sort(std::vector<int>& _source);
	static void heap_sort(std::vector<int>& _source);
	static void quick_sort(std::vector<int>& _source);
	static void intro_sort(std::vector<int>& _source);
	static void share_sort(std::vector<int>& _source);
	static void in_place_merge_sort(std::vector<int>& _source);
	static void cocktail_sort(std::vector<int>& _source);
	static void comb_sort(std::vector<int>& _source);
	static void gnome_sort(std::vector<int>& _source);
	static void odd_even_transportation_sort(std::vector<int>& _source);
private:
	static void partial_quick_sort(std::vector<int>& _source, int _from, int _to);
	static int quick_sort_partition(std::vector<int>& _source, int _from, int _to);
	static void make_heap_structure(std::vector<int>& _source);
	static void merge_sort_partial_merge(std::vector<int>& _source1,
										 std::vector<int>& _source2,
										 std::vector<int>& _result);
	static void heap_sort_downheap(std::vector<int>& _source, int _leaf, int _root);
};

#endif
