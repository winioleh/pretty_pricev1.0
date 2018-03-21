# from bs4 import BeautifulSoup
# import re
# import requests
#
#
# def parse(barcode="5449000054227"):
#
#     url = "http://mysupermarket.org.ua/index.php?search="+barcode
#     headres = {
#        "Content-Type": "text/html; charset=CP1251",
#             "Referer": "http://mysupermarket.org.ua/index.php?search=",
#             "Upgrade-Insecure-Requests": "1",
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
#     }
#
#
#     response = requests.get(url, headers=headres)
#
#
#     soup = BeautifulSoup(response.text,"html.parser")
#     kw = {"class": "list"}
#     res = soup.find("td", width="25%")
#     # if res is None:
#     #     return
#     res = res.findAll("p")
#     print(res)
#     res = [str(x) for x in res if  "<a" in str(x)]
#     answer = []
#     # print(res)
#     # for tag in res:
#         # print(tag)
#
#     return answer or None
# test = parse()
# print(test)