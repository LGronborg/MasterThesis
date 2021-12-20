import unittest
import numpy as np
import subprocess as sp
import glob, os, shutil
import sol
import time

# number of vessels.
n = 1000


list = []
# Creating n vessels
for i in range(n):
    list = list + [sol.createIdentity("{}".format(i))]
#print("0.")

names = ["{}".format(x) for x in range(n)]


# forming the relations.
for i in range(1,n):
    for j in range(i):
        sol.setRelationship(names[j],list[i],"action:{foo}")
    name = "{}".format(i)
    start_time = time.time()
    sol.certCreate(name)
    print("%s" % (time.time() - start_time))