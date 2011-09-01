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
	Cell* c = find_cell(_val);
	if (c != head) {
		c->prev_cell()->next_cell(c->next_cell());
		c->next_cell()->prev_cell(c->prev_cell());
	}

	if (c == head) {
		if (c->next_cell() == NULL)
			head = NULL;
		else
			c->next_cell()->prev_cell(NULL);
			head = c->next_cell();
	}
	delete c;

	return 0;
}

inline Cell* DoublyLinkedList::create_cell(int _val) {
	return new Cell(_val, NULL, NULL);
}

Cell* DoublyLinkedList::find_cell(int _val) {
	Cell* c = NULL;
	for (c = head; c; c = c->next_cell() )
		if ( c->get_data() == _val )
			return c;
}

void DoublyLinkedList::print_all() {
	Cell* c = head;
	while(1) {
		if (c)
			cerr << c->get_data() << endl;
		else
			break;

		if (!c->next_cell())
			break;
		c = c->next_cell();
	}
}
