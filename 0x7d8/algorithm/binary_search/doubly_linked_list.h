#include <iostream>
#include <vector>

class Cell;
class DoublyLinkedList;

class Cell {
public:
	Cell(int _data, Cell* _next, Cell* _prev);
	Cell();
	~Cell();
	Cell* next_cell();
	Cell* prev_cell();
	void next_cell(Cell* cell);
	void prev_cell(Cell* cell);
	int get_data();
private:
	int data;
	Cell* next;
	Cell* prev;
};


class DoublyLinkedList {
public:
	DoublyLinkedList();
	~DoublyLinkedList();
	int insert_cell(int _val);
	int delete_cell(int _val);
	Cell* create_cell(int _val);
	void print_all();
	void init_addressv();
	int list_length();

	Cell* linear_search(int _val);
	Cell* binary_search(int _val, int _start, int _end);
private:
	std::vector<Cell*> addressv;
	Cell* head;
};
