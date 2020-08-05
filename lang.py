rus = {
    'greeting': "Mods updater v%v% by SStive39",
    'path.wrong': "Wrong path: %path%",
    'path.enter': "Please enter right path:"
}


def p(key, **vals):
    phrase = rus[key]
    for k, v in vals.items():
        phrase = phrase.replace(f"%{k}%", v)
    print(phrase)
