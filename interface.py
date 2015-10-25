import ngrams_list


def interface():
    print("Welcome!")
    n = int(input("What type of n-gram would you like to use for your model? Enter a number between 1 and 4: "))
    fin = input("What training data do you want to use? Enter the path to a text file: ")

    model = ngrams_list.NGramModel(fin, n)

    print("You made the model!")
    print(model.model)
    print(type(model.model))
    menu(model)
    print("Thank you and goodbye")


def menu(model):
    nxt = int(input("""What would you like to do now? Enter one of the following numbers:
    1: Generate some random sentences
    2: Find out which words are the most common
    3: Find out which word occurs with the most different words
    4: Find out all the words that can occur after a specific history
    0: Exit
    """))

    if nxt == 1:
        number = int(input("How many sentences would you like? Enter an integer: "))
        for i in range(number):
            print(model.generate_sentence())
        menu(model)
    elif nxt == 2:
        number = int(input("How many words would you like? Enter an integer: "))
        words = model.most_common_words(number)
        for item in words:
            print(item)
        menu(model)
    elif nxt == 3:
        print(model.most_next_words())
        menu(model)
    elif nxt == 4:
        history = input("What history are you interested in? Enter a string of n-1 words: ")
        words = model.n_grams_with(history)
        for item in words:
            print(item)
        menu(model)
    elif nxt == 0:
        return None
    else:
        print("Invalid input, please try again.")
        menu(model)

if __name__ == "__main__":
    interface()
