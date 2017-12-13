from plane import Plane
from vector import Vector
from decimal import Decimal,getcontext

getcontext().prec = 30



def matrix_mul(A,B):

    num_row_A,num_column_B = len(A[0]),len(B)
    if not num_column_B == num_row_A:
        raise ValueError
    return [[sum(x * y for x , y in zip(x , y)) for y in zip(*B)] for x in A]

A = [[1,0,2],
     [-1,3,1],
     [1,2,5]]

B = [[3,1],
     [2,1],
     [1,0]]

def augment_matrix(A,b):

    for i , vectors in enumerate(A):
        for i_b , vectors_b in enumerate(b):
            if not  i_b == i:
                continue

            vectors += vectors_b
    return A

# print augment_matrix(A,B)



def gj_Solve(A, b, decPts=4, epsilon=1.0e-16):
    h , w = shape(A)
    m = A
    if not len(A) == len(b):
        return None

    row_pos = 0;col_pos = 0;ik = 0;jk = 0
    while row_pos < h and col_pos < w:
        mik = -1
        for i in range(row_pos,h):
            if abs(m[i][col_pos] > mik):
                mik = abs(m[i][col_pos])
                ik = i

            if mik == 0:
                col_pos += 1
                continue

        if ik != row_pos:







    return None
gj_Solve(A,B)


class Hyperplane(Plane):
    EITHER_DIM_OR_NORMAL_VEC_MUST_BE_PROVIDE_MSG = 'Either the dimension the hyperplane nor normal_vector'

    def __init__(self, dimension = None, normal_vector = None, constant_term = None):

        if not dimension and not  normal_vector:
            raise  Exception(self.EITHER_DIM_OR_NORMAL_VEC_MUST_BE_PROVIDE_MSG)

        elif not normal_vector:
            self.dimension = dimension
            all_zeros = ['0'] * self.dimension
            normal_vector = Vector(all_zeros)

        else:
            self.dimension = normal_vector.dimension

        self.normal_vector = normal_vector

        super(Hyperplane,self).__init__(dimension=dimension,normal_vector=normal_vector,constant_term=constant_term)



if __name__ == '__main__':
    I = [[1.44598, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 1, 0],
         [0, 0, 0, 1]]





    # print matrix_mul(A,B)


    def shape(M):
        return len(M),len(M[0])

    def matxRound(M,decPts = 4):
        for vectors in M:
            for i in range(len(vectors)):
                c = vectors[i]
                vectors[i] = round(c,decPts)

    def transpose(M):
        row , column = shape(M)
        res = []

        for i in range(column):
            coords = [0] * row
            for x in range(row):
                coords[x] = M[x][i]
            res.append(coords)

        return res

    def matxMultiply(A,B):

        def mutilply(coefficient,B_vector):
            return [coefficient * x for x in B_vector]

        def plus(vectors):
            try:
                num_v = len(vectors[0])
                coords = [0] * num_v
                for i in range(num_v):
                    s = 0
                    for idx , v in enumerate(vectors):
                        s += v[i]
                    coords[i] = s
                return coords
            except Exception as e:
                raise e




        # 1.for each element in A and new a list after for each list
        # 2.for each list in B , if idx is legal user mutilply() selector and inset in res
        # 3.operation each list in rea and plus in legal idx







