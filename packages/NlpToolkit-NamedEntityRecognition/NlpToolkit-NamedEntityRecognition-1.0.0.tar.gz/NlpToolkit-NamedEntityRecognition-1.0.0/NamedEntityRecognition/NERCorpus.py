from Corpus.Corpus import Corpus
from DataStructure.CounterHashMap import CounterHashMap

from NamedEntityRecognition.NamedEntitySentence import NamedEntitySentence


class NERCorpus(Corpus):

    """
    Another constructor of NERCorpus which takes a fileName of the corpus as an input, reads the
    corpus from that file.

    PARAMETERS
    ----------
    fileName : str
        Name of the corpus file.
    """
    def __init__(self, fileName=None):
        self.sentences = []
        self.wordList = CounterHashMap()
        if fileName is not None:
            inputFile = open(fileName)
            lines = inputFile.readlines()
            for line in lines:
                self.addSentence(NamedEntitySentence(line))

    """
    addSentence adds a new sentence to the sentences list

    PARAMETERS
    ----------
    s : Sentence
        Sentence to be added.
    """
    def addSentence(self, s: NamedEntitySentence):
        self.sentences.append(s)