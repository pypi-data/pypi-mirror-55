#IMPORTS
import requests
import re
import sys
from tika import parser
import string


def pull_from_web(link):
    #loading book data from web
    html_data = requests.get(str(link))
    raw_text = html_data.text
    #removing some garbage so that we have actual ascii chars, and moving to lowercase
    text = re.sub(r'[^\x00-\x7f]',r'', raw_text.lower().rstrip())
    return text

def pull_from_file(path):
    with open(path, 'r') as file:
        data = file.read().replace('\n', '')
        data = re.sub(r'[^\x00-\x7f]',r'', data.lower().rstrip())
    return data

def pull_from_pdf(path):
    raw = parser.from_file(path)
    #raw = re.sub(r'[^\x00-\x7f]',r'', raw.lower().rstrip())
    return (raw['content'])

#redo the text processing so we return a list format of every word in the text but it is, lowered, remove unwanted (. , " : ! ?) punctuation
def load_raw_text(urls, method="web", merge_data=True):
  if method=="web":
    if merge_data:
        text = ""
        for link in urls:
            print("Pulling from Link: ", str(link))
            text+=pull_from_web(link)
        print("Chars Loaded: ", len(text))
        return text
    else:
        raw_data_list = []
        for link in urls:
            print("Pulling from Link: ", str(link))
            raw_data_list.append(pull_from_web(link))
        words_pulled = 0
        for data in raw_data_list:
            words_pulled += len(data)
        print("Chars Loaded: ", words_pulled)
        return raw_data_list


  elif method=="text":
    if merge_data:
        text = ""
        for link in urls:
            print("Pulling from Link: ", str(link))
            text+=pull_from_file(link)
        print("Chars Loaded: ", len(text))
        return text
    else:
        raw_data_list = []
        for link in urls:
            print("Pulling from Link: ", str(link))
            raw_data_list.append(pull_from_file(link))
        words_pulled = 0
        for data in raw_data_list:
            words_pulled += len(data)
        print("Chars Loaded: ", words_pulled)
        return raw_data_list

  elif method=="pdf":
    if merge_data:
        text = ""
        for link in urls:
            print("Pulling from Link: ", str(link))
            text+=pull_from_pdf(link)
        print("Chars Loaded: ", len(text))
        return text
    else:
        raw_data_list = []
        for link in urls:
            print("Pulling from Link: ", str(link))
            raw_data_list.append(pull_from_pdf(link))
        words_pulled = 0
        for data in raw_data_list:
            words_pulled += len(data)
        print("Chars Loaded: ", words_pulled)
        return raw_data_list
