from random import randint
print("afd1.txt")
r = ""
for i in range(5000000):
    if randint(0,1) == 0:
        r += "b"
    else:
        r += "a"
print(r)
