#!/usr/local/bin/python3.6

import math

class QuaternionDomainError(Exception):
	pass

class Quaternion:
	#real - Real part of quaternion
	#i, j, k - Imaginary part of quaternion
	def __init__(self, init: 'float|complex|list[float]|Quaternion' = 0):
		if isinstance(init, float):
			self.real = init
			self.i = 0.0
			self.j = 0.0
			self.k = 0.0
		elif isinstance(init, complex):
			self.real = init.real
			self.i = init.imag
			self.j = 0.0
			self.k = 0.0
		elif isinstance(init, list):
			self.real = init[0]
			self.i = init[1]
			self.j = init[2]
			self.k = init[3]
		elif isinstance(init, Quaternion):
			self.real = init.real
			self.i = init.i
			self.j = init.j
			self.k = init.k
		else:
			raise QuaternionDomainError("Can't create quaternion from " + str(type(init)))

	def __str__(self)-> 'string':
		string = str(self.real)

		if self.i > 0:
			string += " + " + str(self.i) + "i"
		elif self.i < 0:
			string += " - " + str(-self.i) + "i"

		if self.j > 0:
			string += " + " + str(self.j) + "j"
		elif self.j < 0:
			string += " - " + str(-self.j) + "j"

		if self.k > 0:
			string += " + " + str(self.k) + "k"
		elif self.k < 0:
			string += " - " + str(-self.k) + "k"

		return string
	
	def __eq__(self, other: 'Quaternion')-> 'bool':
		if isinstance(other, Quaternion):
			return self.real == other.real and self.i == other.i and self.j == other.j and self.k == other.k
		else:
			raise QuaternionDomainError("Can't equal quaternion with " + str(type(other)))

	def __add__(self, other: 'Quaternion')-> 'Quaternion':
		if isinstance(other, Quaternion):
			return Quaternion([self.real + other.real, self.i + other.i, self.j + other.j, self.k + other.k])
		else:
			raise QuaternionDomainError("Can't add " + str(type(other)) + " to quaternion")

	def __radd__(self, other: 'Quaternion')-> 'Quaternion':
		return self.__add__(other)

	def __neg__(self)-> 'Quaternion':
		return Quaternion([-self.real, -self.i, -self.j, -self.k])

	def __sub__(self, other: 'Quaternion')-> 'Quaternion':
		return self.__add__(other.__neg__())

	def __rsub__(self, other: 'Quaternion')-> 'Quaternion':
		return other.__add__(self.__neg__())

	def __mul__(self, other: 'Quaternion')-> 'Quaternion':
		if isinstance(other, float):
			return Quaternion([other*self.real, other*self.i, other.self.j, other*self.k])
		elif isinstance(other, complex):
			other = Quaternion(other)
		elif isinstance(other, Quaternion):
			real = self.real * other.real - self.i * other.i - self.j * other.j - self.k * other.k
			i = self.real * other.i + self.i * other.real + self.j * other.k - self.k * other.j
			j = self.real * other.j + self.j * other.real + self.k * other.i - self.i * other.k
			k = self.real * other.k + self.k * other.real + self.i * other.j - self.j * other.i
			return Quaternion([real, i, j, k])
		else:
			raise QuaternionDomainError("Can't multiplicate quaternion with " + str(type(other)))

	def __rmul__(self, other: 'float|complex|Quaternion')-> 'Quaternion':
		if isinstance(other, float):
			return Quaternion([other*self.real, other*self.i, other.self.j, other*self.k])
		elif isinstance(other, complex):
			other = Quaternion(other)
		elif isinstance(other, Quaternion):
			real = self.real * other.real - self.i * other.i - self.j * other.j - self.k * other.k
			i = self.real * other.i + self.i * other.real - self.j * other.k + self.k * other.j
			j = self.real * other.j + self.j * other.real - self.k * other.i + self.i * other.k
			k = self.real * other.k + self.k * other.real - self.i * other.j + self.j * other.i
			return Quaternion([real, i, j, k])
		else:
			raise QuaternionDomainError("Can't multiplicate quaternion with " + str(type(other)))

	def abs2(self)-> 'float':
		return self.real ** 2 + self.i ** 2 + self.j ** 2 + self.k ** 2

	def __abs__(self)-> 'float':
		return math.sqrt(self.abs2())

	def __reversed__(self):
		absolute2 = self.abs2()
		if absolute2 != 0:
			return Quaternion([self.real / absolute2, -self.i / absolute2, -self.j / absolute2, -self.k / absolute2])
		else:
			raise QuaternionDomainError("Can't divide by zero")

	def __truediv__(self, other):
		return self.__mul__(other.__reversed__())

	def __rtruediv__(self, other):
		return self.__rmul__(other.__reversed__())

u = Quaternion(1 + 6j)
v = Quaternion([-12, 4, 7, -1])

print(u)
print(v)
print(u + v)
print(u - v)
print(u * v)
print(v * u)
print(u / v)
print(abs(u))
