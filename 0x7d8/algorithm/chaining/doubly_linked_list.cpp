#include "doubly_linked_list.h"

using std::cerr;
using std::endl;

Cell::Cell(std::string _data, Cell* _next, Cell* _prev) {
	data = _data;
	length = _data.length();
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

inline std::string Cell::get_data() {
	return this->data;
}

inline int Cell::get_length() {
	return this->length;
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

int DoublyLinkedList::insert_cell(std::string _data) {
	int _val = _data.length();
	if ( head == NULL )
		head = create_cell(_data);
	else {
		Cell* p = head;
		Cell* c = NULL;
		for ( c = head; c; c = c->next_cell() ) {
			if (c->get_length() > _val)
				break;
			p = c;
		}

		if ( c == head ) {
			Cell* new_head = create_cell(_data);
			new_head->next_cell(head);
			head->prev_cell(new_head);
			head = new_head;
		}
		else {
			Cell* new_cell = create_cell(_data);
			p->next_cell(new_cell);
			if (c)
				c->prev_cell(new_cell);
			new_cell->next_cell(c);
			new_cell->prev_cell(p);
		}
	}

	return 0;
}

int DoublyLinkedList::delete_cell(std::string _data) {
	Cell* c = find_cell(_data);
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

inline Cell* DoublyLinkedList::create_cell(std::string _data) {
	return new Cell(_data, NULL, NULL);
}

Cell* DoublyLinkedList::find_cell(std::string _data) {
	int _val = _data.length();
	Cell* c = NULL;
	for (c = head; c; c = c->next_cell() )
		if ( c->get_length() == _val )
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

int HashList::hash_function(std::string _data) {
	int length = _data.length();
	int hash_val = 0;
	for (int i = 0; i < length; i++) {
		hash_val += _data.at(i);
	}
	return hash_val % HASH_DIV;
}

void HashList::insert_data(std::string _data) {
	int key = hash_function(_data);

	if (!hash_chain[key])
		hash_chain[key] = new DoublyLinkedList();

	hash_chain[key]->insert_cell(_data);	
}

void HashList::delete_data(std::string _data) {
	int key = hash_function(_data);

	if (!hash_chain[key])
		return;

	hash_chain[key]->delete_cell(_data);	
}

void HashList::print_all() {
	std::map<int, DoublyLinkedList*>::iterator itr;
	for (itr = hash_chain.begin(); itr != hash_chain.end(); itr++) {
		cerr << "----- " << itr->first << " : " << itr->second << " -----" << endl;
		itr->second->print_all();
	}
}
