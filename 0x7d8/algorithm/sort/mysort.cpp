#include "mysort.h"
#include <ctime>

//---------------------------------------------------------
/**
 * Implementation of Bubble Sort
 */
void Sort::bubble_sort(std::vector<int>& _source) {
	int length = _source.size();

	for (int i = 0; i < length; i++) {
		for (int j = length - 1; j > i; j--) {
			if (_source[j] < _source[j-1])
				std::swap(_source[j], _source[j-1]);
		}
	}
}

//---------------------------------------------------------
/**
 * Implementation of Selection Sort
 */
void Sort::selection_sort(std::vector<int>& _source) {
	int length = _source.size();
	int min;
	for (int i = 0; i < length; i++) {
		min = i;
		for (int j = i; j < length; j++) {
			if (_source[min] > _source[j])
				std::swap(_source[min], _source[j]);
		}
	}
}

//---------------------------------------------------------
/**
 * Implementation of Insertion Sort
 */
void Sort::insertion_sort(std::vector<int>& _source) {
	int length = _source.size();

	for (int i = 0; i < length; i++) {
		for (int j = i; j > 0 && _source[j-1] > _source[j]; j--) {
			std::swap(_source[j-1], _source[j]);
		}
	}
}

//---------------------------------------------------------
/**
 * Implementation of Shell Sort
 */
void Sort::shell_sort(std::vector<int>& _source, int _interval = Sort::SHELL_SORT_INTERVAL) {
	int length = _source.size();

	int width;
	for (width = 1; width < length / _interval; width = _interval*width + 1); 

	/*
	 * The basis is insertion sort
	 * 1. Do insertion sort for every other width element
	 * 2. Narrow width
	 */
	for (; width > 0; width /= _interval) {
		for (int i = width; i < length; i += width) {
			for (int j = i; j >= width && _source[j-width] > _source[j]; j -= width) {
				std::swap(_source[j-width], _source[j]);
			}
		}
	}

}

//---------------------------------------------------------
/**
 * Implementation of Quick Sort
 */
void Sort::quick_sort(std::vector<int>& _source) {
	int length = _source.size();

	partial_quick_sort(_source, 0, length-1);
}

void Sort::partial_quick_sort(std::vector<int>& _source, int _from, int _to) {
	if (_from > _to)
		return;

	int v = quick_sort_partition(_source, _from, _to);

	partial_quick_sort(_source, _from, v-1);
	partial_quick_sort(_source, v+1, _to);
}

int Sort::quick_sort_partition(std::vector<int>& _source, int _from, int _to) {
	int pivot = _source[_to];
	int i = _from - 1;
	int j = _to;

	/*
	 * 1. seek start point of i
	 * 2. decrease j until pivot > _source[j]
	 * 3. swap s[i] and s[j]
	 * 4. restart increasing i
	 *
	 * Point 1: set pivot value as rightest number
	 * Point 2: start i, j from the opposite side
	 */
	while (1) {
		while(_source[++i] < pivot);
		while(i < --j && pivot < _source[j]);

		if (i >= j)
			break;

		std::swap(_source[i], _source[j]);
	}

	std::swap(_source[i], _source[_to]);

	return i;
}

//---------------------------------------------------------
/**
 * Implementation of Merge Sort
 */
void Sort::merge_sort(std::vector<int>& _source) {
	int length = _source.size();
	if (length > 1) {
		int mid = length/2;
		std::vector<int> former, latter;

		std::copy( _source.begin(), _source.begin() + mid, std::back_inserter(former) );
		std::copy( _source.begin() + mid, _source.end(), std::back_inserter(latter) );

		merge_sort(former);
		merge_sort(latter);

		merge_sort_partial_merge(former, latter, _source);
	}
}

void Sort::merge_sort_partial_merge(std::vector<int>& _former,
									std::vector<int>& _latter,
									std::vector<int>& _source) {
	int length1 = _former.size();
	int length2 = _latter.size();
	int i = 0, j = 0;

	/// implement some sort algorithm
	int idx = 0;
	while (i < length1 && j < length2) {
		if (_former[i] < _latter[j]) {
			_source[idx] = _former[i];
			i++;
		}
		else {
			_source[idx] = _latter[j];
			j++;
		}
		idx++;
	}

	if (i < length1) {
		for (int k = i; k < length1; k++) {
			_source[idx] = _former[k];
			idx++;
		}
	}
	else {
		for (int k = j; k < length2; k++) {
			_source[idx] = _latter[k];
			idx++;
		}
	}
}
//---------------------------------------------------------
/**
 * Implementation of Heap Sort
 */
void Sort::heap_sort(std::vector<int>& _source) {
	int length = _source.size();

	int leaf = length;
	int root = length/2;

	while (root > 0) {
		heap_sort_downheap(_source, leaf, root);
		root--;
	}

	while (leaf > 0) {
		std::swap(_source[1], _source[leaf]);
		leaf--;
		heap_sort_downheap(_source, leaf, 1);
	}

}


void Sort::heap_sort_downheap(std::vector<int>& _source, int _leaf, int _root) {

}

//---------------------------------------------------------
void Sort::intro_sort(std::vector<int>& _source) {

}

void Sort::share_sort(std::vector<int>& _source) {

}

void Sort::in_place_merge_sort(std::vector<int>& _source) {

}

void Sort::cocktail_sort(std::vector<int>& _source) {

}

void Sort::comb_sort(std::vector<int>& _source) {

}

void Sort::gnome_sort(std::vector<int>& _source) {

}

void Sort::odd_even_transportation_sort(std::vector<int>& _source) {

}

