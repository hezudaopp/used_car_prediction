from numpy import *

"""locally weighted linear regression"""
def lwlr(test_point,x_arr,y_arr,k=1.0):
    x_mat = mat(x_arr)
    y_mat = mat(y_arr).T
    m = shape(x_mat)[0]
    weights = mat(eye((m)))
    for j in range(m):                      #next 2 lines create weights matrix
        diff_mat = test_point - x_mat[j,:]     #
        weights[j,j] = exp(diff_mat*diff_mat.T/(-2.0*k**2))
    xTx = x_mat.T * (weights * x_mat)
    if linalg.det(xTx) == 0.0:
        print "This matrix is singular, cannot do inverse"
        return -1
    ws = xTx.I * (x_mat.T * (weights * y_mat))
    return test_point * ws

#squared error sum
def rss_error(y_arr, y_hat_arr):
	return ((array(map(float, y_arr)) - array(map(float, y_hat_arr))) ** 2).sum()