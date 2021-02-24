path_to_GEO = "/Data/GEO_Queries/"
path_to_queries = "/Data/Queries/"

with open(path_to_GEO + "q1_metastasis+brain_GEO.txt", 'r') as geo_file:
    for line in geo_file:
        print(line)
