import re

PATTERNS = {
    int: r"^[-+]?[0-9]+$",
    float: r"[+-]?([0-9]*[.])?[0-9]+",
    str: r".+",
}


def cycled_input(text: str, input_type, *additional_conditions):
    """
    :param text: text to print before user input
    :param input_type: required type
    :param additional_conditions: lambda func that validate user input
    :return:
    """
    if input_type in PATTERNS:
        while True:
            user_input = input(text)
            if bool(re.fullmatch(PATTERNS[input_type], user_input)):
                user_input = input_type(user_input)

                is_valid = True
                for cond in additional_conditions:
                    if callable(cond) and not cond(user_input):
                        is_valid = False
                        break

                if is_valid:
                    return input_type(user_input)
                else:
                    print("input value is not valid.")
            else:
                print("You entered wrong value. Let's try again.")
    else:
        return None


def cycled(func):
    def wrapper():
        while True:
            func()
            c = cycled_input("Do you want to continue?(y\\n)? ", str, lambda v: v is 'y' or v is 'n')
            if c is 'n':
                break
    return wrapper
