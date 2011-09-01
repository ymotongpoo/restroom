#include <iostream>

class Cell;
class LinkedList;

class Cell {
public:
	Cell(int _data, Cell* _next);
	Cell();
	Cell* next_cell();
	void next_cell(Cell* cell);
	int get_data();
private:
	int data;
	Cell* next;
};


class LinkedList {
public:
	LinkedList();
	~LinkedList();
	int insert_cell(int _val);
	int delete_cell(int _val);
	Cell* create_cell(int _val);
	Cell* find_cell(int _val);
	void print_all();

private:
	Cell* head;
};
