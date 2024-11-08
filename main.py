import os
from autocorrect import AutoCorrect

def to_lower_string(word: str) -> str:
    return word.lower()

def main():
    if not os.path.exists("dictionary/words_alpha_sorted.txt"):
        AutoCorrect.sort_dictionary("dictionary/words_alpha.txt", "dictionary/words_alpha_sorted.txt")
    AC = AutoCorrect("dictionary/words_alpha_sorted.txt")
    while True:
        word = input("Enter a word: ")
        AC.set_word(to_lower_string(word))
        if AC.check_spelling():
            print("\nSpelling of the word is correct.\n")
        else:
            print("\nSpelling of the word is wrong. Possible right spellings are given below:\n")
            arranged = AC.check_letter_arrangement()
            exchanged = AC.check_exchanged_letters()
            extra = AC.check_extra_letters()
            extra2 = AC.check_extra_letters(2)
            extra3 = AC.check_extra_letters(3)
            missing = AC.check_missing_letters()
            missing2 = AC.check_missing_letters(2)
            missing3 = AC.check_missing_letters(3)
            MandE = AC.check_missing_and_extra_letters()
            MandE2 = AC.check_missing_and_extra_letters(2)
            MandE3 = AC.check_missing_and_extra_letters(1, 2)
            MandE4 = AC.check_missing_and_extra_letters(2, 2)
            if not (arranged or exchanged or extra or extra2 or extra3 or missing or missing2 or missing3 or MandE or MandE2 or MandE3 or MandE4):
                print("\nNo such word exists.\n")
        print()

if __name__ == "__main__":
    main()
