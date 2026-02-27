import random
import time
'''
#устойчивая
def bubble_sort(arr):
    N = len(arr)
    for i in range(N):
        for j in range(N-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
        #print(arr)
    return arr

#устойчивая
def insert_sort(arr):
    N = len(arr)
    for i in range(N):
        tmp = arr[i]
        j = i - 1
        while j >= 0 and tmp < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = tmp
        print(arr)
    return arr
'''

def select_sort(arr):
    N = len(arr)
    for i in range(N-1):
        min = 10000000
        for j in range(i,N):
            if arr[j] < min:
                min = arr[j]
                min_index = j
        tmp = arr[i]
        arr[i] = min
        arr[min_index] = tmp
    return arr

'''
# in-place сортировки
def merge(A,B):
    len_a = len(A)
    len_b = len(B)
    C = []
    i = 0
    j = 0
    while i < len_a or j < len_b:
        if i >= len_a:
            C.append(B[j])
            j += 1
            continue
        if j >= len_b:
            C.append(A[i])
            i += 1
            continue
        if A[i] < B[j]:
            C.append(A[i])
            i += 1
        else:
            C.append(B[j])
            j += 1

    return C

def merge_sort(arr):
    N = len(arr)
    if N == 1:
        return arr

    ind = N//2
    L = arr[0:ind]
    R = arr[ind:]
    return merge(merge_sort(L),merge_sort(R))

A = [random.choice('abcd') for i in range(10)]
print(A)
print(merge_sort(A))


def insertion_sort(a):
  n = len(a)
  for i in range(1, n):
    for j in range(i, 0, -1):
      if a[j] < a[j-1]:
        a[j], a[j-1] = a[j-1], a[j]
        print(a)

a = [15, -6, 3, 14, -23, 3, 12]
insertion_sort(a)
'''