import numpy as np
import igraph
import itertools
from statistics import acc,th

def compute_topological_sort(weights):
    OUT=1
    g1 = igraph.Graph.Weighted_Adjacency(weights.tolist(), attr="weight")
    d1=g1.feedback_arc_set(weights=weights.flatten())
    g1.delete_edges(d1)
    sorted_types=g1.topological_sorting(mode=OUT)    # Best rank is first
    return sorted_types#np.asarray(sorted_types).reshape(-1,1)

def get_short_rankings(distribution):
    n,k=distribution.shape
    inverse_rankings=-np.ones((n,k),dtype="int")
    argsort_rankings=np.copy(inverse_rankings)
    short_rankings=np.copy(argsort_rankings)
    
    for i in range(n):
        inverse_rankings[i]=np.asarray([np.where(distribution==i+1)[0]],dtype="int")
    
    for i in range(n):
        temp_short=distribution[inverse_rankings[i]]
        temp_sorted=np.sort(temp_short,axis=1)
        index_sorted=np.asarray([np.where(temp_sorted[j]==i+1) for j in range(k)]).reshape(k)
        short_rankings[i]=np.sort(index_sorted)
    
    return short_rankings

def get_rankings_from_types(sorted_types, short_rankings, sigma_list):
    rankings=np.zeros(len(short_rankings),dtype='int')
    rank=0
    for i in range(len(sorted_types)):
        for j in range(len(short_rankings)):
            if np.array_equal(sigma_list[sorted_types[i]], short_rankings[j]):
                rankings[j]=rank
                rank+=1
    return rankings+1
        

if __name__ == '__main__':

    distribution = np.genfromtxt('data_n_1000_k_6.csv', delimiter=',', dtype='int')
    short_rankings=get_short_rankings(distribution)
        
    n,k=distribution.shape    
    k_list = list(range(k))
    sigma_list = np.asarray(list(itertools.combinations_with_replacement(k_list,k)),dtype='int')
    
    weights=np.loadtxt('weights_6_0_10_0_10.txt')
    assert len(sigma_list)==weights.shape[0]
    sorted_types=compute_topological_sort(weights)
    
    rankings=get_rankings_from_types(sorted_types, short_rankings, sigma_list)
    print (acc(rankings,0.02))
    print (acc(rankings,0.05))
    print (th(rankings,0.1))
    print (th(rankings,0.5))