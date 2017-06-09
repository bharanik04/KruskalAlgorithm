# -*- coding: utf-8 -*-
"""
Created on Thu Feb  10 18:16:37 2017

@author: Bharani Kodirangaiah

Python program for kruskal's algorithm to find Minimum Spanning tree
Find the utilization on each link
Calculating average hop count between any two nodes, finding delay using utilization and 
average hop on T1 link
"from Part1 import Weight" is a class which finds distance between each node using pythogoreans theorem
"""
from DistanceBetweenNodes import Weight        
from functools import reduce

class Graph:
    
    def __init__(self,filename1):
        self.graph = []
        self.result = []
        self.groups = []
        self.links = []
        self.parent = {}
        self.paths = {}
        self.a_to_b = []
        self.Avghop = 0

    # calculated distance between src, dst using Pythagorean formula(wt) is sent to add in self.graph
    def add_link(self, src, dst, wt):
        self.graph.append([src, dst, wt])
    
    
    #To add links using kruskal algorithm
    """
    self.graph list which contains set of [(node1,node2,weight)]. Picks the smallest edge
    from self.graph, adds link to result and nodes to self.groups. next smallest edge is taken
    check whether the connection is already present, from previous result. If there is 
    no connection it adds.    
    self.groups -contains nodes which are connected
    self.result - contains links of nodes and weight on there link
    """
    def MST_Algorithm(self):
        #Sort self.graph in ascending order
        self.graph = sorted(self.graph, key=lambda l: l[2])
        #taking each link to check for adding connections
        for link in self.graph:
            x,y,z = link    # dividing to get node1, node2 and weight
            link_group = None
            i = 0
            for group in self.groups:   
                i += 1
                if (x in group) and (y in group):   # checking if the connections is already present in added list
                    link_group = i
                    break
                if x in group:
                    if link_group != None:
                        #print ('a')
                        self.join_groups(link_group, i)
                        break
                    else:
                        group.append(y)
                        self.result.append(link)
                        link_group = i
                        continue
                if y in group:
                    if link_group != None:
                        self.join_groups(link_group, i)
                        break
                    else:
                        group.append(x)
                        self.result.append(link)
                        link_group = i
                        continue

            if link_group == None:          #executed first time to add the least weighted connection
                self.groups.append([x,y])   # adding  connection to list
                self.result.append(link)

        w=0    
        print("\n----------------------------------------\nPart 1:")
        for u,v,weight in self.result:
            print ("%d -- %d == %.2f km" % (u,v,float(weight)))
            w+=weight       #adding weight for each connections
        print("\nMST weight = {} km\n\n".format(w))
        #print("result {}".format(self.result))
        
    # which joins two groups into              
    def join_groups(self, grp1, grp2):
        grp1 -= 1
        grp2 -= 1
        grp = self.groups[grp1] + self.groups[grp2]
        self.groups.pop(grp2)
        self.groups.pop(grp1)
        self.groups.append(grp)
    
    """
    Called in find_parent_nodes function, just to initialize parent of a node to NONE
    Self.links is a list of nodes which are connected
    """
    def determine_nodes(self):
        for link in self.result:
            src, dst, wt = link
            if not src in self.links:
                self.links.append(src)
            if not dst in self.links:
                self.links.append(dst)

    """
    parent is a dictionary, we assign the root as 1st element in the self.result i.e first
    node in with the less weight. while loops till value in parent dictionary is not none
    calls find_parent function to create a parent dictionary
    """
    def find_parent_nodes(self):
        self.determine_nodes()
        parent = {}
        for node in self.links:
            parent[node] = None
        #Identify Root as 1st least weight connection
        self.root = self.result[0][0]
        print ('root node is : {}'.format(self.root))
        i = 0
        while None in parent.values():    
            for link in self.result:
                src, dst, wt = link
                result = self.find_parent(parent, src, dst, self.root)
                if result:
                    i += 1
                    parent = result
        #print('parent - {}'.format(self.parent))
        return parent
    
    """
    function is called in find_parent_nodes, it create dictionary i.e
    parent[node1]= node2, node2 is the parent of node1
    """
    # To find parent for each node and add to dictionary parent[vlaue]=root
    def find_parent(self, parent, src, dst, root):
        #print ('Entered find_parent\nsrc-{}, dst-{}, root-{}'.format(src, dst, root))
        if src == root or dst == root:
            parent[src] = root
            parent[dst] = root
        elif parent[src] == None and parent[dst] == None:
            return False
        elif parent[src] == None:
            parent[src] = dst
        elif parent[dst] == None:
            #print('d')
            parent[dst] = src
        #print("parent : {}".format(parent))
        return parent
    
    """
    function takes one node and finds the route to root
    route contains the list of nodes which routes particular node to root    
    """
    def route_to_root(self, parent, node, root, route = []):
        #print("Parent: {}".format(self.parent))
        #print ('entered route_to_root - node-{}, route={}'.format(node, route))
        if parent[node] == root:
            route.append(root)
            return route
        else:
            if not route:
                route = [node,]
            route.append(parent[node])
            return self.route_to_root(parent, parent[node], self.root, route)
    
    """
    Function used to find connection between two nodes (a,b), route to root returns list
    of nodes connected the node to root. to fint(1,5)
    Example: a_to_root =[1,2,3], b_to_root= [5,4,3], check for the common element in b_to_root
    takes the index, a_i=2 and b_i=2 ; self.a_to_b = [1,2,3] ;b_to_root = [5,4]; reverse 
    b_to_root = [4,5] and join this self.a_to_b = [1,2,3,4,5]
    """
    def node_to_node(self,parent, a, b):
        a_to_root = self.route_to_root(parent, a, self.root, [a,])
        b_to_root = self.route_to_root(parent, b, self.root, [b,])
        #Identify nearest common node
        for node in a_to_root:
            if node in b_to_root:
                a_i = a_to_root.index(node)
                b_i = b_to_root.index(node)
                self.a_to_b = a_to_root[:a_i + 1]
                b_to_root = b_to_root[:b_i]
                b_to_root.reverse()
                self.a_to_b += b_to_root
                break
        return self.a_to_b
    
    """
    Function to count average hop count:
        path- list of list of nodes between node A and B like, [[1,2,4,3],[1,4],[2,8,9]]
        table - traffic table in list
    takes the datarate from traffic table and counts the hop from path and subsituted in
    formula, average hop count = (sum(traffic*hopcount))/sum(traffic)
    """ 
    def hop_count(self,path,table):
        sum_trhop=0
        sum_traf = 0 ; 
        path_count=[]
        i=0;
        for links in path:
            path_count.append(len(links)-2)
        print("path_count {}\nlinks {}".format(path_count,path))
        for tab in table:
            print("{} -- {} {} kbps {} hops".format(tab[0],tab[1],tab[2],path_count[i]))
            sum_trhop+=path_count[i]*int(tab[2])
            sum_traf+=int(tab[2])       #sum of traffics (datarate given in text file)
            i+=1
        self.Avghop= sum_trhop/sum_traf
        print("Average hops = (sum(traffic*hopcount))/sum(traffic)\n\t   = {}/{}".format(sum_trhop,sum_traf))
        print("\nAverage hop = {:.2f} hops\n".format(float(self.Avghop)))
    
    """
    Function to create a dictionary of links and there traffic from traffic_table
    x - link and datarate(sent from main)
    d - empty dictionary at first and is addded in this function
    v=0 ; list of d[(node1,node2)]=datarate (node1 and node2 are from traffic table)--> data_flow (main)
    v=1 ; list of d[(node1,node2)] =0 (node1 and node2 are from MST links)--> traffic_flow (main)
    """
    # creating dictionary for each link, dic[link]= datarate
    def traffictable_dictionary(self,x, d, v = ''):
        y = []
        #print("x {}".format(x))
        for i in x:
            y.append(int(i))
        if not v:
            d[(y[0], y[1])] = y[2] # d[(node1, node2)]= datarate from traffic table
        else:
            d[(y[0], y[1])] = 0 #initilizing each link to zero from self.result(MST links)
            return y
    """
    function to find utilization on each link:
    takes a link(node1 amd node2) as argument, initially traffic_flow for all links is 0
    if statement find the link (src,dst) in traffic_flow dictionary and adds datarate
    """   
    def find_utilization(self,src, dst):
        #print ('src - {}, dst - {}'.format(src, dst))
        if (src, dst) in traffic_flow:
            traffic_flow[(src, dst)] += dataflow
        elif (dst, src) in traffic_flow:
            traffic_flow[(dst, src)] += dataflow
        else:
            print ('not found')
        return dst

    def average_delay(self,u):
        print("TBar =  0.0054   ; Average Hop = {:.2f} ; Max Utilization = {:.2f}%".format(self.Avghop, u))
        return ((0.0054*self.Avghop)/(1-(u/100)))



        
