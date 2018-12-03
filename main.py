import model
import requests
from lxml import etree
import multiprocessing
import re

def next_page(pg):
    return model.PAGE_URL+str(pg)

def re_url(url):
    pattern = re.compile('.*\?')
    img_url = pattern.search(url).group(0)[6:-1]+'_1920x1080.jpg'
    print(model.IMG_URL+img_url)
    return model.IMG_URL+img_url

def get_img_items(list,start_page):
    html = requests.get(model.BASE_URL+start_page)
    html_etree = etree.HTML(html.text)
    list.append(html_etree.xpath('/html/body/div/div/div/a/@href'))
    next_page_href = html_etree.xpath('/html/body/div[4]/a[2]/@href')

    if(html_etree.xpath('/html/body/div[4]/a[2]/@href') and next_page_href[0] != '/?p=84'):  #设置停止页
        print(next_page_href[0])
        get_img_items(list = list,start_page=next_page_href[0])
    else:
        return list

def Downloads(url,title1):
    data = requests.get(url,headers = model.header)
    # print(data)
    with open('img\\' + title1 + '.jpg','wb+') as f:
        f.write(data.content)

if __name__ == '__main__':
    url_list = []
    jpg_list = []
    get_img_items(list = url_list,start_page=model.PAGE_URL+'1')    #设置起始页
    for i in url_list:
        for j in i:
            jpg_list.append(re_url(j))

    for title,url in enumerate(jpg_list):
        p1 = multiprocessing.Process(target=Downloads, args=(url, str(title, )))
        p1.start()
        p1.join()
    # re_url('/photo/AlanTuringNotebook_EN-AU7743633207?force=home_1')
    # Downloads('http://h1.ioliu.cn/bing/AlanTuringNotebook_EN-AU7743633207_1920x1080.jpg','1')
# print(re_url("/photo/AlanTuringNotebook_EN-AU7743633207?force=home_1"))