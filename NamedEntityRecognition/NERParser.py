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


def search_mirnas(sentences):
    """ given pos labeled sentences 
    searches for miRNAs definitions
    change tokens NN,JJ as MIR
    sentences: array of sentences,
      each element is a set of words with their tags    
    returns sentence array with new tags
    """    
    # since the elements are tuple(immutable), 
    # create new sentences array
    tagged_sent = []
    for sent in sentences:
        new_sent = []  
        for elm in sent:
            # if miRNA 
            tag = elm[1]
            if re.search(mirnaPattern,elm[0]):
                tag = MIRNA_TAG
            elif re.search(mirnaShort,elm[0]):
                tag = MIRNA_SHORT
            new_sent.append((elm[0],tag))
        tagged_sent.append(new_sent)
    return tagged_sent 
   

def search_expressions(sentences):
    """ given pos tagged sentences,
    searched for the expressions 
    exps are stored in a file 
    sentences: array of sentence, with tags of each word
    returns sentence array tagged with expressions 
    """
    with open(ExpFile) as fxp:
        expressions = fxp.readlines()
    expressions = [e.replace('\n','') for e in expressions]
    expPattern = "|".join(expressions)
    expPattern = "("+expPattern+")"+EXPSUFFIX
    tagged_sent = []
    tagDict = {"NN":EXP_TAG_N,
               "JJ":EXP_TAG_ADJ,
               "VB":EXP_TAG_V,
               "VNB":EXP_TAG_PASTV}
    for sent in sentences:
        new_sent = []
        for term in sent:
            tag = term[1]
            if re.search(expPattern,term[0]): 
                tag = tagDict.get(term[1])
            new_sent.append((term[0],tag))           
        tagged_sent.append(new_sent) 
    return tagged_sent            
    

def search_cancer_names(sentences):
    """ given pos tagged sentences 
       finds cancer names and tag them 
       returns an array of sentences 
    """     
    #TODO with bigrams 
    
    return 


def search_entity(sentences):
    sentences = search_mirnas(sentences)
    tagged_sents = search_expressions(sentences)
    tagged_sents = search_cancer_names(tagged_sents)
    return tagged_sents 
   



  
