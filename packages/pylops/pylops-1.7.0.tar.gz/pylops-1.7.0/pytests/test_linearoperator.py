import pytest

import numpy as np
from numpy.testing import assert_array_almost_equal

from pylops.basicoperators import MatrixMult, VStack, Diagonal, Zero

par1 = {'ny': 11, 'nx': 11,
        'imag': 0, 'dtype':'float32'}  # square real
par2 = {'ny': 21, 'nx': 11,
        'imag': 0, 'dtype':'float32'}  # overdetermined real
par1j = {'ny': 11, 'nx': 11,
         'imag': 1j, 'dtype':'complex64'} # square imag
par2j = {'ny': 21, 'nx': 11,
         'imag': 1j, 'dtype': 'complex64'}  # overdetermined imag


@pytest.mark.parametrize("par", [(par1), (par2), (par1j)])
def test_eigs(par):
    """Eigenvalues and condition number estimate with ARPACK
    """
    # explicit=True
    diag = np.arange(par['nx'], 0, -1) +\
           par['imag'] * np.arange(par['nx'], 0, -1)
    Op = MatrixMult(np.vstack((np.diag(diag),
                               np.zeros((par['ny'] - par['nx'], par['nx'])))))
    eigs = Op.eigs()
    assert_array_almost_equal(diag[:eigs.size], eigs, decimal=3)

    cond = Op.cond()
    assert_array_almost_equal(np.real(cond), par['nx'], decimal=3)

    #  explicit=False
    Op = Diagonal(diag, dtype=par['dtype'])
    if par['ny'] > par['nx']:
        Op = VStack([Op, Zero(par['ny'] - par['nx'], par['nx'])])
    eigs = Op.eigs()
    assert_array_almost_equal(diag[:eigs.size], eigs, decimal=3)

    cond = Op.cond()
    assert_array_almost_equal(np.real(cond), par['nx'], decimal=3)


@pytest.mark.parametrize("par", [(par1), (par2), (par1j), (par2j)])
def test_conj(par):
    """Complex conjugation
    """
    M = 1j * np.ones((par['ny'], par['nx']))
    Op = MatrixMult(M, dtype=np.complex)
    Opconj = Op.conj()

    x = np.arange(par['nx']) + \
        par['imag'] * np.arange(par['nx'])
    y = Opconj * x

    # forward
    assert_array_almost_equal(Opconj * x, np.dot(M.conj(), x))

    # adjoint
    assert_array_almost_equal(Opconj.H * y, np.dot(M.T, y))


@pytest.mark.parametrize("par", [(par1), (par2)])
def test_apply_columns_explicit(par):
    """Apply columns to explicit and non-explicit operator
    """
    M = np.ones((par['ny'], par['nx']))
    Mop = MatrixMult(M, dtype=par['dtype'])
    M1op = MatrixMult(M, dtype=par['dtype'])
    M1op.explicit = False
    cols = np.sort(np.random.permutation(np.arange(par['nx']))[:par['nx']//2])

    Mcols = M[:, cols]
    Mcolsop = Mop.apply_columns(cols)
    M1colsop = M1op.apply_columns(cols)

    x = np.arange(len(cols))
    y = np.arange(par['ny'])

    # forward
    assert_array_almost_equal(Mcols @ x, Mcolsop.matvec(x))
    assert_array_almost_equal(Mcols @ x, M1colsop.matvec(x))

    # adjoint
    assert_array_almost_equal(Mcols.T @ y, Mcolsop.rmatvec(y))
    assert_array_almost_equal(Mcols.T @ y, M1colsop.rmatvec(y))