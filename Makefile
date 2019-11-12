all: compose_cpu.so compose_gsl.so

compose_cpu.so: compose_cpu.c
	gcc compose_cpu.c -o compose_cpu.so -fPIC -shared -O2
compose_gsl.so: compose_gsl.c
	gcc compose_gsl.c -o compose_gsl.so -fPIC -shared `pkg-config --libs gsl` -O2

