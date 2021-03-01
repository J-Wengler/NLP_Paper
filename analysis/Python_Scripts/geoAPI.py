evaluateGEO()

def evaluateGEO():
    path_to_GEO_queries = "/Data/GEO_Queries/"
    path_to_queries = "/Data/Queries/"

    geo_results = []
    query_results = []

    query_list = ["q1_metastasis+brain_GEO.txt", "q2_sars_GEO.txt", "q3_h1n1+infection+mouse+lethal_GEO.txt"
                  "q4_acute_leukemia+mll+progression_GEO.txt", "q5_BRCA+Cancer_GEO.txt",
                  "q6_heart_development+age+failure_GEO.txt"]
    for path in query_list:
        with open(path_to_GEO_queries + path, 'r') as geo_file:
            for line in geo_file:
                if line.startswith("Series"):
                    split_sent = line.split()
                    geo_results.append(split_sent[2])

        with open(path_to_queries + f"{path[1]}/names.txt", 'r') as query_file:
            for line in query_file:
                query_results = line.split()

        num_relevant = 0
        for series in geo_results:
            if series in query_results:
                num_relevant = num_relevant + 1

        resultsDirPath = f"/Data/Results/GEO_Queries/geo_results.txt"
        with open (resultsDirPath, 'w+') as out_file:
            out_file.write(f"q{path[1]} returned {num_relevant} in {len(query_results)}")

