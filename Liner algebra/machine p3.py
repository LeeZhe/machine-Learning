#!/usr/bin/python
#coding:utf-8
from copy import  deepcopy

# 以上的信息随自己的需要改动吧
def print_matrix(info, m):  # 输出矩阵
    i = 0;
    j = 0;
    l = len(m)
    print info
    for i in range(0, len(m)):
        for j in range(0, len(m[i])):
            if (j == l):
                print ' |',
            print '%6.4f' % m[i][j],
        print
    print


def swap(a, b):
    t = a;
    a = b;
    b = t
def swap_row(M, r1, r2):
    M[r1],M[r2] = M[r2],M[r1]




def solve(ma, b=0, n=0):
    global m;
    m = ma  # 这里主要是方便最后矩阵的显示
    global s;

    i = 0;
    j = 0;
    row_pos = 0;
    col_pos = 0;
    ik = 0;
    jk = 0
    mik = 0.0;
    temp = 0.0

    n = len(m)

    # row_pos 变量标记行循环, col_pos 变量标记列循环


    # print_matrix("一开始 de 矩阵", m)

    while ((row_pos < n) and (col_pos < n)):

        mik = - 1
        for i in range(row_pos, n):
            if (abs(m[i][col_pos]) > mik):
                mik = abs(m[i][col_pos])
                ik = i

        if (mik == 0.0):
            col_pos = col_pos + 1
            return None
        print_matrix("选主元", m)

        # 交换两行
        if (ik != row_pos):
            for j in range(col_pos, n):
                swap(m[row_pos][j], m[ik][j])
                swap(m[row_pos][n], m[ik][n]);  # 区域之外？

        print_matrix("交换两行", m)

        try:
            # 消元
            m[row_pos][n] /= m[row_pos][col_pos]
        except ZeroDivisionError:
            # 除零异常 一般在无解或无穷多解的情况下出现……
            return 0;

        j = n - 1
        while (j >= col_pos):
            m[row_pos][j] /= m[row_pos][col_pos]
            j = j - 1

        for i in range(0, n):
            if (i == row_pos):
                continue
            m[i][n] -= m[row_pos][n] * m[i][col_pos]

            j = n - 1
            while (j >= col_pos):
                m[i][j] -= m[row_pos][j] * m[i][col_pos]
                j = j - 1

        row_pos = row_pos + 1;
        col_pos = col_pos + 1

    return [[m[x][n]] for x in range(n)]

def transpose(M):
    row , column = shape(M)
    res = []
    for i in range(column):
        coords = [0] * row
        for x in range(row):
            coords[x] = M[x][i]
        res.append(coords)
    return res

def matxMultiply(A, B):
    num_column_A,num_row_B = len(A[0]),len(B)
    if not num_row_B == num_column_A:
        raise ValueError('Column A must equal row B')

    return [[sum(x * y for x , y in zip(x , y)) for y in zip(*B)] for x in A]


def augmentMatrix(A,b):
    return [x + y for x , y in zip(A,b)]

def swapRows(M,r1,r2):
    M[r1],M[r2] = M[r2],M[r1]

def scaleRow(M,r1,scale):
    M[r1] = [x * scale for x in M[r1]]

def addScaledRow(M, r1, r2, scale):
    if scale == 0:
        raise ValueError('scale must not equal zero')
    M[r1] = [x + y * scale for x , y in zip(M[r1],M[r2])]


def gj_Solve(A, b, decPts=4, epsilon=1.0e-16):
    if not len(A) == len(b):
        return None
    n = len(A)
    m = augmentMatrix(A, b)
    row_pos, col_pos = 0, 0
    while row_pos < n and col_pos < n:
        mik = -1
        ik = 0
        for i in range(row_pos, n):
            if (abs(m[i][col_pos]) > abs(mik)):
                mik = m[i][col_pos]
                ik = i

        if mik == epsilon:
            return None

        if ik != row_pos:
            swapRows(m,ik,row_pos)

        scaleRow(m,row_pos,1.0 / mik)
        for i in range(n):
            if i == row_pos:
                continue
            addScaledRow(m,i,row_pos,-m[i][col_pos])

        row_pos += 1
        col_pos += 1
    return [[m[x][n]] for x in range(n)]


# X^TXh = X^TY

def linearRegression(X, Y):
    X_T = transpose(X)
    X_T_Y = matxMultiply(X_T,Y)
    X_T_X = matxMultiply(X_T,X)
    res = gj_Solve(X_T_Y,X_T_X)

    return res[0][0], res[1][0]

if __name__ == '__main__':
    matrix = [[7.0, 5.0, - 3.0, -5.0, 1],
              [-4,  6, 2, -2.0 , 1],
              [-9, 4, -5, -9 , 1],
              [-9, 10, 5, -4, 1]]

    m2 = deepcopy(matrix)

    matrix2 = [[7.0, 5.0, - 3.0, -5.0],
              [-4, 6, 2, -2.0],
              [-9, 4, -5, -9],
              [-9, 10, 5, -4]]

    b = [[1],[1],[1],[1]]

    m = gj_Solve(matrix2,b)

    print_matrix('结果',m)



    # gauss_jordan(matrix)

    # print solve(m2)
    # print

    # print_matrix("方程组及其解 m2", m2)


        # 输出方程组及其解
    # print_matrix("方程组及其解 matrix", matrix)
    # for i in range(0, len(m2)):
    #     print ("x[%d] = %6.4f" % (i, m[i][len(m)]))