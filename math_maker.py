import random


def addition():
    a = random.randint(1, 100)
    b = random.randint(1, 100)
    question = "{} + {}=?".format(a, b)
    return [a + b, question]


def subtraction():
    a = random.randint(1, 100)
    b = random.randint(1, 100)
    question = "{} - {}=?".format(a, b)
    return [a - b, question]


def mult():
    a = random.randint(1, 100)
    b = random.randint(1, 100)
    question = "{} * {}=?".format(a, b)
    return [a * b, question]


def division():
    a = random.randint(1, 100)
    b = random.randint(1, 100)
    question = "{} / {}=?".format(a, b)
    return [round(a / b, 2), question]


if __name__ == "__main__":
    l = [addition(), subtraction(), mult(), division()]
    for func in l:
        print(func[1] + " answer: " + str(func[0]))
