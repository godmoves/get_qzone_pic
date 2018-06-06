#!coding:utf-8
import json
from multiprocessing import Semaphore, Process, freeze_support
import requests
from selenium import webdriver
import time
from urllib.request import urlopen

login_uin = '123456789'  # your own qq
pwd = '1233456789'       # your password
album_uin = '123456789'  # your target qq


def download_pic(s, url, index):
    s.acquire()
    path = str(index) + ".jpg"
    data = urlopen(url).read()
    f = open('./pic/' + path, "wb")
    f.write(data)
    f.close()
    s.release()


def main():
    s = requests.Session()

    # login in browser
    driver = webdriver.Chrome()
    driver.set_window_size(1000, 600)
    driver.get('https://mobile.qzone.qq.com')
    driver.find_element_by_id('u').clear()
    driver.find_element_by_id('u').send_keys(login_uin)
    driver.find_element_by_id('p').clear()
    driver.find_element_by_id('p').send_keys(pwd)
    driver.find_element_by_id('go').click()
    # waiting for qzonetoken
    while True:
        qzonetoken = driver.execute_script("return window.shine0callback")
        if qzonetoken:
            break
        time.sleep(0.1)
    # read cookies and shutdown browser
    cookies = driver.get_cookies()
    driver.quit()

    cookies_ = {}
    for cookie in cookies:
        if cookie['name'] == 'p_skey':
            skey = cookie['value']
        cookies_[cookie['name']] = cookie['value']

    # calculate gtk
    e = 5381
    for i in range(len(skey)):
        e = e + (e << 5) + ord(skey[i])
    g_tk = str(2147483647 & e)

    # read album lists
    requests.utils.add_dict_to_cookiejar(s.cookies, cookies_)
    url = "https://mobile.qzone.qq.com/list?qzonetoken=" + qzonetoken + "&g_tk=" + \
        g_tk + "&format=json&list_type=album&action=0&res_uin=" + album_uin + "&count=50"
    r = s.get(url)
    data = json.loads(r.text.encode('utf-8'))

    i = 0
    # set number of processes
    sp = Semaphore(15)
    for album in data['data']['vFeeds']:
        process = []
        print('album name:' + album['pic']['albumname'])
        print('album id:' + album['pic']['albumid'])
        print('pic num:' + str(album['pic']['albumnum']))
        print('start downloading...')
        # read pic list in current album
        url = "https://h5.qzone.qq.com/webapp/json/mqzone_photo/getPhotoList2?qzonetoken=" + qzonetoken + \
            "&g_tk=" + g_tk + "&uin=" + album_uin + \
            "&albumid=" + album['pic']['albumid'] + "&ps=0"
        r = s.get(url)
        photo_datas = json.loads(r.text.encode('utf-8'))
        for T in photo_datas['data']['photos']:
            for pic in photo_datas['data']['photos'][T]:
                print('Index:' + str(i) + ' pic name:' +
                      pic['picname'] + '，url:' + pic['1']['url'])
                p = Process(target=download_pic, args=(sp, pic['1']['url'], i,))
                process.append(p)
                i += 1
        print("=" * 30)

        for p in process:
            p.start()

        for p in process:
            p.join()


if __name__ == "__main__":
    freeze_support()
    main()
