def blue_eq_1(context: str) -> bool:
    return int(context[0]) == 1


def blue_gt_1(context: str) -> bool:
    return int(context[0]) > 1


def blue_lt_3(context: str) -> bool:
    return int(context[0]) < 3


def blue_eq_3(context: str) -> bool:
    return int(context[0]) == 3


def blue_gt_3(context: str) -> bool:
    return int(context[0]) > 3


def yellow_lt_3(context: str) -> bool:
    return int(context[1]) < 3


def yellow_eq_3(context: str) -> bool:
    return int(context[1]) == 3


def yellow_gt_3(context: str) -> bool:
    return int(context[1]) > 3


def yellow_lt_4(context: str) -> bool:
    return int(context[1]) < 4


def yellow_eq_4(context: str) -> bool:
    return int(context[1]) == 4


def yellow_gt_4(context: str) -> bool:
    return int(context[1]) > 4


def blue_is_even(context: str) -> bool:
    return int(context[0]) % 2 == 0


def blue_is_odd(context: str) -> bool:
    return int(context[0]) % 2 == 1


def yellow_is_even(context: str) -> bool:
    return int(context[1]) % 2 == 0


def yellow_is_odd(context: str) -> bool:
    return int(context[1]) % 2 == 1


def purple_is_even(context: str) -> bool:
    return int(context[2]) % 2 == 0


def purple_is_odd(context: str) -> bool:
    return int(context[2]) % 2 == 1


def zero_1s(context: str) -> bool:
    return context.count('1') == 0


def one_1(context: str) -> bool:
    return context.count('1') == 1


def two_1s(context: str) -> bool:
    return context.count('1') == 2


def three_1s(context: str) -> bool:
    return context.count('1') == 3


def zero_3s(context: str) -> bool:
    return context.count('3') == 0


def one_3(context: str) -> bool:
    return context.count('3') == 1


def two_3s(context: str) -> bool:
    return context.count('3') == 2


def three_3s(context: str) -> bool:
    return context.count('3') == 3


def zero_4s(context: str) -> bool:
    return context.count('4') == 0


def one_4(context: str) -> bool:
    return context.count('4') == 1


def two_4s(context: str) -> bool:
    return context.count('4') == 2


def three_4s(context: str) -> bool:
    return context.count('4') == 3


def blue_lt_yellow(context: str) -> bool:
    return int(context[0]) < int(context[1])


def blue_eq_yellow(context: str) -> bool:
    return int(context[0]) == int(context[1])


def blue_gt_yellow(context: str) -> bool:
    return int(context[0]) > int(context[1])


def blue_lt_purple(context: str) -> bool:
    return int(context[0]) < int(context[2])


def blue_eq_purple(context: str) -> bool:
    return int(context[0]) == int(context[2])


def blue_gt_purple(context: str) -> bool:
    return int(context[0]) > int(context[2])


def yellow_lt_purple(context: str) -> bool:
    return int(context[1]) < int(context[2])


def yellow_eq_purple(context: str) -> bool:
    return int(context[1]) == int(context[2])


def yellow_gt_purple(context: str) -> bool:
    return int(context[1]) > int(context[2])


