

from statistics import mean
from copy import deepcopy
from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from nltk import FreqDist

from headless_browser import get_text_from_url
from data_processing import tokenizer
from data_processing import processing_keywords
from data_processing import get_keyword_frequency
from data_processing import clear_extra_spaces_invisible_characters
from data_processing import counting_letters_and_marks
from data_processing import get_frequency_matrix
from data_processing import get_table_2_matrix
from create_txt_file import create_file

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


class Data(BaseModel):
    keywords: list
    urls: list
    own_page: list


@app.get("/")
def root():
    return FileResponse("templates/index.html")


@app.post("/table")
def postdata(request: Request, keywords: list = Form(), urls: list = Form(), own_page: list = Form()):
    keywords = keywords[0].split('\r\n')
    processed_keywords = processing_keywords(keywords)

    urls = urls[0].split('\r\n')
    target_urls = deepcopy(urls)
    if '' not in own_page:
        urls.extend(own_page)

    letters_and_marks_data = []
    frequency_data = []
    for url in urls:
        text = get_text_from_url(url)
        text = clear_extra_spaces_invisible_characters(text)
        letters_and_marks = counting_letters_and_marks(text)
        tokenized_text_words = tokenizer(text)

        frequency_data.append(get_keyword_frequency(
            processed_keywords,
            text,
            letters_and_marks,
            FreqDist(tokenized_text_words))[0])

        letters_and_marks_data.append(get_keyword_frequency(
            processed_keywords,
            text,
            letters_and_marks,
            FreqDist(tokenized_text_words))[1])

    if '' in own_page:
        frequency_data.append(['-' for _ in range(len(processed_keywords))])
        letters_and_marks_data.append('-')

    frequency_matrix = get_frequency_matrix(frequency_data)

    data = [[word, *frequency_matrix[i], min(frequency_matrix[i][:-1]), max(frequency_matrix[i][:-1]), int(mean(frequency_matrix[i][:-1])),] for i, word in enumerate(processed_keywords)]

    table_2_matrix = get_table_2_matrix(target_urls, letters_and_marks_data)

    min_letters = min(letters_and_marks_data[:-1])
    max_letters = max(letters_and_marks_data[:-1])
    mean_letters = int(mean(letters_and_marks_data[:-1]))

    data = sorted(data, key=lambda x:(len(x[0])), reverse=True)
    text = create_file(urls, data, [min_letters, max_letters, mean_letters])

    temp = [i for i in data if sum(i[1:-4]) != 0]
    data = sorted(temp, key=lambda x:(len(x[0])), reverse=True)
    return templates.TemplateResponse(
        "table.html",
        {
            "request": request,
            "urls": urls,
            "target_urls": target_urls,
            "data": data,
            "letters_and_marks_data": letters_and_marks_data,
            "table_2_matrix": table_2_matrix,
            "min_letters": min_letters,
            "max_letters": max_letters,
            "mean_letters": mean_letters,
            "text": text,
            "keyword_1": data[0][0]
        })
