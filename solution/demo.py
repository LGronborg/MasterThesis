import sol.py

# Demo of offline Vessel use case

Vessel = sol.createIdentity("Vessel")
VesselCompany = sol.createIdentity("VesselCompany")
service = sol.createIdentity("service")
serviceWorker = sol.createIdentity("serviceWorker")

# Vessel have an innate trust to its parent company.
sol.setRelationship("Vessel", VesselCompany, "action:{*}")
sol.give_states("Vessel", "VesselCompany")
# Vessel can be offline from here

# Set further relationships, but not sharing them.
sol.setRelationship("VesselCompany", service, "action:{work}")
sol.setRelationship("service", serviceWorker, "action:{work.front}")

# Check that handshake doesn't work. Would require contact to Vessel
print(sol.handshake("Vessel", "serviceWorker", "action:{work.front}"))

# Share states down the line of trust.
sol.give_states("VesselCompany", "service")
sol.give_states("service", "serviceWorker")

# Vessel & serviceWorker meets
# Check that now "serviceWorker" can prove that Vessel should trust him
# with "action:{work.front}".
print(sol.handshake("Vessel", "serviceWorker", "action:{work.front}"))


#--------------------------------------------------------------------------------------------------------------------------------------------
# Demo of 3. party Vessel (random entity) use case

# Creating identities.
Vessel = sol.createIdentity("Vessel")
VesselCompany = sol.createIdentity("VesselCompany")
randomEntity = sol.createIdentity("randomEntity")
service = sol.createIdentity("service")
serviceWorker = sol.createIdentity("serviceWorker")

# Vessel have an innate trust to its parent company.
sol.setRelationship("Vessel", VesselCompany, "action:{*}")
# Set further relationships, but not sharing them.
sol.setRelationship("VesselCompany", service, "action:{work}")
sol.setRelationship("service", serviceWorker, "action:{work.front}")

# Share states down the line of trust.
sol.give_states("VesselCompany", "randomEntity")
sol.give_states("service", "serviceWorker")
sol.give_states("randomEntity", "Vessel")

# Check that handshake doesn't work.
print(sol.handshake("Vessel", "serviceWorker", "action:{work.front}"))

# Share every known state to service worker.
sol.give_states("Vessel","serviceWorker")

# Check that handshake does work.
print(sol.handshake("Vessel", "serviceWorker", "action:{work.front}"))

#--------------------------------------------------------------------------------------------------------------------------------------------
# Demo of centralized hub use case

# Creating identities.
Vessel = sol.createIdentity("Vessel")
VesselCompany = sol.createIdentity("VesselCompany")
service = sol.createIdentity("service")
serviceWorker = sol.createIdentity("serviceWorker")
centralizedHub = sol.createIdentity("centralizedHub")

# Set further relationships, but not sharing them.
sol.setRelationship("Vessel", VesselCompany, "action:{*}")
sol.setRelationship("VesselCompany", service, "action:{work}")
sol.setRelationship("service", serviceWorker, "action:{work.front}")

# Share states to the centralized hub.
sol.give_states("Vessel", "centralizedHub")
sol.give_states("VesselCompany", "centralizedHub")
sol.give_states("service", "centralizedHub")

# Check that handshake doesn't work.
print(sol.handshake("Vessel", "serviceWorker", "action:{work.front}"))

# Share all the states from the centralized hub to the service worker.
sol.give_states("centralizedHub", "serviceWorker")

# Check that handshake does work.
print(sol.handshake("Vessel", "serviceWorker", "action:{work.front}"))


#--------------------------------------------------------------------------------------------------------------------------------------------
# Demo of revoking trust use case

# Creating identities.
Vessel = sol.createIdentity("Vessel")
VesselCompany = sol.createIdentity("VesselCompany")
service = sol.createIdentity("service")
serviceWorker = sol.createIdentity("serviceWorker")
centralizedHub = sol.createIdentity("centralizedHub")

# Set further relationships, but not sharing them.
sol.setRelationship("Vessel", VesselCompany, "action:{*}")
sol.setRelationship("VesselCompany", service, "action:{work}")
sol.setRelationship("service", serviceWorker, "action:{work.front}")

# Share states to the centralized hub.
sol.give_states("Vessel", "centralizedHub")
sol.give_states("Vessel", "VesselCompany")
sol.give_states("VesselCompany", "centralizedHub")
sol.give_states("service", "centralizedHub")

# Check that handshake doesn't work.
print(sol.handshake("Vessel", "serviceWorker", "action:{work.front}"))

# Share all the states from the centralized hub to the service worker.
sol.give_states("centralizedHub", "serviceWorker")

# Check that handshake does work.
print(sol.handshake("Vessel", "serviceWorker", "action:{work.front}"))

sol.delRelationship("VesselCompany", service)
sol.give_states("VesselCompany", "centralizedHub")
sol.give_states("centralizedHub", "serviceWorker")

# Check that handshake does work.
print(sol.handshake("Vessel", "serviceWorker", "action:{work.front}"))