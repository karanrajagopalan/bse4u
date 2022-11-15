HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}


ALL_INDEX = {
    "URL": "https://api.bseindia.com/BseIndiaAPI/api/MktCapBoard/w?",
    "PAYLOAD": {
        "cat": "1",
        "type": "2"
    }
}

INDEX_SCRIPS = {
    "URL": "https://api.bseindia.com/BseIndiaAPI/api/GetMktData/w?",
    "PAYLOAD": {
        "ordcol": "TT",
        "strType": "index",
        "strfilter": ""
    }
}

SCRIP_MARKET_CAP = {
    "URL": "https://api.bseindia.com/BseIndiaAPI/api/StockTrading/w",
    "PAYLOAD": {
        "flag": "",
        "quotetype": "",
        "scripcode": ""
    }
}

SCRIP_CURRENT_PRICE = {
    "URL": "https://api.bseindia.com/BseIndiaAPI/api/getScripHeaderData/w",
    "PAYLOAD": {
        "scripcode": "",
        "Debtflag": "",
        "seriesid": ""
    }
}

SCRIP_HISTORIC_PRICE = {
    "URL": "https://api.bseindia.com/BseIndiaAPI/api/StockReachGraph/w",
    "PAYLOAD": {
        "scripcode": "",
        "flag": "",
        "fromdate": "",
        "todate": "",
        "seriesid": ""
    }
}

SCRIP_ANNOUNCEMENTS = {
    "URL": "https://api.bseindia.com/BseIndiaAPI/api/AnnGetData/w?",
    "PAYLOAD": {
        "strCat": "-1",
        "strPrevDate": "",
        "strScrip": "",
        "strSearch": "P",
        "strToDate": "",
        "strType": "C"
    }
}

