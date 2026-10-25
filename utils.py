# Вспомогательные функции — общие утилиты для всех модулей
# Не зависят от бизнес-логики, используются везде

from datetime import datetime


def formatirovat_datu(data_str, format_vhod="%Y-%m-%d %H:%M", format_vyhod="%d.%m.%Y %H:%M"):
    # конвертируем формат даты для отображения
    try:
        data = datetime.strptime(data_str, format_vhod)
        return data.strftime(format_vyhod)
    except ValueError:
        return data_str


def urezat_tekst(tekst, maks_dlina=50):
    # обрезаем длинный текст и добавляем многоточие
    if len(tekst) <= maks_dlina:
        return tekst
    return tekst[:maks_dlina - 3] + "..."


def pluralizovat(chislo, odin, dva, pyat):
    # правильное склонение числительных на русском
    # пример: pluralizovat(5, "задача", "задачи", "задач")
    if 11 <= chislo % 100 <= 19:
        return f"{chislo} {pyat}"
    ostatok = chislo % 10
    if ostatok == 1:
        return f"{chislo} {odin}"
    if 2 <= ostatok <= 4:
        return f"{chislo} {dva}"
    return f"{chislo} {pyat}"


def razdelitel(simvol="=", dlina=40):
    # печатаем разделительную линию нужной длины
    print(simvol * dlina)


def tekushaya_data():
    return datetime.now().strftime("%Y-%m-%d %H:%M")