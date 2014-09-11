using Clustering

directory = ARGS[1]
files = readdir(directory)


for f in files

    list_of_strings = split(f, ['.', '_'])
    
    index_ns = findin( list_of_strings, ["ns"])[1] + 1
    index_nt = findin( list_of_strings, ["nt"])[1] + 1

    ns = int(list_of_strings[index_ns])
    nt = int(list_of_strings[index_nt])

    nr = ns*nt
    
    dist_matrix = readdlm(directory*f)
    
    target_cluster_number = ns
    
    seeds = [i for i=1:nt:nr]
    
    km = kmedoids(dist_matrix, target_cluster_number, init=seeds)
    
    println("k = ")
    print(ns)
    println(length(km.counts))
    print(":")
    print(km.counts)
    print("\n")
    
end