#Print a trans flag
from rp import *
colors    =pip_import('colors','ansicolors')
color     =lambda n:(colors.color(' '*100,bg=n)+'\n')*7
blue      =color(75) 
white     =color(15)
pink      =color(211)
trans_flag=blue+pink+white+pink+blue
print(trans_flag)