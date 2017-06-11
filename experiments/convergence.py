import csv
import numpy as np
import matplotlib.pyplot as plt

def extract_distance(filename):
    datafile = csv.reader(open(filename, newline=''), delimiter=',')
    next(datafile,None) # Ignore the header line
    algo_list=['random_circle_removal','page_rank','em','borda_ordering']
    array_distance=np.zeros((0,4))
    dist=np.zeros((1,4))
    for row in datafile:
        algo_index=algo_list.index(row[3])
        dist[0,algo_index]=float(row[5])
        if algo_index==3:
            array_distance=np.vstack((array_distance,dist))
    
    return array_distance

def create_plot(distances_all):
    num_algos=distances_all.shape[1]
    ylist=[]
    for j in range(num_algos):
        distances=distances_all[:,j].flatten()
        y=np.zeros((0,1))
        x=np.zeros((0,1))
        
        m=[1,2,5,10,25,50,100]
        for i in m:
            dist=distances.reshape(i,-1)
            c=dist.mean(axis=0).reshape(-1,1)
            
            x=np.vstack((x,np.repeat(i,c.shape[0]).reshape(-1,1)))
            y=np.vstack((y,c))
        ylist.append(y)
    
    ax = plt.gca()
    ax.scatter(x,ylist[0],color='c',alpha=0.5, label='Random Priority')
    ax.scatter(x*0.98,ylist[1],color='r',alpha=0.5, label='Random Walk')
    ax.scatter(x*1.02,ylist[2],color='b',alpha=0.5, label='EM')
    ax.scatter(x,ylist[3],color='g',alpha=0.5, label='Borda Score')
    ax.set_xscale('log')
    ld=plt.legend(loc='upper left',prop={'size':16})
    for handle in ld.legendHandles:
        handle.set_sizes([150.0])
    ax.set_xticks(m)    
    ax.set_xticklabels(m)
        
if __name__ == '__main__':
    distances=extract_distance('../out/results_n_1000_k_[5].csv')
    distances=distances[:1000,:]
    create_plot(distances)
    