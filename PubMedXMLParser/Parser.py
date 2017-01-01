import xml.etree.ElementTree as ET
from Article import PublicationDate
from Article import PubMedArticle


class PubMedArticleParser(object):
    def __init__(self, file_path):
        self.__index_of_article = 0
        self.__num_of_article_without_date = 0
        self.__fp = file_path
        self.__articles = []

    def __del__(self):
        pass

    def __len__(self):
        return len(self.__articles)

    def __find_articles(self, root):
        for article in root.findall("PubmedArticle"):
            pubmed_id = int(article.find("MedlineCitation").find("PMID").text)
            pub_date = self.__get_date(article.find("./MedlineCitation/Article/Journal/JournalIssue/PubDate"))
            title = article.find("./MedlineCitation/Article/ArticleTitle").text
            abstract = self.__get_abstract(article.find("./MedlineCitation/Article/Abstract"))
            self.__articles.append(PubMedArticle(pubmed_id, pub_date, title, abstract))

    def __get_date(self, pub_date):
        try:
            pd = PublicationDate(int(pub_date.find("Year").text),
                                 pub_date.find("Month").text,
                                 int(pub_date.find("Day").text))
        except:
            self.__num_of_article_without_date += 1
            #print "No date at article#%d! #%d" % (self.__index_of_article, self.__num_of_article_without_date)
            return None
        else:
            return pd
        finally:
            self.__index_of_article += 1

    def __get_abstract(self, abstract):
        ret_val = ""
        for abstract_text in abstract.findall("AbstractText"):
            if abstract_text.text is not None:
                ret_val += abstract_text.text
            else:
                ret_val = abstract.text
                break
        return ret_val

    def parse(self):
        try:
            tree = ET.parse(self.__fp)
            root = tree.getroot()
            self.__find_articles(root)
        except:
            print "Something is wrong within input file :("

    def get_articles(self):
        return self.__articles