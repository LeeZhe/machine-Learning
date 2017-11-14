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
        k = self[row].constant_term

        new_normal_vector = n.times_scalar(coefficient)
        new_constant_term = k * coefficient

        self[row] = Plane(normal_vector = new_normal_vector,constant_term= new_constant_term)

        return self[row]

    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):

        n1 = self[row_to_add].normal_vector
        n2 = self[row_to_be_added_to].normal_vector
        k1 = self[row_to_add].constant_term
        k2 = self[row_to_be_added_to].constant_term
        new_normal_vector = n1.times_scalar(coefficient).plus(n2)
        new_constant_term = k1 * coefficient + k2
        self[row_to_be_added_to] = Plane(normal_vector=new_normal_vector, constant_term=new_constant_term)


    def indices_of_first_nonzero_terms_in_each_row(self):
        num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_equations

        for i, p in enumerate(self.planes):
            try:
                indices[i] = p.first_none_zero_index(p.normal_vector.coordinates)
            except Exception as e:
                if str(e) == Plane.NO_NONE_ZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e
        return indices

    def compute_triangular_form(self):
        system = deepcopy(self)

        num_equations = len(system)
        num_variables = system.dimension

        j = 0
        for i in range(num_equations):
            while j < num_variables:
                c = MyDecimal(system[i].normal_vector[j])
                if c.is_near_zero():
                    # add func
                    swap_succeed = system.swap_with_row_below_for_none_zero_coefficient_if_able(i,j)
                    if not  swap_succeed:
                        j += 1
                        continue

                system.clear_coefficients_below(i,j)
                # print system
                j += 1
                break

        return system


    def compute_rref(self):

        tf = self.compute_triangular_form()

        # print tf

        num_equations = len(tf)
        pivots_indices = tf.indices_of_first_nonzero_terms_in_each_row()
        for i in range(num_equations)[::-1]:
            j = pivots_indices[i]
            if j < 0:
                continue
            tf.scale_row_to_make_coefficient_equal_one(i,j)
            tf.clear_coefficient_above(i,j)
        return tf



    def scale_row_to_make_coefficient_equal_one(self, row, col):
        n = self[row].normal_vector

        if MyDecimal(n[col]).is_near_zero():
            return

        beta = Decimal('1.0') / n[col]
        self.multiply_coefficient_and_row(beta,row)

    def clear_coefficient_above(self,row,col):
        for k in range(row)[::-1]:
            n = self[k].normal_vector
            alpha = -(n[col])
            self.add_multiple_times_row_to_row(alpha,row,k)


    def swap_with_row_below_for_none_zero_coefficient_if_able(self, row , col):
        num_equations = len(self)

        for k in range(row + 1,num_equations):

            coefficient = MyDecimal(self[k].normal_vector[col])
            if not  coefficient.is_near_zero():
                self.swap_rows(row,k)
                return True

            return False

    def clear_coefficients_below(self, row, col):
        num_equations = len(self)
        beta = self[row].normal_vector[col]
        for k in range(row + 1 , num_equations):
            gamma = self[k].normal_vector[col]
            alpha = -gamma / beta
            # print alpha,row,k
            self.add_multiple_times_row_to_row(alpha, row, k)
            # print  self

    def compute_solution(self):
        try:
            return self.do_gaussian_elimination_and_extract_solution()

        except Exception as e:
            if str(e) == self.NO_SOLUTIONS_MSG:
                return str(e)
            else:
                raise e
        pass


    def do_gaussian_elimination_and_extract_solution(self):
        rref = self.compute_rref()

        print rref
        rref.raise_exception_if_contradictory_equation()

        direction_vectors = rref.extract_direction_vectors_for_parametrization()
        basepoint = rref.extract_basepoint_for_parametrization()

        return Parametrization(basepoint, direction_vectors)



    def raise_exception_if_contradictory_equation(self):
        for p in self.planes:
            try:
                p.first_none_zero_index(p.normal_vector)

            except Exception as e:
                if str(e) == 'No nonzero elements found':
                    constant_term = MyDecimal(p.constant_term)
                    if not constant_term.is_near_zero():
                        raise Exception(self.NO_SOLUTIONS_MSG)

                else:
                    raise e


    def raise_exception_if_too_few_pivots(self):
        pivot_indices = self.indices_of_first_nonzero_terms_in_each_row()
        num_pivots = sum([1 if index >= 0 else 0 for index in pivot_indices])
        num_variables = self.dimension

        if num_pivots < num_variables:
            raise Exception(self.INF_SOLUTIONS_MSG)



    def extract_direction_vectors_for_parametrization(self):
        num_variables = self.dimension
        pivot_indices = self.indices_of_first_nonzero_terms_in_each_row()
        free_variable_indices = set(range(num_variables)) - set(pivot_indices)

        direction_vectors = []

        for free_var in free_variable_indices:
            vector_coords = [0] * num_variables
            vector_coords[free_var] = 1

            for i,p in enumerate(self.planes):
                pivot_var = pivot_indices[i]
                if pivot_var < 0:
                    break
                vector_coords[pivot_var] = -p.normal_vector[free_var]
            direction_vectors.append(Vector(vector_coords))
            # print direction_vectors[0]
        return  direction_vectors

    def extract_basepoint_for_parametrization(self):
        num_variables = self.dimension
        pivot_indices = self.indices_of_first_nonzero_terms_in_each_row()

        base_point_coords = [0] * num_variables

        for i , p in enumerate(self.planes):
            pivot_var = pivot_indices[i]
            if pivot_var < 0:
                break
            base_point_coords[pivot_var] = p.constant_term
        # print Vector(base_point_coords)
        return Vector(base_point_coords)




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


