en = {
    'greeting':             "Mods updater v%v% by SStive39",
    'path.wrong':           "Wrong path: %path%",
    'path.enter':           "Please enter right path:",
    'step.scan':            "Scanning mods on client... ",
    'step.upd.check':       "Checking for updates... ",
    'step.upd.download':    "Downloading updates... ",
    'ok':                   "Ok",
    'done':                 "Done!"
}


def p(key, **vals):
    phrase = en[key]
    for k, v in vals.items():
        phrase = phrase.replace(f"%{k}%", v)

    if key.split('.')[0] in ['step']:
        print(phrase, end='')
    else:
        print(phrase + '\n')
