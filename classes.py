from itertools import permutations
import random
from datetime import date
import json

p_clicked = False


def set_p_status(x):
    global p_clicked
    p_clicked = x


class SakClass:
    def __init__(self):

        self.letters = {'Α': [12, 1], 'Β': [1, 8], 'Γ': [2, 4], 'Δ': [2, 4], 'Ε': [8, 1],
                        'Ζ': [1, 10], 'Η': [7, 1], 'Θ': [1, 10], 'Ι': [8, 1], 'Κ': [4, 2],
                        'Λ': [3, 3], 'Μ': [3, 3], 'Ν': [6, 1], 'Ξ': [1, 10], 'Ο': [9, 1],
                        'Π': [4, 2], 'Ρ': [5, 2], 'Σ': [7, 1], 'Τ': [8, 1], 'Υ': [4, 2],
                        'Φ': [1, 8], 'Χ': [1, 8], 'Ψ': [1, 10], 'Ω': [3, 3]
                        }

        self.all = []

        for i in self.letters:
            numberOfLetters = self.letters.get(i)[0]

            for j in range(numberOfLetters):
                self.all.append(i)

            self.randomize_sak()

    def randomize_sak(self):
        random.shuffle(self.all)

    def __repr__(self):
        return f'Class: {self.__class__}, letters = {self.letters}'

    def getletters(self, n):
        returnableLetters = []

        if n > len(self.all):
            return None

        for i in range(n):
            returnableLetters.append(self.all.pop())

        return returnableLetters

    def put_back_letters(self, letters):
        for letter in letters:
            self.all.append(letter)

        self.randomize_sak()


class Player:

    def __init__(self):
        self.score = 0
        self.letters = []

    def __repr__(self):
        return f'Class: {self.__class__}, score = {self.score}, letters = {self.letters}'

    def setLetters(self, addLetters):
        """
        Τα γράμματα του παίκτη εμπλουτίζονται με τα taken_letters
        :param addLetters: εισερχόμενα γράμματα
        """
        self.letters.extend(addLetters)

    def popLetters(self, lettersToPop):
        """
        Αφαίρεί τα given_letters από τα γράμματα του παίκτη
        :param lettersToPop: λίστα γραμμάτων
        """
        for i in range(len(lettersToPop)):
            self.letters.remove(lettersToPop[i])

    def __str__(self):
        """
        Εμφανίζει τα γράμματα του παίχτη.
        """
        result = ""
        for i in self.letters:
            result = result + " " + i + "," + str(WordInspector.letterValue(i)) + " -"
        return result[:len(result) - 2]

    def makesWord(self, word):
        """
        Επιστρέφει true αν ο παίκτης μπορεί να σχηματίσει τη λέξη με τα
        γράμματα που διαθέτει
        :param word: μία λέξη
        :return: αν μπορεί να φτιάξει τη λέξη
        """
        temp = self.letters.copy()
        for i in word:
            if i not in temp:
                return False
            temp.remove(i)
        return True


class Human(Player):
    """
    Αναπαριστά τον User.
    """

    def __init__(self):
        super().__init__()

    def __repr__(self):
        pass

    def play(self, sak):
        """
        Προσομοιώνει τον γύρο παιχνιδιού του User.
        :param sak:
        :return: false αν τελειώσει το παιχνίδη.
        """
        # Εμφάνισε πληροφορίες για τα γράμματα
        print("----------------------------------------------------------")
        print(f"Στο σακουλάκι: {len(sak.all)} γράμματα - Παίζεις:")
        print(f"Διαθέσιμα Γράμματα: {self}")
        print('(Αλλαγή γραμμάτων με: P)')

        word = self.isValid(sak)

        # Αν θέλει να αλλάξει γράμματα
        if word == 'P':
            sak.put_back_letters(self.letters.copy())
            super().popLetters(self.letters.copy())
            super().setLetters(sak.getletters(7))
            print(f"Τα νέα σου γράμματα: {self}")
            set_p_status(True)
            return True

        # Αν θέλει να σταματήσει
        if word == 'Q':
            return False

        super().popLetters(word)
        self.score += WordInspector.wordValue(word)
        print(f'Αποδεκτή Λέξη - Βαθμοί: {str(WordInspector.wordValue(word))} - Σκορ: {str(self.score)}')
        input(f'ENTER για συνέχεια...')
        temp = sak.getletters(7 - len(self.letters))
        # Αν το σακουλάκι άδειασε
        if temp == None:
            return False

        super().setLetters(temp)
        print("----------------------------------------------------------")
        print(f"Διαθέσιμα Γράμματα: {self}")
        return True

    def isValid(self, sak):
        """
        Ελέγχει αν η είσοδος του χρήστη ειναι έγκυρη.
        :param sak: ο σάκος με τα γράμματα.
        :return: P ή Q ή έγκυρη λέξη.
        """
        word = input("Λέξη: ")
        word = word.upper()

        if word == 'P' or word == 'Q':
            return word

        # check if invalid letters
        if len(word) > 7 or not super().makesWord(word):
            print(f'Δε μπορείς να σχηματίσεις αυτή τη λέξη!')
            return self.isValid(sak)

        # check if invalid word
        if not WordInspector.isValidWord(word):
            print(f'Δεν υπάρχει αυτή η λέξη!')
            return self.isValid(sak)

        return word


