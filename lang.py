en = {
    'greeting':             "Mods updater v%v% by SStive39",
    'path.wrong':           "Cant find minecraft in: %path%",
    'path.enter':           "Please enter right path:",
    'step.scan':            "Scanning mods on client",
    'step.upd.get':         "Updating",
    'step.upd.delete':      "Deleting old mods",
    'ok':                   "Ok",
    'done':                 "Done!",
    'error.server':         "Server error! Please check internet connection or contact with developer.",
    'error.download'        "Downloading error! Please make sure that path %path% is writeable or run script as administrator."
    'os.unsupported':       "Sorry, your os is not supported"
}

rus = {
    'greeting':             "Mods updater v%v% by SStive39",
    'path.wrong':           "Не удается найти Minecraft в папке: %path%",
    'path.enter':           "Пожалуйста, введите путь к папке .minecraft:",
    'step.scan':            "Сканирование установленных модов",
    'step.upd.get':         "Обновление модов",
    'step.upd.delete':      "Удаление старых версий модов",
    'ok':                   "Ок",
    'done':                 "Готово!",
    'error.server':         "Ошибка сервера! Пожалуйста, проверьте интернет соединение или свяжитесь с разработчиком.",
    'error.download'        "Ошибка скачивания! Убедитесь что путь %path% Доступен для записи или запустите программу от имени администратора."
    'os.unsupported':       "К сожалению, эта программа не работает на вашей операционной системе :("
}


def p(key, **vals):
    phrase = get(key, **vals)

    if key.split('.')[0] in ['step']:
        print(phrase, end='... ')
    else:
        print(phrase + '\n')


def get(key, **values):
    phrase = rus[key]
    for k, v in values.items():
        phrase = phrase.replace(f"%{k}%", v)
    return phrase
