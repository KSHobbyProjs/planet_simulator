# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 2022

A helper module to import vector functionality.

@author: Keanan Scarbro
"""

# This is a redundant class. Apparently, numpy.array([...]) does the exact same thing
# Using numpy.array would have been better; it offers far more utilization
class Vector(list):
    # Dunder methods to handle how the Vector is treated when acted on by normal operations
    def __add__(self, y):
        if isinstance(y, Vector) == False:
            raise TypeError("Can't add a vector to a non-vector")
        if len(self) != len(y):
            raise Exception("Can't add two vectors with different lengths")
        return Vector([self[i] + y[i] for i in range(len(self))])
    
    def __iadd__(self, y):
        return self.__add__(y)
    
    def __sub__(self, y):
        if isinstance(y, Vector) == False:
            raise TypeError("Can't add a vector to a non-vector")
        if len(self) != len(y):
            raise Exception("Can't add two vectors with different lengths")
        return Vector([self[i] - y[i] for i in range(len(self))])
    
    def __isub__(self, y):
        return self.__sub__(y)
    
    def __mul__(self, y):
        if isinstance(y, int) == False and isinstance(y, float) == False:
            raise TypeError("Can't multiply a vector by a non-scalar")
        return Vector([item * y for item in self])
    
    def __imul__(self, y):
        return self.__mul__(y)
    
    def __rmul__(self, y):
        return self.__mul__(y)
    
    def __truediv__(self, y):
        if isinstance(y, int) == False and isinstance(y, float) == False:
            raise TypeError("Can't divide a vector by a non-scalar")
        return Vector([item / y for item in self])
    
    def __itruediv__(self, y):
        return self.__truediv__(y)
    
    def __rtruediv__(self, y):
        return self.__truediv__(y)
    
    def __abs__(self):
        return Vector([abs(item) for item in self])

    
    # Static methods representing the Levi-Civita and Kronecker Delta symbols
    @staticmethod
    def levi_civita(i, j, k):
        subscript_array = [i, j, k]
        
        for subscript in subscript_array:
            if subscript <= 0 or subscript > 3:
                raise Exception("This function only supports subscripts between 0 and 3." + \
                                " A number outside of this range was passed")
                    
        for index in range(len(subscript_array) - 1):
            for next_index in range(index + 1, len(subscript_array)):
                # If any of the subscripts are equal, return 0
                if subscript_array[index] == subscript_array[next_index]: return 0
                
        # Check whether or not (ijk) is an even or odd permutation of (123). Even
        # represents an even number of swaps while odd represents an odd number of swaps.
        # For example, (132) is an odd permutation because it includes an odd number
        # of swaps (1 swap: 2 and 3). (231) is an even permutation because it 
        # includes an even number of swaps (2 swaps: 1 and 3, then 2 and 3 (or another way))
        even_permutations = ([1, 2, 3], [2, 3, 1], [3, 1, 2])
        odd_permutations = ([2, 1, 3], [3, 2, 1], [1, 3, 2])
        if subscript_array in even_permutations: return 1
        elif subscript_array in odd_permutations: return -1
     
    @staticmethod
    def kronecker_delta(i, j):
        return 0 if i != j else 1
    
    # Methods to handle standard vector operations    
    def norm(self):
        mag = 0
        for num in self:
            mag += num**2
        return mag**.5
    
    def unit_vec(self):
        if self.norm() == 0: return Vector([0, 0, 0])
        return Vector(self / self.norm())
    
    def dot_product(self, y):
        if len(self) != len(y): 
            raise Exception("Can't take the dot product of two vectors with differing lengths")
        sum_ = 0
        for i in range(len(self)):
            sum_ += self[i] * y[i]
        return sum_
    
    def cross_product(self, y):
        if isinstance(y, Vector) == False:
            raise TypeError("Can't take the cross product between a vector and a non vector")
        if len(self) != len(y):
            raise Exception("Can't produce cross product of vectors of unequal dimension")
        if len(self) > 3:
            raise Exception("This function can't produce a cross product when the vectors have more than 3 dimensions")
        u = []
        for k in range(3):
            sum_ = 0
            for j in range(3):
                for i in range(3):
                    sum_ += Vector.levi_civita(i + 1, j + 1, k + 1) * self[i] * y[j]
            u.append(sum_) 
        return Vector(u)