class Computer(Player):
    """
    Αναπαριστά τον Η/Π.
    """

    def __init__(self, mode='1'):
        super().__init__()
        self.mode = mode

    def __repr__(self):
        pass

    def play(self, sak):
        """
        Προσομοιώνει τον γύρο παιχνιδιού του Η/Π.
        :param sak:
        :return: false αν τελειώσει το παιχνίδη.
        """
        # Εμφάνισε πληροφορίες για τα γράμματα
        print("----------------------------------------------------------")
        print(f"Στο σακουλάκι: {len(sak.all)} γραμματα - Παίζει ο Η/Υ:")
        print(f"Γράμματα Η/Υ: {self}")

        # Φτιάχνει τη λέξη με βάση τον αλγόριθμο.
        word = ""
        if self.mode == '1':
            word = self.min()
        elif self.mode == '2':
            word = self.max()
        elif self.mode == '3':
            word = self.smart()
        elif self.mode == '4':
            word = self.fail()

        # Αν ο υπολογιστής δε μπορεί να σχηματίσει λέξη
        if word == None:
            return False

        super().popLetters(word)
        self.score += WordInspector.wordValue(word)
        print(f'Λέξη: {word}, Βαθμοί: {str(WordInspector.wordValue(word))} - Σκορ H/Y: {str(self.score)}')
        temp = sak.getletters(7 - len(self.letters))
        # Αν το σακουλάκι άδειασε
        if temp is None:
            return False

        super().setLetters(temp)
        return True

    def min(self):
        """
        Γυρνάει τη πρώτη λέξη με τα λιγότερα γράμματα
        :return:
        """
        for i in range(2, len(self.letters) + 1):
            perms = [''.join(p) for p in permutations(self.letters, i)]
            for per in perms:
                if WordInspector.isValidWord(per):
                    return per
        return None

    def max(self):
        """
        Γυρνάει τη πρώτη λέξη με τα περισσότερα γράμματα
        :return:
        """
        for i in range(len(self.letters), 1, -1):
            perms = [''.join(p) for p in permutations(self.letters, i)]
            for per in perms:
                if WordInspector.isValidWord(per):
                    return per
        return None

    def validCombos(self):
        """
        Γυρνάει όλες τις αποδεκτές λέξεις
        :return:
        """
        valid_combos = []
        for i in range(2, len(self.letters)):
            perms = [''.join(p) for p in permutations(self.letters, i)]
            for per in perms:
                if WordInspector.isValidWord(per):
                    valid_combos.append(per)

        if len(valid_combos) == 0:
            return None
        return valid_combos

    def smart(self):
        """
        Γυρνάει τη καλύτερη λέξη
        :return:
        """
        validCombinations = self.validCombos()
        if not validCombinations:
            return None

        maximizedWord = validCombinations[0]
        maxScoreValue = WordInspector.wordValue(maximizedWord)
        for combination in validCombinations:
            if maxScoreValue < WordInspector.wordValue(combination):
                maximizedWord = combination
                maxScoreValue = WordInspector.wordValue(combination)

        return maximizedWord

    def fail(self):
        """
        Γυρνάει τη δεύτερη καλύτερη λέξη
        :return:
        """
        validCombinations = self.validCombos()
        if not validCombinations:
            return None

        maximizedWord = self.smart()
        validCombinations.remove(maximizedWord)
        maximizedWord = validCombinations[0]
        maxScoreValue = WordInspector.wordValue(maximizedWord)
        for combination in validCombinations:
            if maxScoreValue < WordInspector.wordValue(combination):
                maximizedWord = combination
                maxScoreValue = WordInspector.wordValue(combination)

        return maximizedWord


