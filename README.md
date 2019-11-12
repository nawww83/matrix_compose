# matrix_compose
Matrix composition

1. Какие пакеты надо установить на Ubuntu 18

sudo apt update

sudo apt install build-essential

sudo apt install gsl-dev

sudo apt install pkg-config

2. Инструкция по сборке

Перейти в папку с файлами данного проекта, открыть терминал и выполнить

make

В итоге в папке должно появиться две библиотеки *.so.

3. Запуск бенчмарка

python3 compose_bench.py
