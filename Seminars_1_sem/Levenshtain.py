def isequal(p:str,q:str):
    if p == q:
        return 0
    else:
        return 1

def minDistance(word1: str, word2: str) -> int:
    n = len(word1)
    m = len(word2)

    dp = [[0]*(m+1) for _ in range(n+1)]

    for i in range(1,n+1):
        for j in range(1,m+1):
            if i==j:
                dp[i][j]=0
            if j==0 and i>0:
                dp[i][j]=i
            if i==0 and j>0:
                dp[i][j]=j
            else:
                    dp[i][j] = min(
                    dp[i][j-1]+1,
                    dp[i-1][j]+1,
                    dp[i-1][j-1]+isequal(word1[i-1],word2[j-1]),
                )
    print(dp)
    return dp[n][m]

s=input()
t=input()
print(minDistance(s,t))