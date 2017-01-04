from PubMedXMLParser.Parser import PubMedArticleParser
from NamedEntityRecognition.NERParser import process_abstract, search_entity

fp = PubMedArticleParser("../../Data/pubmed_result_2013.xml")
#fp = PubMedArticleParser("../sample-pubs/pubmed_result.xml")

try:
    fp.parse()
except IOError:
    print "Check file path!"
else:
    print "Number of articles within input file: %d\n" % len(fp)
    #print content of the last article from article list
    print fp.get_articles().pop()

    for article in fp.get_articles():
        abstract = article.get_abstract()
        sentences = process_abstract(abstract)
        tagged_sentences = search_entity(sentences)
        

