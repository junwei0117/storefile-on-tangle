from iota import *
from random import SystemRandom
import re,os,math,random

filename = ''

def NodeInfo():
    node_info = api.get_node_info()
    print("node_info:")
    print node_info


def GenerateSeed():
    alphabet = u'9ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    generator = SystemRandom()
    seed = str(u''.join(generator.choice(alphabet) for _ in range(81)))
    return seed

def GetBytesFromFile(file_link):  
    BytesFile = open(file_link, "rb").read()
    
    return BytesFile

def GetFilename(file_link):
    f = open(file_link)
    filename = os.path.basename(f.name)
    return filename

def ToTrytes(BytesFile):
    TrytesFile = str(TryteString.from_bytes(BytesFile))
    return TrytesFile

def FilenameToTag(file_link):
    filename = GetFilename(file_link).upper()
    up_filename = filename.split(".")[0]
    return up_filename

'''def TransferChunk(TrytesFile,file_link):
    chunks = re.findall(r'.{1,2187}',TrytesFile)
    i = 0
    new_address = GenerateSeed()
    TransactiuonsList = []
    print "Splitting file into %d chunks" %(len(chunks))
    for i in range(len(chunks)):
        api.send_transfer(
        depth=depth,
        transfers=[
                    ProposedTransaction(
                        address=Address(new_address),
                        value=0,
                        message=TryteString.from_string(chunks[i]),
                        tag=FilenameToTag(file_link)
                    )
                ],
        min_weight_magnitude=14,
        inputs=[Address(new_address, key_index=0, security_level=0)]
        )
        i = i + 1
        print "transaction #%d : %s" %(i,GetTransactiuonsHash(new_address)) 
        TransactiuonsList.append(GetTransactiuonsHash(new_address))
    return TransactiuonsList'''

def GetTransactiuonsHash(address):
    transactions_hash = api.find_transactions(addresses = [address])[u'hashes'][-1]
    return transactions_hash

def GetBundleHash(address):
    bundle_hash = api.get_bundles(GetTransactiuonsHash(address))
    return bundle_hash

def StartUpload(TrytesFile,file_link):
    chunks = re.findall(r'.{1,2187}',TrytesFile)
    seed = GenerateSeed()
    TransactiuonsList = []
    Transaction_index = 0
    i = 0
    for i in range(len(chunks)):
        TransactiuonsList.append(api.prepare_transfer(
        transfers=[
                    ProposedTransaction(
                        address=Address(seed),
                        value=0,
                        message=chunks[i],
                        tag= FilenameToTag(file_link)
                    )
                ]
    ))
    print "Splitting file into %d chunks" %(len(chunks))
    #print TransactiuonsList
    TransferChunk(TransactiuonsList,Transaction_index,seed)


def TransferChunk(TransactiuonsList,Transaction_index,seed):
    api.send_trytes(TransactiuonsList[Transaction_index][u'trytes'],int(math.floor(random.randint(0,1)*(12-4+1)+4)),14)
    Transaction_index+=1
    if (Transaction_index != len(TransactiuonsList)):
        print "transaction #%d : %s" %(Transaction_index-1,GetTransactiuonsHash(seed))
        TransferChunk(TransactiuonsList,Transaction_index,seed)
    else:
        print "transaction #%d : %s" %(Transaction_index,GetTransactiuonsHash(seed))
        print "upload complete"


depth = 3 
NodeUrl = "http://210.240.162.109:14265"
api = Iota(NodeUrl)
file_link = raw_input("where is your file?")        #get file link
BytesFile = GetBytesFromFile(file_link)             #get bytes from file
TrytesFile = ToTrytes(BytesFile)                    #get trytes from bytes
StartUpload(TrytesFile,file_link)










