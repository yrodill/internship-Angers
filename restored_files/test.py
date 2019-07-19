def fill(i):
    for j in range(100):
        i.append(j)
    return i

i = []
fill(i)
print(i)
