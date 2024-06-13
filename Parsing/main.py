import json
import requests 
from bs4 import BeautifulSoup
from datetime import datetime
import time




news_dict = {}
def all_news():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
               }
    url = "https://www.golosameriki.com/ukraine"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    bbc_name = soup.find_all("li", class_ = "col-xs-12 col-sm-12 col-md-12 col-lg-12 fui-grid__inner")


    for bbc in bbc_name:
        if bbc.find("h4", class_ = "media-block__title media-block__title--size-3") is not None:
            bbc_title = bbc.find("h4").text.strip()
        if bbc.find("p") is not None:
            bbc_desc = bbc.find("p").text.strip()
        bbc_url = f'https://www.golosameriki.com{bbc.find("a").get("href")}'
        if  bbc.find("span", class_ = "date date--mb date--size-3") is not None:
            bbc_date_time = bbc.find("span", class_ = "date date--mb date--size-3").text.strip()




        bbc_id = bbc_url.split("/")[-1]
        bbc_id = bbc_id[:-4]



        news_dict[bbc_id] = {
            "bbc_title": bbc_title,
            "bbc_desc": bbc_desc,
            "bbc_date_time": bbc_date_time,
            "bbc_url": bbc_url
        }

    with open("news_dict.json", "w", encoding='utf8') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)



def check_news_update():
    with open("news_dict.json", encoding='utf8') as file:
        news_dict = json.load(file)
    
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
               }
    url = "https://www.golosameriki.com/ukraine"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    bbc_name = soup.find_all("li", class_ = "col-xs-12 col-sm-12 col-md-12 col-lg-12 fui-grid__inner")

    fresh_news = {}


    for bbc in bbc_name:
        bbc_url = f'https://www.golosameriki.com{bbc.find("a").get("href")}'
        bbc_id = bbc_url.split("/")[-1]
        bbc_id = bbc_id[:-4]

        if bbc_id in news_dict:
            continue
        else:
            if bbc.find("h4", class_ = "media-block__title media-block__title--size-3") is not None:
                bbc_title = bbc.find("h4").text.strip()
            if bbc.find("p") is not None:
                bbc_desc = bbc.find("p").text.strip()
            bbc_url = f'https://www.golosameriki.com{bbc.find("a").get("href")}'
            if  bbc.find("span", class_ = "date date--mb date--size-3") is not None:
                bbc_date_time = bbc.find("span", class_ = "date date--mb date--size-3").text.strip()
            


            news_dict[bbc_id] = {
                "bbc_title": bbc_title,
                "bbc_desc": bbc_desc,
                "bbc_date_time": bbc_date_time,
                "bbc_url": bbc_url
            }


            fresh_news[bbc_id] = {
                "bbc_title": bbc_title,
                "bbc_desc": bbc_desc,
                "bbc_date_time": bbc_date_time,
                "bbc_url": bbc_url
            }
    
    with open("news_dict.json", "w", encoding='utf8') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)
    return fresh_news

        




def main():
    #all_news()
    print(check_news_update())


if __name__ == '__main__':
    main()


