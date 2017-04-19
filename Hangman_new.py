import time 
import random



class bcolors:                    # kolory
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


life = 6
error_list =[]
start = time.time()

def is_repeating():
    '''Ask if user want to play again '''
    answer_repeating = input("Do you want to play again? (yes or no): ").upper()

    if answer_repeating == "YES":
        del error_list[:]
        return(False)                   # gra od nowa
    else:
        print("Have a nice day;)")          # przerywa grę
        exit()

       


def open_file():
    ''' Open file with countries-capitals'''
    plik = open("countries_and_capitals.txt")
    content = plik.readlines()
    plik.close()
    return (content)


def choice_random_capital(content):
    ''' Random selection of pair country-capital, extract it and return tuple (country,capital)'''
    mystery_pair = random.choice(content).upper()
    mystery_pair = mystery_pair.split(" | ")
    mystery_pair[1] = mystery_pair[1].strip()
    return (mystery_pair)


def split_word(mystery_pair):
    ''' Extract capital from pair country-capital and change to single letters'''
    capital = mystery_pair[1]
    print(capital)
    length_capital = list(capital)
    return(length_capital)

def get_country(mystery_pair):
    '''Extract country from pair country-capital '''
    country=mystery_pair[0]
    return (country)

def dash(length_capital):
    ''' Change name of capital for dash. If more than one word - recognize it.'''
    dash_capital = ["_"] * len(length_capital)      # zmiana nazwy stolicy na znaki
    for y in range(len(length_capital)):
        if '' == length_capital[y]:          # jesli stolica sklada sie z wiecej niz jednego slowa zajmuje sie spacjami
            dash_capital.pop(y)
            dash_capital.insert(y, ' ')
    print(' '.join(dash_capital))
    return(dash_capital)


def guessed():
    '''User write the word or letter'''
    global guess
    guesses = input(bcolors.HEADER + "Write the word or letter: " + bcolors.ENDC).upper()
    guess += 1
    print("Guess: ",guess)
    return( guesses)


def check_length(get_string_from_user, capital, dashes, capital_country):
    '''Check length of user's guesses. If is greater than 1 - recognize word. If not - it's letter'''
    if len(get_string_from_user) > 1:
        print("abc")
        word_guess(get_string_from_user, capital, capital_country, dashes)
    else:
        letter_guess(get_string_from_user, capital, dashes, capital_country)


def word_guess(guesses, length_capital, capital_country, dash_capital):
    '''Operations for word: win or lose. If user win, time stop, set date, ask about user's name.'''
    global start
    if list(guesses) == length_capital:             # wygrana
        print(get_score_list(length_capital))
        #is_repeating()
    else:
        bad_word(dash_capital, guesses)
        life_counter(capital_country)


def letter_guess(guesses, length_capital, dash_capital, capital_country):
    ''' Operation for letter: guesses every letter, quesses single letter or lose.'''
    if dash_capital == length_capital:
        print(get_score_list(length_capital))
        #is_repeating()
    elif guesses in length_capital:                       # poprawna litera
        check_letter(length_capital, dash_capital, guesses)
        if dash_capital == length_capital:
            print(get_score_list(length_capital))
            #is_repeating()
    else:
        bad_letter(dash_capital, guesses)
        life_counter(capital_country)


def get_score_list(length_capital):
    global start
    global guess
    end = time.time()
    game_time = end - start
    date = time.strftime("%Y-%m-%d-%H:%M")
    print(bcolors.OKGREEN, "Winner!! Bonus time -5 seconds! You guessed after ", guess, " letters. It took you: ", "%.2f" %(game_time), "second", bcolors.ENDC )
    name = input("What is your name? ")
    scorelist=(name, game_time, length_capital, date)
    return scorelist


def check_letter(length_capital, dash_capital, guesses):
    '''If letter is in capital, change proper dash to this letter'''
    global error_list
    for x in range(len(length_capital)):           # index litery i wstawienie jej na odpowiednią kreskę
        if guesses == length_capital[x]:
            dash_capital.pop(x)
            dash_capital.insert(x, guesses)
    print("Life: ", life)
    print(" ".join(dash_capital))
    print("List of bad answers ", error_list)


