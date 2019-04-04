import json

sorted_exp={
    "development":[],
    "chemical":[],
    "abiotic":[],
    "biotic":[],
    "NA":[]
}

with open("catma5_metadata.json","r") as f:
    data = json.load(f)
    for exp in data:
        for stress in data[exp]["cond3"]:
            if(stress != ""):
                if(float(stress) == 1):
                    sorted_exp["development"].append(exp.replace("#","_"))
                elif(float(stress) == 2):
                    sorted_exp["chemical"].append(exp.replace("#","_"))
                elif(float(stress) >= 3 and float(stress) < 4):
                    sorted_exp["abiotic"].append(exp.replace("#","_"))
                elif(float(stress) >= 4):
                    sorted_exp["biotic"].append(exp.replace("#","_"))
                else:
                    sorted_exp["NA"].append(exp.replace("#","_"))


with open("sorted_exp_by_stress.json","w") as output:
    json.dump(sorted_exp,output)

# print(len(sorted_exp["development"]))