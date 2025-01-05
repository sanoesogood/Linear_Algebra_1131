import numpy as np
import sympy as sp
from enum import Enum

config = {
    "mapping": True
}

class SolType(Enum):
    NO = "no"
    UNIQUE = "unique"
    MANY = "many"
class LinSysSol:
    def __init__(self, rref_coef_mat: np.ndarray, vec: np.ndarray, type: SolType):
        self.rref_coef_mat = rref_coef_mat
        self.vec = vec
        self.type = type

    def __str__(self):
        sol_type_str = f"{self.type.value} solution."
        match self.type:
            case SolType.UNIQUE:
                return self.tostring() + ', ' + sol_type_str
            case SolType.MANY:
                return self.tostring() + ', ' + sol_type_str
            case SolType.NO:
                return sol_type_str

    def tostring(self) -> str:
        return _tostring(self)

def _tostring(self: LinSysSol) -> str:
    if self.type == SolType.NO:
        return "no solution."

    _, pivots = rref(self.rref_coef_mat)
    m, n = len(self.rref_coef_mat), len(self.rref_coef_mat[0])
    free_vars = [i for i in range(n) if i not in pivots]

    ch_map = {f"x{free_var+1}": f"t{i}" for i, free_var in enumerate(free_vars)}
    var_str = [""] * n

    for free_var in free_vars:
        s = f"x{free_var+1}"
        var_str[free_var] += ch_map[s] if config["mapping"] == True else s
        
    all_zero_rows = 0
    for row in range(m):
        if not any(self.rref_coef_mat[row]):
            all_zero_rows += 1

    vec = self.vec[0:m-all_zero_rows]

    for pv_row, pv_col in enumerate(pivots):
        x = ""
        for free_var in free_vars:
            val = -self.rref_coef_mat[pv_row, free_var]
            x += (' + ' if val > 0 else ' - ') + \
                 (str(abs(val)) if abs(val) != 1 and val != 0 else "") + \
                 (ch_map[f"x{free_var+1}"] if config["mapping"] == True else s) \
                 if val != 0 else ""
        var_str[pv_col] += x
        var_str[pv_col] = str(vec[pv_row]) + var_str[pv_col]
    sol_str = '(' + str(var_str).strip("[]").replace("'", '') + ')'

    return sol_str

def rref(mat: np.ndarray):
    # 未來自己實作此部分
    rref_mat, pivots = sp.Matrix(mat).rref()
    return np.array(rref_mat.tolist()), pivots

def solution_type(rref_coef_mat: np.ndarray, vec: np.ndarray) -> LinSysSol:
    """ 
    rref_coef_mat: (m, n)
    vec          : (n,  ) 
    """

    m, n = len(rref_coef_mat), len(rref_coef_mat[0])
    sol_type = None

    all_zero_rows = 0
    for row in range(m):
        # the row that contains all zero is Ture.
        if not any(rref_coef_mat[row]):
            all_zero_rows += 1

    v = vec[m-all_zero_rows:m]
    v_bool = [i == 0 for i in v]

    if False in v_bool:
        sol_type = SolType.NO
    elif m - all_zero_rows == n and all([rref_coef_mat[i, i] == 1 for i in range(n)]):
        sol_type = SolType.UNIQUE
    else:
        sol_type = SolType.MANY
    return sol_type

def solver(mat: np.ndarray, augsize=1) -> list[LinSysSol]:
    """ 
    mat     : (m, p)
    coef_mat: (m, n)
    b_mat   : (m, p-n) 
    """

    if not isinstance(mat, np.ndarray):
        raise ValueError("Input matrix must be a ndarray.")

    rref_mat, _ = rref(mat)
    m, p = len(mat), len(mat[0])
    n = p - augsize

    coef_mat = rref_mat[:, :n]
    b_mat = rref_mat[:, n:p]

    solutions = []
    for b in b_mat.T:
        sol_type = solution_type(coef_mat, b)
        sol = LinSysSol(coef_mat, b, sol_type)
        solutions.append(sol)
        
    return solutions

if __name__ == "__main__":
    def print_sol(mat, augsize=1):
        sol = solver(mat, augsize=augsize)
        print(f"Solutions of matrix (augsize={augsize}) \n{mat} is:")
        for i, sol in enumerate(sol):
            print(f"{i+1}. {sol} for b = {mat[:, len(mat[0]) - augsize + i]}")

    mat1 = np.array([
        [1, 2, 3, 11, 2], 
        [0, -1, 1, -2, 7], 
        [1, 1, 4, 9, 1]
    ])
    
    mat2 = np.array([
        [1, -2, 3, 1, 1], 
        [2, -3, 2, -1, 4], 
        [3, -5, 5, 0, 5], 
        [1, -1, -1, -2, 3]
    ])

    mat3 = np.array([
        [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [0,  2,  0,  2,  4,  9,  6, 21,  3, 11, 25, 15, 21,  1,  1,  1,  0],
        [0,  2,  0,  2,  5,  8,  1, 16, 16, 14,  5, 23, 25,  5,  1, 18,  0], 
        [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
    ])

    mat4 = np.array([
        [1, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
        [0, 1, 0, 2, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 
        [0, 0, 1, 1, -3, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 
        [0, 0, 0, 0, 1, 0, 0, -1, 0, 0, -1, 0, 0, 0, -1]
    ])

    print_sol(mat1, augsize=2)
    print("==================================")
    print_sol(mat2, augsize=3)
    print("==================================")
    print_sol(mat3, augsize=8)
    print("==================================")
    print_sol(mat4, augsize=11)
