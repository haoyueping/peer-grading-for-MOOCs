# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 14:44:23 2017

@author: paras
"""

import csv
import numpy as np

spamReader = csv.reader(open('../out/results_n_1000_k_[5].csv', newline=''), delimiter=',')

next(spamReader,None)
#row1 = next(spamReader)
#print (row1[0])
n=1000#int(float(row1[0]))
#==============================================================================
# rcr_rankings=np.zeros((0,n)).astype(np.int)
# pg_rankings=np.zeros((0,n)).astype(np.int)
# em_rankings=np.zeros((0,n)).astype(np.int)
# bo_rankings=np.zeros((0,n)).astype(np.int)
# array_rankings=[rcr_rankings,pg_rankings,em_rankings,bo_rankings]
#==============================================================================
algo_list=['random_circle_removal','page_rank','em','borda_ordering']
array_distance=np.zeros((0,4))
dist=np.zeros((1,4))
#==============================================================================
# stop=10000
#==============================================================================
i=0
for row in spamReader:
#==============================================================================
#     stop-=1
#     if stop<0:
#         break
#==============================================================================
    algo_index=algo_list.index(row[3])
    dist[0,algo_index]=float(row[5])
    if algo_index==3:
        array_distance=np.vstack((array_distance,dist))
#    array_distance[i%4]
#    i+=1

#==============================================================================
#     row[6]=row[6].replace('[','')
#     row[6]=row[6].replace(']','')
#     row[6]=row[6].replace('\n',' ')
#     row[6]=row[6].replace(',',' ')
#     ranking = np.fromstring(row[6], dtype=int, sep=' ')
#     array_rankings[algo]=np.vstack((array_rankings[algo],ranking))
#==============================================================================

#==============================================================================
# for arr in array_rankings:
#     print (arr.shape)
#==============================================================================

print (array_distance.shape)
