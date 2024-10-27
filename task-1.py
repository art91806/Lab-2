import csv
import json


DATASET_PATH = "books-en.csv"
OUT_PATH = "out.json"

def get_title(dataset):
    dataset.seek(0)
    title = next(dataset)
    title = title.split(";")
    title = [col.strip() for col in title]

    return title

def get_object_alt(line, title):
    reader = csv.DictReader([line], title, delimiter=';', quotechar='"')
    result = next(reader)
    return result


def get_object(line, title):
    fields = []
    value = ""
    in_complex = False

    for char in line:
        if in_complex: 
            value += char

            if char == '"':
                value = value[:-1]
                fields.append(value)
                value = ''
                in_complex = False
        else:
            if char not in (';', '"'):
                value += char
                continue
            
            if char == ';':
                fields.append(value)
                value = ''
                continue
            
            if char == '"':
                in_complex = True
                continue

    result = {col: f for col, f in zip(title, fields)}
    return result


def found_name(dataset, title):
    name = 0

    for line in dataset:
        obj = get_object(line, title)
        name_value = obj["Book-Title"]

        if len(name_value) > 30:
            name += 1

    dataset.seek(0)
    return name


def found_author(dataset, title, author):
    books = []

    for line in dataset:
        obj = get_object(line, title)
        author_value = obj["Book-Author"]
        year_value = obj["Year-Of-Publication"]

        if author_value == author and int(year_value) >= 2000:
            books += [obj]

    dataset.seek(0)

    if len(books) < 1:
        return "Не найдено"
    return books


def filter_year(dataset, title, year):
    filtered = []

    for line in dataset:
        obj = get_object(line, title)
        year_value = obj["Year-Of-Publication"]

        if year_value == str(year):
            filtered += [obj]
        if len(filtered) == 20:
            dataset.seek(0)
            return filtered
            break


if __name__ == "__main__":
    with open(DATASET_PATH, 'r', encoding="utf-8") as dataset:
        title = get_title(dataset)

        found_str30 = found_name(dataset, title)
        print('Задание 1: ',found_str30)
        print('\n')

        print("Введите имя автора:")
        author_name = str(input())
        found_book = found_author(dataset, title, author_name)
        print('Задание 2: ',found_book)

        res = filter_year(dataset, title, 1990)
        print(len(res))

        res = json.dumps(res, indent=4)
        with open(OUT_PATH, "w") as out:
            out.write(res)