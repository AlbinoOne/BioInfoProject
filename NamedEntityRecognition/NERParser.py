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

        self.__CANCERFILE = "../NamedEntityRecognition/icdo3.codes.csv"
        self.__CANCER_TAG = "CANCER-N"
        self.__CANCER_ADJ = "CANCER-ADJ"
        fp = open(self.__CANCERFILE, "r")
        self.__cf_content = fp.read()

    def __construct_expression_pattern(self):
        with open(self.__ExpFile) as fp:
            exps = [line.strip('\n') for line in fp.readlines()]
            return "(" + "|".join(exps) + ")" + self.__EXPSUFFIX
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
                # find the cancer name
            # TODO: error finding cancer names
            #       update the list
            if term[1] == "NN" and (term[0] in self.__cf_content):
                tag = self.__CANCER_TAG
            new_sent.append((term[0], tag))
        return new_sent

    def search_entity(self, sentences):
        return list(map(lambda sent: self.search_tags(sent), sentences))