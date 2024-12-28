import numpy as np
import sympy as sp

def rref(mat: np.array):
    rref_mat, pivots = sp.Matrix(mat).rref()
    return (np.array(rref_mat.tolist()), pivots)

# def ker(mat, augsize):
#     """
#     augsize is a positive integer.\n
#     If augsize == 0, solve the homogeneous system Ax = 0 and give the kernel.\n
#     Else augsize > 0, it's means that A is a augmented matrix.\n
#     Solve the nonhomogeneous system Ax = y, give its kernel and particular solution.
#     """

#     m = len(mat)
#     n = len(mat[0])

#     # homogeneous system (optional)
#     if augsize == 0:
#         np.insert(mat, n, np.zeros(m), axis=1)

#     rref_mat, pivots = rref(mat)
#     coef_size = (m, n - augsize)
#     sol = {"kernel": {}, "particular": {}}

#     for idx in range(n):
#         # TODO: Represented the x_pivot is linear combination of x_i vector excepted x_pivot.
#         if idx in pivots:
#             continue

#         col = rref_mat.T[idx]

#         # kernel is a subspace of R^n
#         while len(col) != coef_size[1]:
#             if len(col) > coef_size[1]:
#                 col = np.delete(col, -1)
#             else:
#                 col = np.insert(col, len(col), 0, axis=0)

#         if idx <= coef_size[1] - 1:
#             col = -col
#             col[idx] = 1
#             sol["kernel"].update({f"col{idx+1}": col})
#         else:
#             sol["particular"].update({f"col{idx+1}": col})
    
#     return sol

def _sol(mat, augsize=0):
    coef_size = (len(mat), len(mat[0]) - augsize)
    rref_mat, pivots = rref(mat)
    sol = {"var": {}, "ans": {}}

    for idx in range(len(mat[0])):
        # TODO: Represented the x_pivots are a linear combination of x_i vector except x_pivots.
        if idx in pivots:
            continue

        col = rref_mat.T[idx]

        # kernel is a subspace of R^n
        while len(col) != coef_size[1]:
            if len(col) > coef_size[1]:
                col = np.delete(col, -1)
            else:
                col = np.insert(col, coef_size[0], 0, axis=0)

        if idx <= coef_size[1] - 1:
            col = -col
            col[idx] = 1
            sol["var"].update({f"x{idx+1}": col})
        else:
            sol["ans"].update({f"ans{idx+1-coef_size[1]}": col})
    
    return sol