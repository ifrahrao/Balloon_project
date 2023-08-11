import requests
from bs4 import BeautifulSoup
import json
def toyworldinc():
    url="https://toyworldinc.co"

    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    new_links = []
    for link in soup.findAll('a'):
        if 'collections' in link.get('href'):
            new_links.append(link.get('href'))
    baloons_items = []
    for new_link in set(new_links):
        if 'http' not in new_link:
            new_link=url+new_link
        page = requests.get(new_link)

        # print(page.text)
        soup = BeautifulSoup(page.content, "html.parser")
        products = soup.select('div.product-thumbnail')


        for elem in products:
            title = elem.select('a.product-thumbnail__title')[0].text
            purchase_link=url+elem.select('a.product-thumbnail__title')[0].get('href')
            price=elem.select('span')[0].text
            if elem.select(".product-thumbnail__media img"):
                image_link=elem.select(".product-thumbnail__media img")[0].get('src')
            else:
                image_link=""
            # review_label = elem.select('div.ratings')[0].text
            info = {
                "title": title.strip(),
                "price" : price.strip(),
                "purchase_link" : purchase_link.strip(),
                "image_link":image_link.strip()
                # "review": review_label.strip()
            }
            baloons_items.append(info)

    with open('toysworldinc.json', 'w') as fp:
        json.dump(baloons_items, fp, indent=2)
    print(baloons_items)

def winner_party_supplies():
    url="https://winner-party-supplies.myshopify.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    new_links = []
    for link in soup.findAll('a'):
        if 'collections' in link.get('href'):
            new_links.append(link.get('href'))
    baloons_items = []

    for new_link in set(new_links):
        if 'http' not in new_link:
            new_link = url + new_link
        page = requests.get(new_link)
        soup = BeautifulSoup(page.content, "html.parser")

        products = soup.select('div.grid-view-item')
        #
        for elem in products:
            title = elem.select('div.grid-view-item__title')[0].text
            print(type(elem.select('div.grid-view-item__title')))
            purchase_link = url + elem.select('a.grid-view-item__link')[0].get('href')
            price = elem.select('span.price-item')[0].text
            image_link = elem.select("div.grid-view-item__image-wrapper img")[0].get('data-src')
            image_link_width = elem.select("div.grid-view-item__image-wrapper img")[0].get('data-widths')
            image_link=image_link.replace("{width}",str(json.loads(image_link_width)[-1]))

            info = {
                "title": title.strip(),
                "price": price.strip(),
                "purchase_link": purchase_link.strip(),
                "image_link": image_link.strip()
            }
            baloons_items.append(info)

    # with open('winner_party_supplies.json', 'w') as fp:
    #     json.dump(baloons_items, fp, indent=2)

def havinaparty():
    url = "https://havinaparty.com/"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    new_links = []

    with open('havinaparty_links.json', 'r') as json_file:
        new_links = json.load(json_file)
    # for link in soup.findAll('a'):
    #     link_href=link.get('href')
    #     if link_href and url in link_href:
    #         new_links.append(link.get('href'))
    # new_list_change=list(set(new_links))

    print(len(new_links))
    baloons_items = []
    for new_link in new_links[800:]:

        if 'http' not in new_link:
            new_link = url + new_link
        page = requests.get(new_link)
        soup = BeautifulSoup(page.content, "html.parser")


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


    with open('havinaparty_v3(800-).json', 'w') as fp:
        json.dump(baloons_items, fp,indent=2)
    print(baloons_items)

def alpartyballoons():
    url = "https://alpartyballoons.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    new_links = []
    for link in soup.findAll('a'):

        if 'collections' in link.get('href') and 'products' not in link.get('href'):
            new_links.append(link.get('href'))
    baloons_items = []

    for new_link in set(new_links):
        if 'http' not in new_link:
            new_link = url + new_link
        try:
            print(new_link)

            # new_link="https://alpartyballoons.com/collections/foil-balloons"
            page1 = requests.get(new_link)
            soup1 = BeautifulSoup(page1.content, "html.parser")

            # products = soup1.select('div.grid__item')

            pagination = soup1.findAll("span", {"class": "page"})[-1].text
            print(pagination)
            for i in range(int(pagination)+1):

                new_link_v2=new_link+"?page="+str(i)
                page2 = requests.get(new_link_v2)
                soup2 = BeautifulSoup(page2.content, "html.parser")

                products = soup2.select('div.grid__item')
                for elem in products:
                    title = elem.select('div.product-card__name')
                    if title:
                        title=title[0].text

                        purchase_link = elem.select('a.product-card')[0].get('href')
                        image_link = elem.select("div.product-card__image img")[0].get('data-src')
                        image_link_width = elem.select("div.product-card__image img")[0].get('data-widths')
                        image_link = image_link.replace("{width}", str(json.loads(image_link_width)[-1]))
                        if elem.select('.product-card__price'):
                            price = elem.select('.product-card__price')[0].text
                            price=price.replace("\n","")
                            price=' '.join(price.split())

                        else:
                            price="SOLD OUT"


                        info = {
                            "title": title,
                            "price": price,
                            "purchase_link": "https://alpartyballoons.com"+purchase_link.strip(),
                            "image_link": image_link.strip()
                        }
                        baloons_items.append(info)
                # print(len(baloons_items))
        except Exception as e:
            print(e)
            print("Rejected:",new_link)

    # with open('alpartyballoons.json', 'w') as fp:
    #     json.dump(baloons_items, fp,indent=2)
    # print(baloons_items)

