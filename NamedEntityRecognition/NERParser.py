import nltk
import re

# TODO: expand the pattern

MIRSTART = r"(([mM][iI])|(micro)|(let)|(hsa)|(mmu))[-]?"
mirnaPattern = MIRSTART+r"[rR]?[Nn]?[Aa]?[-]?(let)?[0-9a-z\-]*"
mirnaShort = MIRSTART + r"[rR]?[Nn]?[Aa]?[-]?[0-9,/&a-zA-Z]*"
MIRNA_TAG = "MIR"
MIRNA_SHORT = "MIR-SHORT"

# contains expressions' roots 
ExpFile = "expressionPattern"
EXPSUFFIX = "[a-z]*"
EXP_TAG_V = "EXP-V"
EXP_TAG_N = "EXP-N"
EXP_TAG_ADJ = "EXP-ADJ"
EXP_TAG_PASTV = "EXP-PASTV"

CANCERFILE = "icdo3.codes.csv"
CANCER_TAG = "CANCER-N"
CANCER_ADJ = "CANCER-ADJ"

def process_abstract(abstract):
    """ for a given abstract, process it as follows: 
    1 - get sentences 
    2 - get words for each sentence
    3 - apply part-of-speech tagging for each sentence 
    returns pos labeled sentences
    """
    sentences = nltk.sent_tokenize(abstract)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences] 
    return sentences


def search_tags(sentence):
    """ given postagged sentence 
       re-tag mirnas,expression and cancer names 
       returns new tagged sentences as an array
    """
    fp = open(CANCERFILE,"r")
    with open(ExpFile) as fxp:
        expressions = fxp.readlines()
    expressions = [e.replace('\n','') for e in expressions]
    expPattern = "|".join(expressions)
    expPattern = "("+expPattern+")"+EXPSUFFIX

    tagDict = {"NN":EXP_TAG_N,
               "JJ":EXP_TAG_ADJ,
               "VB":EXP_TAG_V,
               "VNB":EXP_TAG_PASTV}
    new_sent = []  
    for term in sentence:
        # if miRNA 
        tag = term[1]
        if re.search(mirnaPattern,term[0]):
            tag = MIRNA_TAG
        elif re.search(mirnaShort,term[0]):
            tag = MIRNA_SHORT
        # if expression
        if re.search(expPattern,term[0]): 
            tag = tagDict.get(term[1])    
        # find the cancer name 
        # TODO: error finding cancer names 
        #       update the list
        if term[1] == "NN" and (term[0] in fp.read()) : 
            tag = CANCER_TAG
        new_sent.append((term[0],tag))
    return new_sent  

def search_entity(sentences):
    tagged_sents = []
    for sent in sentences:
        tagged_sents.append(search_tags(sent)) 
    return tagged_sents            
  
   



  
