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
        if self.n == 1:
            self.model = self.unigram_count()  # linked list of nodes, with associated probabilities
        else:  # self.n > 1:
            self.model = self.make_ngram_model()

    def tokenise(self):
        """
        Tokenise the file using NLTK, add sentence start/end tokens after each "." token.
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
        x = tokens_ll.head
        while x is not None:
            if x.key == ".":  # when you find a full stop
                tokens_ll.list_insert_middle(x, "</s>")  # insert end of sentence marker
                tokens_ll.list_insert_middle(x.next_node, "<s>")  # and after that insert start of sentence marker
            x = x.next_node  # look at next node

        return tokens_ll

    def unigram_count(self):
        """
        Work out the probability of all the unigrams in the list of tokens, from their counts.
        :return: dictionary of all unigrams and associated probabilities
        """
        unigram_dict = {}

        # make a dictionary of counts
        x = self.tokens.head
        while x is not None:
            if x.key not in unigram_dict:  # if you haven't encountered this token yet
                unigram_dict[x.key] = 1  # add a new entry to the dictionary, count 1
            else:  # you have already seen this token
                unigram_dict[x.key] += 1  # increment its count in the dictionary
            x = x.next_node

        # turn the counts into probabilities
        total_tokens = self.tokens._size
        for word in unigram_dict:
            unigram_dict[word] = unigram_dict[word]/total_tokens
        return unigram_dict

    def make_ngram_model(self):
        """
        Build a linked list from the tokens, where each node key is a possible history (n-1 gram), freq is the count of
        that history in the text, data is a dictionary where keys are the words that can follow this history, and values
        are relative probabilities of getting that word given the history, calculated from counts.
        :return:  Linked list of n-grams
        """
        print("finding ngrams!!")
        word = self.tokens.head
        ngrams_lst = linked_list.LinkedList()
        # ngrams_lst is a LinkedList containing ngrams, key = history (n-1 preceding words), freq = frequency of history
        # data = dict of possible second words and probabilities

        # make a fake initial history, consisting of n-2 spaces and a start of sentence token
        wordlist = [" "]*(self.n - 2)

        while word:  # you haven't reached the end of the list of tokens yet
            if wordlist[0] != " ":  # ie you have stepped on enough through the tokens to get a real history
                new_key = " ".join(wordlist)
                if not ngrams_lst.head:  # first time through, when ngrams_lst is empty, don't want to search it
                    ngrams_lst.list_insert_tail(new_key)
                    ngrams_lst.tail.freq = 1
                    ngrams_lst.tail.data = {word.key: 1}
                else:  # there are items in ngrams_list
                    found = ngrams_lst.binary_search(new_key)  # node if found, None if not
                    if not found:  # history doesn't have any bigrams yet
                        # add a new node to freq_lst with key prev_word.key and freq 1 and data {}
                        ngrams_lst.list_insert_tail(new_key)
                        ngrams_lst.tail.freq = 1
                        ngrams_lst.tail.data = {word.key: 1}
                    else:  # prev_word already has some bigrams
                        found.freq += 1
                        if word.key in found.data:  # that bigram has been seen before
                            found.data[word.key] += 1  # increment its count
                        else:   # not seen that bigram yet
                            found.data[word.key] = 1  # add a new entry to the dictionary
            # shuffle all the items in the history along 1 place, add word as the last item, step on word to next token
            for i in range(len(wordlist)-1):
                wordlist[i] = wordlist[i+1]
            wordlist[-1] = word.key
            word = word.next_node

        print("doing maths!")
        # this bit turns counts of words given history into probabilities
        history = ngrams_lst.head
        while history:  # iterate through ngrams_lst
            for final_word in history.data:
                prob = history.data[final_word]/history.freq
                history.data[final_word] = prob
            history = history.next_node
        print("model made!")
        return ngrams_lst

    @staticmethod
    def generate_word(prob_dict):  # pass this a dictionary of probabilities (_Node.data)
        """
        Generate a random word (key) from a dictionary of possible words and probabilities.
        :param prob_dict: dictionary where keys are possible next words given history, and values are relative
        probabilities.
        :return: word, one of the keys from the dictionary, as a string
        """
        r = random.random()  # generate a random float 0 < r < 1
        cumulative_prob = 0
        for word in prob_dict:
            cumulative_prob += prob_dict[word]  # keep adding up the probabilities of the words you can choose from
            if cumulative_prob > r:  # until the sum gets bigger than the random number,
                return word  # then return the word you got to

    def generate_sentence_unigram(self):
        """
        Generate a pseudo-random sentence from a unigram model. This is called by generate_sentence() if self.n is 1, ie
        the user asked for a unigram model.
        :return: a sentence, as a string
        """
        sentence = []
        new_word = ""
        count = 0  # in case the function fails to generate an end of sentence tag after a sensible length
        while new_word != "</s>" and count < 50:  # until you find an end of sentence tag or have generated 50 words
            new_word = self.generate_word(self.model)  # generate a new word
            sentence.append(new_word)  # add it to the list of words
            count += 1
        sentence_str = " ".join(sentence[:-1])  # make a string from the list
        if sentence_str != "":  # you generated some words
            return sentence_str  # TODO tidy up the output a bit? get rid of whitespace around punctuation

        else:  # you generated an empty sentence
            return self.generate_sentence_unigram()

    def generate_sentence(self):
        """
        Generate a pseudorandom sentence using the n-gram model made in __init__. Currently only working for n <=4
        :return: a sentence! as a string, or None if user chose invalid n for class
        """
        if self.n == 1:  # in this case you can use the much simpler generate_sentence_unigram() method, so call that
            return self.generate_sentence_unigram()
        else:
            text = []
            count = 0  # track how many words you have generated,
            # just in case it fails to randomly generate an end of sentence tag in a sensible time

            # set up the initial (n-1)-gram
            if self.n == 2:  # TODO generalise this initialisation bit somehow, to allow for any n
                prev_list = ["<s>"]
            elif self.n == 3:
                prev_list = ["</s>", "<s>"]
            elif self.n == 4:
                prev_list = [".", "</s>", "<s>"]
            else:
                print("Not implemented yet, pick 1 <= n <= 4")
                return None

            # generate words
            while prev_list[-1] != "</s>" and count < 50:  # keep going until you find an end of sentence marker
                new_key = " ".join(prev_list)  # make a key from the history, in the same way as in make_ngram_model()
                node = self.model.binary_search(new_key)  # find the node with this key
                if node:
                    new_word = self.generate_word(node.data)
                    text.append(new_word)
                    for i in range(len(prev_list)-1):
                        prev_list[i] = prev_list[i+1]
                    prev_list[-1] = new_word
                    count += 1
                else:  # when the (n-1)-gram you made in the key hasn't been seen in your text
                    # TODO implement some kind of backoff or smoothing?
                    break

            # make a string from the list of words you generated
            sentence_str = " ".join(text[:-1])  # dont want to return the end of sentence marker
            if sentence_str != "":
                return sentence_str  # TODO tidy up the output a bit? get rid of whitespace around punctuation
            else:  # if it failed to generate any words
                return self.generate_sentence()  # call itself again, until you get a sentence that is not empty

    def n_grams_with(self, word):
        """
        Return all the words that can follow the specified word (or (n-1)-gram).
        :param word: the word(s) at the start of the n-gram as a string
        :return: A generator containing all the possible following words, if found, or None if not found.
        """
        # Basically this just prints the keys from the dictionary you made for each word in make_ngram_model()
        if self.n == 1:
            print("You made a unigram model, you can't work this out!")
            return None
        else:
            node = self.model.binary_search(word)
            if node:
                print("Words that follow '{}' are:".format(node.key))
                for item in node.data:
                    print(item)
                    yield item
            else:
                return None

    def most_common_words(self, n=10):
        """
        Return the n most common words in the corpus
        :param n: How many words you want to be returned (integer)
        :return: ***
        """
        self.model.insertionsort()
        word = self.model.head
        counter = 0
        while counter < n and word:
            yield word.key
            word = word.next_node
            counter += 1

    def most_next_words(self):
        """
        Return the word that can occur with the most different words after it
        :return: word, or None if the model is unigrams.
        """
        if self.n == 1:
            print("You made a unigram model, you can't work this out!")
            return None
        else:
            data = self.model.mergesort()  # sort the model on the length of its dictionary
            return data.tail.key

if __name__ == "__main__":
    mod = NGramModel("textfortest.txt", 1)
    #print(mod.tokenise())
    print(mod.generate_sentence())
    print(mod.model)
    print(mod.most_common_words(), "here")
    # print(mod.model.head.data)
    print(mod.generate_sentence())