class WordInspector:
    """
    Αναπαριστά ολους τους κανόνες του παιχνιδιού σχετικά με τις λέξεις.
    Αποθηκεύουμε σε λεξικό για να έχουμε πρόσβαση σε Ο(1)
    """
    values = {'Α': 1, 'Β': 8, 'Γ': 4, 'Δ': 4, 'Ε': 1, 'Ζ': 10, 'Η': 1, 'Θ': 10,
              'Ι': 1, 'Κ': 2, 'Λ': 3, 'Μ': 3, 'Ν': 1, 'Ξ': 10, 'Ο': 1, 'Π': 2,
              'Ρ': 2, 'Σ': 1, 'Τ': 1, 'Υ': 2, 'Φ': 8, 'Χ': 8, 'Ψ': 10, 'Ω': 3}

    # Read the greek7.txt
    wordsFile = {}
    try:
        with open('greek7.txt', 'r', encoding="utf-8") as file:
            for line in file.read().splitlines():
                wordsFile[line] = len(line)
    except FileNotFoundError:
        print('Δε βρέθηκε αρχείο με λέξεις! Βye!')
        exit()

    @staticmethod
    def letterValue(letter):
        """
        :param letter: Ένα γράμμα.
        :return: η αξία του.
        """
        return WordInspector.values[letter]

    @staticmethod
    def wordValue(word):
        """
        :param word: μια λέξη.
        :return: η αξία της.
        """
        return sum([WordInspector.values[letter] for letter in word])

    @staticmethod
    def isValidWord(word):
        """
        :param word: μια λέξη.
        :return: true , αν υπάρχει μια τέτοια λέξη.
        """
        return word in WordInspector.wordsFile


