import urllib.request
from bs4 import BeautifulSoup
import json

postDetails = {}

def scrapeDetails(url):
    headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}
    request = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(html,'html.parser')
    post = soup.find('div',attrs={'id':'siteTable'})
    commentArea = soup.find('div',attrs={'class':'commentarea'})
    title = post.find('a',attrs={'class':'title'}).text
    upvotes = post.find('div',attrs={'class':'score unvoted'}).text
    originalPoster = post.find('a',attrs={'class':'author'}).text
    postPermalink = request.full_url
    commentsCount = post.find('a',attrs={'class':'bylink comments may-blank'}).text
    comments = commentArea.find_all('div', attrs={'class':'entry unvoted'})
    extractedComments = []
    for comment in comments:
        if comment.find('form'):
            authorClass = comment.find('a',attrs={'class':'author'})
            if authorClass is None:
                commenter = ""
            else:
                commenter = authorClass.text
            commentText = comment.find('div',attrs={'class':'md'}).text
            commmentPermalink = comment.find('a',attrs={'class':'bylink'})['href']
            commentRecord = {
                'commenter':commenter,
                'commentText':commentText,
                'commentPermalink':commmentPermalink
            }
            extractedComments.append(commentRecord)
    postDetails.update({
        'title':title,
        'upvotes':upvotes,
        'originalPoster':originalPoster,
        'postPermalink':postPermalink,
        'commentsCount':commentsCount,
        'extractedComments':extractedComments
    })

def dumpDetails():
    with open('dumpPostScrape.json', 'w') as outfile:
        json.dump(postDetails, outfile)

if __name__ == "__main__":
    scrapeDetails(str(input("Which post do you want to scrape? ")))
    dumpDetails()