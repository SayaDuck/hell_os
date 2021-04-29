import urllib
import json
import requests
import db_builder as dbb # weirdly this works as db_builder

def main():
    # open the file containing the api key
    # with open('key_nasa.txt', 'r') as files:
    # key = files.read()
    # append api key to rest of the url
    url = "https://www.fruityvice.com/api/fruit/all"
    # send http request to the domain and save response
    with urllib.request.urlopen(url) as response:
    # convert response from http request to bytes
        resp = response.read()
    # convert bytes to python dictionary
        resp = json.loads(resp)
        xp = 0
        for i in resp:
            xp += 10
            name = i["name"]
            print (name)
            nutrition = i["nutritions"]
            print (nutrition)
            dbb.add_fruit(name,str(nutrition),img(name), xp)
            print (img(name))

def img(search_query):
    key = "ESVzjJnKEHmc0b4AJOMLMuDo1RjdDO77QHcQXpXYWVM"
    url = urllib.request.urlopen('https://api.unsplash.com/search/photos/?per_page=1&query=' + search_query + '&client_id=' + key)
    now_json = json.load(url) # url -> json
    link = now_json['results'][0]['urls']['raw']
    return link

main()