class Game:
    def __init__(self):
        self.sak = SakClass()
        self.human = Human()
        self.mode = '1'
        self.computer = Computer(self.mode)
        self.playing = None
        self.history = Game.getHistoryData()
        self.theWinner = None

    def __repr__(self):
        return f'Class: {self.__class__}, algorithm = {self.mode}, playing = {self.playing.__class__}'

    def __str__(self):
        """
        Εμφανίζει την κατάσταση του παιχνιδιού αν τελείωνε την δεδομένη στηγμή.
        """
        if self.theWinner == self.computer:
            return "Νικητής ο Η/Υ με Σκορ: " + str(self.computer.score) + '\n' \
                   + "Σκορ Παίκτη: " + str(self.human.score)
        elif self.theWinner == self.human:
            return "Νικητής ο Παίκτης με Σκορ: " + str(self.human.score) + '\n' \
                   + "Σκορ Η/Υ: " + str(self.computer.score)
        else:
            return "Ισοπαλία" + '\n' \
                   + "Σκορ Η/Υ: " + str(self.computer.score) + '\n' \
                   + "Σκορ Παίκτη: " + str(self.human.score)

    def setup(self):
        """
        Αρχικοποιεί ένα παιχνίδι
        """
        self.sak = SakClass()
        self.human = Human()
        self.computer = Computer(self.mode)
        self.sak.randomize_sak()
        self.init_player(self.human)
        self.init_player(self.computer)
        self.playing = random.choice([self.human, self.computer])
        self.history = Game.getHistoryData()
        self.theWinner = None

    def menu(self):
        """
        Προσομοιώνει το main menu του παιχνιδιού
        Δέχετε τις εισόδους τους χρήστη και ανακατευθεύνει στις επιλογές
        """
        print("##### SCRABBLE #####")
        print("+--------------------+")
        print("1: Σκορ")
        print("2: Ρυθμίσεις")
        print("3: Παιχνίδι")
        print("Q: Έξοδος")
        print("+--------------------+")

        userInput = input("Επιλογή Μενού: ")
        if userInput == '1':
            self.history = Game.getHistoryData()

            if len(self.history) == 0:
                print("Σκορ : Κενό")

            else:
                print("Σκορ :")
                for event in self.history:
                    print(event)
                    print()
            self.menu()

        if userInput == '2':
            self.settings()
            self.menu()

        if userInput == '3':
            self.run()
            self.menu()

        if userInput == 'Q':
            print("---- Έξοδος ----")
            exit()

        print("\n=====[Μη διαθέσιμη επιλογή]=====")
        print(" Διαθέσιμα 1, 2, 3 ή q")
        print("================================\n")
        self.menu()

    def settings(self):
        """
        Προσομοιώνει το menu ρυθμίσεων του παιχνιδιού.
        Ορίζει τον αλγόριθμο με τον οποίο παίζει ο Η/Υ
        """
        if self.mode == '1':
            print(f'Λειτουργία MIN: Ενεργή')
        elif self.mode == '2':
            print(f'Λειτουργία ΜΑΧ: Ενεργή')
        elif self.mode == '3':
            print(f'Λειτουργία SMART: Ενεργή')
        elif self.mode == '4':
            print(f'Λειτουργία SMART-FAIL: Ενεργή')

        print("##### Ρυθμίσεις #####")
        print("+---------------------+")
        print(" 1: MIN")
        print(" 2: MAX")
        print(" 3: SMART")
        print(" 4: SMART-FAIL")
        print("+---------------------+")

        settings_choice = input("Επιλογή Λειτουργίας: ")
        if settings_choice in ['1', '2', '3', '4']:
            self.mode = settings_choice
            if settings_choice == '1':
                print(f'[✅] Λειτουργία MIN: Ενεργή')
            elif settings_choice == '2':
                print(f'[✅] Λειτουργία MAX: Ενεργή')
            elif settings_choice == '3':
                print(f'[✅] Λειτουργία SMART: Ενεργή')
            elif settings_choice == '4':
                print(f'[✅] Λειτουργία SMART-FAIL: Ενεργή')

            return

        print("\n=====[Μη διαθέσιμη επιλογή]=====")
        print(" Διαθέσιμα 1, 2, 3 ή 4")
        print("================================\n")
        self.settings()


    def run(self):
        """
        Προσομειώνει ένα παιχνίδι scrabble
        :return:
        """
        self.setup()

        while True:
            if not self.playing.play(self.sak):
                break

            if self.playing == self.human and p_clicked == False:

                self.playing = self.computer

            elif self.playing == self.human and p_clicked == True:
                self.playing = self.human
                set_p_status(False)
            else:
                self.playing = self.human

        if self.computer.score > self.human.score:
            self.theWinner = self.computer
        elif self.computer.score < self.human.score:
            self.theWinner = self.human

        self.end()

    def end(self):
        """
        Εκτελεί τις ενέργειες τερματισμού του παιχνιδιού
        """
        print(">>>>>>>>>>>[Καλή Συνέχεια]<<<<<<<<<<")
        print("Τερματισμός...\n")
        print(self)

        # Κατασκευάζει το στατιστικό του παιχνιδιού
        # temp = f'{len(self.stats) + 1}. '
        #
        # temp += f'{date.today()} '
        #
        # if self.winner == self.computer:
        #     temp += f'Lose'
        # elif self.winner == self.human:
        #     temp += f'Win'
        # else:
        #     temp += f'Draw'
        #
        # temp += f' Your score: {self.human.score}'

        temp = f'{len(self.history) + 1}. {date.today()} '
        temp += self.__str__()

        # Προσθέτει το στατιστικό στα υπόλοιπα στατιστικά
        self.history.append(temp)
        Game.saverOfHistory(self.history)

    def init_player(self, player):
        player.setLetters(self.sak.getletters(7))

    @staticmethod
    def getHistoryData():
        """
        Διαβάζει τα στατιστικά του παίκτη
        :return: τα στατιστικά
        """
        try:
            with open('history.json', 'r') as f:
                return json.load(f)["history"]
        except FileNotFoundError:
            temp = []
            with open("history.json", 'w') as f:
                json.dump({"history": temp}, f)
            return temp

    @staticmethod
    def saverOfHistory(stats):
        """
        Αποθηκεύει τα στατιστικά του παίκτη στο αρχείο
        """
        try:
            with open('history.json', 'w') as f:
                json.dump({"history": stats}, f)
        except FileNotFoundError:
            print("Παρουσιάστηκε πρόβλημα με το αρχείο.")
