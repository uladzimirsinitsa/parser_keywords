
import nltk
from nltk import word_tokenize

nltk.download('punkt')


def tokenizer(words: str) -> list:
    marks = '''!()-—»«[]{};?@#$%:'"\\,./^&amp;*_'''
    data = word_tokenize(words, language='russian')
    return [item.lower() for item in data if item not in marks]


def processing_keywords(keywords: list) -> list:
    output_keywords = []
    for word in keywords:
        lenght = len(tokenizer(word))
        if lenght == 0:
            continue
        if lenght == 1:
            output_keywords.append(word)
        if lenght > 1:
            output_keywords.extend(tokenizer(word))
            output_keywords.append(word)
    return list(set(output_keywords))


def get_keyword_frequency(keywords: list, text: str, letters_and_marks: int, word_fd: dict):

    frequency = []
    for word in keywords:
        lenght = len(tokenizer(word))
        if lenght == 0:
            continue
        elif lenght == 1:
            if word_fd.get(word):
                frequency.append(word_fd.get(word))
            else:
                frequency.append(0)
        else:
            score = text.count(word)
            if score == 0:
                frequency.append(0)
            else:
                frequency.append(score)
    return frequency, letters_and_marks


def counting_letters_and_marks(text: str) -> int:
    text_ = text.replace(' ', '')
    temp = []
    marks = '''!()-—»«[]{};?@#$%:'"\\,./^&amp;*_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'''
    return sum(item not in marks for item in text)


def clear_extra_spaces_invisible_characters(text: str) -> str:
    text = text.replace("\n", " ").replace("\t", " ")
    text = text.lower()
    while "  " in text:
        text = text.replace("  ", " ")
    return text


def get_frequency_matrix(frequency_data: list):
    frequency_matrix = []
    for i, item in enumerate(frequency_data[0]):
        item_ = [item]
        item_.extend(j[i] for j in frequency_data[1:])
        frequency_matrix.append(item_)
    return frequency_matrix


def get_table_2_matrix(target_urls: list, letters_and_marks_data: list):
    table_2 = list(target_urls)
    table_2.append("Ваша страница")
    table_2_matrix = []

    for i, item in enumerate(table_2):
        item_ = [item, letters_and_marks_data[i]]
        table_2_matrix.append(item_)
    return table_2_matrix
