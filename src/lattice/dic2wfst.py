# <eps> 0

import sys

if len(sys.argv) < 2:
    print("!!Usage: python3 %s [dic_int] (optionally) epsid"%sys.argv[0])
    sys.exit(1)

eps = 0
if len(sys.argv) == 3 :
    eps = int(sys.argv[2])

state = 0
#end_state = -1
dic_int = open(sys.argv[1])

for line in dic_int:
    part = line.strip().split("\t")
    if len(part) != 2:
        print("Format error!!")
        sys.exit(2)

    word = int(part[0])
    phones = part[1].split(" ")

    for i, phone in enumerate(phones):
        state = state + 1
        if i == 0:
            print("0 %d %s 0"%(state, phone))
        else :
            print("%d %d %s 0"%(state - 1,state, phone))

    print("%d 0 0 %s"%(state, word))
    
#    if end_state == -1:
#        end_state = state
#        print("%d 0 0 0"%end_state)
#        state += 1
#    else:
#        print("%d 0 0 0"%(state, end_state))

