# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 15:06:00 2017

@author: Bharani Kodirangaiah


Program takes text file as input and find the distance between nodes using pythogoreans theorem
Input file contains node , x-axis, y-axis
"""
from itertools import combinations

class Weight:
    

    def __init__(self, filename,filename1):
        self.filename= filename
        self.filename1= filename1
    
    def distance_cal(self,coor1,coor2):
        node1,x1,y1=coor1
        node2,x2,y2 =coor2
        node1= int(node1)
        node2= int(node2)
        result= ((int(x2)-int(x1))**2 + (int(y2)-int(y1))**2)**0.5
        result = '{:.3f}'.format(float(result))
        return [node1 , node2, result]
        
    def Find_distance(self):
        coordinate1=[]
        coordinate2=[]
        traffic_lable = []
        node_location = []
        my_list=[]
        nodes=[]
        #result=[]
        
        with open(self.filename) as f:
            lines= f.read().count("\n")+1
            f.seek(0,0)
            mylist= f.read().splitlines()
        
        for i in range(lines):
            node_location.append(mylist[i].split())
        
        for i in node_location:
            nodes.append(i[0])

        comb_list= [list(t) for t in list(combinations(nodes,2))]
       
        with open(self.filename1) as f:
            lines1= f.read().count("\n")+1
            f.seek(0,0)
            mylist1= f.read().splitlines()
        
        
        for i in range(lines1):
            traffic_lable.append(mylist1[i].split())
       
        
        for j in comb_list:
            #print("j[0] = {}, j[1]= {}".format(j[0],j[1]))            
            for i in node_location:
                #print("i = {}".format(i))
                if j[0] == i[0]:
                    coordinate1.append(i)
                    #print("cordinate1 : {}".format(coordinate1))
                if j[1] == i[0]:
                    coordinate2.append(i)
                    #print("cordinate2 : {}".format(coordinate2))
                    #print(coordinate2)
         
        for i in range(len(coordinate1)):
            #print("coon1 {}  : coon2 {}   ".format(coordinate1[i],coordinate2[i]))
            my_list.append(list(self.distance_cal(coordinate1[i],coordinate2[i])))
        #print("Final list {} ".format(my_list))
        return my_list, traffic_lable


filename = "D:\\Brown_Lab2\\node location.txt"
filename1 = "D:\\Brown_Lab2\\traffic table.txt"
g= Weight(filename,filename1)
a,b=g.Find_distance()
