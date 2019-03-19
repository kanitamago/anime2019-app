import pandas as pd
import re
import os

def clean_info():
    df = loading()
    df = fill_null(df)
    comment_list = commentFunc(df)
    return [df, comment_list]

def loading():
    df = pd.read_csv("app/input/anime2019.csv")
    return df

"""
def remove_letters(title):
    pattern = "_[0-9]+$"
    result = re.sub(pattern, "", title)
    return result
"""

def commentFunc(df):
    titles = df["title"].values
    comments = df["comment"].values
    splited_comment = []
    for title, comment in zip(titles, comments):
        splited_comment.append(comment.split("SPLIT_POINT"))
    return splited_comment

def fill_null(df):
    df["comment_count"] = df["comment_count"].fillna(0).astype(int)
    return df

#exist_comment = df[df.comment_count > 0]
#print(exist_comment["img"].values)
