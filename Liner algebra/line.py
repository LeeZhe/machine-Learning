from  decimal import Decimal,getcontext
from vector import Vector
from math import acos

getcontext().prec = 30

class Line(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self,normal_vector = None,contant_term = None,dimension = 2):

        self.dimension = dimension
        if not normal_vector:
            normal_vector = ['0'] * self.dimension
        self.normal_vector = normal_vector

        # self.dimension = len(normal_vector.coordinates)

        if not contant_term:
            contant_term = Decimal('0')
        self.contant_term = Decimal(contant_term)
        self.set_basepoint()

    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.contant_term
            basepoint_coors = ['0'] * self.dimension
            inital_index = Line.first_none_zero_index(n.coordinates)
            inital_coefficient = n.coordinates[inital_index]
            basepoint_coors[inital_index] = c / inital_coefficient
            self.basepoint = Vector(basepoint_coors)
        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e

    def __eq__(self, ell):

        if self.normal_vector.is_zero():
            if not ell.normal_vector.is_zero():
                return False
            else:
                diff = self.contant_term - ell.contant_term
                return Mydecimal(diff).is_near_zero()
        elif ell.normal_vector.is_zero():
            return False

        if not self.is_parallel_to(ell):
            return False

        x0 = self.basepoint
        y0 = ell.basepoint
        # print x0, '\n', y0
        basepoint_difference = x0.minus(y0)

        return self.normal_vector.is_orthogonal_to(basepoint_difference)


    def is_parallel_to(self,ell):

        n = self.normal_vector
        v = ell.normal_vector
        # print n.is_parallel_to(v)
        return n.is_parallel_to(v)

    def intersection_with(self, ell):
        try:
            A,B = self.normal_vector.coordinates
            C,D = ell.normal_vector.coordinates
            k1,k2 = self.contant_term,ell.contant_term

            z_cer = A * D - B * C
            if Mydecimal(z_cer).is_near_zero():
                return None

            x_numerator = D * k1 - B * k2
            y_numerator = -C * k1 + A * k2

            one_over_dem = Decimal(1.) / z_cer

            return Vector([x_numerator, y_numerator]).times_scalar(one_over_dem)

        except Exception as e:
            if self == ell:
                return self
            else:

                print str(e)

                return None

    def is_in_line(self,eps = 1e-10):
        A, B = self.normal_vector.coordinates
        x, y = self.basepoint.coordinates
        k = self.contant_term
        return A * x + B * y - k < eps
    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):

            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))
            return output

        n = self.normal_vector

        try:
            initial_index = Line.first_none_zero_index(n.coordinates)
            access = ['x','y','z']

            terms = [write_coefficient(n.coordinates[i], is_initial_term=(i == initial_index)) + access[i]
                     for i in range(self.dimension) if round(n.coordinates[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.contant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output









    @staticmethod
    def first_none_zero_index(iterable):
        for index , item in enumerate(iterable):
            if not Mydecimal(item).is_near_zero():
                return index
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)



class Mydecimal(Decimal):
    def is_near_zero(self, eps = 1e-10):
        return abs(self) < eps


if __name__ == '__main__':

    # ell1 = Line(Vector([4.046, 2.836]), 1.21)
    # ell1 = Line(Vector([0, 0]), 1.21)
    # ell2 = Line(Vector([10.115, 7.09]), 3.025)
    # print ell1.intersection_with(ell2)
    # print 'ell1 is equal ell2' , ell1 == ell2
    # print 'ell1 is parallel to ell2' , ell1.is_parallel_to(ell2)

    # ell3 = Line(Vector([7.204, 3.182]), 8.68)
    # ell4 = Line(Vector([8.172, 4.114]), 9.883)
    # print ell3.intersection_with(ell4)
    #
    ell3 = Line(Vector([1.182, 5.562]), 8.68)
    ell4 = Line(Vector([1.773, 8.343]), 9.525)
    print ell3.intersection_with(ell4)
    print 'ell3 is equal to ell4', ell3 == ell4
    print 'ell3 is parallel to ell4' , ell3.is_parallel_to(ell4)
