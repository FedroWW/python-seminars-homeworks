import numpy as np
import matplotlib.pyplot as plt


def vandermonde_matrix(n):
    A = np.zeros((n + 1, n + 1))
    for i in range(n + 1):
        for j in range(n + 1):
            A[i][j] = (i / n) ** j if n != 0 else 1
    return A


cond_vandermonde = np.zeros(101)

for i in range(1, 101):
    matrix = vandermonde_matrix(i)
    matrix_inv = np.linalg.inv(matrix)
    cond_vandermonde[i] = np.array(np.linalg.norm(matrix) * np.linalg.norm(matrix_inv))

n_values = np.zeros(101)

for i in range(1, 101):
    n_values[i] = np.array(i)
plt.semilogy(n_values, cond_vandermonde)
plt.ylabel('n')
plt.xlabel('Число Обусловленности')
plt.title('Зависимость числа обусловленности от n')
plt.show()