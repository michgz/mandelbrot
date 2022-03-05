#!/usr/bin/env python3

"""
Builds the application provided by josch online at:

  https://github.com/josch/mandelbrot

without needing to install GMP and MPFR (they are built locally
and linked in).

GMP and MPFR must both have been downloaded and configured (i.e.
"./configure" has been run for both. GCC and M4 are both needed
to be installed.

"""




import os
import pathlib
import shutil



MPFR_DIR = pathlib.Path("mpfr-4.1.0")
GMP_DIR = pathlib.Path("gmp-6.2.1")



# Make MPFR - must be already configured, and have "m4" installed
old_cwd = os.get_cwd()
os.chdir(str(MPFR_DIR))
os.system("make all")


# Make GMP - must be already configured
os.chdir(str(GMP_DIR))
os.system("make all")
os.chdir(old_cwd)


# Copy locally
shutil.copy(str(MPFR_DIR.joinpath("src", ".libs", "libmpfr.so")), ".")
shutil.copy(str(GMP_DIR.joinpath(".libs", "libgmp.so")), ".")


# Make josch's program. 
os.system("gcc -O3 -Wall -I /usr/local/include -L /usr/local/lib mandel_mpfr.c libgmp.so libmpfr.so -lm -o mandel_mpfr")


# Done!

