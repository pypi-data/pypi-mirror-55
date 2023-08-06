import numpy as np
import numba as nb


@nb.jit(fastmath=True, cache=True)
def expreval(basis, x, M, output_array):
    # u_{ijk} = X_{im}Y_{jn}Z_{ko} u_{mno}
    # u_{ij}  = X_{im}Y_{jn} u_{mn}
    shape = output_array.shape
    if len(x) == 2:
        for md in M:
            bv = basis
            if bv.rank > 0:
                bv = bv[md[0]]
            S = np.array([md[1].shape[1], md[2].shape[1]], dtype=np.int)
            output_array = _eval2D(np.array(shape, dtype=np.int), md[1], md[2], S, bv, output_array)

    elif len(x) == 3:
        for md in M:
            bv = basis
            if bv.rank > 0:
                bv = bv[md[0]]
            S = np.array([md[1].shape[1], md[2].shape[1], md[3].shape[1]], dtype=np.int)
            output_array = _eval3D(np.array(shape, dtype=np.int), md[1], md[2], md[3], S, bv, output_array)

    return output_array

@nb.jit(nopython=True, fastmath=True, cache=True)
def _eval2D(shape, md1, md2, S, bv, output_array):
    for i in range(shape[0]):
        for j in range(shape[1]):
            for m in range(S[0]):
                for n in range(S[1]):
                    output_array[i, j] +=  md1[i, m]*md2[j, n]*bv[m, n]
    return output_array

@nb.jit(nopython=True, fastmath=True, cache=True)
def _eval3D(shape, md1, md2, md3, S, bv, output_array):
    for i in range(shape[0]):
        for j in range(shape[1]):
            for k in range(shape[2]):
                for m in range(S[0]):
                    for n in range(S[1]):
                        for o in range(S[2]):
                            output_array[i, j, k] +=  md1[i, m]*md2[j, n]*md3[k, o]*bv[m, n, o]
    return output_array
