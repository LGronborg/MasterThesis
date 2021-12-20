import unittest
import numpy as np
import subprocess as sp
import glob, os, shutil
import sol
import time

# number of vessels.
n = 1000


list = []
# Creating n vessel
for i in range(n):
    list = list + [sol.createIdentity("{}".format(i))]

# forming the relations.
for i in range(1,n):
    old_name = "{}".format(i-1)
    new_name = "{}".format(i)
    sol.setRelationship(old_name,list[i],"action:{foo}")
    #sol.give_states(old_name,new_name)

#print(0.)

# Sharing the states.
for i in range(n-1):
    name = "{}".format(i)
    sol.give_states(name,"{}".format(n-1))
    start_time = time.time()
    (sol.handshake("0",name,"action:{foo}"))
    print("%s" % (time.time() - start_time))
