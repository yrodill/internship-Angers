import re

firstLine=True
with open("AT_protein_links.txt") as f:
    lines=f.readlines()

    with open("AT_PPI_normalized.csv","w") as output:
        for l in lines:
            col = l.split(" ")
            if (firstLine != True):
                reg1 = re.match(r"\d+.([\w\d]+).\d",col[0])
                reg2 = re.match(r"\d+.([\w\d]+).\d",col[1])           
                output.write(reg1.group(1)+","+reg2.group(1)+","+col[2])
            else:
                output.write(col[0]+","+col[1]+","+col[2])
                firstLine = False