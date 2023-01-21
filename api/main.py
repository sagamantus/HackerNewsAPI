from typing import Union, Dict, List
from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
import bs4
import uvicorn
import requests

app = FastAPI()


def page_extractor(page: int) -> Dict[str, Union[str, Dict[str, List[str]]]]:
    URL = "https://news.ycombinator.com/"
    r = requests.get(f"{URL}?p={page}")
    soup = BeautifulSoup(r.text, 'html.parser')

    response = {
        "page": str(page),
        "data": []
    }

    i: bs4.element.Tag
    for i in soup.find_all('tr', {'class': "athing"}):
        rank = i.find('span', {'class': 'rank'}).text[:-1]
        titleline = i.find('span', {'class': 'titleline'}).find('a')
        title = titleline.text
        url = titleline['href']
        response['data'].append([rank, title, url])
    return response


@app.get("/")
def root():
    return {"Hacker News API": "API to fetch news from https://news.ycombinator.com/"}


@app.get("/news/")
def hacker_news(page: int = 1):
    if page <= 0:
        raise HTTPException(status_code=400, detail="Invalid page number. Page number must be greater than or equal to 1.")
    return page_extractor(page)


if __name__ == "__main__":
    uvicorn.run(app, port=8000, host='0.0.0.0')
