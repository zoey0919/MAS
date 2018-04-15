#!/usr/bin/env python3
# Ulas Kamaci - 2018-04-02

import numpy as np
from matplotlib import pyplot as plt

def my_herm(input_mtx,block_dim):
    r""" This function realizes the Hermitian transpose operation for a block
    matrix with diagonal blocks. However, the function assumes that the input
    matrix has its (block_dim^2 by block_dim^2) diagonal blocks reshaped into
    (block_dim by block_dim) blocks. We call this reshaped form as the
    "compressed" form.

    Args:
        input_mtx: The input matrix whose hermitian will be taken. It must be
            in the "compressed" form. For example, if the dimension of the
            "uncompressed" input_mtx is (row_num*block_dim^2 by
            col_num*block_dim^2), then the dimension of input_mtx must be
            (row_num*block_dim by col_num*block_dim)
        block_dim: Dimension of each block in input_mtx (assuming square blocks)

    Returns:
        out: The output matrix, which is in the "compressed" form of the
            Hermitian transpose of the original block matrix with diagonal
            blocks.
    """
    # number of blocks in row and column dimensions
    row_num = int(input_mtx.shape[0]/block_dim)
    col_num = int(input_mtx.shape[1]/block_dim)

    out = np.zeros((col_num*block_dim,row_num*block_dim),dtype=complex)

    for i in range(col_num):
        for j in range(row_num):
            out[i*block_dim:(i+1)*block_dim , j*block_dim:(j+1)*block_dim] = (
            np.conjugate(input_mtx[j*block_dim:(j+1)*block_dim ,
            i*block_dim:(i+1)*block_dim])
            )

    return out

def my_mul(x,y,block_dim):
    """ This function realizes the matrix multiplication operation for a block
    matrix with diagonal blocks. However, the function assumes that the input
    matrix has its (block_dim^2 by block_dim^2) diagonal blocks reshaped into
    (block_dim by block_dim) blocks. We call this reshaped form as the
    "compressed" form.

    Args:
        x: The input matrix as being the first multiplicand. It must be in the
            "compressed" form. For example, if the dimension of the
            "uncompressed" x is (row_num*block_dim^2 by col_num*block_dim^2),
            then the dimension of x must be (row_num*block_dim by
            col_num*block_dim)
        y: The second multiplicand, having the same properties as x
        block_dim: Dimension of each block in x and y (assuming square blocks)

    Returns:
        out: The output matrix, which is the compressed (see the function
            definition) version of the multiplication of the two block diagonal
            matrices with diagonal blocks
    """
    row_x = int(x.shape[0]/block_dim)
    col_x = int(x.shape[1]/block_dim)
    col_y = int(y.shape[1]/block_dim)

    out = np.zeros((x.shape[0],y.shape[1]),dtype=complex)

    for i in range(row_x):
        for j in range(col_y):
            for k in range(col_x):
                out[i*block_dim:(i+1)*block_dim , j*block_dim:(j+1)*block_dim]=(
                out[i*block_dim:(i+1)*block_dim , j*block_dim:(j+1)*block_dim]+
                x[i*block_dim:(i+1)*block_dim , k*block_dim:(k+1)*block_dim]*
                y[k*block_dim:(k+1)*block_dim , j*block_dim:(j+1)*block_dim])

    return out

def my_inv(A,block_dim):
    """ This function realizes the matrix inversion operation for a Hermitian
    symmetric block matrix with diagonal blocks. However, the function assumes
    that the input matrix has its (block_dim^2 by block_dim^2) diagonal blocks
    reshaped into (block_dim by block_dim) blocks. We call this reshaped form
    as the "compressed" form.

    Args:
        A: The input matrix whose inverse will be computed. It must be in the
            "compressed" form. For example, if the dimension of the
            "uncompressed" A is (numblocks*block_dim^2 by numblocks*block_dim^2)
            , then the dimension of A must be (numblocks*block_dim by
            numblocks*block_dim)
        block_dim: Dimension of each block in A (assuming square blocks)

    Returns:
        out: The compressed (see the function definition) version of the inverse
    """

    numblocks = int(A.shape[0]/block_dim)
    print('numblocks=%d' % numblocks)

    if numblocks == 1:
        out = 1 / A
        return out

    elif numblocks == 2:
        A11 = A[ :block_dim , :block_dim]
        A12 = A[ :block_dim , block_dim:2*block_dim]
        A21 = A[block_dim:2*block_dim , :block_dim]
        A22 = A[block_dim:2*block_dim, block_dim:2*block_dim]

        A11i = 1/A11
        A22hat = A22 - my_mul(my_herm(A12,block_dim),my_mul(A11i,A12,block_dim),block_dim)
        A22hati = 1/A22hat;

        A11hati = A11i + my_mul(A11i,my_mul(A12,my_mul(A22hati,my_mul(my_herm(A12,block_dim),A11i,block_dim),block_dim),block_dim),block_dim);

        A21hat = -my_mul(A22hati,my_mul(A21,A11i,block_dim),block_dim);
        A12hat = my_herm(A21hat,block_dim);

        out = np.concatenate((np.concatenate((A11hati,A12hat),axis=1),np.concatenate((A21hat,A22hati),axis=1)),axis=0)

        return out

    else:
        numblocks1 = int(np.floor(numblocks/2))

        A11 = A[:block_dim*numblocks1, :block_dim*numblocks1];
        A12 = A[:block_dim*numblocks1, block_dim*numblocks1:];
        A21 = A[block_dim*numblocks1: ,:block_dim*numblocks1];
        A22 = A[block_dim*numblocks1: ,block_dim*numblocks1:];

        A11i = my_inv(A11,block_dim);
        A22hat = A22 - my_mul(my_herm(A12,block_dim),my_mul(A11i,A12,block_dim),block_dim);
        A22hati = my_inv(A22hat,block_dim);

        A11hati = A11i + my_mul(A11i,my_mul(A12,my_mul(A22hati,my_mul(my_herm(A12,block_dim),A11i,block_dim),block_dim),block_dim),block_dim);

        A21hat = -my_mul(A22hati,my_mul(A21,A11i,block_dim),block_dim);
        A12hat = my_herm(A21hat,block_dim);

        out = np.concatenate((np.concatenate((A11hati,A12hat),axis=1),np.concatenate((A21hat,A22hati),axis=1)),axis=0)

        return out

