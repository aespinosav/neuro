using Clustering

directory = ARGS[1]
files = readdir(directory)

function assigned_class(i, km)
    ns = length(km.medoids)

    cluster = km.assignments[i]
    cluster_stim = km.medoids[cluster]%ns + 1
end

function real_class(i, km)
    ns = length(km.medoids)
    stim = i%ns + 1
end

function conf_matrix(km)

    ns = length(km.medoids)
    
    matrix = zeros(Int, ns, ns)
    
        for i in range(1,length(km.assignments))
            rc = real_class(i, km)
            ac = assigned_class(i, km)
            
            matrix[rc, ac] += 1
        end
        
    return matrix
end

#
#function counts_good_index(km)
#    
#    ns = length(km.medoids)
#    
#    counts_good = zeros(ns)
    
#    for i in range(1, ns)
#        real_c = real_class(km.medoids[i], km)
#        counts = km.counts[i]
#        
#        counts_good[real_c] = counts
#    end
#    
#    return counts_good
#end

function counts_good_index(confusion_matrix, ns)
    
    #ns = length(conf_matrix[1,:])
    counts_good = Int[]
    
    for i in range(1, ns)
        push!(counts_good, sum(confusion_matrix[:,i]))
    end
    
    return counts_good
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
    println("Counts:\n$(counts_good_index(confusion_matrix, ns)) \n")
    println("Confusion Matrix:\n", confusion_matrix, "\n" )
    
    for k in km.medoids
        println(real_class(k, km))
    end
    

    
end