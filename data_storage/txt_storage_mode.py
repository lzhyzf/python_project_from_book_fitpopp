import requests
from pyquery import PyQuery as pq

url = "https://www.zhihu.com/explore"
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
}
html = requests.get(url, headers = headers).text
doc = pq(html)
items = doc('.explore-tab .feed-item').items()
for item in items:
    question = item.find('h2').text()
    author = item.find('.author-link-line').text()
    answer = pq(item.find('.content').html()).text()
    with open('explore.txt', 'a', encoding = 'utf-8') as f:
        f.write('\n'.join([question, author, answer]))
        f.write('\n' + '=' * 50 + '\n')
