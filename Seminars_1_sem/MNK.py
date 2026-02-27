import numpy as np


arr = np.array([1,2,3])
print(arr)
arr2 = np.array([2,3,4])
matrix = np.stack([arr,arr,arr2])
matrix2 = np.stack([arr,arr2,arr2])
print(matrix, matrix2)
print(matrix*matrix2)
print(matrix@matrix2)


arr = np.array([1,2,3])
print(arr)
arr2=np.array([2,3,4])
print(arr@arr2) #скалярное произведегние

matrix = np.array([arr,arr,arr2])

#Метод наименьших квадратов
y=[0,0.206,0.309,0.412,0.515,0.618,0.721,0.824,0.927,1.030]
x=[0,1.247,2.282,3.049,4.558,5.518,6.693,7.819,8.898,10.143]

def mnk(x,y):
    x = np.array(x)
    y = np.array(y)
    b = ((x*y).mean() - x.mean()*y.mean())/((x**2).mean() - x.mean()**2)
    a = y.mean() - b*x.mean()
    return a, b

print(mnk(x,y))

arr0=np.zeros(5)
arr1=np.ones(5)
arr1=np.ones(1)*5
print(arr1)
print (arr1+arr0)

arr1 = np.ones((2,2))
print(arr1)
arr2 = np.array([0,1])*0.5
print(arr1+arr2)
# arr2**2 == arr2*arr2
#arr2 = np.ones(2)*5
#print(arr2)
#print(arr1+arr2)


import numpy as np


def sigma_k_calculation(x, y):
    """
    Вычисляет погрешность коэффициента наклона σₖ.

    Формула: σₖ = 1/√N * √[((y²) - (y)²)/((x²) - (x)²) - k²]
    """
    x = np.array(x)
    y = np.array(y)

    if len(x) != len(y):
        raise ValueError("Длины массивов x и y должны совпадать")

    N = len(x)

    # Средние значения
    x_mean = np.mean(x)
    y_mean = np.mean(y)

    # Средние квадратов
    x2_mean = np.mean(x ** 2)
    y2_mean = np.mean(y ** 2)

    # Коэффициент наклона k
    k = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)

    # Вычисление σₖ
    numerator = y2_mean - y_mean ** 2
    denominator = x2_mean - x_mean ** 2

    if denominator == 0:
        return float('inf'), k  # или raise исключение

    expression = (numerator / denominator) - k ** 2

    # Обработка отрицательного значения под корнем
    if expression < 0:
        expression = 0  # или использовать abs(expression)

    sigma_k = (1 / np.sqrt(N)) * np.sqrt(expression)

    return sigma_k, k

x = [(2.4+5.8/100)**2,(2.4+6.8/100)**2,(2.4+7.8/100)**2,(2.4+8.8/100)**2,(2.4+9.8/100)**2,(2.4+10.8/100)**2,(2.4+11.8/100)**2,(2.4+12.8/100)**2,(2.4+13.8/100)**2,(2.4+14.8/100)**2]
y = [1.623**2,1.666**2,1.732**2,1.81**2,1.867**2,1.974**2,2.065**2,2.177**2,2.26**2,2.357**2]

sigma_k, k = sigma_k_calculation(x, y)
print(f"k = {k:.4f}")
print(f"σₖ = {sigma_k:.4f}")