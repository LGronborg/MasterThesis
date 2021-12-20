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
mal_perp = sol.createIdentity("mal_perp")

#Create the initial trust between the vessel and the company.
sol.setRelationship("vessel",company,"action:{*}")
sol.give_states("vessel","company")

#Checking initial trust.
tmp = (sol.handshake("vessel","company","action:{*}"))
print(tmp)

#Capmany is compromised, and issue's a malicious relation to oneself.
sol.setRelationship("company",mal_perp,"action:{*}")
#Shares the infected state through a certificate.
sol.give_states("company", "mal_perp")

#Leak is found and tried to mitigate.
sol.delRelationship("company", mal_perp)

#Needs rework!

#New state is quickly shared to mitigate.
sol.give_states("company", "vessel")
# Since for our handshake the information needs to be at the second target the state is also shared to the perp.
sol.give_states("company", "mal_perp")

#Mal_perp shares known trust to vessel to gain access.
sol.give_states("mal_perp", "vessel")

#Access is denied.
tmp = (sol.handshake("vessel","mal_perp","action:{*}"))
print(tmp)