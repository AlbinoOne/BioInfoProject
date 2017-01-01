from PubMedXMLParser.Parser import PubMedArticleParser

fp = PubMedArticleParser("../../Data/pubmed_result_2013.xml")
#fp = PubMedArticleParser("../sample-pubs/pubmed_result.xml")

try:
    fp.parse()
except IOError:
    print "Check file path!"
else:
    print "Number of articles within input file: %d\n" % len(fp)
    #print content of the last article from article list
    print fp.get_articles().pop().get_abstract()
