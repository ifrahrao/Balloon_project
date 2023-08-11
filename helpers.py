import json
from colour import Color
import re
def balloons_with_color(data):
    temp = []
    res = []
    color_list=["light","rose","hot","dark","royal","lime","baby","navy","shiny"]
    for i in data:
        val=i["title"]

        match=False
        for j in val.split(' '):
            try:
                if "/" in j:
                    if j.split("/")[0]!="":
                        _color=Color(j.split("/")[0])
                        if _color:
                            i["color"]=j.split("/")[0]
                        _color = Color(j.split("/")[1])
                        if _color:
                            i["color"] = i["color"]+", "+j.split("/")[1]

                _color = Color(j)
                if _color:

                    if "color" in i and i["color"] and j:
                        i["color"] = i["color"]+", "+j
                    elif j and "#" not in j:
                        i["color"]=j

                    # if "Balloon" not in val:
                    match=True


                        # print("", _color)
                        # print(val)

            except Exception as e:
                # print(e)
                pass

        if "color" in i and i["color"] and val.split(i["color"])[0]:


            if ((val.split(i["color"])[0]).split()[-1]).lower() in color_list:
                i["color"]=(val.split(i["color"])[0]).split()[-1]+" "+i["color"]

        # if "balloon" not in i["purchase_link"] and "balloon" not in val.lower() and "color" not in i:
        #     pass
        # else:
        if "color" not in i:
            i["color"]=""
        res.append(i)
    return res


def balloons_with_brands(data):
    brands_list=["betallatex", "decomex", "gemar", "kalisan", "qualatex", "tuftex","anagram","balloonia","sempertex"]
    res=[]
    for i in data:
        val=i["title"]
        for j in val.split(" "):

            if j.lower() in brands_list:
                i["brand"]=j
        if "brand" not in i:
            i["brand"]=""
        res.append(i)
    return res


def price_filter(data):
    res = []
    for i in data:
        if re.findall('[^A-Za-z\ ]', i["price"]):
            i["price"]=re.sub('[A-Za-z\ ]', '', i["price"])
        res.append(i)
    return res


def remove_duplicates(data):
    temp = []
    res = []
    for i in data:
        val=i["title"]
        if val not in temp:
            temp.append(i["title"])
            res.append(i)
    return res


def extract_size(data):
    res=[]
    print(len(data))
    for i in data:
        val=i["title"]
        i["size"]=""
        result = re.search(
            '(?<!\S)(\d+(?:,\d+)?) *(?:(?:in(?:ch)?|")(?: +W)?)? ?(?:x|by) ?(\d+(?:,\d+)?)(?: ?x ?\d+(?:,\d+)?)* *(?:(?:in(?:ch)?|")(?: +L)?)?(?: ?x ?(\d+(?:,\d+)?))* *(?:(?:in(?:ch)?|")(?: +H)?)?',
            val)
        if result:
            print(val)
            print(result)
            i["size"]=result.group()
            print(i["size"])
        if "\"" in val:
            print(val)

            result=re.search('(?<!\S)(\d+(?:,\d+)?) *(?:(?:in(?:ch)?|")(?: +W)?)? ?(?:x|by) ?(\d+(?:,\d+)?)(?: ?x ?\d+(?:,\d+)?)* *(?:(?:in(?:ch)?|")(?: +L)?)?(?: ?x ?(\d+(?:,\d+)?))* *(?:(?:in(?:ch)?|")(?: +H)?)?',val)
            print(result)
            print(val.split("\"")[0].split()[-1])


# with open('toysworldinc_1.json', 'r') as f:
#     data = json.load(f)
# # remove_duplicates(data)
# extract_size(data)