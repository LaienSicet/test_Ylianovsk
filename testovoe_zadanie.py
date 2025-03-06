from instryment import *

# без асинхронности. прсто выполнение первой части ТЗ.

print(1)
a = obrabotka_stranihi('1')
for i in a:
    print(i, a[i], '\n')

print('-'*100, '\n', 2)
b = obrabotka_stranihi('2')
for i in b:
    print(i, b[i], '\n')