#include "doubly_linked_list.h"

using std::cerr; using std::endl;

Cell::Cell(int _data, Cell* _next, Cell* _prev) {
	data = _data;
	next = _next;
	prev = _prev;
}

Cell::Cell() {
	Cell(0, NULL, NULL);
}

Cell::~Cell() {
	next = NULL;
	prev = NULL;
}

inline Cell* Cell::next_cell() {
	return this->next;
}

inline Cell* Cell::prev_cell() {
	return this->prev;
}

inline void Cell::next_cell(Cell* _cell) {
	this->next = _cell;
}

inline void Cell::prev_cell(Cell* _cell) {
	this->prev = _cell;
}

inline int Cell::get_data() {
	return this->data;
}

DoublyLinkedList::DoublyLinkedList() {
	head = NULL;
}

DoublyLinkedList::~DoublyLinkedList() {
	Cell* n = NULL;
	for( Cell* c = head; c; ) {
		n = c->next_cell();
		delete c;
		c = n;
	}
}

int DoublyLinkedList::insert_cell(int _val) {
	if ( head == NULL )
		head = create_cell(_val);
	else {
		Cell* p = head;
		Cell* c = NULL;
		for ( c = head; c; c = c->next_cell() ) {
			if (c->get_data() > _val)
				break;
			p = c;
		}

		if ( c == head ) {
			Cell* new_head = create_cell(_val);
			new_head->next_cell(head);
			head->prev_cell(new_head);
			head = new_head;
		}
		else {
			Cell* new_cell = create_cell(_val);
			p->next_cell(new_cell);
			if (c)
				c->prev_cell(new_cell);
			new_cell->next_cell(c);
			new_cell->prev_cell(p);
		}
	}

	return 0;
}

int DoublyLinkedList::delete_cell(int _val) {
	Cell* c = linear_search(_val);
	c->prev_cell()->next_cell(c->next_cell());
	c->next_cell()->prev_cell(c->prev_cell());
	delete c;
	
	return 0;
}

inline Cell* DoublyLinkedList::create_cell(int _val) {
	return new Cell(_val, NULL, NULL);
}

void DoublyLinkedList::print_all() {
	Cell* c = head;
	while(1) {
		cerr << c->get_data() << endl;
		if ( !c->next_cell() )
			break;
		c = c->next_cell();
	}
}

void DoublyLinkedList::init_addressv() {
	addressv.clear();
	for (Cell* c = head; c; c = c->next_cell())
		addressv.push_back(c);
}

int DoublyLinkedList::list_length() {
	return addressv.size();
}

Cell* DoublyLinkedList::linear_search(int _val) {
	Cell* c = NULL;
	for (c = head; c; c = c->next_cell() )
		if ( c->get_data() == _val )
			return c;
	return NULL;
}

Cell* DoublyLinkedList::binary_search(int _val, int _start, int _end) {
	int center = (_start + _end)/2;
	cerr << "[binary search] " << center << "\t" << _start << "\t" << _end << endl;
	Cell* c = addressv[center];

	if (c->get_data() == _val)
		return c;
	else if (c->get_data() < _val)
		binary_search(_val, center, _end);
	else
		binary_search(_val, _start, center);
}
