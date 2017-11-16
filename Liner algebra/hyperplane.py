from plane import Plane
from vector import Vector
from decimal import Decimal,getcontext

getcontext().prec = 30


class Hyperplane(Plane):
    ELTHAER_DIM_OR_NORMAL_VEC_MUST_BE_PROVICED_MSG = 'Either the dimension the hyperplane nor normal_vector'

    def __init__(self, dimension = None, normal_vector = None, constant_term = None):

        if not dimension and not  normal_vector:
            raise  Exception(self.ELTHAER_DIM_OR_NORMAL_VEC_MUST_BE_PROVICED_MSG)

        elif not normal_vector:
            self.dimension = dimension
            all_zeros = ['0'] * self.dimension
            normal_vector = Vector(all_zeros)

        else:
            self.dimension = normal_vector.dimension

        self.normal_vector = normal_vector

        super(Hyperplane,self).__init__(dimension=dimension,normal_vector=normal_vector,constant_term=constant_term)


