from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import json
import boto3
from io import BytesIO
import sys,io,time,
def create_soup(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup


def tize(text):
    text = text.strip()
    text = text.replace("<br/>", "\n").replace(f"\t","")
    text = text.replace('0원', '').replace(',', '')
    text = ''.join([char for char in text if not char.isdigit()])
    text = text.replace('<tr>', '').replace('<td>', '')
    text = text.replace('<!-- <ul class="list-st"> -->','').replace('<ul class="list-st">', '').replace('</ul>', '')
    text = text.replace('<', '').replace('>', '').replace('!', '').replace('--', '').replace('amp;', '').replace('&lt;', '').replace('&gt;', '').replace('//', '').replace('()', '').replace('Kcal', '').strip()
    return text


def north(num=0):
    url = "https://www.kaist.ac.kr/kr/html/campus/053001.html?dvs_cd=fclt"
    soup = create_soup(url)
    menu_list = soup.find_all("ul", attrs={"class": "list-1st"})
    names = ['조식 8:00~9:30', '중식 11:30~14:00', '석식 17:30~19:00']
    menu_br = str(soup.find_all("tr")[1]).split("/td")[num]
    strs = str(names[num])+"\n"+str(tize(menu_br).replace("Kcal", ""))
    return strs


def east(num=0):
    url = "https://www.kaist.ac.kr/kr/html/campus/053001.html?dvs_cd=east1"
    soup = create_soup(url)
    menu_list = soup.find_all("ul", attrs={"class": "list-1st"})
    names = ['조식 8:00~10:00', '중식 11:30~14:00', '석식 17:30~19:00']
    menu_br = str(soup.find_all("tr")[1]).split("/td")[num]
    strs = str(names[num])+"\n" + str(tize(menu_br).replace("Kcal", "").replace("구세트", "3구세트"))
    return strs


def tize_list(menu_list):
    menu_list = [menu for menu in menu_list if menu not in ['', '/']]
    menu_list = menu_list[2:]
    menu_list = [menu for menu in menu_list if menu != '오늘의샐러드']
    menu_list = [menu for menu in menu_list if menu != '*일품코너는김치단무지장국(//)이샐러드바에준비되어있습니다.*']
    return menu_list

application = Flask(__name__)
@application.route("/bot", methods=["POST"])
def bot():
    request_data = json.loads(request.get_data().decode('utf-8'))
    # params = request_data['action']['params']
    # print(params)
    blockinfo = request_data['intent']['name']
    print(blockinfo)
    # errorcode = request_data['intent']['extra']['reason']['code']
    # print(errorcode)
    # if errorcode != 101:
    #     print('error')
    #     one_more = True
    for _ in range(2):
        if blockinfo == "북측아침_block":
            response = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "basicCard": {
                                "title": "북측아침",
                                "description": str(north(0)),
                            }
                        }
                    ]
                }
            }
        elif blockinfo == "동측아침_block":
            response = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "basicCard": {
                                "title": "동측아침",
                                "description": str(east(0)),
                            }
                        }
                    ]
                }
            }


        elif blockinfo == "북측점심_block":
            response = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "basicCard": {
                                "title": "북측점심",
                                "description": str(north(1)),
                            }
                        }
                        , {
                            "basicCard": {
                                "title": "북측점심",
                                "description": str(north(1)),
                            }
                        }
                    ]
                }
            }
        elif blockinfo == "동측점심_block":
            response = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "basicCard": {
                                "title": "동측점심",
                                "description": str(east(1)),
                            }
                        }
                    ]
                }
            }
        elif blockinfo == "북측저녁_block":
            response = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "basicCard": {
                                "title": "북측저녁",
                                "description": str(north(2)),
                            }
                        }
                    ]
                }
            }
        elif blockinfo == "동측저녁_block":
            response = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "basicCard": {
                                "title": "동측저녁",
                                "description": str(east(2)),
                            }
                        }
                    ]
                }
            }
        elif blockinfo == "저녁_all":
            response = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": str(north(2)+"\n"+east(2))
                            }
                        }
                    ]
                }
            }
        elif blockinfo == "그외":
            response = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "제작중..."
                            }
                        }
                    ]
                }
            }
        else:
            response = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "Error"
                            }
                        }
                    ]
                }
            }
    return jsonify(response)


if __name__ == "__main__":
    application.run()
