#include <iostream>

class Cell;
class CircularlyLinkedList;

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


class CircularlyLinkedList {
public:
	CircularlyLinkedList();
	~CircularlyLinkedList();
	int insert_cell(int _val);
	int delete_cell(int _val);
	Cell* create_cell(int _val);
	Cell* find_cell(int _val);
	void print_all();

private:
	Cell* head;
};
