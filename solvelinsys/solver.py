import numpy as np
import sympy as sp
from enum import Enum

class SolType(Enum):
    NO = "no"
    UNIQUE = "unique"
    MANY = "many"

class LinSysSol:
    def __init__(self, rref_coef_mat, vec, type: SolType):
        self.rref_coef_mat = rref_coef_mat
        self.vec = vec
        self.type = type

    def __str__(self):
        sol_type_str = f"{self.type.value} solution."
        match self.type:
            case SolType.UNIQUE:
                return self._tostring() + ', ' + sol_type_str + f" for b = {sol.vec}"
            case SolType.MANY:
                return self._tostring() + ', ' + sol_type_str + f" for b = {sol.vec}"
            case SolType.NO:
                return sol_type_str + f" for b = {sol.vec}"

    def tostring(self) -> str:
        return self._tostring()

    def _tostring(self) -> list[str]:
        m, n = len(self.rref_coef_mat), len(self.rref_coef_mat[0])
        _, pivots = rref(self.rref_coef_mat)
        free_vars = [i for i in range(n) if i not in pivots]
        var = []

        for free_var in free_vars:
            var.append((f"x{free_var+1}", {f"x{free_var+1}": 1}))

        for pv_row, pv_col in enumerate(pivots):
            if pv_col < n:
                x = {}
                for free_var in free_vars:
                    x.update({f"x{free_var+1}": -self.rref_coef_mat[pv_row, free_var]})
                var.append((f"x{pv_col+1}", x))

            var.sort()
        
        ch_map = {f"x{free_var+1}": f"t{i}" for i, free_var in enumerate(free_vars)}

        var_str = []
        for _, vec in var:
            l = ""
            for k, v in vec.items():
                l = l + \
                    (' + ' if v >= 0 else ' - ') + \
                    (str(abs(v)) if v != 1 and v != 0 else "") + \
                    ch_map[k]
            var_str.append(l)
        
        sol_lst = []
        vec = list(self.vec)
        for i in range(n):
            sol_lst.append(str(vec[i]) + var_str[i])

        sol_str = '(' + str(sol_lst).strip("[]").replace("'", '') + ')'

        return sol_str

def rref(mat: np.array):
    # 未來自己實作此部分
    rref_mat, pivots = sp.Matrix(mat).rref()
    return np.array(rref_mat.tolist()), pivots

def solution_type(rref_coef_mat, vec) -> LinSysSol:
    """ 
    rref_coef_mat: (m, n)
    vec          : (n,  ) 
    """

    m, n = len(rref_coef_mat), len(rref_coef_mat[0])
    sol_type = None

    # unique solution:
    if all([rref_coef_mat[i, i] == 1 \
            for i in range(m if m < n else n)]):
            sol_type = [SolType.UNIQUE]
    
    # many solution or no solution
    else:
        all_zero_rows = 0
        for row in range(m):
            # the row that contains all zero is Ture.
            if not any(rref_coef_mat[row]):
                all_zero_rows += 1
                
        # 可以做出告訴為什麼無解 (如: 因為 0 != 1, 無解) 的效果
        v = vec[-all_zero_rows:]
        v_bool = [i == 0 for i in v]
        sol_type = SolType.NO if False in v_bool else SolType.MANY
            
    return sol_type

def solver(mat, augsize=1) -> LinSysSol:
    """ 
    mat     : (m, p)
    coef_mat: (m, n)
    b_mat   : (n, p) 
    """

    rref_mat, _ = rref(mat)
    m, p = len(mat), len(mat[0])
    n = p - augsize

    coef_mat = rref_mat[:, :n]
    b_mat = rref_mat[:, n:p]
    print(coef_mat)
    print(b_mat)
    solutions = []
    for b_vec in b_mat.T:
        sol_type = solution_type(coef_mat, b_vec)
        sol = LinSysSol(coef_mat, b_vec, sol_type)
        solutions.append(sol)
    
    return solutions

if __name__ == "__main__":
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

    sol1 = solver(mat1, augsize=2)
    sol2 = solver(mat2)

    print(f"Solutions of matrix (augsize=2) \n{mat1} is:")
    for i, sol in enumerate(sol1):
        print(f"{i+1}. {sol}")

    print("==================================")

    print(f"Solutions of matrix (augsize=1) \n{mat2} is:")
    for i, sol in enumerate(sol2):
        print(f"{i+1}. {sol}")
