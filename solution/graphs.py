import os
import numpy as np
import matplotlib.pyplot as plt


# Handshake.
with open('handshake_out.txt') as f:
    lines = (f.readlines())
handshake = [float(x[:-2]) for x in lines]

plt.plot(handshake)
plt.xlabel('Length of trust of chain')
plt.ylabel('Time in seconds')
plt.title("Testing Handshake")
plt.savefig('scale_handshake.png')

plt.clf()

# Relations.
with open('relations_out.txt') as f:
    lines = (f.readlines())
relations = [float(x[:-2]) for x in lines]

plt.plot(relations)
plt.xlabel('Relations in the state')
plt.ylabel('Time in seconds')
plt.title("Testing Create Relation")
plt.savefig('scale_relations.png')

plt.clf()

# Change.
with open('change_out.txt') as f:
    lines = (f.readlines())
change = [float(x[:-2]) for x in lines]

plt.plot(change)
plt.xlabel('Relations in the state')
plt.ylabel('Time in seconds')
plt.title("Testing Changing a Relation")
plt.savefig('scale_change.png')

plt.clf()

# Certificates.
with open('certificates_out.txt') as f:
    lines = (f.readlines())
certificates = [float(x[:-2]) for x in lines]

plt.plot(certificates)
plt.xlabel('Number of relations in certificate')
plt.ylabel('Time in seconds')
plt.title("Testing Certificate Creation")
plt.savefig('scale_certificate.png')

plt.clf()

# Import.
with open('import_out.txt') as f:
    lines = (f.readlines())
importt = [float(x[:-2]) for x in lines]

plt.plot(importt)
plt.xlabel('Number of already imported certificates')
plt.ylabel('Time in seconds')
plt.title("Testing Import")
plt.savefig('scale_import.png')


# To run all for the graphs and create the graphs run:
# python3 handshake_out.py >> handshake_out.txt && python3 relations_out.py >> relations_out.txt && python3 change_out.py >> change_out.txt && python3 certificates_out.py >> certificates_out.txt && python3 import_out.py >> import_out.txt && python3 graphs.py


#dir_name = "./"
#test = os.listdir(dir_name)

#for item in test:
#    if item.endswith(".txt"):
#        os.remove(os.path.join(dir_name, item))