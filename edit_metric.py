import numpy as np

def edit_length_metric(u, v, q = 1):
  
    m = len(u)
    n = len(v)
  
    G = np.zeros((m +1)*(n+1)).reshape(m + 1,n + 1)
  
    G[:,0] = range(m+1)
    G[0,:] = range(n+1)
  
    for i in range(1, m+1):
        for j in range(1,n+1):
            a = G[i-1, j-1] + q*abs(u[i-1] - v[i-1])
            b = G[i-1,j] + 1
            c = G[i, j-1] + 1
      
            G[i,j] = min([a,b,c])
  
    dist = G[-1, -1]
  
    return G
  
  
  