# alpartyballoons()

def balloonsbyjolie():
    url = "https://balloonsbyjolie.com"

    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    new_links = []
    for link in soup.findAll('a'):
        if 'collections' in link.get('href'):
            new_links.append(link.get('href'))
    baloons_items = []
    for new_link in set(new_links):
        if 'http' not in new_link:
            new_link = url + new_link
        print(new_link)
        page = requests.get(new_link)

        # print(page.text)
        soup = BeautifulSoup(page.content, "html.parser")
        products = soup.select('div.block')

        for elem in products:
            try:
                properties=[]
                title = elem.select('a.product-block-title')[0].text
                purchase_link = url + elem.select('a.product-block-title')[0].get('href')

                if len(elem.select('span'))==2:
                    price = elem.select('span')[0].text+" " +elem.select('span')[1].text
                else:
                    price = elem.select('span')[0].text
        #         if elem.select(".product-thumbnail__media img"):
                image_link = elem.select(".rimage-wrapper img")[0].get('src')
        #         else:
        #             image_link = ""
        #         # review_label = elem.select('div.ratings')[0].text
                info = {
                    "title": title.strip(),
                    "price": price.strip(),
                    "purchase_link": purchase_link.strip(),
                    "image_link": image_link.strip()
                    # "review": review_label.strip()
                }
                baloons_items.append(info)
            except Exception as e:
                print(e)
                print("rejebted:",new_link)

    #
    with open('balloonsbyjolie.json', 'w') as fp:
        json.dump(baloons_items, fp, indent=2)
    # print(baloons_items)\

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
    for new_link in set(new_links):
        if 'http' not in new_link:
            new_link = url + new_link
        try:
            print(new_link)

            # new_link="https://alpartyballoons.com/collections/foil-balloons"
            page1 = requests.get(new_link)
            soup1 = BeautifulSoup(page1.content, "html.parser")

            # products = soup1.select('div.grid__item')
            if soup1.findAll("span", {"class": "page"}):
                pagination = soup1.findAll("span", {"class": "page"})[-1].text
                print(pagination)

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
                    if not products:
                        print("not",new_link_v2)
                    for elem in products:
                        title = elem.select('div.grid-product__title')[0].text

                        purchase_link = elem.select('a.grid-product__link')[0].get('href')
                        image_link = elem.select("div.image-wrap img")[0].get('data-src')
                        image_link_width = elem.select("div.image-wrap img")[0].get('data-widths')
                        image_link = image_link.replace("{width}", str(json.loads(image_link_width)[-1]))
                        price = elem.select('span')[0].text
                        price = price.replace("\n", "")
                        price = ' '.join(price.split())


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
                if not products:
                    print("not", new_link)

                for elem in products:
                    title = elem.select('div.grid-product__title')[0].text

                    purchase_link = elem.select('a.grid-product__link')[0].get('href')
                    image_link = elem.select("div.image-wrap img")[0].get('data-src')
                    image_link_width = elem.select("div.image-wrap img")[0].get('data-widths')
                    image_link = image_link.replace("{width}", str(json.loads(image_link_width)[-1]))
                    price = elem.select('span')[0].text
                    price = price.replace("\n", "")
                    price = ' '.join(price.split())

                    info = {
                        "title": title,
                        "price": price,
                        "purchase_link": "https://balloonposh.com" + purchase_link.strip(),
                        "image_link": image_link.strip()
                    }
                    baloons_items.append(info)

        #         # print(len(baloons_items))
        except Exception as e:
            print(e)
            print("Rejected:", new_link)
    with open('balloonposh.json', 'w') as fp:
        json.dump(baloons_items, fp, indent=2)

def balloonsdirect():
    url = "https://balloonsdirect.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    new_links = []
    for link in soup.findAll('a'):
        if link.get('href') and 'supplies' not in link.get('href') and 'customprint' not in link.get('href') and 'www' not in link.get('href') \
                and 'balls' not in link.get('href'):
            new_links.append(link.get('href'))
    baloons_items = []
    rejected_list = []
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

            # products = soup1.select('div.grid__item')
            # if soup1.findAll("span", {"class": "page"}):
            #     pagination = soup1.findAll("span", {"class": "page"})[-1].text
            #     print(pagination)


        except Exception as e:
            print(e)
            print("Rejected:", new_link)

    with open('balloondirect.json', 'w') as fp:
        json.dump(baloons_items, fp, indent=2)
# toyworldinc()
balloonsdirect()