def blue_smallest(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return blue < yellow and blue < purple


def yellow_smallest(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return yellow < blue and yellow < purple


def purple_smallest(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return purple < blue and purple < yellow


def blue_largest(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return blue > yellow and blue > purple


def yellow_largest(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return yellow > blue and yellow > purple


def purple_largest(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return purple > blue and purple > yellow


def even_odd_of_num(context: str) -> tuple[int, int]:
    even_num = 0
    odd_num = 0
    for num in context:
        if int(num) % 2 == 0:
            even_num += 1
        else:
            odd_num += 1
    return even_num, odd_num


def more_even_numbers(context: str) -> bool:
    even_num, odd_num = even_odd_of_num(context)
    return even_num > odd_num


def more_odd_numbers(context: str) -> bool:
    even_num, odd_num = even_odd_of_num(context)
    return even_num < odd_num


def zero_even_numbers(context: str) -> bool:
    even_num, odd_num = even_odd_of_num(context)
    return even_num == 0


def one_even_number(context: str) -> bool:
    even_num, odd_num = even_odd_of_num(context)
    return even_num == 1


def two_even_numbers(context: str) -> bool:
    even_num, odd_num = even_odd_of_num(context)
    return even_num == 2


def three_even_numbers(context: str) -> bool:
    even_num, odd_num = even_odd_of_num(context)
    return even_num == 3


def sum_is_even(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return (blue + yellow + purple) % 2 == 0


def sum_is_odd(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return (blue + yellow + purple) % 2 == 1


def blue_yellow_sum_lt_6(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return (blue + yellow) < 6


def blue_yellow_sum_eq_6(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return (blue + yellow) == 6


def blue_yellow_sum_gt_6(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return (blue + yellow) > 6


def triple_number(context: str) -> bool:
    return len(set(context)) == 1


def double_number(context: str) -> bool:
    return len(set(context)) == 2


def no_repetition(context: str) -> bool:
    return len(set(context)) == 3


def no_pairs(context: str) -> bool:
    return len(set(context)) != 2


def has_pair(context: str) -> bool:
    return len(set(context)) == 2


def ascending_order(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return blue < yellow < purple


def descending_order(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return blue > yellow > purple


def no_order(context: str) -> bool:
    return not ascending_order(context) and not descending_order(context)


def sum_lt_6(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return (blue + yellow + purple) < 6


def sum_eq_6(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return (blue + yellow + purple) == 6


def sum_gt_6(context: str) -> int:
    blue, yellow, purple = map(int, context)
    return (blue + yellow + purple) > 6


def three_ascending(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return yellow == blue + 1 and purple == yellow + 1


def two_ascending(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    first_pair_ascends = yellow == blue + 1
    second_pair_ascends = purple == yellow + 1
    return first_pair_ascends != second_pair_ascends

def no_ascending(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return yellow != blue + 1 and purple != yellow + 1


def purple_lt_3(context: str) -> bool:
    return int(context[2]) < 3


def blue_lt_4(context: str) -> bool:
    return int(context[0]) < 4


def purple_lt_4(context: str) -> bool:
    return int(context[2]) < 4


def yellow_eq_1(context: str) -> bool:
    return int(context[1]) == 1


def purple_eq_1(context: str) -> bool:
    return int(context[2]) == 1


def purple_eq_3(context: str) -> bool:
    return int(context[2]) == 3


def blue_eq_4(context: str) -> bool:
    return int(context[0]) == 4


def purple_eq_4(context: str) -> bool:
    return int(context[2]) == 4


def yellow_gt_1(context: str) -> bool:
    return int(context[1]) > 1


def purple_gt_1(context: str) -> bool:
    return int(context[2]) > 1


def purple_gt_3(context: str) -> bool:
    return int(context[2]) > 3


def blue_smallest_or_tie(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return blue <= yellow and blue <= purple


def yellow_smallest_or_tie(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return yellow <= blue and yellow <= purple


def purple_smallest_or_tie(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return purple <= blue and purple <= yellow


def blue_largest_or_tie(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return blue >= yellow and blue >= purple


def yellow_largest_or_tie(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return yellow >= blue and yellow >= purple


def purple_largest_or_tie(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return purple >= blue and purple >= yellow


def sum_multiple_of_3(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return (blue + yellow + purple) % 3 == 0


def sum_multiple_of_4(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return (blue + yellow + purple) % 4 == 0


def sum_multiple_of_5(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return (blue + yellow + purple) % 5 == 0


def blue_yellow_sum_eq_4(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return (blue + yellow) == 4


def blue_purple_sum_eq_4(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return (blue + purple) == 4


def yellow_purple_sum_eq_4(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return (yellow + purple) == 4


def blue_purple_sum_eq_6(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return (blue + purple) == 6


def yellow_purple_sum_eq_6(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return (yellow + purple) == 6


def blue_gt_4(context: str) -> bool:
    return int(context[0]) > 4


def purple_gt_4(context: str) -> bool:
    return int(context[2]) > 4


def yellow_lt_blue(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return yellow < blue


def yellow_eq_blue(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return yellow == blue

def yellow_gt_blue(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    return yellow > blue

def three_in_sequence_in_ascending_or_descending(context: str) -> bool:
    blue, yellow, purple = map(int, context)
    diff1 = yellow - blue
    diff2 = purple - yellow
    return diff1 == diff2 and abs(diff1) == 1

def two_in_sequence_in_ascending_or_descending(context: str) -> bool:
    if three_in_sequence_in_ascending_or_descending(context):
        return False
    blue, yellow, purple = map(int, context)
    return abs(yellow - blue) == 1 or abs(purple - yellow) == 1

def no_sequence_in_ascending_or_descending(context: str) -> bool:
    return not two_in_sequence_in_ascending_or_descending(context) and not three_in_sequence_in_ascending_or_descending(context)

