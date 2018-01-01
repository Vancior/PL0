from sys import argv
from Pcode import PcodeMachine

script, file = argv
file = open(file, 'r')
codes = list()
count = 0
while True:
    line = file.readline().strip('\n')
    if line:
        codes.append(line)
        count += 1
    else:
        break

machine = PcodeMachine(codes, count)
machine.exe()
