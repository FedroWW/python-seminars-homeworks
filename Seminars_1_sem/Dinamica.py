
#сколько существует различных групп с суммой сил n,таких что
#сила каждого участника группы отличасется меньше чем в 2 раза
#в dp[i][j] будем хранить количество неинтересных групп с суммой сил j
#при этом каждый участник группы имеет силу не больше i

def notinterest(n):
    dp = [[0] * (n+1) for _ in range(n+1)]
    dp[0][0] = 1
    for i in range(1, n + 1):
            for j in range(0, i):
                dp[i][j] = dp[i - 1][j]
            for j in range(i, n + 1):
                dp[i][j] = dp[i - 1][j]
                if j - i >= 0:
                    dp[i][j] += dp[i//2][j - i]
    return dp[n][n]

n = int(input())
print(notinterest(n))



'''
2 вариант выполнения

def turnir(n):
    dp = [[0] * (n + 1) for i in range(n + 1)]
    dp[0][0] = 1
    for i in range(1, n + 1):
        for j in range(0, n + 1):
            dp[i][j] = dp[i - 1][j]
            if j >= i:
                dp[i][j] += dp[i // 2][j - i]
    return dp[n][n], dp


print(turnir(int(input())))
'''




'''

#N- количество товаров M-лимит ресурсов
# в первой строке содержатся иксы и их сумма от 0 до N<=M
#  во второй строке игики и их сумма должна быть максимизирована
#в dp[i][j] будем хранить максимальную сытость в зависимсти от товара

def sol(N,M,x,y):
    resources=[0]
    resources.extend(x) #метод добавления в начало
    points=[0]
    points.extend(y)
    dp=[[0] * (M+1) for _ in range(N+1)]
    for i in range(1,N+1):
        for j in range(1,M+1):
            if (resources[i]>j):
                dp[i][j]=dp[i-1][j]
            else:
                dp[i][j]=max(dp[i-1][j],dp[i-1][j-resources[i]]+points[i])

    return dp[N][M]

N,M=map(int, input().split())
x=list(map(int, input().split()))
y=list(map(int, input().split()))
print(sol(N,M,x,y))


#мы идём по полю и не можем два раза подряд повторить один и тот же шаг
#задача собрать максимальное количество гемов

n, m = map(int, input().split())
elem= [list(map(int, input().split())) for _ in range(n)]
dp = [[[-10 ** 10] * 3 for _ in range(m)] for _ in range(n)]
dp[0][0][0] = elem[0][0]

# 0 - слева, 1 - сверху, 2 - диагональ
if m > 1:
    dp[0][1][0] = elem[0][1] + elem[0][0]
if n > 1:
    dp[1][0][1] = elem[1][0] + elem[0][0]
if n > 1 and m > 1:
    dp[1][1][2] = elem[1][1] + elem[0][0]
for i in range(1, n):
    for j in range(1, m):
        if dp[i][j - 1][1] != -10 ** 10 or dp[i][j - 1][2] != -10 ** 10:
            dp[i][j][0] = max(dp[i][j - 1][1], dp[i][j - 1][2]) +  elem[i][j]

        if dp[i - 1][j][0] != -10 ** 10 or dp[i - 1][j][2] != -10 ** 10:
            dp[i][j][1] = max(dp[i - 1][j][0], dp[i - 1][j][2]) + elem[i][j]

        if dp[i - 1][j - 1][0] != -10 ** 10 or dp[i - 1][j - 1][1] != -10 ** 10:
            dp[i][j][2] = max(dp[i - 1][j - 1][1], dp[i - 1][j - 1][0]) + elem[i][j]


print(max(dp[n - 1][m - 1]))
'''




