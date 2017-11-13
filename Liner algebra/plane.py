from vector import Vector
from decimal import Decimal,getcontext
from line   import  Line
getcontext().prec = 30

class Plane(Line):
    def __init__(self, normal_vector=None, constant_term=None, dimension=3):

        super(Plane,self).__init__(normal_vector,constant_term,dimension)








if __name__ == '__main__':
    p1 = Plane(normal_vector=Vector(['-0.412','3.806','0.728']),constant_term='-3.46')
    p2 = Plane(normal_vector=Vector(['1.03', '-9.515', '-1.82']),constant_term='8.65')
#
#
    print('first pair planes are parallel?: {}'.format(p1.is_parallel_to(p2)))
    print('first pair planes are equal?: {}'.format(p1==p2))
#
    p1 = Plane(normal_vector=Vector(['2.611','5.528','0.283']), constant_term = '4.6')
    p2 = Plane(normal_vector=Vector(['7.715','8.306','5.342']), constant_term = '3.76')
# #
#     print('1111',p1,p2)
# #
    print('second pair of planes are parallel?: {}'.format(p1.is_parallel_to(p2)))
    print('second pair of planes are equal?: {}'.format(p1 == p2))

    p1 = Plane(normal_vector=Vector(['-7.926', '8.625', '-7.217']), constant_term = -7.952)
    p2 = Plane(normal_vector=Vector(['-2.642', '2.875', '-2.404']), constant_term = -2.443)
    # #
    print p1 , '\n' , p2
    # #
    print('third pair of planes are parallel?: {}'.format(p1.is_parallel_to(p2)))
    print('third pair of planes are equal?: {}'.format(p1 == p2))
