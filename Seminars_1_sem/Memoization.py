#с запоминанием
#cache(кэш)-список cache[n]=f(n)
#cache=[0*n]
def fib_memo(n,cache=[]):
    if n==0:
        return 0
    if n==1:
        return 1
    if cache[n]!=0:
        return cache[n]
    cache[n]=fib_memo(n-1,cache)+fib_memo(n-2,cache)
    return cache[n]

import time

t=time.time()
cache=[0]*51
print(fib_memo(50, cache))
t=time.time()-t
print(t)


# Горизонтальная рекурсивная ёлка
def func(x, symb):
    if x == 1:
        print(symb * ((N - x) // 2 + 1))
        return

    # то что до рекурсивного вызова
    # вызывается на прямом ходу рекурсии
    print(symb * ((N - x) // 2 + 1))
    func(x - 2, symb)
    # то что после рекурсивного вызова
    # вызывается на обратном ходу рекурсии
    print(symb * ((N - x) // 2 + 1))

N=7
s='@'
print(func(N,s))