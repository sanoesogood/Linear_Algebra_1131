import numpy as np
import sympy as sp
from func import _sol

class VectorSpace:
    def __init__(self, mat):
        self.mat = np.array(mat)

        self.rowspace = np.array(self.row(self.mat))
        self.colspace = np.array(self.row(self.mat.T))
        self.nullspace = np.array(self.ker(self.mat))
        self.lnullspace = np.array(self.ker(self.mat.T))
    
    def row(self, mat):
        rref_mat, _ = sp.Matrix(mat).rref()
        rowspace = []
        for r in rref_mat.tolist():
            if all(num == 0 for num in r):
                continue
            rowspace.append(r)
        return rowspace

    def ker(self, mat):
        var = _sol(mat)["var"]
        nullspace = []
        for _, v in var.items():
            nullspace.append(v)
        return nullspace

if __name__ == "__main__":
    mat = np.array([[1, 2], [3, 6], [4, 8]])
    M = VectorSpace(mat)

    print(f"row(A) = span{M.rowspace}")
    print(f"col(A^T) = span{M.colspace}")
    print(f"null(A) = span{M.nullspace}")
    print(f"null(A^T) = span{M.lnullspace}")
