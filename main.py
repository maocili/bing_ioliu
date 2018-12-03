import model
import requests
from lxml import etree
import multiprocessing
import re
import pandas as pd


def next_page(pg):
    return model.PAGE_URL+str(pg)

def re_url(url):
    '''
    通过大图网页链接，通过正则得到图片标识
    :param url:必应大图链接抵制
    :return:返回一下可以下载的地址
    '''
    pattern = re.compile('.*\?')
    img_url = pattern.search(url).group(0)[6:-1]+'_1920x1080.jpg'
    print(model.IMG_URL+img_url)
    return model.IMG_URL+img_url

def get_img_items(url_list,start_page,info_list):
    '''
    获取页面中的img大图网页链接
    :param url_list:用于存放大图网页链接
    :param start_page:起始页
    :param info_list:存放照片信息
    :return:在mian中的url_list中直接修改
    '''
    html = requests.get(model.BASE_URL+start_page)
    html_etree = etree.HTML(html.text)
    url_list.append(html_etree.xpath('/html/body/div/div/div/a/@href'))
    next_page_href = html_etree.xpath('/html/body/div[4]/a[2]/@href')

    title = html_etree.xpath('/html/body/div[3]/div/div/div[1]/h3/text()')
    calendar = html_etree.xpath('/html/body/div[3]/div/div/div[1]/p[1]/em/text()')
    location = html_etree.xpath('/html/body/div[3]/div/div/div[1]/p[2]/em/text()')
    eye = html_etree.xpath('//p[@class="view"]/em/text()')
    heart = html_etree.xpath('/html/body/div[3]/div/div/div[2]/span/em/text()')
    download = html_etree.xpath('/html/body/div[3]/div/div/div[2]/a[2]/em/text()')
    img_url = html_etree.xpath('/html/body/div/div/div/a/@href')

    for title,calendar,location,eye,heart,download,img_url in zip(title,calendar,location,eye,heart,download,img_url):
        info_list.append([title,calendar,location,eye,heart,download,model.BASE_URL+img_url])


    if(html_etree.xpath('/html/body/div[4]/a[2]/@href') and next_page_href[0] != '/?p=20'):  #设置停止页
        print(next_page_href[0])
        get_img_items(url_list = url_list,start_page=next_page_href[0],info_list=info_list)

    else:
        return url_list,info_list

def Downloads(url,title1):
    '''
    下载图片于跟目录下的img文件夹
    :param url:下载地址 xxxx.jpg
    :param title1:文件名称
    :return:
    '''
    data = requests.get(url,headers = model.header)
    # print(data)
    with open('img\\' + title1 + '.jpg','wb+') as f:
        f.write(data.content)


def info_save_excel(info_list):
    df = pd.DataFrame(info_list,columns=['title','calendar','location','eye','heart','download','img_url'])
    df.to_excel('img_info.xlsx')


if __name__ == '__main__':
    url_list = []
    jpg_list = []
    info_list = []
    get_img_items(url_list = url_list,start_page=model.PAGE_URL+'1',info_list = info_list)    #设置起始页

    info_save_excel(info_list)
    p1 = multiprocessing.Process(target=info_save_excel, args=(info_list,))
    p1.start()

    for i in url_list:
        for j in i:
            jpg_list.append(re_url(j))

    for title,url in enumerate(jpg_list):
        p2 = multiprocessing.Process(target=Downloads, args=(url, str(title, )))
        p2.start()
        p2.join()

# re_url('/photo/AlanTuringNotebook_EN-AU7743633207?force=home_1')
# Downloads('http://h1.ioliu.cn/bing/AlanTuringNotebook_EN-AU7743633207_1920x1080.jpg','1')
# print(re_url("/photo/AlanTuringNotebook_EN-AU7743633207?force=home_1"))