#Print a trans flag
from rp import *

#Use this website to turn colors into xterm numbers: https://jonasjacek.github.io/colors/
colors    =pip_import('colors','ansicolors')#Use this library to turn numbers into colors...
color     =lambda n,h=7:(colors.color(' '*100,bg=n)+'\n')*h

light_blue      =color(75) 
white     =color(15)
light_pink=color(211)
trans_flag=light_blue+light_pink+white+light_pink+light_blue

hot_pink  =color(162,14)
dull_purple    =color(127)
dark_blue =color(19,14)
bi_flag=hot_pink+dull_purple+dark_blue

red  =color(9)
orange  =color(208)
yellow  =color(11)
green  =color(40)
blue  =color(33)
purple=color(129)
pride_flag=red+orange+yellow+green+blue+purple

print(random_choice(trans_flag,bi_flag,pride_flag))

assert False,'Not gay enough...try importing me again.'#Throw an error so the import fails, letting us import it again and print another flag...