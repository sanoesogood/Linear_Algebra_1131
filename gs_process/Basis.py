# /**----------------------------------------------------------*
#  * first version: 2024/12/21                                 *
#  * github: https://github.com/sanoesogood                    *
#  *----------------------------------------------------------**/

import numpy as np

class Basis:
    def __init__(self, basis):
        self.basis = basis

    def orthogonol(self):
        return gs_process(self.basis)

    def orthonormal(self):
        return np.array([v / np.linalg.norm(v) for v in gs_process(self.basis)])


def _sum_proj_v_onto_u(v, u_set):
    return sum([np.dot(v, u.T) / np.dot(u, u.T) * u for u in u_set])

def gs_process(basis):
    u_set = []
    for v in basis:
        if not u_set:
            u_set.append(v)
            continue

        u = v - _sum_proj_v_onto_u(v, u_set)
        u_set.append(u)
    return np.array(u_set)
