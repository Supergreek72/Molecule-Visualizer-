CC = clang
CFLAGS = -Wall -std=c99 -pedantic
LDFlAGS =-L.

Python_header = /usr/include/python3.9
Python_lib = usr/lib/python3.7/config-3.7m-x86_64-linux-gnu
p_version = python3.9

all: libmol.so mol.o _molecule.so

libmol.so: mol.o
	$(CC) -shared -o libmol.so mol.o

mol.o: mol.c mol.h
	$(CC) $(CFlAGS) -c -fpic mol.c -o mol.o

_molecule.so: molecule_wrap.o
	$(CC) molecule_wrap.o -dynamiclib -shared -L. -lm -lmol -L $(Python_lib) -l$(p_version) -o _molecule.so

molecule_wrap.o: molecule_wrap.c
	$(CC) $(CFLAGS) -I $(Python_header) -fpic -c molecule_wrap.c -o molecule_wrap.o

molecule_wrap: molecule.i
	swig -python molecule.i

clean:
	rm *.o *.so

