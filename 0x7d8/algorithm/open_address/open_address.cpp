#include "open_address.h"

void OpenAddress::insert_data(std::string _data) {
	int key = hash_function(_data);
	DictionaryIter itr = hash_list.find(key);
	if (itr != hash_list.end())
		key = rehash_function(_data);

	hash_list.insert( Dictionary::value_type(key, _data) );
}

void OpenAddress::delete_data(std::string _data) {
	DictionaryIter itr = find_data(_data);
	hash_list.erase(itr);
}

DictionaryIter OpenAddress::find_data(std::string _data) {
	DictionaryIter itr;
	int key = hash_function(_data);
	for (int i = 0; itr != hash_list.end(); i++) {
		itr = hash_list.find(key);
		if (itr->second.compare(_data) == 0)
			return itr;
		key += HASH_DIV*i;
	}
}

int OpenAddress::hash_function(std::string _data) {
	int hash_val = 0;
	for (int i = 0; i < _data.length(); i++) {
		hash_val += _data.at(i);
	}
	return hash_val % HASH_DIV;
}

int OpenAddress::rehash_function(std::string _data) {
	int _hash_val = hash_function(_data) + HASH_DIV;
	DictionaryIter itr = hash_list.begin();
	int i = 0;
	while(1) {
		itr = hash_list.find(_hash_val);
		if (itr == hash_list.end())
			break;

		_hash_val += HASH_DIV*(i+1);
		i++;
	}

	return _hash_val;
}

void OpenAddress::print_all() {
	for (DictionaryIter itr = hash_list.begin();
		 itr != hash_list.end(); itr++)
	{
		std::cerr << itr->first << " -> " << itr->second << std::endl;
	}
}
