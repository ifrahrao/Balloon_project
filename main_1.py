import requests
from bs4 import BeautifulSoup
import json
import re
import time
import schedule
import helpers
import db
from helpers import balloons_with_color,balloons_with_brands,remove_duplicates,price_filter

def toyworldinc():
    url="https://toyworldinc.co"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    new_links = []
    for link in soup.findAll('a'):
        if 'collections' in link.get('href'):
            new_links.append(link.get('href'))
    baloons_items = []
    new_links=list(set(new_links))
    new_links.remove("/collections/conwin-and-premium-balloon-accessories")
    new_links.remove("https://toyworldinc.co/collections/conwin-and-premium-balloon-accessories")
    new_links.remove("/collections/party-supplies")
    new_links.remove("/collections/backdrops-circular-arches-cake-stands")
    new_links.remove("/collections/toys-games-crafts")
    new_links.remove("/collections/hi-float")
    new_links.remove("/collections/berwick-offray-curling-ribbon")
    for new_link in set(new_links):
        if 'http' not in new_link:
            new_link=url+new_link
        page = requests.get(new_link)
        soup = BeautifulSoup(page.content, "html.parser")
        products = soup.select('div.product-thumbnail')

        # products = []

        for elem in products:
            title = elem.select('a.product-thumbnail__title')[0].text

            purchase_link=url+elem.select('a.product-thumbnail__title')[0].get('href')
            price=elem.select('span')[0].text
            if elem.select(".product-thumbnail__media img"):
                image_link=elem.select(".product-thumbnail__media img")[0].get('src')
            else:
                image_link=""
            info = {
                "title": title.strip(),
                "price" : price.strip(),
                "purchase_link" : purchase_link.strip(),
                "image_link":image_link.strip()
            }
            baloons_items.append(info)

    baloons_items=helpers.remove_duplicates(baloons_items)
    baloons_items=helpers.price_filter(baloons_items)
    baloons_items=helpers.balloons_with_color(baloons_items)
    baloons_items=helpers.balloons_with_brands(baloons_items)
    category={"name":"Toys World Inc",
              "slug":"toys_world_inc",
              "description":"This is toys world inc balloons"}
    # db.insert_balloons_products(baloons_items,category)
    with open('toysworldinc.json', 'w') as fp:
        json.dump(baloons_items, fp, indent=2)


def winner_party_supplies():
    url="https://winner-party-supplies.myshopify.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    new_links = []
    for link in soup.findAll('a'):
        if 'collections' in link.get('href'):
            new_links.append(link.get('href'))
    baloons_items = []
    new_links=set(new_links)
    new_links.remove("https://winner-party-supplies.myshopify.com/collections/pro-tapes")
    new_links.remove("/collections/balloon-arch")
    new_links.remove("/collections/winner-party")
    new_links.remove("/collections/all")
    new_links.remove("/collections/balloon-glow")
    new_links.remove("/collections/new-arrivals")
    new_links.remove("/collections/party-accessories")
    new_links.remove("/collections/premium-accessories")
    new_links.remove("/collections/pro-tapes")
    new_links.remove("/collections/accessories")
    new_links.remove("/collections/hi-float")
    new_links.remove("/collections/clik-clik")
    new_links.remove("/collections/novedades-peyma")
    new_links.remove("/collections/hearts")
    new_links.remove("/collections/love")
    new_links.remove("/collections/borosino")
    new_links.remove("/collections/new-years")
    new_links.remove("/collections/inflators")
    new_links.remove("/collections/conwin")

    for new_link in set(new_links):
        if 'http' not in new_link:
            new_link = url + new_link
        page = requests.get(new_link)
        soup = BeautifulSoup(page.content, "html.parser")

        products = soup.select('div.grid-view-item')


        for elem in products:
            title = elem.select('div.grid-view-item__title')[0].text

            if title == "Conwin Snap-on Soft-Touch Outlet 36500":
                print(new_link)
            purchase_link = url + elem.select('a.grid-view-item__link')[0].get('href')
            price = elem.select('span.price-item')[0].text
            image_link = elem.select("div.grid-view-item__image-wrapper img")[0].get('data-src')
            image_link_width = elem.select("div.grid-view-item__image-wrapper img")[0].get('data-widths')
            image_link=image_link.replace("{width}",str(json.loads(image_link_width)[-1]))
            if re.compile('|'.join(["Bag","Plate"]),re.IGNORECASE).search(title):
                print("title", title)
                pass

            else:
                info = {
                    "title": title.strip(),
                    "price": price.strip(),
                    "purchase_link": purchase_link.strip(),
                    "image_link": image_link.strip()
                }
                baloons_items.append(info)
    baloons_items = helpers.remove_duplicates(baloons_items)
    baloons_items = helpers.price_filter(baloons_items)
    baloons_items = helpers.balloons_with_color(baloons_items)
    baloons_items = helpers.balloons_with_brands(baloons_items)
    category = {"name": "Winner Party Supplies",
                "slug": "winner_party_supplies",
                "description": "This is winner party supplies balloons"}
    # db.insert_balloons_products(baloons_items, category)
    with open('winner_party_supplies.json', 'w') as fp:
        json.dump(baloons_items, fp, indent=2)

