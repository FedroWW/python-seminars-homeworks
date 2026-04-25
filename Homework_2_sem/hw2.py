# №1 ПЕРИОДИКА

# Эврика:
# Если lps вычислен для всей строки s длины n, то:
# Наибольшая длина собственного префикса, совпадающего с суффиксом — lps[n-1]
# Наименьший период p = n - lps[n-1]
# Если n % p == 0, то ответ p, иначе ответ n

import sys
def computeLPSArray(pattern):
    n = len(pattern)
    lps = [0] * n
    len1 = 0
    i = 1
    while i < n:
        if pattern[i] == pattern[len1]:
            len1 += 1
            lps[i] = len1
            i += 1
        else:
            if len1 != 0:
                len1 = lps[len1 - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def min_period(s):
    n = len(s)
    if n == 0:
        return 0
    lps = computeLPSArray(s)
    p = n - lps[-1]
    return p if n % p == 0 else n


def solve():
    N_line = sys.stdin.readline()
    if not N_line:
        return
    N = int(N_line.strip())

    # пропуск пустой строки после N
    line = sys.stdin.readline()
    while line and line.strip() == '':
        line = sys.stdin.readline()

    results = []
    count = 0
    while count < N:
        s = line.strip()
        results.append(str(min_period(s)))
        count += 1

        # читаем оставшиеся пустые строки до следующего теста или конца ввода
        line = sys.stdin.readline()
        while line and line.strip() == '' and count < N:
            line = sys.stdin.readline()

    print('\n\n'.join(results))
solve()

#________
# Манакер <--- идея=задача
#--------
# Эврика: найдем сумму максимальных радиусов (то бишь количество палиндромов с данным центром)
# от всех центров для четных и не четных палинромов и получим кол-во палиндромов в слове  :)
def count_palindromes(s):
    n = len(s)
    if n == 0:
        return 0

    d1 = [0] * n  #количество палиндромов нечетной длины с центром в символе i == максимальный радиус
    # границы самого правого из уже найденных палиндромов
    l = 0
    r = -1
    for i in range(n):
        # k - текущий радиус
        k = 1 if i > r else min(d1[l + r - i], r - i + 1) # l+r-1 зеркальный индекс для i
        while i - k >= 0 and i + k < n and s[i - k] == s[i + k]:
            k += 1
        d1[i] = k
        if i + k - 1 > r:
            l = i - k + 1
            r = i + k - 1
    # аналогично с четными палиндромами только центр между i и i-1
    d2 = [0] * n
    l = 0
    r = -1
    for i in range(n):
        k = 0 if i > r else min(d2[l + r - i + 1], r - i + 1)
        while i - k - 1 >= 0 and i + k < n and s[i - k - 1] == s[i + k]:
            k += 1
        d2[i] = k
        if i + k - 1 > r:
            l = i - k
            r = i + k - 1

    total = sum(d1) + sum(d2)
    return total


import sys
s = sys.stdin.readline().strip()
print(count_palindromes(s))


#________
# Циклики
#--------
# Идея:
# Строим суффиксный массив как prefix doubling
# сортируем циклические сдвиги
# поиск слова:слово соответствует сдвигу с s[0]. В массиве sa ищется индекс i, для которого sa[i] == 0 (+1)
# столбец:для каждого сдвига с началом start берётся символ, предшествующий start в циклической строке: s[(start - 1) % n]

def suffix_array(s):
    s += "$"
    n = len(s)
    p = [0] * n
    c = [0] * n

    # индексация степени двойки с k = 0
    a = sorted((ch, i) for i, ch in enumerate(s))
    for i in range(n):
        p[i] = a[i][1]

    c[p[0]] = 0
    for i in range(1, n):
        c[p[i]] = c[p[i - 1]] + (a[i][0] != a[i - 1][0])

    k = 0
    while (1 << k) < n:
        p = [(x - (1 << k)) % n for x in p]
        p.sort(key=lambda x: (c[x], c[(x + (1 << k)) % n]))

        c_new = [0] * n
        c_new[p[0]] = 0

        for i in range(1, n):
            prev = (c[p[i - 1]], c[(p[i - 1] + (1 << k)) % n])
            now = (c[p[i]], c[(p[i] + (1 << k)) % n])
            c_new[p[i]] = c_new[p[i - 1]] + (now != prev)

        c = c_new
        k += 1
    return p[1:]  #убрали $

def solve():
    import sys
    s = sys.stdin.readline().strip()
    if not s:
        print(-1)
        print()
        return

    n = len(s)
    sa = suffix_array(s)

    # Позиция исходного слова начинается с индекса 0,
    pos = -1
    for i, start in enumerate(sa):
        if start == 0:
            pos = i + 1     # а нумерация с 1
            break
    last_col = ''.join(s[(start - 1) % n] for start in sa)

    print(pos)
    print(last_col)
solve()