class Parametrization(object):

    BASEPT_AND_DIR_VECTORS_MUST_BE_IN_SAME_DIM_MSG = 'The basepoint and direction vectors should all live in the same dimension'

    def __init__(self, basepoint, direction_vectors):

        self.basepoint = basepoint
        self.direction_vectors = direction_vectors
        self.dimension = self.basepoint.dimension

        try:
            for v in direction_vectors:
                assert v.dimension == self.dimension

        except AssertionError:
            raise Exception(self.BASEPT_AND_DIR_VECTORS_MUST_BE_IN_SAME_DIM_MSG)

    def __str__(self):
        num_decimal_places = 3
        def write_coefficient(ponit_x,coefficient,is_initial_term = False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            output += str(round(ponit_x,num_decimal_places)) + ' '

            if coefficient < 0:
                output += '-'
            if coefficient >= 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))
            return output

        try:

            temp = []

            for n in self.direction_vectors:
                initial_index = Plane.first_none_zero_index(n)
                access = ['x', 'y', 'z']
                terms = [write_coefficient(self.basepoint[i],n[i],is_initial_term=(i == initial_index)) + 't' for i in range(self.dimension)]

                temp = ['{} = {}'.format(access[i],x) for i , x in enumerate(terms)]

            return '\n'.join(temp)

            pass

        except Exception as e:
            raise e

        return 'test'





class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps



if __name__ == '__main__':
    p1 = Plane(normal_vector=Vector([.786, .786, .588]), constant_term = -.714)
    p2 = Plane(normal_vector=Vector([-.138, -.138, .244]), constant_term = .319)

    sys =  LinearSystem([p1,p2])

    print sys.compute_solution()
    #
    # p1 = Plane(normal_vector=Vector([8.631, 5.112, -1.816]), constant_term=-5.113)
    # p2 = Plane(normal_vector=Vector([4.315, 11.132, -5.27]), constant_term=-6.775)
    # p3 = Plane(normal_vector=Vector([-2.158, 3.01, -1.727]), constant_term=-.831)
    #
    # sys = LinearSystem([p1,p2,p3])
    # print sys.compute_solution()
    #
    # p1 = Plane(normal_vector=Vector([5.262, 2.739, -9.878]), constant_term=-3.441)
    # p2 = Plane(normal_vector=Vector([5.111, 6.358, 7.638]), constant_term=-2.152)
    # p3 = Plane(normal_vector=Vector([2.016, -9.924, -1.367]), constant_term=-9.278)
    # p4 = Plane(normal_vector=Vector([2.167, -13.543, -18.883]), constant_term=-10.567)
    #
    # sys = LinearSystem([p1, p2, p3,p4])
    #
    # print sys.compute_triangular_form()
    #
    # print sys.compute_solution()


    # p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    # p2 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='2')
    # s = LinearSystem([p1, p2])
    # r = s.compute_rref()
    # if not (r[0] == p1 and
    #                 r[1] == Plane(constant_term='1')):
    #     print 'test case 2 failed'
    #
    # p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    # p2 = Plane(normal_vector=Vector(['0', '1', '0']), constant_term='2')
    # p3 = Plane(normal_vector=Vector(['1', '1', '-1']), constant_term='3')
    # p4 = Plane(normal_vector=Vector(['1', '0', '-2']), constant_term='2')
    # s = LinearSystem([p1, p2, p3, p4])
    # r = s.compute_rref()
    # if not (r[0] == Plane(normal_vector=Vector(['1', '0', '0']), constant_term='0') and
    #                 r[1] == p2 and
    #                 r[2] == Plane(normal_vector=Vector(['0', '0', '-2']), constant_term='2') and
    #                 r[3] == Plane()):
    #     print 'test case 3 failed'
    #
    # p1 = Plane(normal_vector=Vector(['0', '1', '1']), constant_term='1')
    # p2 = Plane(normal_vector=Vector(['1', '-1', '1']), constant_term='2')
    # p3 = Plane(normal_vector=Vector(['1', '2', '-5']), constant_term='3')
    # s = LinearSystem([p1, p2, p3])
    # r = s.compute_rref()
    # if not (r[0] == Plane(normal_vector=Vector(['1', '0', '0']), constant_term=Decimal('23') / Decimal('9')) and
    #                 r[1] == Plane(normal_vector=Vector(['0', '1', '0']), constant_term=Decimal('7') / Decimal('9')) and
    #                 r[2] == Plane(normal_vector=Vector(['0', '0', '1']), constant_term=Decimal('2') / Decimal('9'))):
    #     print 'test case 4 failed'
