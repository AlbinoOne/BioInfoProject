import nltk
import re

# TODO: expand the pattern

MIRSTART = r"(([mM][iI])|(micro)|(let)|(has)|(mmu))[-]?"
mirnaPattern = MIRSTART+r"[rR]?[Nn]?[Aa]?[-]?(let)?[0-9a-z\-]*"
mirnaShort = MIRSTART + r"[rR]?[Nn]?[Aa]?[-]?[0-9,/&a-zA-Z]*"

MIRNA_TAG = "MIR"
MIRNA_SHORT = "MIR-SHORT"

def process_abstract(abstract):
""" for a given abstract, process it as follows: 
    1 - get sentences 
    2 - get words for each sentence
    3 - apply part-of-speech tagging for each sentence 
returns pos labeled sentences
"""
    sentences = nltk.sent_tokenize(document)
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
            # TODO for expressions
            new_sent.append((elm[0],tag))
        tagged_sent.append(new_sent)
    return tagged_sent 
   

