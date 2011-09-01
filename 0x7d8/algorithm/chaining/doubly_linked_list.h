#include <iostream>
#include <map>

class Cell;
class DoublyLinkedList;
class HashCell;
class HashList;

static const int HASH_DIV = 100;

class Cell {
public:
	Cell(std::string _data, Cell* _next, Cell* _prev);
	Cell();
	~Cell();
	Cell* next_cell();
	Cell* prev_cell();
	void next_cell(Cell* cell);
	void prev_cell(Cell* cell);
	std::string get_data();
	int get_length();
private:
	int length;
	std::string data;
	Cell* next;
	Cell* prev;
};


class DoublyLinkedList {
public:
	DoublyLinkedList();
	~DoublyLinkedList();
	int insert_cell(std::string _data);
	int delete_cell(std::string _data);
	Cell* create_cell(std::string _data);
	Cell* find_cell(std::string _data);
	void print_all();

private:
	Cell* head;
};

class HashList {
public:
	void insert_data(std::string _data);
	void delete_data(std::string _data);
	void print_all();
private:
	int hash_function(std::string _data);
	std::map<int, DoublyLinkedList*> hash_chain;
};