def get_havina_party(links):
    url = "https://havinaparty.com/"
    baloons_items = []
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

        if check_title:
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


    size=int(len(new_list_change)/3)

    baloons_items=get_havina_party(new_list_change[:size])
    res=get_havina_party(new_list_change[size:size+size])
    for r in res:
        baloons_items.append(r)
    res=get_havina_party(new_list_change[size+size:])
    for r in res:
        baloons_items.append(r)
    baloons_items = helpers.remove_duplicates(baloons_items)
    baloons_items = helpers.price_filter(baloons_items)
    baloons_items = helpers.balloons_with_color(baloons_items)
    baloons_items = helpers.balloons_with_brands(baloons_items)
    category = {"name": "Havina Party",
                "slug": "havina_party",
                "description": "This is havina party balloons"}
    # db.insert_balloons_products(baloons_items, category)
    with open('havinaparty.json', 'w') as fp:
       json.dump(baloons_items, fp,indent=2)

def alpartyballoons():
    url = "https://alpartyballoons.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    new_links = []
    for link in soup.findAll('a'):

        if 'collections' in link.get('href') and 'products' not in link.get('href'):
            new_links.append(link.get('href'))
    baloons_items = []
    new_links=set(new_links)
    new_links.remove("/collections/accessories")
    new_links.remove("/collections/all")
    for new_link in set(new_links):
        if 'http' not in new_link:
            new_link = url + new_link
        try:
            page1 = requests.get(new_link)
            soup1 = BeautifulSoup(page1.content, "html.parser")

            pagination = soup1.findAll("span", {"class": "page"})[-1].text
            for i in range(int(pagination) + 1):

                new_link_v2 = new_link + "?page=" + str(i)
                page2 = requests.get(new_link_v2)
                soup2 = BeautifulSoup(page2.content, "html.parser")

                products = soup2.select('div.grid__item')

                for elem in products:
                    title = elem.select('div.product-card__name')
                    if title:
                        title = title[0].text

                        purchase_link = elem.select('a.product-card')[0].get('href')
                        image_link = elem.select("div.product-card__image img")[0].get('data-src')
                        image_link_width = elem.select("div.product-card__image img")[0].get('data-widths')
                        image_link = image_link.replace("{width}", str(json.loads(image_link_width)[-1]))
                        if elem.select('.product-card__price'):
                            price = elem.select('.product-card__price')[0].text
                            price = price.replace("\n", "")
                            price = ' '.join(price.split())

                        else:
                            price = "SOLD OUT"

                        info = {
                            "title": title,
                            "price": price,
                            "purchase_link": "https://alpartyballoons.com" + purchase_link.strip(),
                            "image_link": image_link.strip()
                        }
                        baloons_items.append(info)

        except Exception as e:
            pass
    baloons_items = helpers.remove_duplicates(baloons_items)
    baloons_items = helpers.price_filter(baloons_items)
    baloons_items = helpers.balloons_with_color(baloons_items)
    baloons_items = helpers.balloons_with_brands(baloons_items)
    category = {"name": "Al Party Balloons",
                "slug": "al_party_balloons",
                "description": "This is al party balloons"}
    # db.insert_balloons_products(baloons_items, category)
    with open('alpartyballoons.json', 'w') as fp:
       json.dump(baloons_items, fp,indent=2)


