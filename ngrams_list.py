# TODO add methods for other values of n (trigram, 4-gram etc)
# TODO add method for returning x most common words (sort the list by freq field)
# TODO find a way to use the other sort algorithm, something like return which word can go with the most other words?
from nltk import word_tokenize
import random
import linked_list


class NGramModel:
    def __init__(self, file, n):
        """
        :param file: path to text file to be used as training data
        :param n: the n for your n-gram model (2 uses bigrams etc)
        :return:
        """
        self.file = file
        self.n = n
        self.tokens = self.tokenise()  # linked list of tokens of text in order, including sentence start/end
        self.model = self.make_bigram_model()

    def tokenise(self):  # TODO test!
        """
        Tokenise the file using NLTK, add sentence start/end tokens.
        :return: linked list of tokens, including start/end of sentence tokens
        """
        # TODO exception handling!
        # read in file
        with open(self.file) as fin:
            text = fin.read()

            # tokenise the file using the NLTK word_tokenise() function
            tokens_list = word_tokenize(text)

        # we have a module object linked_list (imported) that provides a class called LinkedList()
        tokens_ll = linked_list.LinkedList()
        for tok in tokens_list:   # put these tokens into a linked list
            tokens_ll.list_insert_tail(tok)

        # insert sentence start token at start of text, sentence end token at end
        tokens_ll.list_insert_head("<s>")
        tokens_ll.list_insert_tail("</s>")

        # search tokens_ll for instances of _Node with key ".", when find one, insert two nodes: </s> and <s>
        x = tokens_ll.head  # Shouldn't it be _head? (I suppose we are using this from the module)  # no, cos @property
        while x is not None:
            if x.key == ".":  # when you find a full stop
                tokens_ll.list_insert_middle(x, "</s>")  # insert end of sentence marker
                tokens_ll.list_insert_middle(x.next_node, "<s>")  # and after that insert start of sentence marker
            x = x.next_node  # look at next node

        return tokens_ll

    def unigram_count(self):  # TODO this is currently redundant. use it somewhere or delete it
        """
        Work out the counts of all the unigrams in the list of tokens.
        :return: dictionary of all unigrams and associated counts
        """
        unigram_dict = {}
        x = self.tokens.head
        while x is not None:
            if x.key not in unigram_dict:  # if you haven't encountered this token yet
                unigram_dict[x.key] = 1  # add a new entry to the dictionary, count 1
            else:  # you have already seen this token
                unigram_dict[x.key] += 1  # increment its count in the dictionary
            x = x.next_node
        return unigram_dict

    def make_bigram_model(self):
        # TODO use a better search algorithm!
        print("finding bigrams!")
        word = self.tokens.head
        bigrams_lst = linked_list.LinkedList()  # this stores bigrams, key = first word, value = dict of possible second words and probabilities
        prev_word = ""
        while word:  # traverse the list of tokens to the end
            if prev_word != "":
                if not bigrams_lst.head:  # for the first time through, when the list is empty, just add the thing
                    # add a new node to freq_lst with key prev_word.key and freq 1 and data {}
                    bigrams_lst.list_insert_tail(prev_word)
                    bigrams_lst.tail.freq = 1
                    bigrams_lst.tail.data = {}
                    # add entry to this dictionary data[word] = 1
                    bigrams_lst.tail.data[word.key] = 1
                else:
                    found = bigrams_lst.binary_search(prev_word)  # node if found, None if not
                    if not found:  # prev_word doesn't have any bigrams yet
                        # add a new node to freq_lst with key prev_word.key and freq 1 and data {}
                        bigrams_lst.list_insert_tail(prev_word)
                        bigrams_lst.tail.freq = 1
                        bigrams_lst.tail.data = {}
                        # add entry to this dictionary data[word] = 1
                        bigrams_lst.tail.data[word.key] = 1

                    else:  # prev_word already has some bigrams
                        found.freq += 1
                        if word.key in found.data:  # that bigram has been seen before
                            found.data[word.key] += 1  # increment its count
                        else:   # not seen that bigram yet
                            found.data[word.key] = 1  # add a new entry to the dictionary
            prev_word = word.key
            word = word.next_node

        # turn counts into probabilities
        print("doing maths!")
        firstword = bigrams_lst.head
        while firstword:  # iterate through bigrams list
            for secondword in firstword.data:
                prob = firstword.data[secondword]/firstword.freq
                firstword.data[secondword] = prob  # replace counts in bigrams dict with relative probability
            firstword = firstword.next_node
        print("model made!")
        return bigrams_lst

    @staticmethod
    def generate_word(probDict):  # pass this a dictionary of probabilities (_Node.data)
        r = random.random()
        cumulative_prob = 0
        for word in probDict:
            cumulative_prob += probDict[word]
            if cumulative_prob > r:
                return word

    def generate_sentence(self):
        text = []
        prev_word = "<s>"  # start with a beginning of sentence marker
        count = 0  # just in case it fails to randomly generate an end of sentence tag in a sensible time ...
        while prev_word != "</s>" and count < 50:  # keep going until you find an end of sentence marker
            node = self.model.binary_search(prev_word)
            new_word = self.generate_word(node.data)
            text.append(new_word)
            prev_word = new_word
            count += 1
        return " ".join(text[:-1])  # dont want to return the end of sentence marker
        #TODO tidy up the output a bit? get rid of whitespace around punctuation

    def n_grams_with(self, word):
        """
        Return all the words that can follow the specified word (or (n-1)-gram).
        :param word: the word(s) at the start of the n-gram as a string
        :return: A generator containing all the possible following words, if found, or None if not found.
        """
        node = self.model.binary_search(word)
        if node:
            print(node.key)
            for item in node.data:
                yield item.key
        else:
            return None

    def most_common_words(self, n=10):
        """
        Return the n most common words in the corpus
        :param n: How many words you want to be returned (integer)
        :return: ***
        """
        mod = self.model.quicksort()
        word = mod.head
        counter = 1
        while counter < n and word:
            yield word.key

if __name__ == "__main__":
    mod = NGramModel("sml_test.txt", 2)
    # print(mod.tokenise())
    print(mod.generate_sentence())
    print(mod.generate_sentence())
    print(mod.generate_sentence())
    print(mod.generate_sentence())
    print(mod.generate_sentence())
    print(mod.generate_sentence())
    print(mod.generate_sentence())
    print(mod.generate_sentence())
    print(mod.generate_sentence())
    #words = mod.most_common_words(20)
    # for item in words:
      #  print(item)
