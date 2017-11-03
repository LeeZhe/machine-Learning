from math import  sqrt,acos,pi
from decimal import Decimal,getcontext

getcontext().prec = 30


class Vector():

    CAN_NOT_OPERATION_ZERO_VECTOR = 'Can not operation zero vector'
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = 'No unique orthogonal component'
    ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG = 'only define in two or three dims'

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



    def component_parallel_to(self,basic):
        try:
            u = basic.normalized()
            size_vector = self.dot(u) #component vector size
            return u.times_scalar(size_vector)
        except Exception as e:
            if str(e) == self.CAN_NOT_OPERATION_ZERO_VECTOR:
                raise Exception(self.CAN_NOT_OPERATION_ZERO_VECTOR)
            else:
                raise e
    def component_orthogonal_to(self,basic):
        try:
            projection = self.component_parallel_to(basic)
            return self.minus(projection)

        except Exception as e:
            if str(e) == self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e
    # cross
    def cross(self,v):
        try:
            x_1,y_1,z_1 = self.coordinates
            x_2,y_2,z_2 = v.coordinates
            new_coordinates = [y_1 * z_2 - z_1 * y_2,
                               -(x_1 * z_2 - z_1 * x_2),
                               x_1 * y_2 - y_1 * x_2]
            return Vector(new_coordinates)
        except ValueError as e:
            msg = str(e)
            if msg == 'need more than 2 values to unpack':
                # if has less than 3 count add 0 in coordinates
                self_embedded_R3 = Vector(self.coordinates + (0,))
                print self_embedded_R3
                v_embedded_R3    = Vector(v.coordinates + (0,))
                return self_embedded_R3.cross(v_embedded_R3)
            elif msg == 'need more than 1 value to unpack':
                raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG)
            else:
                print str(e)
    def area_of_parallelogram_with(self, v):
        cross_vector = self.cross(v)
        return cross_vector.magnitude()
    def area_of_triangle_with(self, v):
        return self.area_of_parallelogram_with(v) / 2


    def plus(self,v):
        new_coordinates = [x + y for x ,y in zip(self.coordinates,v.coordinates)]
        return Vector(new_coordinates)

    def minus(self,v):

        new_coordinates = [x - y for x , y in zip(self.coordinates,v.coordinates)]

        return Vector(new_coordinates)

    def times_scalar(self, c):
        return Vector([x * c for x in self.coordinates])


v1 = Vector([8.462, 7.893, -8.187])
v2 = Vector([6.984, -5.975, 4.778])

v3 = Vector([-8.987, -9.838, 5.031])
v4 = Vector([-4.268, -1.861, -8.866])

print v1.cross(v2)
print v3.area_of_parallelogram_with(v4)
# v3 = Vector([-9.88,-3.264,-8.159])
# v4 = Vector([-2.155,-9.353,-9.473])
#
# print v3.component_orthogonal_to(v4)
# print v1.component_parallel_to(v2)