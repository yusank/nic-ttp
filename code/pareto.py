import numpy as np
import pandas as pd

# input arguments 1-->df with first column as cost and second column as time
# 2--> fp_xl file path for excel file
# 3--> fp_pg file path for png file 
# returns 1--> indexes of the non-dominated solutions with maximum cost and minimum time
# returns 2--> corresponding non dominated solution
# creates excel file and saves at file path fp_xl
# creates plot of the non-dominated solutions and saves png file at path fp_pg


def pareto_front(df,fp_xl,fp_pg):
    points1=df.values
    df.iloc[:,0]=-1*df.iloc[:,0]
    points=df.values
    mask2=np.ones(points.shape[0])
    pp=[]
    mask2=np.ones(points.shape[0])
    for i in range(len(points)-1):
        c=np.all((np.sum((points[i]<points[:i]),axis=1)-np.prod((points[i]<points[:i]),axis=1))==1)
        d=np.all((np.sum((points[i]<points[i+1:]),axis=1)-np.prod((points[i]<points[i+1:]),axis=1))==1)
        if c and d :
            mask2[i]=False
    mask2 = ~mask2.astype(bool)
    pareto_index=pd.Series(points1[:,1])[mask2].index
    pd.Series(pareto_index).to_excel(fp_xl) 
    plt.figure()
    plt.plot(points1[:,1],points1[:,0],'o',ms=2)
    pareto_sol=points1[mask2]
    plt.plot(points1[mask2][:,1],points1[mask2][:,0],'D',ms=5,color='red',label='Pareto front')
    plt.xlabel("time")
    plt.ylabel("profit")
    plt.legend()
    plt.tight_layout()
    plt.savefig(fp_pg,dpi=300)
    return pareto_index,pareto_sol