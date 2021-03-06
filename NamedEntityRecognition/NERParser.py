import nltk
import re
# TODO: expand the pattern

class PubMedNERParser(object):
    def __init__(self):
        self.__MIRSTART = r"(([mM][iI])|(micro)|(let)|(hsa)|(mmu))[-]?"
        self.__mirna_pattern = self.__MIRSTART + r"[rR]?[Nn]?[Aa]?[-]?(let)?[0-9a-z\-]*"
        self.__mirnaShort = self.__MIRSTART + r"[rR]?[Nn]?[Aa]?[-]?[0-9,/&a-zA-Z]*"
        self.__MIRNA_TAG = "MIR"
        self.__MIRNA_SHORT = "MIR-SHORT"

        # contains expressions' roots
        self.__ExpFile = "../NamedEntityRecognition/expressionPattern"
        self.__EXPSUFFIX = "[a-z]*"
        self.__EXP_TAG_V = "EXP-V"
        self.__EXP_TAG_N = "EXP-N"
        self.__EXP_TAG_ADJ = "EXP-ADJ"
        self.__EXP_TAG_PASTV = "EXP-PASTV"
        self.__expression_pattern = self.__construct_expression_pattern()

        self.__CANCERFILE = "../NamedEntityRecognition/cancer-list.csv"
        self.__CANCER_TAG = "CANCER-N"
        self.__CANCER_ADJ = "CANCER-ADJ"
        #self.__cf_content = fp.read()
        self.__cancer_dict = self.__construct_cancer_dict()
        #print  self.__cancer_dict

    def __construct_expression_pattern(self):
        with open(self.__ExpFile) as fp:
            exps = [line.strip('\n') for line in fp.readlines()]
            return "(" + "|".join(exps) + ")" + self.__EXPSUFFIX
        return ""

    def __construct_cancer_dict(self):
        with open(self.__CANCERFILE) as fp:
            return [line.strip('\n') for line in fp.readlines()]
        return ""

    def process_abstract(self, abstract):
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

    def search_tags(self, sentence):
        """ given postagged sentence
            re-tag mirnas,expression and cancer names
            returns new tagged sentences as an array
        """
        tagDict = {"NN": self.__EXP_TAG_N,
                   "NNS": self.__EXP_TAG_N,
                   "JJ": self.__EXP_TAG_ADJ,
                   "VB": self.__EXP_TAG_V,
                   "VBN": self.__EXP_TAG_PASTV,
                   "VBD": self.__EXP_TAG_PASTV,
                   "VBZ": self.__EXP_TAG_V}
        new_sent = []
        for term in sentence:
            # if miRNA
            tag = term[1]
            if re.search(self.__mirna_pattern, term[0]):
                tag = self.__MIRNA_TAG
            elif re.search(self.__mirnaShort, term[0]):
                tag = self.__MIRNA_SHORT
            # if expression
            if re.search(self.__expression_pattern, term[0]):
                tag = tagDict.get(term[1])
            #       update the list
            if term[0] in self.__cancer_dict:
                if term[1] == "NN":
                    tag = self.__CANCER_TAG
                elif term[1] == "JJ":
                    #print "mahmut", term[0]
                    tag = self.__CANCER_ADJ

            new_sent.append((term[0], tag))
        return new_sent

    def search_entity(self, sentences):
        return list(map(lambda sent: self.search_tags(sent), sentences))

    def search_sent_patterns(self,sentence):
        sent_pattern = []
        for term in sentence:
            if term[1] in [self.__MIRNA_TAG,self.__MIRNA_SHORT]:
                sent_pattern.append(term)
            elif term[1] in [self.__EXP_TAG_V,self.__EXP_TAG_N,self.__EXP_TAG_ADJ,self.__EXP_TAG_PASTV]:
                sent_pattern.append(term)
            elif term[1] in [self.__CANCER_TAG,self.__CANCER_ADJ]:
                sent_pattern.append(term)
        return sent_pattern

    def rule_matching(self,sent_pattern):
        # tier 1 
        # mirna check
        relation = {}

        mS = filter(lambda x: x[1] in [self.__MIRNA_TAG,self.__MIRNA_SHORT],sent_pattern)
        mCount = len(mS)
        if mCount == 0:
            return {}
        else:
            relation["miRNA"] = mS[0][0]

        expVs = filter(lambda x: x[1] in [self.__EXP_TAG_V,self.__EXP_TAG_PASTV],sent_pattern)
        expVCount = len(expVs)
        expNs = filter(lambda x: x[1] in [self.__EXP_TAG_N,self.__EXP_TAG_ADJ],sent_pattern)
        expNCount = len(expNs)

        if expVCount == 0 and expNCount == 0:
            return {}

        up_terms = ["over express", "overexpress", "over-express", "highly express", "high express", "up regulat",
                    "upregulat", "up-regulat", "positive regulat", "increase", "forced expression",
                    "enhanced expression",
                    "promote", "oncogenic"]
        down_terms = ["under express", "underexpress", "under-express", "lower express", "lower-express", "down regula",
                      "downregulat", "down-regulat", "negative regula", "decrease", "repress", "suppress", "inhibit",
                      "delete"]
        up_term_exp = "(" + "|".join(up_terms) + ")" + self.__EXPSUFFIX
        down_term_exp = "(" + "|".join(down_terms) + ")" + self.__EXPSUFFIX

        for term in sent_pattern:
            if re.search(up_term_exp, term[0]):
                relation["type"] = "up"
            elif re.search(down_term_exp, term[0]):
                relation["type"] = "down"

        cS = filter(lambda x: x[1] in [self.__CANCER_ADJ, self.__CANCER_TAG],sent_pattern)
        cName = ""
        for c in cS:
            if c[1] == self.__CANCER_ADJ:
                cName = c[0]
        for c in cS:
            if cName != "":
                cName += " "
            if c[1] == self.__CANCER_TAG:
                cName += c[0]
                break
        cCount = len(cS)
        if cCount != 0:
            relation["cancer"] = cName
            if expVCount != 0:
                relation["tier"] = "T1"
            elif expNCount != 0:
                relation["tier"] = "T2"
        else:
            relation["tier"] = "T4"

        return relation  
