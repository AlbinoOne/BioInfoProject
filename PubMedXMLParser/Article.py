class PubMedArticle(object):
    def __init__(self, pubmed_id, publication_date, title, abstract):
        self.__pubmed_id = pubmed_id
        self.__publication_date = publication_date
        self.__title = title
        self.__abstract = abstract

    def __str__(self):
        ret_val = "Article Id: %d\n" % self.__pubmed_id
        if self.__publication_date is not None:
            ret_val += "Publication Date: %d-%s-%d\n" % (self.__publication_date.year, self.__publication_date.month, self.__publication_date.day)
        ret_val += "Title: %s\n" % self.__title
        ret_val += "Abstract: %s" % self.__abstract
        return ret_val.encode('utf-8')

    def get_pubmed_id(self):
        return self.__pubmed_id

    def get_publication_date(self):
        return self.__publication_date

    def get_title(self):
        return self.__title

    def get_abstract(self):
        return self.__abstract


class PublicationDate(object):
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day