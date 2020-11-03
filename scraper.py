import urllib
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
#from selenium import webdriver

USER_AGENT = r'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 RuxitSynthetic/1.0 v6331309485 t38550 ath9b965f92 altpub'

def main():
    src_df = pd.read_csv('schools_la_not_low.csv')

    headers = {"user-agent" : USER_AGENT}
    #test = ['Ednovate - Brio College Prep']
    for i, row in src_df.iterrows():
    #for i, row in enumerate(test):
        # url = 'http://www.' + row['website']
        url = google_search(row['School'])
        #url = google_search(row)
        #print(url)
        soup = None
        response = None
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'lxml')
        except:
            print('unsuccessful')
            #print ('Unsucessful: ' + str(response.reason))
            continue

        emails = [result.text for result in soup.select("a[href*=mailto]")]
        phones = re.findall(r'\(?\b[2-9][0-9]{2}\)?[-. ]?[2-9][0-9]{2}[-. ]?[0-9]{4}\b', response.text)
        #phone = get_phone(soup)
        #email = get_email(soup)

        src_df.loc[i,'Phones'] = str(phones)
        src_df.loc[i,'Emails'] = str(emails)
        src_df.loc[i,'URL'] = str(url)
        print ('website:%s\nphones: %s\nemails: %s\n' %(url, phones, emails))

    src_df.to_csv('contacts_la_not_low.csv', index=False)
    '''
    url = google_search('solano middle school')
    #print(url)


    resp = requests.get(url, headers=headers)

    soup = None
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "lxml")
        #print('yeah!')
    else:
        raise Error('GET URL %s was unsuccessful. Reason: %s' % (url,resp.reason))

    results = []
    for tag in soup.find_all(string=re.compile("@")):
        results.append(tag.string)
        #print(tag.string)

    for link in soup.find_all('a'):

        print(link.prettify())
    '''

def google_search(query):
    # code modified from https://hackernoon.com/how-to-scrape-google-with-python-bo7d2tal
    query = query.replace(' ', '+')
    search_URL = f"https://google.com/search?q={query}"
    print(search_URL)
    #search_URL = 'https://google.com/search?q=' + query
    headers = {"user-agent" : USER_AGENT}
    resp = requests.get(search_URL, headers=headers)

    soup = None
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "lxml")
    else:
        raise Error('Query %s was unsuccessful. Reason: %s' % (query,resp.reason))

    link = None
    anchor = None

    # finds and returns first google result
    try:
        g = soup.find('div', class_='r')
        anchor = g.find('a')
    except:
        print('no div tag with class r exists')

    try:
        link = anchor['href']
    except:
        print('anchor is None?')

    return(link)

    '''
    results = []
    for g in soup.find_all('div', class_='r'):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            title = g.find('h3').text
            item = {
                "title": title,
                "link": link
            }
            results.append(item)
            break # only need first result

    return(results[0]['link'])
    '''

'''
# source: https://stackoverflow.com/questions/54416896/how-to-scrape-email-and-phone-numbers-from-a-list-of-websites
def get_phone(soup):
    try:
        phone = soup.select("a[href*=callto]")[0].text
        return phone
    except Error as e:
        print(e)
        pass

    try:
        phone = re.findall(r'\(?\b[2-9][0-9]{2}\)?[-][2-9][0-9]{2}[-][0-9]{4}\b', response.text)[0]
        return phone
    except:
        pass

    try:
       phone = re.findall(r'\(?\b[2-9][0-9]{2}\)?[-. ]?[2-9][0-9]{2}[-. ]?[0-9]{4}\b', response.text)[-1]
       return phone
    except:
        print ('Phone number not found')
        phone = ''
        return phone
'''

'''
# souce: https://stackoverflow.com/questions/54416896/how-to-scrape-email-and-phone-numbers-from-a-list-of-websites
def get_email(soup):
    try:
        email = re.findall(r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', response.text)[-1]
        return email
    except:
        pass

    try:
        email = soup.select("a[href*=mailto]")[-1].text
    except:
        print ('Email not found')
        email = ''
        return email
'''

if __name__ == '__main__':
    main()