def bad_word(dashes, get_string_from_user):
    '''User write incorrect word and lose 2 life '''
    global life
    life -= 2
    print("Life: ", life)
    bad_answers(dashes, get_string_from_user)


def bad_letter(dashes, get_string_from_user):
    '''User write incorrect letter and lose 1 life '''
    global life
    life -= 1
    print("Life: ", life)
    bad_answers(dashes, get_string_from_user)


def bad_answers(dash_capital, guesses):
    global error_list
    ''' Incorrect user's answers are add to error_list'''
    print(" ".join(dash_capital))
    error_list += [guesses]
    print("List of bad answers ", error_list)


def life_counter(capital_country):                             # Brakuje zmiennych contry i capital
    '''Different drawings depending on life'''
    global life
    if life == 5:
        print(draw_1())
    elif life == 4:
        print(draw_2())
    elif life == 3:
        print(draw_3())
    elif life == 2:
        print(draw_4())
    elif life == 1:
        print(draw_5())                            # wskazówka
        print("Hint! The capital of", get_country(capital_country))
    elif life < 1:
        print(draw_6())                            # przegrana
        print(bcolors.FAIL, "Game over!! Good answer is ", capital_country[1], bcolors.ENDC)
        #is_repeating()


def scorelist(name, game_time, capital, date):
    '''Create scorelist and ranking list '''
    scorelist = [name, "|", str("%.2f" % (game_time)), "|", str(capital), "|",  str(date), "\n"]

    plik = open('highscore.txt', 'a')           # działania na pliku (utworzenie nowego, zapis str z danymi)
    plik = open('highscore.txt').read()
    plik = open('highscore.txt', 'a')
    plik.writelines(scorelist)
    plik.close()

    plik = open('highscore.txt').read()         # działania na pliku (otworzenie zapisów)
    plik2 = plik.split("\n")
    plik2.pop()
    data1 = []
    for x in range(len(plik2)):
        plik3 = plik2[x].split()
        plik4 = plik3[0].split("|")
        data1.append(plik4)

    not_sorted = True                           # sortowanie wg game_time - indeks [1] na scorelist
    while not_sorted:
        not_sorted = False
        for i in range(0, len(data1) - 1):
            if float(data1[i][1]) > float(data1[i+1][1]):
                abc = data1[i]
                data1[i] = data1[i+1]
                data1[i+1] = abc
                not_sorted = True
    print(data1)


def draw_1():
    return("""
            +---+
            |   |
            0   |
                |
                |
                |
            =======
            """)


def draw_2():
    return("""
            +---+
            |   |
            0   |
           /    |
                |
                |
            =======
            """)


def draw_3():
    return("""
            +---+
            |   |
            0   |
           /|   |
                |
                |
            =======
            """)


def draw_4():
    return("""
            +---+
            |   |
            0   |
           /|\  |
                |
                |
            =======
            """)


def draw_5():
    return("""
            +---+
            |   |
            0   |
           /|\  |
           /    |
                |
            =======
            """)


def draw_6():
    return("""
            +---+
            |   |
            0   |
           /|\  |
           / \  |
                |
            =======
            """)

def main():
    ''' Operation of the entire program '''
    while True:
        global life
        global guess
        life = 6
        error_list=[]
        guess = 0
        print("Guess: ", guess)
        print("Life: ", life, "\n")
        reading_data = open_file()          # otwiera i zczytuje plik
        capital_country = choice_random_capital(reading_data)           # losuje randomowa stolice
        capital = split_word(capital_country)
        dashes = dash(capital)                # zamienia wylosowana stolice na _
        while True:
            get_string_from_user = guessed()
            check_length(get_string_from_user, capital, dashes, capital_country)
            if list(get_string_from_user) == capital or "_" not in dashes:
                is_repeating()
                break
            elif life<1:
                is_repeating()
                break


main()