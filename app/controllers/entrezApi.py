from Bio import Entrez

def searchByTerm(searchTerm):
    Entrez.email = "paocalderon22@gmail.com"  # Always tell NCBI who you are
    print searchTerm
    handlerGenes = Entrez.esearch(db="gene", term=searchTerm)
    record = Entrez.read(handlerGenes)
    geneList = []
    for i in record["IdList"]:
        elementList = []
        handlerId = Entrez.efetch(db="gene", id=i, rettype="fasta", retmode="text")
        elementList.append(i)
        elementList.append(getDisplay(handlerId.read()))
        geneList.append(elementList)
    return geneList

def getDisplay(element):
    string = element[4:]
    arrayString = str.split(string, 'Other')
    return arrayString[0]

def getFastaInfo(elementID):
    Entrez.email = "paocalderon22@gmail.com"  # Always tell NCBI who you are
    print elementID
    handle = Entrez.efetch(db="nucleotide", id=elementID, rettype="fasta", retmode="txt")
    return handle.read()

# GBSeq_sequence-gb
# TSeq_sequence-fasta