def balloonsbyjolie():
    url = "https://balloonsbyjolie.com"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    new_links = []
    for link in soup.findAll('a'):
        if 'collections' in link.get('href'):
            new_links.append(link.get('href'))
    baloons_items = []
    new_links=set(new_links)
    new_links.remove("/collections/manual-pumps")
    new_links.remove("/collections/electric-pumps")
    new_links.remove("/collections/gift-card")
    new_links.remove("/collections/balloon-accessories")
    new_links.remove("https://balloonsbyjolie.com/collections/balloon-accessories")
    new_links.remove("/collections/drinks")
    new_links.remove("/collections/cutter")
    new_links.remove("/collections/hi-float")
    new_links.remove("/collections/ribbon")
    new_links.remove("/collections/balloon-shine-1")
    new_links.remove("/collections/weights")
    new_links.remove("/collections/glue")
    for new_link in set(new_links):
        if 'http' not in new_link:
            new_link = url + new_link
        page = requests.get(new_link)
        soup = BeautifulSoup(page.content, "html.parser")
        products = soup.select('div.block')
        if products:
            print(new_link)


        for elem in products:
            try:
                properties=[]
                title = elem.select('a.product-block-title')[0].text

                purchase_link = url + elem.select('a.product-block-title')[0].get('href')

                if len(elem.select('span'))==2:
                    price = elem.select('span')[0].text+" " +elem.select('span')[1].text
                else:
                    price = elem.select('span')[0].text
                image_link = elem.select(".rimage-wrapper img")[0].get('src')

                info = {
                    "title": title.strip(),
                    "price": price.strip(),
                    "purchase_link": purchase_link.strip(),
                    "image_link": image_link.strip()
                    # "review": review_label.strip()
                }
                baloons_items.append(info)
            except Exception as e:
                pass
    baloons_items = helpers.remove_duplicates(baloons_items)
    baloons_items = helpers.price_filter(baloons_items)
    baloons_items = helpers.balloons_with_color(baloons_items)
    baloons_items = helpers.balloons_with_brands(baloons_items)
    category = {"name": "Balloons By Jolie",
                "slug": "balloons_by_jolie",
                "description": "This is balloons by jolie"}
    # db.insert_balloons_products(baloons_items, category)
    with open('balloonsbyjolie.json', 'w') as fp:
        json.dump(baloons_items, fp, indent=2)

