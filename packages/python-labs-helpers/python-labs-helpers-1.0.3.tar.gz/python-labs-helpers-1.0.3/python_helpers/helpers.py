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


def input_string(text: str, *additional_conditions) -> str:
    return cycled_input(text, str, lambda v: len(v) > 0, *additional_conditions)


def natural_only(v: int) -> bool:
    return v > 0


def input_int(text: str, *additional_conditions) -> int:
    return cycled_input(text, int, *additional_conditions)


def input_float(text: str, *additional_conditions) -> float:
    return cycled_input(text, float, *additional_conditions)


def cycled(func, text="Do you want to continue"):
    def wrapper():
        while True:
            func()
            c = cycled_input("{}?(y\\n)? ".format(text), str, lambda v: v is 'y' or v is 'n')
            if c is 'n':
                break
    return wrapper
