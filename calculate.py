import argparse
import pandas as pd
import numpy as np

"""
Benoît Bothorel
Avril 2019
Calculette pour multiplication en utilisant la méthode numérique de 
la multiplication japonaise. (utilisation d'un Dataframe)

Usage : python calculate.py [NUMBER1] [NUMBER2] [OPTION(S)]
"""

parser = argparse.ArgumentParser(description='Process some integers.',
                                usage="python calculate.py [NUMBER1] [NUMBER2] [OPTION(S)]")

parser.add_argument('n1', metavar='d', type=str, help='nb1')
parser.add_argument('n2', metavar='d', type=str, help='nb2')
parser.add_argument('--v', action="store_true", help='verbose')

args = parser.parse_args()

#Transformation des nombres en listes pour les colonnes du Dataframe
a=list(args.n1)
b=list(args.n2)

df = pd.DataFrame(index=a,columns=b)

#Multiplication du chiffre des colonnes et des lignes
for i in range(len(df.index)):
    for j in range(len(df.columns)):
        df.values[i][j] = int(df.index.values[i]) * int(df.columns.values[j])

df=pd.DataFrame(df.values,index=a,columns=b)
if(args.v):
    print(df)

#Rassemblement des nombres par diagonale
numbers=[]
for i in range(len(df.index)+len(df.columns)-1):
    numbers.append([])

for i in range(len(df.columns)):
    for j in range(len(df.index)):
            numbers[i+j].append(df.values[j][i])
if(args.v):
    print(numbers)

#Addition des nombres de chaque groupe
calcs=[]    
for i in numbers[::-1]:
    number=0
    if(type(i) is list):
        for j in i:
            number+=j
        calcs.append(number)
    else:
        calcs.append(i)
if(args.v):
     print(calcs)

#Calcul final de la multiplication
result=0
rest=0
for i in range(0,len(calcs)):
    if(i == len(calcs)-1):
        result += (calcs[i]+rest)*10**i
    else:
        unite = (calcs[i]+rest)%10
        rest = (calcs[i]+rest)//10
        result += unite*10**i


print("{} * {} = {} !".format(args.n1,args.n2,result))
print("Vérification...")

if(result == int(args.n1) * int(args.n2)):
    print('True !')
else:
    print("False ! C'était {} !".format(int(args.n1)*int(args.n2)))