path =[]
data_flow = {}
traffic_flow = {}

filename = "D:\\Brown_Lab2\\node location.txt"
filename1 = "D:\\Brown_Lab2\\traffic table.txt"
s1= Weight(filename,filename1)               
my_list, table =s1.Find_distance()
print ("list[node1,node2,distance]:  {}\n\n Traffic_table: {}".format(my_list, table))
g = Graph(filename)
for i in my_list:   # final list of node and its distance calculated in import Part1
    g.add_link(i[0],i[1],float(i[2]))
    
g.MST_Algorithm()
print("\n----------------------------------------\nPart 2:")
parent = g.find_parent_nodes()
for link in table:
    path.append(g.node_to_node(parent,int(link[0]), int(link[1])))
print("For the list in traffic table these are the connecting nodes\n{}\n".format(path))
# executing lambda fnction for each content in table
# function and list in map, each elememnt in table list is passed as 'x'
table1 = list(map(lambda x: g.traffictable_dictionary(x, data_flow), table)) 
# g.result orginal links
traffic = list(map(lambda x: g.traffictable_dictionary(x, traffic_flow, 1), g.result)) 


"""
path : it has a list of nodes between A and B, data_flow contains datarate of (A,B)
reduce function takes function and list as parameter, feeds in 2 consecutive elements in 
list p to the function i.e g.find_utilization(p[0],p[1]), scope is with in for loop. So, 
dataflow can be used in function
"""
for p in path:
    if (p[0],p[-1]) in data_flow:
        dataflow = data_flow[(p[0], p[-1])]
    else:
        dataflow = data_flow[(p[-1],p[0])]
    reduce(g.find_utilization, p)    
#print ("traffic_flow {}".format(traffic_flow))              

avg_util=0   
util = 0
u=[]
print("\n(Location1,Location2) Load   Utilization")
for key in traffic_flow:
    u.append((traffic_flow[key]/1544)*100)
    util+=(traffic_flow[key]/1544)*100
    print("\t   {}  {} Kbps ---{:.2f} %".format(key,traffic_flow[key],float(traffic_flow[key]/1544)*100))



print("Maximum utilization = {:.2f}%".format(max(u)))
avg_util=util/len(traffic_flow)

print("Average utilization = {:.2f}%".format(avg_util))  

print("\n----------------------------------------\nPart 3:")
g.hop_count(path,table)
print("\n----------------------------------------\nPart 4:")
print("average delay {:.4f} sec".format(g.average_delay(max(u))))