import string
import random

from jkg_evaluators.core import CasePerformance, EvalCase, CompleteEvaluation

from typing import Callable


class IndexWithMostALetters(EvalCase):
    performance_bigger_better = True

    def __init__(self,
                 list_of_words: list):

        self.list_of_words = list_of_words
        self.n = len(list_of_words)

    def _evaluate(self, solution: Callable) -> CasePerformance:

        true_solution = -1
        top_num_as = 0
        for idx, word in enumerate(self.list_of_words):
            act = sum([l.lower() == 'a' for l in word])
            if act > top_num_as:
                true_solution = idx
                top_num_as = act

        out = solution(self.list_of_words)

        is_success = (out == true_solution)

        return CasePerformance(
            is_successful=is_success,
            performance=int(is_success)
        )


class LetterOccurrences(EvalCase):
    performance_bigger_better = True

    def __init__(self,
                 list_of_words: list,
                 letter: str):

        self.list_of_words = list_of_words
        self.letter = letter

    def _evaluate(self, solution: Callable) -> CasePerformance:

        true_solution = 0
        for word in self.list_of_words:
            if self.letter.lower() in word.lower():
                true_solution += 1

        out = solution(self.list_of_words,
                       self.letter)

        is_success = (out == true_solution)

        return CasePerformance(
            is_successful=is_success,
            performance=int(is_success)
        )


class WordWithMostOfLetter(EvalCase):
    performance_bigger_better = True

    def __init__(self,
                 list_of_words: list,
                 letter: str):

        self.list_of_words = list_of_words
        self.letter = letter

    def _evaluate(self, solution: Callable) -> CasePerformance:

        true_solution = ''
        max_num = 0
        for word in self.list_of_words:
            letter_count = sum([l == self.letter.lower()
                                for l in word])
            if letter_count > max_num:
                max_num = letter_count
                true_solution = word

        out = solution(self.list_of_words,
                       self.letter)

        is_success = (out == true_solution)

        return CasePerformance(
            is_successful=is_success,
            performance=int(is_success)
        )


class LargestMultiple(EvalCase):
    performance_bigger_better = True

    def __init__(self,
                 list_of_numbers: list):

        self.list_of_numbers = list_of_numbers

    def _evaluate(self, solution: Callable) -> CasePerformance:

        sorted_nums = sorted(self.list_of_numbers)

        out = solution(self.list_of_numbers)

        bot_multi = sorted_nums[-1] * sorted_nums[-2]
        top_multi = sorted_nums[0] * sorted_nums[1]

        if bot_multi > top_multi:
            true_solution = bot_multi
        else:
            true_solution = top_multi

        is_success = (out == true_solution)

        return CasePerformance(
            is_successful=is_success,
            performance=int(is_success)
        )


class SumOfDistinctOddPosInts(EvalCase):
    performance_bigger_better = True

    def __init__(self,
                 list_of_numbers: list):

        self.list_of_numbers = list_of_numbers

    def _evaluate(self, solution: Callable) -> CasePerformance:

        true_solution = 0
        for x in set(self.list_of_numbers):
            if ((x % 2) != 0) and (x > 0):
                true_solution += x

        out = solution(self.list_of_numbers)

        is_success = (out == true_solution)

        return CasePerformance(
            is_successful=is_success,
            performance=int(is_success)
        )


class LargestAscending(EvalCase):
    performance_bigger_better = True

    def __init__(self,
                 list_of_numbers: list):

        self.list_of_numbers = list_of_numbers

    def _evaluate(self, solution: Callable) -> CasePerformance:

        def check_sorted(num):
            sl = sorted(str(abs(num)))
            return ''.join(sl) == str(abs(num))

        filtered = [x for x in self.list_of_numbers if check_sorted(x)]

        try:
            true_solution = max(filtered)
        except ValueError:
            true_solution = 0

        out = solution(self.list_of_numbers)

        is_success = (out == true_solution)

        return CasePerformance(
            is_successful=is_success,
            performance=int(is_success)
        )


