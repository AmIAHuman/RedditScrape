import urllib.request
from bs4 import BeautifulSoup
import json
import PostScrape

extractedRecords = []

def crawlPagesUpTo(pages):
    if int(pages) < 1:
        print("Invalid integer.")
        return
    headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}
    print('Extracting from a total of %d links.'%(int(pages) * 25))
    for page in range(int(pages)):
        curr = "https://old.reddit.com/top/"
        if page != 0:
            curr += "?count=" + str(page * 25) + "&after=t3_" + str(getRecords()[-1]['tag'])
        request = urllib.request.Request(curr, headers=headers)
        html = urllib.request.urlopen(request).read()
        soup = BeautifulSoup(html, 'html.parser')
        siteTable = soup.find("div", attrs={'id':'siteTable'})
        links = siteTable.find_all("a", class_="title")
        commentLinks = siteTable.find_all("a", class_="bylink comments may-blank")
        for index in range(25):
            PostScrape.resetDetails()
            title = links[index].text
            url = links[index]['href']
            comments = commentLinks[index].text
            commenturl = commentLinks[index]['href']
            tag = commenturl.split('/')[6]
            ad = False
            print('%d. Extracting data from %s.'%((index + 1), commenturl))
            PostScrape.scrapeDetails(commenturl)
            postDetails = PostScrape.getDetails()
            if not url.startswith('http'):
                url = "https://old.reddit.com" + url
            if not commenturl.startswith('http'):
                commenturl = "https://old.reddit.com" + commenturl
            if url.startswith('https://alb.reddit.com') or url.startswith('http://alb.reddit.com'):
                ad = True
            record = {
                'title':title,
                'url':url,
                'comments':comments,
                'commenturl':commenturl,
                'tag':tag,
                'ad':ad,
                'postDetails':postDetails
            }
            extractedRecords.append(record)
        print('Finished extracting from a total of %d links.'%(int(pages) * 25))

def resetRecords():
    extractedRecords.clear()

def dumpRecords():
    with open('dumpCrawl.json', 'w') as outfile:
        json.dump(extractedRecords, outfile)

def getRecords():
    return extractedRecords

if __name__ == "__main__":
    crawlPagesUpTo(input("How many pages would you like to crawl? "))
    dumpRecords()