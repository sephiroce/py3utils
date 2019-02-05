import sys

#a="50	52	10029	10029	3.36976433"
#b="50	8.03051281"
#s=a

for line in sys.stdin:
    elems=line.strip().split("\t")
    if len(elems) == 5:
        print("%s %s %s 0.0,%s,"%(elems[0], elems[1], elems[2], elems[4]))
    elif len(elems) == 2:
        print("%s 0.0,%s,"%(elems[0],elems[1]))
    else:
        print("Format!!")

