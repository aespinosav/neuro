using Clustering

directory = ARGS[1]
files = readdir(directory)

function assigned_class(i, ns, km)
    cluster = km.assignments[i]
    cluster_stim = km.medoids[cluster]%ns + 1
end

function real_class(i, ns)
    stim = i%ns + 1
end

function conf_matrix(km)

    ns = length(km.medoids)
    
    matrix = zeros(Int, ns, ns)
    
        for i in range(1,length(km.assignments))
            rc = real_class(i, ns)
            ac = assigned_class(i, ns, km)
            
            matrix[rc, ac] += 1
        end
        
    return matrix
end

for f in files

    list_of_strings = split(f, ['.', '_'])
    
    index_ns = findin( list_of_strings, ["ns"])[1] + 1
    index_nt = findin( list_of_strings, ["nt"])[1] + 1

    ns = int(list_of_strings[index_ns])
    nt = int(list_of_strings[index_nt])

    nr = ns*nt
    
    dist_matrix = readdlm(directory*f)
    
    target_cluster_number = ns
    
    seeds = Int[i for i=1:ns]
    
    km = kmedoids(dist_matrix, target_cluster_number)
    
    confusion_matrix = conf_matrix(km)
    
    
    
    str1 = "ns = $ns; nt = $nt; nr = $nr\nClusters match: $(length(km.counts)==ns)"
    println(str1)
    println(km.counts, "\n")
    println("Confusion Matrix:\n", confusion_matrix, "\n" )
    #println(km.assignments)
    

    
end