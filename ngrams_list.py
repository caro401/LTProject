from nltk import word_tokenize
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

    def tokenise(self):  # TODO test!
        """
        Tokenise the file using NLTK, add sentence start/end tokens.
        :return: linked list of tokens, including start/end of sentence tokens
        """
        # read in file
        # TODO exception handling!
        with open(self.file) as fin:
            text = fin.read()

            # tokenise the file using the NLTK word_tokenise() function
            tokens_list = word_tokenize(text)

        # we have a module object linked_list (imported) that provides a function called LinkedList()
        tokens_ll = linked_list.LinkedList()
        for tok in tokens_list:   # put these tokens into a linked list
            tokens_ll.list_insert_tail(tok)

        # insert sentence start token at start of text, sentence end token at end
        tokens_ll.list_insert_head("<s>")
        tokens_ll.list_insert_tail("</s>")

        # search tokens_ll for instances of _Node with key ".", when find one, insert two nodes: </s> and <s>
        x = tokens_ll.head  # Shouldn't it be _head? (I suppose we are using this from the module)
        while x is not None:
            if x.key == ".":  # when you find a full stop
                tokens_ll.list_insert_middle(x, "</s>")  # insert end of sentence marker
                tokens_ll.list_insert_middle(x.next_node, "<s>")  # and after that insert start of sentence marker
            x = x.next_node  # look at next node

        return tokens_ll

    def unigram_count(self):  # TODO test! compare to NLTK output?  this is now redundant...
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

    def ngram_count(self, n):  # TODO test. Compare with NLTK?
        """
        Work out the counts of all the n-grams in the list of tokens (generalised version of unigram count)
        :param n:
        :return:
        """
        ngram_dict = {}
        x = self.tokens.head  # start of n-gram
        y = x
        for i in range(n-1):
            y = y.next_node  # y represents the end of the n-gram
        while y is not None:  # ie while the n-gram won't go off the end of the list

            # build the key from the values of the nodes between x and y inclusive
            k = x.key  # the n-gram
            iter_node = x
            for i in range(n-1):
                iter_node = iter_node.next_node
                k = k + " " + iter_node.key

            # update the dictionary based on this key
            if k not in ngram_dict:
                ngram_dict[k] = 1
            else:
                ngram_dict[k] += 1

            # increment the pointers to the start and end of the n-gram
            x = x.next_node
            y = y.next_node
        return ngram_dict

    def make_bigram_model(self):
        word = self.tokens.head
        bigrams_lst = linked_list.LinkedList()  # this stores bigrams, key = first word, value = dict of possible second words and probabilities
        prev_word = ""
        while word:  # traverse the list of tokens to the end
            if prev_word != "":
                pass
                # found = bigrams_lst.find(prev_word.key)  # node if found, None if not
                # found_bigrams = bigrams_lst.find(prev_word.key)
                # if not found:  # prev_word doesn't have any bigrams yet
                    # add a new node to freq_lst with key prev_word.key and freq 1 and data {}
                    # add entry to this dictionary data[word] = 1
                # else:  # prev_word already has some bigrams
                    # found.freq += 1
                    # if word in found_bigrams.data:  # that bigram has been seen before
                        # found_bigrams.data[word] += 1  # increment its count
                    # else:   # not seen that bigram yet
                        # found_bigrams.data[word] = 1  # add a new entry to the dictionary
            prev_word = word
            word = word.next_node

        # turn counts into probabilities
        # firstword = bigrams_lst.head
        # while firstword:  # iterate through bigrams list
            # for secondword in firstword.data:
                # prob = firstword.data[secondword]/firstword.freq
                # firstword.data[secondword] = prob  # replace counts in bigrams dict with relative probability
        return bigrams_lst


if __name__ == "__main__":
    mod = NGramModel("sml_test.txt", 2)
    # print(mod.tokenise())
    print(mod.ngram_count(3))
