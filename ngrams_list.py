import nltk
from nltk import word_tokenize
import linked_list


class NGramModel:
    def __init__(self, file, n):
        self.file = file
        self.n = n
        self.tokens = self.tokenise()

    def tokenise(self):
        """
        Tokenise the file usling NLTK, add sentence start/end tokens
        :return: linked list of tokens, including start/end of sentence tokens
        """
        # read in file
        # TODO execption handling!
        with open(self.file) as fin:
            text = fin.read()

            # tokenise the file using the NLTK word_tokenise() function
            tokens_list = word_tokenize(text)

        # put these tokens into a linked list
        tokens_ll = linked_list.LinkedList()
        for tok in tokens_list:
            tokens_ll.list_insert_tail(tok)

        # insert sentence start token at start of text, sentence end token at end
        tokens_ll.list_insert_head("<s>")
        tokens_ll.list_insert_tail("</s>")

        # search tokens_ll for instances of _Node with key ".", when find one, insert two nodes: </s> and <s>
        x = tokens_ll._head
        while x is not None:
            if x.key == ".":  # when you find a full stop
                tokens_ll.list_insert_middle(x, "</s>")  # insert end of sentence marker
                tokens_ll.list_insert_middle(x.next_node, "<s>")  # and after that insert start of sentence marker
            x = x.next_node  # look at next node

        return tokens_ll

    def unigram_count(self):
        """
        Work out the counts of all the unigrams in the list of tokens.
        :return: dictionary of all unigrams and associated counts
        """
        unigram_dict = {}
        x = self.tokens._head
        while x is not None:
            if x.key not in unigram_dict:  # if you haven't encountered this token yet
                unigram_dict[x.key] = 1  # add a new entry to the dictionary, count 1
            else:  # you have already seen this token
                unigram_dict[x.key] += 1  # increment its count in the dictionary
            x = x.next_node
        return unigram_dict











if __name__ == "__main__":
    mod = NGramModel("sml_test.txt", 2)
    mod.tokenise()