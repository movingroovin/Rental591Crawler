import requests
from bs4 import BeautifulSoup
import json

from datetime import datetime, timedelta
import time
import sched
schedule = sched.scheduler(time.time, time.sleep)

def rental591Crawler(scanTime):
    ## 設定條件
    # ???
    is_new_list = "1"

    # ???
    type = "1"

    # 類型 ＝> 0: 不限, 1: 整層住家, 2: 獨立套房, 3: 分租套房, 4: 雅房, 8: 車位, 24: 其他
    kind = "1"

    # 租金 (nullable) => 0: 不限, 1: 5000以下, 2: 5000-10000, 3: 10000-20000, 4: 20000-30000, 5: 30000-40000, 6: 40000-60000, 7: 60000以上
    # 自訂範圍: int, int e.g. 40000,50000 (40000-50000)/ 40000, (40000以上)/ ,50000(50000以下)
    rentprice = "40000,60000"

    # 格局 => 0: 不限, 1: 1房, 2: 2房, 3: 3房, 4: 4房, 5: 5房以上
    pattern = "3"

    # 坪數: 0,0: 不限, int, int
    area = "0,0"

    # ???
    searchtype = "1"

    # 地區 => 1: 台北, 2: 基隆, 3: 新北
    region = "1"

    # 排序條件(nullable): posttime/ area/ money
    order = "posttime"

    # 排序(nullable) => desc/ asc
    orderType = "desc"

    # 頁數： 30筆一頁
    # firstRow = ""

    # 全部筆數: response裡會有records<str>
    # totalRows = ""

    # 結合條件
    url = "https://rent.591.com.tw/home/search/rsList?is_new_list=" + is_new_list + "&type=" + type
    url = url + "&kind=" + kind + "&searchtype=" + searchtype + "&region=" + region + "&order="+ order+ "&orderType=" +orderType + "&rentprice=" + rentprice + "&pattern=" + pattern + "&area=" + area
    # url = "https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=1&searchtype=1&region=3"
    # print(url)

    #---- 開始 ----#
    # 先打一次首頁取得cookies和csrf-token
    session = requests.Session()
    preRequest = session.get("https://www.591.com.tw/",
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
            # "Accept": "application/json, text/javascript, */*; q=0.01",
            # "Accept-Encoding": "gzip, deflate, br",
            # "Connection": "keep-alive",
            # "Host": "rent.591.com.tw",
            # "Referer": "https://rent.591.com.tw/?kind=0&region=3",
            # "Sec-Fetch-Dest": "empty",
            # "Sec-Fetch-Mode": "cors",
            # "Sec-Fetch-Site": "same-origin",
            # "X-Requested-With": "XMLHttpRequest",
            # "X-CSRF-TOKEN": ""
        })
    cookies = preRequest.cookies.get_dict() # get_dict() 轉為字典
    # print(preRequest.text)

    # 用bs4取得首頁html, 篩出csrf-token
    soup = BeautifulSoup(preRequest.text, "html.parser")
    csrf_token = soup.select_one('meta[name="csrf-token"]')["content"]
    # print(csrf_token)

    # 正式發出request
    res = session.get(url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
            "Cookie": "webp=" + cookies["webp"] + "; PHPSESSID=" + cookies["PHPSESSID"] + "; user_index_role=1; T591_TOKEN=0126b460912eebd94fcfefe392532d75; tw591__privacy_agree=0; __auc=03522428173fca340d77c66e950; _ga=GA1.3.1001465899.1597671424; _ga=GA1.4.1001465899.1597671424; _fbp=fb.2.1597671424894.212433219; imgClick=9672733; localTime=2; is_new_index=1; is_new_index_redirect=1; __utma=82835026.1001465899.1597671424.1598619275.1598619275.1; __utmc=82835026; __utmz=82835026.1598619275.1.1.utmcsr=l.facebook.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _fbc=fb.2.1602005561201.IwAR080KBVpgsA0y1EvoDy3qx82_N7Hu6LeM2c3LTz5UD3VZ0H60zuKoeLohs; last_search_type=1; new_rent_list_kind_test=0; urlJumpIp=" + region +"; urlJumpIpByTxt=%E5%8F%B0%E5%8C%97%E5%B8%82; user_browse_recent=a%3A5%3A%7Bi%3A0%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%229889635%22%3B%7Di%3A1%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%229917447%22%3B%7Di%3A2%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%229743063%22%3B%7Di%3A3%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%229682581%22%3B%7Di%3A4%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%229737386%22%3B%7D%7D; c10f3143a018a0513ebe1e8d27b5391c=1; _gid=GA1.3.1018328732.1602865049; _gat=1; _gid=GA1.4.1018328732.1602865049; _dc_gtm_UA-97423186-1=1; _gat_UA-97423186-1=1; 591_new_session=" + cookies["591_new_session"],
            "X-CSRF-TOKEN": csrf_token
        })
    # print(res.text)
    content = res.content.decode()
    jsonData = json.loads(content)
    testData = jsonData["data"]["data"][0]
    print(testData["id"], testData["fulladdress"], testData["kind_name"], testData["price"])

    for item in jsonData["data"]["data"]:
        postTime = datetime.strptime(item["ltime"], "%Y-%m-%d %H:%M:%S")
        if (datetime.now() - postTime < timedelta(minutes=scanTime)):
            # LINE Notify
            headers_lineNotify = {
                "Authorization": "Bearer " + "JvPatlmOcSTev6vmDiWDrd8q08rMvuja257W9WVsZPA", # Wei Chen
                # "Authorization": "Bearer " + "9FiwZCAvCkGRD9a4wgHCNF74mciGW7pTCL1JbTWTMzu", # Group: 借我測Line Notify
                "Content-Type": "application/x-www-form-urlencoded"
            }

            params = {
                "message": "最新房屋出租資訊: " + item["fulladdress"] + " " + item["kind_name"]  + " " + item["price"] + "/月" + " https://rent.591.com.tw/rent-detail-" + str(item["id"]) + ".html" 
            }

            res_lineNotify = requests.post("https://notify-api.line.me/api/notify", headers=headers_lineNotify, params=params)
            print(res_lineNotify)

while True:
    schedule.enter(30, 0, rental591Crawler, (100, ))
    schedule.run()