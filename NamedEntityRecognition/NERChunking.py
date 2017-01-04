import nltk

def chunking_sentences(sentences):
    grammar = r"""
        MIR-PHRASE :{<MIR|MIR-SHORT><NN>*} 
        CANCER-PHRASE :{<DT>*<JJ>*<CANCER><NN>*}
        EXP-N-PHRASE:{<DT>*<JJ>*<EXP-N><IN>?}
        EXP-PASSIVE-PHRASE:{<EXP-PASTV>}
        EXP-ADJ-PHRASE:{<DT>*<NN>*<EXP-ADJ><NN>}
    """     
    cp = nltk.RegexpParser(grammar)
    sent_tree = cp.parse_sents(sentences)   
    return sent_tree
