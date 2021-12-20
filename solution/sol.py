import numpy as np
import subprocess as sp
import glob, os, shutil

#Takes name of node fx. alice and returns public key of newly created identity
def createIdentity(identity:str):
    if os.path.exists("storage-"+identity):
        shutil.rmtree("storage-"+identity, ignore_errors=False, onerror=None)
    os.mkdir("storage-"+identity)
    store = "./storage-" + identity
    out = sp.run(["./../target/release/trinity", "-s", store, "identity", "create"],text=True,capture_output=True)
    return out.stdout

#Takes name of node fx. alice and deletes it, Irreversible
def delIdentity(identity:str):
    if os.path.exists("storage-"+identity):
        res = shutil.rmtree("storage-"+identity, ignore_errors=False, onerror=None)
        return res
    else:
        return "Path doesn't exist"

#Takes name of node fx. alice, public key of the target and the policy to assign the target
def setRelationship(identity:str,target:str,policy:str):
    store = "./storage-" + identity
    out = sp.run(["./../target/release/trinity", "-s", store, "relationship", "set", target, policy],text=True,capture_output=True)
    return out.stdout

#Takes name of node fx. alice and create a certificate
def certCreate(identity:str):
    store = "./storage-" + identity
    out = sp.run(["./../target/release/trinity", "-s", store, "certificate", "create"],text=True,capture_output=True)
    #print(out.stdout)
    return (out.stdout).split()[0]

#Takes name of node fx. alice and publishes to local-storage or delegation store if used
def certPublish(identity:str):
    store = "./storage-" + identity
    out = sp.run(["./../target/release/trinity", "-s", store, "certificate", "publish"],text=True,capture_output=True)
    return out.stdout

#Takes name of node fx. alice and imports a certificate
def certImport(identity:str,certificate:str):
    store = "./storage-" + identity
    out = sp.run(["./../target/release/trinity", "-s", store, "raw", "import", certificate],text=True,capture_output=True)
    return out.stdout

#Takes name of node fx. alice and returns the public key of the identity
def getPubKey(identity:str):
    store = "./storage-" + identity
    out = sp.run(["./../target/release/trinity", "-s", store, "identity", "public-key"],text=True,capture_output=True)
    return out.stdout

#Takes name of node fx. alice and reinitializes it
def reinitialize(identity:str):
    store = "./storage-" + identity
    out = sp.run(["./../target/release/trinity", "-s", store, "identity", "reinitialize"],text=True,capture_output=True)
    return out.stdout


#Takes name of node fx. alice and the public key of a target to remove the relationship from identity
def delRelationship(identity:str,target:str):
    store = "./storage-" + identity
    out = sp.run(["./../target/release/trinity", "-s", store, "relationship", "delete", target],text=True,capture_output=True)
    return out.stdout

#Takes name of node fx. alice and lists the relationships of the identity
def listRelationship(identity:str):
    store = "./storage-" + identity
    out = sp.run(["./../target/release/trinity", "-s", store, "relationship", "list"],text=True,capture_output=True)
    return out.stdout

#Retrieves the [date,pubkey] from a certificate   #ADD A VERIFICATION HERE
def getCertStateInfo(cert:str):
    out = sp.run(["./../target/release/trinity-certificate-pp",cert],text=True,capture_output=True)
    splittet = out.stdout.split()
    try:
        pkey = splittet.index("public_key:") + 2
        date = splittet.index("creation_date:") +2
        return [splittet[date],splittet[pkey]]
    except:
        return False 

#Retrieves the certificates form a .yaml file
def GetCertsFromState(identity:str):
    yaml = "./storage-" + identity + "/state.yaml"
    out = sp.run(["./yq","e",".identities.*.state",yaml],text=True,capture_output=True)
    return out.stdout.split()

#Iterates through an array of certificates and replaces in local yaml if newer or no pub-key(identity) is found
def publish(identity:str,inp):
    yaml = "./storage-" + identity + "/state.yaml"
    if not os.path.exists(yaml):
        k = open(yaml, "x")
        k.close()
    for i in inp:
        inf = getCertStateInfo(i)
        if inf != False:
            tmpStr = ".identities."+inf[1][1:-2]+".date"
            out = sp.run(["./yq","e",tmpStr,yaml],text=True,capture_output=True)
            if out.stdout < inf[0][:-1] or out.stdout == "null\n" :
                tmpStr = ".identities."+inf[1][1:-2]+".date=\""+inf[0][:-1]+"\"|.identities."+inf[1][1:-2]+".state=\""+i+"\""
                sp.run(["./yq", "e", "-i", tmpStr, yaml],text=True,capture_output=False)

#Imports  the  certificates  found in the  nodes  State  file
def loadStates(identity:str):
    yaml = "./storage-" + identity + "/state.yaml"
    if os.path.exists(yaml):
        out = sp.run(["./yq", "e", ".identities.*.state", yaml],text=True,capture_output=True)
        retval = (out.stdout).split()
        if retval != ['null']:
            for x in retval:
                certImport(identity, x)
        return (out.stdout).split()
    else:
        return "error, yaml file doesn't exists."

#Shares  the  state  file  between  two  nodes
def shareState(source:str, target:str):
    yaml_source = "./storage-" + source + "/state.yaml"
    if not os.path.exists(yaml_source):
        return "no certificates to share."
    else:
        yaml_target = "./storage-" + target + "/state.yaml"
        out = sp.run(["./yq", "e", ".identities.*.state", yaml_source],text=True,capture_output=True)
        certs = (out.stdout).split()
        publish(target,certs)

#Uses certCreate, publish, shareState and loadStates in that order to transfer
#the state from source to target
def give_states(source:str, target:str):
    cert = certCreate(source)
    publish(source,[cert])
    shareState(source, target)
    loadStates(target)

#Performs a handshake  between  source  and  target  with a given policy
def handshake(source:str, target:str, policy:str):
    out = sp.run(["./handshake.sh", source, target, policy],text=True,capture_output=True)
    return out.stdout