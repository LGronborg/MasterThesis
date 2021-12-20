import unittest
import numpy as np
import subprocess as sp
import glob, os, shutil
import sol


#Create identities.
vessel = sol.createIdentity("vessel")
company = sol.createIdentity("company")
service = sol.createIdentity("service")
worker = sol.createIdentity("worker")
hub = sol.createIdentity("hub")

#Create the initial trust between the vessel and the company.
sol.setRelationship("vessel",company,"action:{foo}")
sol.give_states("vessel","company")

#Checking initial trust.
tmp = (sol.handshake("vessel","company","action:{foo}"))
print(tmp)

#Create the trust between the company and the service.
sol.setRelationship("company",service,"action:{foo}")

#Share this new state to the centralized hub.
sol.give_states("company","hub")

#DDOS'ing the cantralized hub.
shutil.rmtree("storage-hub")

#Try getting data from the hub?

#Instead share the state directly.
sol.give_states("company", "service")

#Create the trust between the service and the worker.
sol.setRelationship("service",worker,"action:{foo}")

#Share trust inside company.
sol.give_states("service", "worker")

#Share trust to the vessel.
sol.give_states("worker", "vessel")

#Check trust.
tmp = sol.handshake("vessel","service","action:{foo}")
print(tmp)


#Clear storage.
shutil.rmtree("storage-vessel")
shutil.rmtree("storage-company")
shutil.rmtree("storage-service")
shutil.rmtree("storage-worker")