class SmallestWhereDoubleAlso(EvalCase):
    performance_bigger_better = True

    def __init__(self,
                 list_of_numbers: list):

        self.list_of_numbers = list_of_numbers

    def _evaluate(self, solution: Callable) -> CasePerformance:

        filtered = [x for x in self.list_of_numbers
                    if ((x * 2) in self.list_of_numbers)]

        try:
            true_solution = min(filtered)
        except ValueError:
            true_solution = 0

        out = solution(self.list_of_numbers)

        is_success = (out == true_solution)

        return CasePerformance(
            is_successful=is_success,
            performance=int(is_success)
        )


class LargestEvenDivided(EvalCase):
    performance_bigger_better = True

    def __init__(self,
                 list_of_numbers: list,
                 number: int):

        self.list_of_numbers = list_of_numbers
        self.number = number

    def _evaluate(self, solution: Callable) -> CasePerformance:

        true_solution = None

        for n in self.list_of_numbers:
            if (n / self.number) % 2 == 0:
                if true_solution is None:
                    true_solution = n
                elif n > true_solution:
                    true_solution = n

        if true_solution is None:
            true_solution = 0

        out = solution(self.list_of_numbers,
                       self.number)

        is_success = (out == true_solution)

        return CasePerformance(
            is_successful=is_success,
            performance=int(is_success)
        )


class LastWithThreeMultDiff(EvalCase):
    performance_bigger_better = True

    def __init__(self,
                 list_of_numbers: list,
                 number: int):

        self.list_of_numbers = list_of_numbers
        self.number = number

    def _evaluate(self, solution: Callable) -> CasePerformance:

        true_solution = 0

        for n in self.list_of_numbers:
            if (n - self.number) % 3 == 0:
                true_solution = n

        out = solution(self.list_of_numbers,
                       self.number)

        is_success = (out == true_solution)

        return CasePerformance(
            is_successful=is_success,
            performance=int(is_success)
        )


word_lists = [
    {'list_of_words': ['b', 'bb', 'bbb']},
    {'list_of_words': ['aa', 'aaa', 'aa', 'a']},
    {'list_of_words': ['ba', 'babab', 'AaAaA', 'Ahha']},
    {'list_of_words': ['123', 'lala', '', '', '', 'aA']}
]

num_lists = [
    {'list_of_numbers': [0, 1, 2, 3, 4]},
    {'list_of_numbers': [0, 0, 10, 3, 10]},
    {'list_of_numbers': [-20, -40, 0, 1, 2, 3, 40]},
    {'list_of_numbers': [-1100, 100, 20]},
    {'list_of_numbers': [0, 1]},
    {'list_of_numbers': [21, 120, 220]},
]

random.seed(42)
for _r in range(10, 501):
    word_lists.append(
        {'list_of_words': [''.join(random.choices(string.ascii_letters + string.digits,
                                                  k=random.randint(0, 120)))
                           for _ in range(_r)]}
    )

    num_lists.append(
        {'list_of_numbers': [random.randint(-1000, 1000)
                             for _ in range(_r)]}
    )

words_with_letter = [{'letter': random.choice(string.ascii_letters),
                      **kwargs}
                     for kwargs in word_lists]

numberlists_with_numebrs = [{'number': random.randint(1, 10),
                             **kwargs}
                            for kwargs in num_lists]

string_with_most_a_letters = CompleteEvaluation(
    case_kwarg_list=word_lists,
    case=IndexWithMostALetters
)

letter_occurrences = CompleteEvaluation(
    case_kwarg_list=words_with_letter,
    case=LetterOccurrences
)

word_with_most_of_letters = CompleteEvaluation(
    case_kwarg_list=words_with_letter,
    case=WordWithMostOfLetter
)

largest_multiple = CompleteEvaluation(
    case_kwarg_list=num_lists,
    case=LargestMultiple
)

sum_odd_positives = CompleteEvaluation(
    case_kwarg_list=num_lists,
    case=SumOfDistinctOddPosInts
)

largest_ascending_num = CompleteEvaluation(
    case_kwarg_list=num_lists,
    case=LargestAscending
)

smallest_where_double_also = CompleteEvaluation(
    case_kwarg_list=num_lists,
    case=SmallestWhereDoubleAlso
)

largest_even_divided = CompleteEvaluation(
    case_kwarg_list=numberlists_with_numebrs,
    case=LargestEvenDivided
)

last_with_three_multiple_difference = CompleteEvaluation(
    case_kwarg_list=numberlists_with_numebrs,
    case=LastWithThreeMultDiff
)
