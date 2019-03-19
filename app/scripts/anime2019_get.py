from bs4 import BeautifulSoup
import requests
import csv

def get_info():

    url = "https://akiba-souken.com/anime/spring/"

    response = requests.get(url)


    soup = BeautifulSoup(response.text, "html.parser")

    itemBoxs = soup.find_all(class_="itemBox")

    remove_letters = {"\n": " ", "\t": "", "\xa0": " "}

    results = {}

    for itemBox in itemBoxs:
        mTitle = itemBox.find(class_="mTitle")
        firstDate = itemBox.find(class_="firstDate")
        itemImg = itemBox.find(class_="itemImg")
        comments = itemBox.select(".commentBox .comment")
        if comments:
            comment_count = len(comments)
            infomation = {}
            comment_list = []
            title = mTitle.find("h2").text
            onAir = firstDate.text.replace("\xa0", remove_letters["\xa0"])
            try:
                img = itemImg.find("img")["src"]
            except:
                print("IMAGE ERROR!!!\ntitle is {}".format(title))
                img = "../static/images/noimage.png"
            infomation["onAir"] = onAir
            infomation["img"] = img
            infomation["comment_count"] = comment_count
            for idx, comment in enumerate(comments):
                comment = comment.find(class_="text").text.replace("\n", remove_letters["\n"]).replace("\t", remove_letters["\t"])
                comment_list.append(comment)
                #title = title+"_"+str(idx+1)
            infomation["comment"] = "SPLIT_POINT".join(comment_list)
            results[title] = infomation
        else:
            infomation = {}
            title = mTitle.find("h2").text
            infomation["onAir"] = firstDate.text.replace("\xa0", remove_letters["\xa0"])
            try:
                img = itemImg.find("img")["src"]
                infomation["img"] = img
            except:
                print("IMAGE ERROR!!!\ntitle is {}".format(title))
                infomation["img"] = "../static/images/noimage.png"
            infomation["comment"] = "コメントなし"
            infomation["comment_count"] = 0
            results[title] = infomation

    #commemt_countになっていて苦労
    fieldnames = ["title", "onAir", "img", "comment", "comment_count"]

    #unicodeerror:
    #https://qiita.com/HyunwookPark/items/ebc963f82355c837c488
    with open("app/input/anime2019.csv", "w", encoding="utf-8") as f:
        writeObj = csv.DictWriter(f, fieldnames=fieldnames, delimiter=",", extrasaction="ignore")
        writeObj.writeheader()
        #データ挿入
        for anime_title, infomations in results.items():
            writeData = {"title": anime_title}
            for header, value in infomations.items():
                writeData[header] = value
            writeObj.writerow(writeData)
