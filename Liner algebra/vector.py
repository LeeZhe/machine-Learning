from math import  sqrt,acos,pi
from decimal import Decimal,getcontext

getcontext().prec = 30


class Vector():

    CAN_NOT_OPERATION_ZERO_VECTOR = 'Can not operation zero vector'

    def __init__(self,coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)
        except ValueError:
            raise ValueError('The coordinates must not empty')
        except TypeError:
            raise TypeError('The coordinates must be iterable')

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def __str__(self):
        return 'Vector: {0}'.format(self.coordinates)

#vector operation
    def magnitude(self):
         square_coordinate = [x ** 2 for x in self.coordinates]
         return sqrt(sum(square_coordinate))

    def normalized(self):
        try:
            vector_size = self.magnitude()
            return self.times_scalar(Decimal(1.) / Decimal(vector_size))
        except  ZeroDivisionError:
            raise Exception(self.CAN_NOT_OPERATION_ZERO_VECTOR)

    def dot(self,v):
        return sum([x * y for x , y in zip(self.coordinates, v.coordinates)])

    def is_parallel_to(self,v):

        return (self.is_zero() or v.is_zero() or self.angle_with(v) == 0 or self.angle_with(v) == pi)

    def is_orthogonal_to(self,v, tolerance = 1e-10):

        return self.dot(v) < tolerance

    def is_zero(self, tolerance = 1e-10):
        return self.magnitude() < tolerance

    def angle_with(self,v,in_degrees = False,tolerance = 1e-10):
        try:
            u1 = self.normalized()
            u2 = v.normalized()
# ensure u1 parallel u2 cause acos math Exception
            if u1.dot(u2) - 1 > 0:
                print 'is run - 1'
                return 0.0

            if u1.dot(u2) + 1 < 0:
                return pi

            angle_with_radians = acos(u1.dot(u2))
            if in_degrees:
                degrees_per_radians =  float(Decimal(180.)) / pi
                return degrees_per_radians * angle_with_radians
            else:
                return angle_with_radians


        except Exception as e:
            if str(e) == self.CAN_NOT_OPERATION_ZERO_VECTOR:
                raise Exception('Can not computer zero vector')
            else:
                raise e

    def plus(self,v):
        new_coordinates = [x + y for x ,y in zip(self.coordinates,v.coordinates)]
        return Vector(new_coordinates)

    def minus(self,v):

        new_coordinates = [x - y for x , y in zip(self.coordinates,v.coordinates)]

        return Vector(new_coordinates)

    def times_scalar(self, c):
        return Vector([x * c for x in self.coordinates])

v1 = Vector([2.118,4.827])
v2 = Vector([0,0])
print v1.is_orthogonal_to(v2)
print v1.is_parallel_to(v2)