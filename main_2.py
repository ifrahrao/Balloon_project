import threading

import requests
from bs4 import BeautifulSoup
import json
import re
import time
import schedule
import helpers
import db
from helpers import balloons_with_color,balloons_with_brands,remove_duplicates,price_filter
baloons_items=[]


def get_havina_party(links):
    url = "https://havinaparty.com/"
    for new_link in links:
        check_title=False
        if 'http' not in new_link:
            new_link = url + new_link
        sess = requests.session()
        page = sess.get(new_link)
        soup = BeautifulSoup(page.content, "html.parser")
        for title in soup.find_all('title'):

            if title!=None and "accessories" in title.get_text().lower():
                print(title.get_text())
                print(new_link)
                check_title=True

        if not check_title:
            products = soup.select('ul.productGrid')
            for elem in products:
                title = elem.select('.card-title')[0].text
                purchase_link = elem.select('div.card-body a')[0].get('href')
                image_link = elem.select("div.card-img-container img")[0].get('src')

                info = {
                    "title": title.strip(),
                    "price": "Login Required",
                    "purchase_link": purchase_link.strip(),
                    "image_link": image_link.strip()
                }
                baloons_items.append(info)
    return baloons_items
def havinaparty():
    url = "https://havinaparty.com/"
    page = requests.get(url)


    soup = BeautifulSoup(page.content, "html.parser")
    new_links = []

    for link in soup.findAll('a'):
        link_href=link.get('href')
        if link_href and url in link_href:
            new_links.append(link.get('href'))
    new_list_change=list(set(new_links))
    # new_list_change.remove("https://havinaparty.com/hi-float-balloon-shine/")
    # new_list_change.remove("https://havinaparty.com/magnet-balloon-holder/")


    link_count=int(len(new_list_change)/5)
    divide_links = []

    divide_links.append([new_list_change[:link_count]])
    divide_links.append([new_list_change[link_count:(link_count + link_count)]])
    divide_links.append([new_list_change[(link_count + link_count):(link_count + link_count + link_count)]])
    divide_links.append([
        new_list_change[(link_count + link_count + link_count):(link_count + link_count + link_count + link_count)]])
    divide_links.append([new_list_change[(link_count + link_count + link_count + link_count):]])
    print(len(divide_links[0]))
    t1 = threading.Thread(target=get_havina_party, args=(divide_links[0]))
    t2 = threading.Thread(target=get_havina_party, args=(divide_links[1]))
    t3 = threading.Thread(target=get_havina_party, args=(divide_links[2]))
    t4 = threading.Thread(target=get_havina_party, args=(divide_links[3]))
    t5 = threading.Thread(target=get_havina_party, args=(divide_links[4]))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

    # wait until all threads finish
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    # baloons_items=get_havina_party(new_list_change[:size])
    # res=get_havina_party(new_list_change[size:size+size])
    # for r in res:
    #     baloons_items.append(r)
    # res=get_havina_party(new_list_change[size+size:])
    # for r in res:
    #     baloons_items.append(r)
    balloons_items = helpers.remove_duplicates(baloons_items)
    balloons_items = helpers.price_filter(balloons_items)
    balloons_items = helpers.balloons_with_color(balloons_items)
    balloons_items = helpers.balloons_with_brands(balloons_items)
    category = {"name": "Havina Party",
                "slug": "havina_party",
                "description": "This is havina party balloons"}
    # db.insert_balloons_products(balloons_items, category)
    with open('havinaparty.json', 'w') as fp:
       json.dump(balloons_items, fp,indent=2)

def balloonsdirect_balloons(new_links):
    url = "https://balloonsdirect.com/"
    for new_link in set(new_links):
        if 'http' not in new_link:
            new_link = url + new_link
        try:
            print("LINK",new_link)

            # new_link="https://alpartyballoons.com/collections/foil-balloons"
            page1 = requests.get(new_link)
            soup1 = BeautifulSoup(page1.content, "html.parser")
            products = soup1.select('div.product-item-info')
            print(len(products))
            if not products:
                print("not", new_link)
            for elem in products:
                title = elem.select('a.product-item-link')[0].text
                title=title.replace("\t","").replace("\n","").strip()

                purchase_link = elem.select('a.product-item-link')[0].get('href')
                image_link = elem.select(".product-image-photo")[0].get('src')
                # image_link_width = elem.select("div.image-wrap img")[0].get('data-widths')
                # image_link = image_link.replace("{width}", str(json.loads(image_link_width)[-1]))
                price = elem.select('span.price')[0].text
                price = price.replace("\n", "")
                price = ' '.join(price.split())

                info = {
                    "title": title,
                    "price": price,
                    "purchase_link": purchase_link.strip(),
                    "image_link": image_link.strip()
                }
                baloons_items.append(info)
        except Exception as e:
            print(e)
            print("Rejected:", new_link)
    return baloons_items
def balloonsdirect():
    url = "https://balloonsdirect.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    new_links = []
    for link in soup.findAll('a'):
        if link.get('href') and 'supplies' not in link.get('href') and 'customprint' not in link.get('href') and 'www' not in link.get('href') \
                and 'balls' not in link.get('href'):
            new_links.append(link.get('href'))
    new_list_change=list(set(new_links))
    link_count = int(len(new_list_change) / 5)
    divide_links = []

    divide_links.append([new_list_change[:link_count]])
    divide_links.append([new_list_change[link_count:(link_count + link_count)]])
    divide_links.append([new_list_change[(link_count + link_count):(link_count + link_count + link_count)]])
    divide_links.append([
        new_list_change[
        (link_count + link_count + link_count):(link_count + link_count + link_count + link_count)]])
    divide_links.append([new_list_change[(link_count + link_count + link_count + link_count):]])
    print(len(divide_links[0]))
    t1 = threading.Thread(target=balloonsdirect_balloons, args=(divide_links[0]))
    t2 = threading.Thread(target=balloonsdirect_balloons, args=(divide_links[1]))
    t3 = threading.Thread(target=balloonsdirect_balloons, args=(divide_links[2]))
    t4 = threading.Thread(target=balloonsdirect_balloons, args=(divide_links[3]))
    t5 = threading.Thread(target=balloonsdirect_balloons, args=(divide_links[4]))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

    # wait until all threads finish
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    balloons_items = helpers.remove_duplicates(baloons_items)
    balloons_items = helpers.price_filter(balloons_items)
    balloons_items = helpers.balloons_with_color(balloons_items)
    balloons_items = helpers.balloons_with_brands(balloons_items)
    category = {"name": "Havina Party",
                "slug": "havina_party",
                "description": "This is havina party balloons"}
    # db.insert_balloons_products(balloons_items, category)
    with open('balloonsdirect.json', 'w') as fp:
        json.dump(balloons_items, fp, indent=2)

balloonsdirect()
