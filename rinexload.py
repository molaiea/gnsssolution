import georinex as gr
import numpy as np
nav = gr.load('rabt3320.19n')
# print(nav.sel(sv='G08')['SVclockBias'])
#print(str(nav.sel(sv='G08').coords['time'][0].values).split('T')[1].split(':'))
# n = nav.sv.size
# for i in range(10,n+1):
#     print(nav.sel(sv='G'+str(i))['SVclockBias'])
R3lambda = np.array(((4, 0, 0), (2, 9, 0), (0,0,1)))
R1lambda = np.array(((1, 2, 0), (0, 9, 0), (0,0,1)))
r_k = 1
R = np.array((0,0,0))
print(R.shape)
print(R3lambda.shape)
print(R1lambda)
print(np.dot(R3lambda, R))