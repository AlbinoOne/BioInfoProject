import nltk

# Tier1 = MIR-PHRASE + EXP-PHRASE + CANCER-PHRASE 
# Tier2 = MIR-PHRASE + 'as' + EXP-N-PHRASE + 'of' + CANCER-PHRASE 
# Tier2 = EXP-ADJ + MIR-PHRASE + 'in' + CANCER-PHRASE
#   (<DT>*<EXP-N><IN>) (<MIR><VBZ><DT>*<JJ>*<TO>) (<EXP-V>) (<CANCER>)

def chunking_sentences(sentences):
    grammar = r"""
        MIR-PHRASE :{<MIR|MIR-SHORT><NN>*} 
        CANCER-PHRASE :{<DT>*<JJ>*<CANCER|CANCER-N><NN|NNS>*}
        EXP-N-PHRASE:{<DT>*<JJ>*<EXP-N><IN>?}
        EXP-PASSIVE-PHRASE:{<EXP-PASTV>}
        EXP-ADJ-PHRASE:{<DT>*<NN>*<EXP-ADJ><NN>}
    """     
    cp = nltk.RegexpParser(grammar)
    sent_tree = cp.parse_sents(sentences)   
    
    return sent_tree
    
