import unittest
import numpy as np
import subprocess as sp
import glob, os, shutil
import sol
import time

# number of vessels.
n = 1000


#list = []
first = sol.createIdentity("0")
# Creating n vessels
for i in range(1,n):
    sol.createIdentity("{}".format(i))


#print("0.")
names = ["{}".format(x) for x in range(n)]
# forming the relations.
for i in range(1,n):
    start_time = time.time()
    sol.setRelationship(first,names[i],"action:{foo}")
    print("%s" % (time.time() - start_time))