import requests
import time

list = {
    2017: 2198,
    2016: 2653,
    2015: 2378,
    2014: 2288,
    2013: 2257,
    2012: 2549,
    2011: 2323,
    2010: 2295,
    2009: 1804,
    2008: 2009,
    2007: 1951,
    2006: 1660,
    2005: 1361,
    2004: 1110,
    2003: 1053,
    2002: 1181,
    2001: 1506,
    2000: 1841,
    1999: 1
}

# 2009 = old url
# http://www.wipo.int/amc/en/domains/decisions/html/%s/%s.html
# 1 = year
# 2 = lowercase case num
#
# 2010+ = new url
# http://www.wipo.int/amc/en/domains/search/text.jsp?case=%s
# 1 = uppercase case num
def getUrl(year, num):
    if year <= 2009:
        return "http://www.wipo.int/amc/en/domains/decisions/html/{0}/d{1}-{2:04d}.html".format(
            year,
            year,
            num
        )
    return "http://www.wipo.int/amc/en/domains/search/text.jsp?case=D{0}-{1:04d}".format(
        year,
        num
    )

def getFileName(year, num):
    return "WIPO/D{0}-{1:04d}.html".format(
        year,
        num
    )

def download(year, num):
    try:
        filename = getFileName(year, num)
        url = getUrl(year, num)
        response = requests.get(url, allow_redirects=False)
        if response.status_code == 200:
            with open(filename, "wb") as file:
                file.write(response.content)
        else:
            print("SERVER RESPONDED WITH {}", response.status_code)
    except Exception as e:
        print("DOWNLOAD FAILED {}", e)

for (year, num) in list.items():
    while num > 0:
        print("Processing year {}, case {}".format(year, num))
        download(year, num)
        num -= 1
        time.sleep(0.1)
