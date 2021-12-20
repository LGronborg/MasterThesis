import unittest
import numpy as np
import subprocess as sp
import glob, os, shutil
import sol
import time

# number of vessels.
n = 1000


list = []
# Creating the first x vessel
for i in range(n):
    list = list + [sol.createIdentity("{}".format(i))]

# forming the relations.
for i in range(1,n):
    old_name = "{}".format(i-1)
    new_name = "{}".format(i)
    sol.setRelationship(old_name,list[i],"action:{foo}")
    #sol.give_states(old_name,new_name)

#print(0.)

#start_time = time.time()
#print("start")
# Sharing the states.
for i in range(n-1):
    name = "{}".format(i)
    start_time = time.time()
    sol.give_states(name,"{}".format(n-1))
    print("%s" % (time.time() - start_time))

# Time.
#setup = (time.time() - start_time)
#print("first {}: {} seconds".format(n-1, setup))

#sol.give_states("{}".format(n-2),"{}".format(n-1))
#print("last took: %s seconds" % (time.time() - start_time - setup))



#sol = (sol.handshake("0","{}".format(n-1),"action:{foo}"))
#print(sol)