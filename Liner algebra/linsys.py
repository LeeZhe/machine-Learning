from decimal import Decimal, getcontext
from copy import  deepcopy

from  vector import Vector
from plane import Plane

getcontext().prec = 30



class LinearSystem(object):
    ALL_PLANES_MUST_BE_LIVE_MSG = 'All planes must be live in same'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'infinitely many solutions'

    def __init__(self, planes):
        try:
            d = planes[0].dimension
            for p in planes:
                assert p.dimension == d

            self.planes = planes
            self.dimension = d

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_LIVE_MSG)

    def swap_rows(self,row1,row2):
        self[row1],self[row2] = self[row2],self[row1]

    def multiply_coefficient_and_row(self,coefficient,row):
        n = self[row].normal_vector
        k = self[row].contant_terms

        new_normal_vector = n.times_scalar(coefficient)
        new_contant_terms = k * coefficient

        self[row] = Plane(normal_vector = new_normal_vector,contant_term = new_contant_terms)

        return self[row]

    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):

        n2 = self[row_to_be_added_to].normal_vector
        k2 = self[row_to_be_added_to].contant_terms

        p = self.multiply_coefficient_and_row(coefficient,row_to_add)

        new_normal_vertor = p.normal_vector.plus(n2)
        new_contant_terms = p.contant_terms * coefficient + k2

        self[row_to_be_added_to] = Plane(normal_vector=new_normal_vertor,contant_term=new_contant_terms)

    def indices_of_first_nonzero_terms_in_each_row(self):
        num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_equations

        for i, p in enumerate(self.planes):
            try:
                indices[i] = p.first_nonzero_index(p.normal_vector.coordinates)
            except Exception as e:
                if str(e) == Plane.NO_NONEZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e
        return indices

    def __len__(self):
        return len(self.planes)

    def __getitem__(self, i):
        return self.planes[i]

    def __setitem__(self, i, x):
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_LIVE_MSG)

    def __str__(self):
        ret = 'Linear System:\n'
        temp = ['Equation {}: {}'.format(i + 1, p) for i, p in enumerate(self.planes)]
        ret += '\n'.join(temp)
        return ret


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps



if __name__ == '__main__':
    p0 = Plane(normal_vector = Vector([1,1,1]), contant_term=3)
    p1 = Plane(normal_vector=Vector(['0', '1', '0']), contant_term='2')
    p2 = Plane(normal_vector=Vector(['1','1','-1']), contant_term='3')
    p3 = Plane(normal_vector=Vector(['1','0','-2']), contant_term='2')

    s = LinearSystem([p0,p1,p2,p3])
    print s

    s.swap_rows(0, 1)
    print s

    if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
        print 'test case 1 failed'

