#ifndef OPEN_ADDRESS_H
#define OPEN_ADDRESS_H

#include <iostream>
#include <map>

typedef std::map<int, std::string> Dictionary;
typedef std::map<int, std::string>::iterator DictionaryIter;

class OpenAddress {
public:
	static const int HASH_DIV = 100;
	void insert_data(std::string _data);
	void delete_data(std::string _data);
	DictionaryIter find_data(std::string _data);
	int hash_function(std::string _data);
	int rehash_function(std::string _data);
	void print_all();
private:
	Dictionary hash_list;
};

#endif