def balloonposh():
    url = "https://balloonposh.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    new_links = []
    for link in soup.findAll('a'):

        if 'collections' in link.get('href') and 'products' not in link.get('href'):
            new_links.append(link.get('href'))
    baloons_items = []
    rejected_list=["https://balloonposh.com//collections/vendors?q=Balloon%20Posh",
                   "https://balloonposh.com//collections/vendors?q=GEMAR"]
    new_links=set(new_links)
    new_links.remove("/collections/all")
    new_links.remove("/collections/happy-striking")
    for new_link in set(new_links):
        if 'http' not in new_link:
            new_link = url + new_link
        try:

            page1 = requests.get(new_link)
            soup1 = BeautifulSoup(page1.content, "html.parser")

            if soup1.findAll("span", {"class": "page"}):
                pagination = soup1.findAll("span", {"class": "page"})[-1].text
                for i in range(int(pagination) + 1):
                    if new_link == "https://balloonposh.com//collections/vendors?q=Balloon%20Posh":

                        new_link_v2="https://balloonposh.com//collections/vendors?page="+str(i)+"&q=Balloon%20Posh"
                    elif new_link == "https://balloonposh.com//collections/vendors?q=GEMAR":

                        new_link_v2="https://balloonposh.com//collections/vendors?page="+str(i)+"&q=GEMAR"
                    else:

                        new_link_v2 = new_link + "?page=" + str(i)
                    page2 = requests.get(new_link_v2)
                    soup2 = BeautifulSoup(page2.content, "html.parser")

                    products = soup2.select('div.grid-product__content')



                    for elem in products:
                        title = elem.select('div.grid-product__title')[0].text
                        if title == "36” Happy New Year Bottle":
                            print(new_link_v2)

                        purchase_link = elem.select('a.grid-product__link')[0].get('href')
                        image_link = elem.select("div.image-wrap img")[0].get('data-src')
                        image_link_width = elem.select("div.image-wrap img")[0].get('data-widths')
                        image_link = image_link.replace("{width}", str(json.loads(image_link_width)[-1]))
                        price = elem.select('span')[0].text
                        price = price.replace("\n", "")
                        price = ' '.join(price.split())

                        if re.compile('|'.join(["Bottle", "Plate", "Glass","Hi Shine","Striker"]), re.IGNORECASE).search(title):
                            print("title", title)
                            pass

                        else:
                            info = {
                                "title": title,
                                "price": price,
                                "purchase_link": "https://balloonposh.com" + purchase_link.strip(),
                                "image_link": image_link.strip()
                            }
                            baloons_items.append(info)
            else:
                page2 = requests.get(new_link)
                soup2 = BeautifulSoup(page2.content, "html.parser")

                products = soup2.select('div.grid-product__content')



                for elem in products:
                    title = elem.select('div.grid-product__title')[0].text
                    if title == "36” Happy New Year Bottle":
                        print(new_link)
                    purchase_link = elem.select('a.grid-product__link')[0].get('href')
                    image_link = elem.select("div.image-wrap img")[0].get('data-src')
                    image_link_width = elem.select("div.image-wrap img")[0].get('data-widths')
                    image_link = image_link.replace("{width}", str(json.loads(image_link_width)[-1]))
                    price = elem.select('span')[0].text
                    price = price.replace("\n", "")
                    price = ' '.join(price.split())
                    if re.compile('|'.join(["Bottle", "Plate", "Glass","Hi Shine","Striker"]), re.IGNORECASE).search(title):
                        print("title", title)
                        pass

                    else:
                        info = {
                            "title": title,
                            "price": price,
                            "purchase_link": "https://balloonposh.com" + purchase_link.strip(),
                            "image_link": image_link.strip()
                        }
                        baloons_items.append(info)

            #         # print(len(baloons_items))
        except Exception as e:
            pass
    baloons_items = helpers.remove_duplicates(baloons_items)
    baloons_items = helpers.price_filter(baloons_items)
    baloons_items = helpers.balloons_with_color(baloons_items)
    baloons_items = helpers.balloons_with_brands(baloons_items)
    category = {"name": "Balloons Posh",
                "slug": "balloons Posh",
                "description": "This is balloons posh"}
    # db.insert_balloons_products(baloons_items, category)
    with open('balloonposh.json', 'w') as fp:
        json.dump(baloons_items, fp, indent=2)
# schedule.every().second.do(toyworldinc)
# def test():
#     print("test")
#
# schedule.every().saturday.at("10:47").do(test)
#
# while 1:
#     schedule.run_pending()
# toyworldinc()
# winner_party_supplies()
# alpartyballoons()
# balloonposh()
# balloonsbyjolie()
havinaparty()
