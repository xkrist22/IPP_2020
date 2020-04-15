#!/usr/bin/python


class stack:
	def __init__(self):
		# NOTE: stack is implemented with list, which is heterogenous 
		# so whole stack can be heterogenous
		self.__data = []

	def get_data(self):
		return self.__data
	
	def push(self, data):
		self.__data.append(data)

	def pop(self):
		if (len(self.__data) <= 0):
			return False

		temp = self.__data[-1]
		self.__data.pop()
		return True

	def top(self):
		if (len(self.__data) <= 0):
			return None
		return self.__data[-1]

	def size(self):
		return len(self.__data)

	def is_empty(self):
		return len(self.__data) == 0
