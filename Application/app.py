from PubMedXMLParser.Parser import PubMedArticleParser
from NamedEntityRecognition.NERParser import PubMedNERParser


fp = PubMedArticleParser("../../Data/pubmed_result_2013.xml")
#fp = PubMedArticleParser("../sample-pubs/pubmed_result.xml")

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
