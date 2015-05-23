import xml.etree.ElementTree as ET
class Article:
    def __init__(self, location):
        self.location = location
        self.tree = ET.parse("./{location}".format(location=self.location))
        self.sentences = self.__get_sentences(self.article())

    def article(self):
        return self.tree.getroot()[0][0][0][1]

    def abstract(self):
        return self.article()[1][0]

    def title(self):
        return self.article()[0]

    def __get_sentences(self, xml_branch):
        sentences = []
        for sentence in xml_branch.findall('.//sentence'):
            words = []
            for token in sentence.findall('.//tok'):
                words.append(token.text)
            sentences.append(words)
        return sentences
