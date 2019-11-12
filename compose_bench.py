import os
import ctypes
from random import randint
import time
import compose

# cc -fPIC -shared -O2 `pkg-config --libs gsl` -o compose_gsl.so compose_gsl.c
# cc -fPIC -shared -O2 -o compose_cpu.so compose_cpu.c

class triple(ctypes.Structure):
    _fields_ = [
    ('r', ctypes.c_ubyte),
    ('g', ctypes.c_ubyte),
    ('b', ctypes.c_ubyte)
    ]

    
class matrix(ctypes.Structure):
    _fields_ = [
    ('m', ctypes.c_int),
    ('n', ctypes.c_int),
    ('element', ctypes.POINTER(triple))
    ]

def print_matrix(m):
    print('[')
    for r in range(m.m):
        print('[', end = '')
        for c in range(m.n):
            idx = r * m.n + c
            print((m.element[idx].r, m.element[idx].g, m.element[idx].b), end = '' if (c + 1 == m.n) else '\n')
        print('],')
    print(']')

lib_path = '.'
lib_file = 'compose_cpu.so'
full_path = os.path.join(lib_path, lib_file)

cpu = ctypes.CDLL(full_path)

lib_path = '.'
lib_file = 'compose_gsl.so'
full_path = os.path.join(lib_path, lib_file)

gsl = ctypes.CDLL(full_path)


rows = 1920
cols = 1080
rc = rows * cols

print('- Инициализация:')
print('1. Python-генерация случайных данных')
t1 = time.time()

d1 = [ (randint(0,255), randint(0,255), randint(0,255)) for _ in range(rc) ]
d2 = [ (randint(0,255), randint(0,255), randint(0,255)) for _ in range(rc) ]

t2 = time.time()
print(f'Затрачено {t2 - t1} секунд')

print(f'2. Заполнение данными четырех C-подобных матриц, dim = [{rows}, {cols}]')
t1 = time.time()

m_1 = matrix()
m_1.m = rows
m_1.n = cols
m_1.element = (triple * rc)(*d1)

m_2 = matrix()
m_2.m = rows
m_2.n = cols
m_2.element = (triple * rc)(*d2)

m_out = matrix()
m_out.m = rows
m_out.n = cols
m_out.element = (triple * rc)()

m_gsl = matrix()
m_gsl.m = rows
m_gsl.n = cols
m_gsl.element = (triple * rc)()

t2 = time.time()
print(f'Затрачено {t2 - t1} секунд')

print('3. Формирование двух gsl-матриц')
t1 = time.time()

res = gsl.form_gsl_matricies(ctypes.byref(m_1), ctypes.byref(m_2))

t2 = time.time()
print(f'Затрачено {t2 - t1} секунд')

print('4. Формирование двух python-матриц в виде словарей')
t1 = time.time()

mp_1 = {}
mp_2 = {}
for i in range(rows):
    for j in range(cols):
        mp_1[i, j] = d1[i * cols + j]
        mp_2[i, j] = d2[i * cols + j]

t2 = time.time()
print(f'Затрачено {t2 - t1} секунд')
t_form_python = (t2 - t1) * 0.5


print(f'- Расчет:')
t_python, t_cpu, t_gsl = 0, 0, 0
iter_c = 20 # Количество итераций
for k in range(iter_c):
    print(f'Итерация {k} из {iter_c}')

    t1 = time.time()
    result = cpu.compose_cpu(ctypes.byref(m_1), ctypes.byref(m_2), ctypes.byref(m_out))

    t2 = time.time()
    t_cpu += (t2 - t1)
    
    t1 = time.time()
    # Второй параметр 1 для исключения копирования внутренней матрицы во внешнюю m_gsl
    result = gsl.compose_gsl(ctypes.byref(m_gsl), ctypes.c_int(1))

    t2 = time.time()
    t_gsl += (t2 - t1)

    t1 = time.time()
    mp_out = compose.compose(mp_1, mp_2)

    t2 = time.time()
    t_python += (t2 - t1 - t_form_python)

gsl.free_gsl_matricies()

print(f'1. cpu_compose')
print(f'  затрачено {t_cpu/iter_c} секунд')
print(f'2. gsl_compose')
print(f'  затрачено {t_gsl/iter_c} секунд')
print(f'3. python native compose')
print(f'  затрачено {t_python/iter_c} секунд (с коррекцией на время формирования выходной матрицы)')
speed_up = t_python / t_cpu
print(f'CPU speed up {speed_up}')
speed_up = t_python / t_gsl
print(f'GSL speed up {speed_up}')


if (rows < 5) and (cols < 5):
    print('CPU compose result:')
    print('m_1')
    print_matrix(m_1)
    print('m_2')
    print_matrix(m_2)
    print('m_1 + m_2')
    print_matrix(m_out)

# Задайте размеры rows, cols менее 5 и вы увидите вывод матриц для контроля правильности счета
if (rows < 5) and (cols < 5):
    print('GSL compose result:')
    res = gsl.form_gsl_matricies(ctypes.byref(m_1), ctypes.byref(m_2))
    # Второй параметр 0 для копирования внутренней матрицы во внешнюю m_gsl
    result = gsl.compose_gsl(ctypes.byref(m_gsl), ctypes.c_int(0))
    print('m_1')
    print_matrix(m_1)
    print('m_2')
    print_matrix(m_2)
    print('m_1 + m_2')
    print_matrix(m_gsl)
