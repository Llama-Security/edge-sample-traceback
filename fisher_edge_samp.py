#! /usr/bin/env python

import random
import sys

class packet_edge:
    def __init__(self,dev,di):
        self.start = dev
        self.end = dev
        self.distance = di

    def add_start(self, strt):
        self.start = strt
        self.distance = 0

    def add_end(self, ed):
        self.end = ed
        
def edge_sample_mark(p, ww, R1):
    """Marking procedure at router R :
    for each packet w
    let x be a random number from [0..1)
    if x < p then
    write R into w .start and 0 into w .distance
    else
    if w .distance = 0 then
    write R into w .end
    increment w .distance"""
    
    x = random.random()
    
    if x < p:
        ww.add_start(R1)
        #w.add_dist(0)
    else:
        if ww.distance == 0:
            ww.add_end(R1)
        ww.distance += 1
    
def edge_sample_recon(x, G1):

    #Algorithm for reconstructing path using edge sampling
    
    """Path reconstruction procedure at victim v :
    let G be a tree with root v
    let edges in G be tuples (start,end,distance)
    for each packet w from attacker
    if w .distance = 0 then
    insert edge ( w .start, v ,0) into G
    else
    insert edge ( w .start, w .end, w .distance) into G
    remove any edge ( x , y , d ) with d != distance from x to v in G
    extract path ( R i .. R j ) by enumerating acyclic paths in G"""

    if x.distance == 0:
        G1.append([x.start, 'v', 0])
    else:
        G1.append([x.start, x.end, x.distance])
    
    

devices = ['A1', 'A2','A3']                               #initializes devices list
attacker = devices[random.randint(0,len(devices)-1)] # Setting attacker
devices.remove(attacker)                             #removes attacker from device list

#Path for each device to victim
path_nodes = [('A1', 'R001', 'R006', 'R011', 'R015', 'R019', 'R022', 'R025', 'R027', 'R029', 'R030'),
              ('A2', 'R002', 'R007', 'R012', 'R016', 'R019', 'R023', 'R025', 'R027', 'R029', 'R030'),
              ('A2', 'R003', 'R008', 'R012', 'R016', 'R019', 'R023', 'R025', 'R027', 'R029', 'R030'),
              ('A3', 'R004', 'R009', 'R013', 'R017', 'R020', 'R023', 'R026', 'R028', 'R029', 'R030'),
              ('A3', 'R005', 'R010', 'R014', 'R018', 'R021', 'R024', 'R026', 'R028', 'R029', 'R030')]

dist = [('R001',9),('R002',9),('R003',9),('R004',9),('R005',9),('R006',8),('R007',8),('R008',8),('R009',8),('R010', 8),('R011', 7),('R012', 7),('R013', 7),('R014', 7),('R015', 6),('R016', 6),('R017', 6),('R018', 6),('R019', 5),('R020', 5),('R021', 5),('R022', 4),('R023', 4),('R024', 4),('R025', 3),('R026', 3),('R027', 2),('R028', 2),('R029', 1),('R030', 0)]
x_times_packet = 100      #Value for number of packets attacker sends per packet from normal user
total_packets = 0        #initializing packet counter.
p = 0.5                  #probablility for marking packet
G = []                   #Initializing G
d = 5
path = []

print("Non-Attackers are using devices: %s" %devices)
print("Attacker is a device: %s" % attacker)
print("_"*40)

for edge in path_nodes: #marking the packets
    print(edge)
    for i in range(0,10):
        if edge[0] == attacker:
            w = packet_edge(attacker, d)
            for i in range(0, x_times_packet):
                for R in edge[1:]:
                    edge_sample_mark(p, w, R)
                    total_packets += 1
                edge_sample_recon(w, G)
        else:
            w = packet_edge(edge[0], d)
            for R in edge[1:]:
                edge_sample_mark(p, w, R)
                total_packets += 1
            #edge_sample_recon(w, G)

G.sort()            #Sorting G
for val in G:
    for dd in dist:
        if val[0] == dd[0]:
            if val[2] != dd[1]:
                G.remove(val)
'''for val in G:
    if val[0] not in path:
        path.append(val[0])'''
print(G)
print("Packets Marked: %d" % total_packets)
