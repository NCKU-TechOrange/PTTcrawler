PTTcrawler
==========

A crawler for web PTT Gossiping

ptt八卦版的網路爬蟲，解析其中資料，爬完會自動產生 data.json，格式如下

    "a_ID": 編號,
    "b_作者": 作者名,
    "c_標題": 標題,
    "d_日期": 發文時間,
    "e_ip": 發文ip,
    "f_內文": 內文,
    "g_推文": {
        "推文編號": {
            "狀態": 推 or 噓 or →,
            "留言內容": 留言內容,
            "留言時間": 留言時間,
            "留言者": 留言者
        }
    },
    "h_推文總數": {
        "all": 推文數目,
        "b": 噓數,
        "g": 推數,
        "n": →數
    }
###執行環境
python 3.x

###如何使用
--------------

    $ python3 pttcrawler.py <BOARDNAME> <START_INDEX> <END_INDEX> <OUTPUT_PATH>

BOARDNAME: 想要爬的版
START_INDEX / END_INDEX: 爬的網址index範圍
OUTPUT_PATH: 最後爬下來的資料輸出的檔名(暫時只支援 .json 檔)

###example
--------------

    $ python3 pttcrawler.py 200 500
    
則會爬取
https://www.ptt.cc/bbs/Gossiping/index200.html 至
https://www.ptt.cc/bbs/Gossiping/index500.html
之間的內容。
    
