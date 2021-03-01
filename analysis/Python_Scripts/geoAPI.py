path_to_GEO = "/Data/GEO_Queries/"
path_to_queries = "/Data/Queries/"

geo_results = []
query_results = []

with open(path_to_GEO + "q4_acute_leukemia+mll+progression_GEO.txt", 'r') as geo_file:
    for line in geo_file:
        if line.startswith("Series"):
            split_sent = line.split()
            geo_results.append(split_sent[2])

with open(path_to_queries + "q4/names.txt", 'r') as query_file:
    for line in query_file:
        query_results = line.split()

num_relevant = 0

for series in geo_results:
    if series in query_results:
        num_relevant = num_relevant + 1


print(f"Number relevant : {num_relevant}")
print(f"Query_results : {len(query_results)}")
print(f"Query 1 : {num_relevant / len(query_results)}")
