from PubMedXMLParser.Parser import PubMedArticleParser
from NamedEntityRecognition.NERParser import PubMedNERParser


def print_relations(relations):
    t1_rels = list(filter(lambda r: "tier" in r.keys() and r["tier"] is "T1", relations))
    t2_rels = list(filter(lambda r: "tier" in r.keys() and r["tier"] is "T2", relations))
    t3_rels = list(filter(lambda r: "tier" in r.keys() and r["tier"] is "T3", relations))
    t4_rels = list(filter(lambda r: "tier" in r.keys() and r["tier"] is "T4", relations))
    for rel in t1_rels:
        print rel
    for rel in t2_rels:
        print rel
    for rel in t3_rels:
        print rel
    for rel in t4_rels:
        print rel

#fp = PubMedArticleParser("../../Data/pubmed_result_2013.xml")
fp = PubMedArticleParser("../sample-pubs/pubmed_result.xml")

try:
    fp.parse()
except IOError:
    print "Check file path!"
else:
    print "Number of articles within input file: %d\n" % len(fp)
    #print content of the last article from article list
    print "Content of the last article in the list:"
    #print str(fp.get_articles().pop())+"\n"

    pnp = PubMedNERParser()

    for article in fp.get_articles():
        abstract = article.get_abstract()
        sentences = pnp.process_abstract(abstract)
        tagged_sentences = pnp.search_entity(sentences)
        #print tagged_sentences
        relations = []
        for sent in tagged_sentences:
            pattern = pnp.search_sent_patterns(sent)
            #print pattern
            relation = pnp.rule_matching(pattern)
            relations.append(relation)
        print_relations(relations)