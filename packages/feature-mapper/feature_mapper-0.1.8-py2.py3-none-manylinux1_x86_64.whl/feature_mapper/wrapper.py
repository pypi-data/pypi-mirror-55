import numpy as np
from scipy import sparse

from .feature_mapper import ffi, lib


def C(spm):
    return dict(shape=spm.shape,
                indices=(len(spm.indices),
                         ffi.cast("int32_t *", spm.indices.ctypes.data)),
                indptr=(len(spm.indptr),
                        ffi.cast("int32_t *", spm.indptr.ctypes.data)))


def Py(c):
    return sparse.csr_matrix(
        (np.ones(c.indices.len,
                 dtype=np.bool), ffi.unpack(c.indices.vec, c.indices.len),
         ffi.unpack(c.indptr.vec, c.indptr.len)),
        shape=(c.shape.rows, c.shape.cols))


def sparsify(mat):
    """
    Take any (kind-of boolean) matrix and convert to sparse row matrix.
    """

    if sparse.issparse(mat):
        return mat.tocsr()
    else:
        return sparse.csr_matrix(np.array(mat, dtype=np.int8))


def map_feature(spm, im):
    spm = C(sparsify(spm))
    im = C(sparsify(im))
    assert spm['shape'][1] == im['shape'][1],\
        "Number of columns of in-feature and mapping matrices must match."
    return Py(lib.remap_rows(spm, im))


def map_feature_smin(spm, im, smin):
    spm = C(sparsify(spm))
    im = C(sparsify(im))
    assert spm['shape'][1] == im['shape'][1],\
        "Number of columns of in-feature and mapping matrices must match."
    return Py(lib.remap_rows_smin(spm, im, smin))
