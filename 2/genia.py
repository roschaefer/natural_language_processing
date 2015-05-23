import xml.etree.ElementTree as ET
class Article:
    def __init__(self, location):
        self.location = location
        self.tree = ET.parse("./{location}".format(location=self.location))
        self.word_tag_sentences = self.__get_word_tag_sentences(self.article())
        self.word_sentences = [[w for w,t in sentence] for sentence in self.word_tag_sentences]
        self.tag_sentences = [[t for w,t in sentence] for sentence in self.word_tag_sentences]

    def article(self):
        return self.tree.getroot()[0][0][0][1]

    def abstract(self):
        return self.article()[1][0]

    def title(self):
        return self.article()[0]

    def __get_word_tag_sentences(self, xml_branch):
        sentences_with_word_tags = []
        for sentence in xml_branch.findall('.//sentence'):
            word_tags = []
            for token in sentence.findall('.//tok'):
                word_tags.append((token.text, token.get('cat')))
            sentences_with_word_tags.append(word_tags)
        return sentences_with_word_tags
