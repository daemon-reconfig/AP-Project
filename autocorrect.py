import os
from collections import defaultdict

class AutoCorrect:
    def __init__(self, dictionary_filename: str) -> None:
        self.dictionary_filename = dictionary_filename
        self.dictionary = self.load_dictionary()

    def load_dictionary(self) -> set:
        if not os.path.exists(self.dictionary_filename):
            raise FileNotFoundError(f"{self.dictionary_filename} not found")
        with open(self.dictionary_filename, 'r') as f:
            return set(word.strip().lower() for word in f)

    def set_word(self, wrong_word: str) -> None:
        self.wrong_word = wrong_word.lower()

    def check_spelling(self) -> bool:
        return self.wrong_word in self.dictionary

    def check_letter_arrangement(self) -> bool:
        found = False
        suggestions = []
        sorted_wrong_word = ''.join(sorted(self.wrong_word))
        for word in self.dictionary:
            if len(word) == len(self.wrong_word) and ''.join(sorted(word)) == sorted_wrong_word:
                suggestions.append(word)
                found = True
        self.print_suggestions("*** Incorrect Arrangement ***", suggestions)
        return found

    def check_exchanged_letters(self, exchanged: int = 1) -> bool:
        return self.check_differing_letters(exchanged, "Exchanged")

    def check_missing_letters(self, missing: int = 1) -> bool:
        return self.check_differing_letters(missing, "Missing", missing=True)

    def check_extra_letters(self, extra: int = 1) -> bool:
        return self.check_differing_letters(extra, "Extra", extra=True)

    def check_missing_and_extra_letters(self, missing: int = 1, extra: int = 1) -> bool:
        found = False
        suggestions = []
        for word in self.dictionary:
            if abs(len(word) - len(self.wrong_word)) == missing - extra:
                if self.check_letters_difference(word, self.wrong_word, missing, extra):
                    suggestions.append(word)
                    found = True
        self.print_suggestions(f"*** {missing} Missing, {extra} Extra Characters ***", suggestions)
        return found

    def check_letters_difference(self, word1: str, word2: str, missing: int = 0, extra: int = 0) -> bool:
        missing_count, extra_count = 0, 0
        iter1, iter2 = iter(word1), iter(word2)
        char1, char2 = next(iter1, None), next(iter2, None)
        while char1 is not None and char2 is not None:
            if char1 == char2:
                char1, char2 = next(iter1, None), next(iter2, None)
            elif missing > 0 and (extra_count == 0 or extra_count > missing_count):
                char1 = next(iter1, None)
                missing_count += 1
            else:
                char2 = next(iter2, None)
                extra_count += 1
        missing_count += sum(1 for _ in iter1)
        extra_count += sum(1 for _ in iter2)
        return missing_count == missing and extra_count == extra

    def check_differing_letters(self, differing: int, label: str, missing: bool = False, extra: bool = False) -> bool:
        found = False
        suggestions = []
        for word in self.dictionary:
            if len(word) == len(self.wrong_word):
                diff_count = sum(1 for a, b in zip(word, self.wrong_word) if a != b)
                if diff_count == differing:
                    suggestions.append(word)
                    found = True
        self.print_suggestions(f"*** {label} Character{'s' if differing > 1 else ''} ***", suggestions)
        return found

    def print_suggestions(self, label: str, suggestions: list) -> None:
        if suggestions:
            print(f"{label}\t:\t{', '.join(suggestions)}\t({len(suggestions)})")
        else:
            print(f"{label}\t:\tNo suggestions found")

    @staticmethod
    def sort_dictionary(unsorted_dictionary_filename: str, sorted_dictionary_filename: str) -> None:
        with open(unsorted_dictionary_filename, 'r') as f:
            words = sorted(set(word.strip().lower() for word in f))
        with open(sorted_dictionary_filename, 'w') as f:
            for word in words:
                f.write(word + '\n')
