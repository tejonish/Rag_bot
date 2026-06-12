# modules/fillers.py

def count_fillers(text):

    fillers = [
        "um",
        "uh",
        "umm",
        "uhh",
        "like",
        "actually",
        "basically",
        "you know",
        "sort of",
        "kind of"
    ]

    text = text.lower()

    count = 0

    found = []

    for filler in fillers:

        c = text.count(filler)

        if c > 0:
            found.append(filler)

        count += c

    return count, found