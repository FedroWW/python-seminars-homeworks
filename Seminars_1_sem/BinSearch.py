def binary_search(arr,x):
    l=0
    r=len(arr)
    while(r-l>1):
        m=(l+r)//2
        if arr[m]<x:
            l=m
        else:
            r=m
    if (arr[l]==x or arr[r]==x):
        return 'Yes'
    else: return 'No'

Z=list(map(int,input().split()))
print(binary_search(Z,5))

