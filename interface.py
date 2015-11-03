#!python3
import ngrams_list


def interface():
    print("Welcome !")
    while True:
        n = input("What type of n-gram would you like to use for your model? Enter a number between 1 and 4, press enter to exit: ")
        if n == '':
            print("Thank you and goodbye.")
            return
        if n in ["1", "2", "3", "4"]:
            break
        else:
            print("Invalid input, please enter a number between 1 and 4.")
            continue

    while True:
        try:
            fin = input("What training data do you want to use? Enter the path to a text file: ")
            if fin == "":
                print("Thank you and goodbye.")
            n = int(n)
            model = ngrams_list.NGramModel(fin, n)
            print("You made the model!")
            break
        except:
            print("Invalid input. Please try again")
            continue
    menu(model)
    print("Thank you and goodbye")


def menu(model):
    nxt = input("""What would you like to do now? Enter one of the following numbers:
    1: Generate some random sentences
    2: Find out which tokens are the most common
    3: Find out which word occurs with the most different words
    4: Find out all the words that can occur after a specific history
    0: Exit
    """)

    if nxt == "1":
        number = input("How many sentences would you like? Enter an integer: ")
        try:
            number = int(number)
            for i in range(number):
                print(model.generate_sentence())
        except ValueError:
            print("Invalid input. Please try again.")
        menu(model)
    elif nxt == "2":
        number = input("How many words would you like? Enter an integer: ")
        try:
            number = int(number)
            words = model.most_common_words(number)
            for item in words:
                print(item)
        except:
            print("Invalid input. Please try again.")
        menu(model)
    elif nxt == "3":
        if model.n == 1:
            print("You made a unigram model, you can't work this out!")
        else:
            print(model.most_next_words())
        menu(model)
    elif nxt == "4":
        if model.n == 1:
            print("You made a unigram model, you can't work this out!")
        else:
            history = input("What history are you interested in? Enter a string of n-1 words: ")
            try:
                words = model.n_grams_with(history)
                for item in words:
                    print(item)
            except:
                print("Invalid input. Please try again.")
        menu(model)
    elif nxt == "0" or nxt == '':
        return
    else:
        print("Invalid input, please try again.")
        menu(model)

if __name__ == "__main__":
    interface()
