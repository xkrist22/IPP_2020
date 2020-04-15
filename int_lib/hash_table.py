#!/usr/bin/python


class hash_table:
	def __init__(self):
		self.__data = {}

	def get_data(self):
		return self.__data

	def insert(self, data, id):
		if (id not in self.__data.keys()):
			self.__data[id] = data
			return True
		else:
			return False

	def actualize(self, data, id):
		if (id not in self.__data.keys()):
			return False
		self.__data[id] = data


	def read(self, id):
		if (id not in self.__data.keys()):
			return False
		return self.__data[id]

	def search(self, id):
		if (id in self.__data.keys()):
			return True
		return False

	def delete(self, id):
		if (id not in self.__data.keys()):
			return False
		del self.__data[id]
		return True

	def clear(self):
		del self.__data
		self.__data = {}
		return True