def indexer(x,i,j,block_dim):
    """Takes the (row,col)^th block of a block matrix with square blocks of size
    block_dim. For example, if the input matrix has dimensons (m*block_dim by
    n*block_dim), then we can regard this matrix as a (m by n) block matrix with
    (block_dim by block_dim) blocks. This function outputs the (i,j)^th block
    out of (m by n) ones.

     Args:
        x: The input matrix, which is considered to be composed of (block_dim by
            block_dim) blocks.
        i: Indicates the row number of the block to be extracted
        j: Indicates the column number of the block to be extracted
        block_dim: Dimension of each block in x (assuming square blocks)

    Returns:
        out: The extracted block of dimension (block_dim by block_dim)
    """
    out = x[i*block_dim:(i+1)*block_dim , j*block_dim:(j+1)*block_dim]
    return out

def block_fft2(x,block_dim,fft_dim):
    """Takes the (fft_dim by fft_dim) point 2D FFT of each (block_dim by
    block_dim) block of the input matrix x. If x is of dimension (m*block_dim by
    n*block_dim), then the output matrix has dimension (m*fft_dim by n*fft_dim)

    Args:
        x: The input matrix
        block_dim: Dimension of each block in x (assuming square blocks)
        fft_dim: Number of points of 2D FFT to be taken. This also determines
            the output block size

    Returns:
        out: The output matrix whose each block is the 2D FFT of the
            corresponding block of the input matrix
    """
    from numpy.fft import fft2, fftshift, ifftshift
    k,p = x.shape
    k = k//block_dim
    p = p//block_dim
    out = np.zeros((k*fft_dim,p*fft_dim),dtype=complex)

    if fft_dim == block_dim:
        for i in range(k):
            for j in range(p):
                temp = indexer(x,i,j,block_dim)
                temp = fftshift(fft2(ifftshift(temp)))
                out[i*fft_dim:(i+1)*fft_dim , j*fft_dim:(j+1)*fft_dim] = temp

    else:
        for i in range(k):
            for j in range(p):
                temp = indexer(x,i,j,block_dim)
                print('temp_indexed=(%d,%d)' % temp.shape)
                pad_dim = int( np.ceil( (fft_dim-block_dim)/2. ) )
                print('pad_dim=%d' % pad_dim)
                temp = np.pad(temp,pad_dim,'constant')
                print('temp_padded=(%d,%d)' % temp.shape)
                temp = temp[:fft_dim,:fft_dim]
                print('temp_truncated=(%d,%d)' % temp.shape)
                temp = fftshift(fft2(ifftshift(temp)))
                print('temp_fft=(%d,%d)' % temp.shape)
                out[i*fft_dim:(i+1)*fft_dim , j*fft_dim:(j+1)*fft_dim] = temp
    return out

def block_ifft2(x,block_dim):
    """Takes 2D inverse FFT of each (block_dim by block_dim) block of the input
    matrix x.

    Args:
        x: The input matrix
        block_dim: Dimension of each block in x (assuming square blocks)

    Returns:
        out: The output matrix whose each block is the 2D inverse FFT of the
            corresponding block of the input matrix
    """
    from numpy.fft import ifft2, fftshift, ifftshift
    k,p = x.shape
    k = k//block_dim
    p = p//block_dim
    out = np.zeros((k*block_dim,p*block_dim),dtype=complex)

    for i in range(k):
        for j in range(p):
            temp = indexer(x,i,j,block_dim)
            temp = fftshift(ifft2(ifftshift(temp)))
            out[i*block_dim:(i+1)*block_dim , j*block_dim:(j+1)*block_dim] = temp
    return out
