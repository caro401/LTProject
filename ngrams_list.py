import nltk
from nltk import word_tokenize
import linked_list


class NGramModel:
    def __init__(self, file, n):
        self.file = file
        self.n = n

    def tokenise(self):
        """
        Tokenise the file usling NLTK, add sentence start/end tokens
        :return: linked list of tokens, including start/end of sentence tokens
        """
        # read in file
        with open(self.file) as fin:
            text = fin.read()
            tokens_list = word_tokenize(text)  # list of tokens from NLTK

        tokens_ll = linked_list.LinkedList
        for tok in tokens_list:
            tokens_ll.list_insert_tail(tok)

        # insert sentence start token at start of text
        tokens_ll.list_insert_head("<s>")  # weeeeird







        # linked list (queue-like) to insert sentence boundary tokens

        # return linked list
