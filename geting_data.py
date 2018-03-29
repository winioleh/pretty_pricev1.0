from bs4 import BeautifulSoup
import re
import requests


def get_a_comparison(barcode="4820017000062"):

    url = "mysupermarket.org.ua/index.php?search="+barcode
    headres = {
       "Content-Type": "text/html; charset=CP1251",
            "Referer": "http://mysupermarket.org.ua/index.php?search=",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
    }


    response = requests.get(url, headers=headres)


    soup = BeautifulSoup(response.text)
    kw = {"class": "list"}
    res = soup.find("td", width="25%")
    if res is None:
        return
    res = res.findAll("p")
    res = [str(x) for x in res if  "<a" in str(x)]
    answer = []
    for tag in res:
        answer.append({"price": float(re.findall('<b>(.*?) grn.</b>', tag)[0]),
                      'name': re.findall('<small>(.*?)</small>', tag)[0]})

    return answer or None

