from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import re
import json
import pandas as pd

path = Service(executable_path='geckodriver.exe')
driver = webdriver.Firefox(service=path)

firefox_option = Options()
firefox_option.add_argument('--headless')
firefox_option.add_argument('--window_size=1600, 900')
firefox_option.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')

domain = 'https://twitter.com'
# url = 'https://twitter.com/Cristiano'

print("Bot Tweets Scrape Twitter Account")
url = input('masukkan url akun: ')
file_name = input('masukkan nama file: ')

driver.get(url)
driver.implicitly_wait(60)
driver.maximize_window()
time.sleep(15)
html = driver.page_source
result = BeautifulSoup(html, 'html.parser')
# print(result)
time.sleep(3)

#nyari tweet via B_soup
artikel = result.find_all("article")
a=1

tweets =[]
for x in artikel:
    #isi tweet
    tweet_1 = x.find_all("span") 
    tweet = tweet_1[5].get_text()    
    if tweet =='':
        tweet = 'Re-Tweet Post<>'
    elif tweet =='·':
        tweet = tweet_1[6].get_text()
    #tampilkan tweet
    # print(f'({a}) {tweet}')

    #check span tweet
    # if a==1:
    #     c=0
    #     for ss in tweet_1:
    #         print(f'({c}) {ss}')
    #         c=c+1

    #link post
    detail_post =x.find_all("a")
    link_tweet = detail_post[3].attrs['href']
    full_link = domain+link_tweet
    #tampilkan link
    # print(full_link)

    #waktu post
    datetime_post = detail_post[3].find("time")
    if datetime_post:
        dt_detail = datetime_post.attrs['datetime']
        date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
        time_pattern = re.compile(r'\d{2}:\d{2}:\d{2}')
        date_post = re.search(date_pattern, dt_detail)
        time_post = re.search(time_pattern, dt_detail)     
        released = f"{date_post[0]} {time_post[0]}"         
        #tampilkan date time
        # print(released+ " (GMT+0)")
    # print('\n')
    report = {
        'tweet' : tweet,
        'post_link' : full_link,
        'datetime_(GMT+0)' : released
    }    
    tweets.append(report)
    #indeks maju
    a=a+1

# print(len(tweets))
for data in range(0,len(tweets)):
    indeks_twit = data +1
    print(f'({indeks_twit}) {tweets[data]}')

def cek_pos():
    post = driver.find_elements(
        by=By.XPATH,
        value='//article'
    )
    return len(post)

def position_y():
    browser = driver.get_window_position()
    return browser

def ambil_tweet(index):
    tweet = post_tweet(index)
    post_link =link(index)
    released= time_released(index)
    return {
        'tweet' : tweet,
        'post_link' : post_link,
        'datetime_post' : released
     }

def post_tweet(index):
    tweet = driver.find_element(
        by=By.XPATH,
        value=f'(//article/div/div/div[2]/div[2]/div[2]/div/span)[{index}]'
    ).text
    return tweet


def link(index):
    post_link = driver.find_element(
        by=By.XPATH,
        value=f'(//article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[3]/a)[{index}]'
    ).get_attribute('href')
    return post_link

def time_released(index):
    released = driver.find_element(
        by=By.XPATH,
        value=f'(//article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[3]/a/time)[{index}]'
    ).get_attribute('datetime')
    date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
    time_pattern = re.compile(r'\d{2}:\d{2}:\d{2}')

    date_post = re.search(date_pattern, released)
    time_post = re.search(time_pattern, released)            
    datetime_post = f"{date_post[0]},{time_post[0]}" 
    return datetime_post

# counting = cek_pos()

# for indeks in range(1,counting+1):
#     data = ambil_tweet(indeks)    
    
#     report = {
#         'tweet' : data['tweet'],        
#         'datetime' : data['datetime_post'],        
#         'link' : data['post_link']
#     }
#     tweets.append(report)

list_tweet = list(map(lambda twit: twit["datetime_(GMT+0)"], tweets))    

#scrolling page steps
scroll = True
factor = 0
y_axis=0
ping =0
while scroll:        
    for x in range(3):
        for y in range (0+factor,2+factor):
            ordinat = y*900
            driver.execute_script(f'window.scrollTo(0,{ordinat})')
            driver.implicitly_wait(30)
            time.sleep(1)

    time.sleep(5)
    html = driver.page_source
    result = BeautifulSoup(html, 'html.parser')        
    time.sleep(3)
    
    # status = y_axis    
    # if status >= 4000:
    if ping >= 15:
        scroll = False
    else:
        scroll = True
        factor = factor+2
        update_artikel = result.find_all("article")
        for d in update_artikel:
            #isi tweet
            try:
                tweet_1 = d.find_all("span")
                # if a==136 :
                #     b=0
                #     for cek in tweet_1:
                #         print(f"({b}) {cek}")
                tweet = tweet_1[5].get_text()
                if tweet =='':
                    tweet = 'Re-Tweet<>'
                #tampilkan tweet
                # print(f'({a+1}) {tweet}')

                #link post
                detail_post =d.find_all("a")
                link_tweet = detail_post[3].attrs['href']
                full_link = domain+link_tweet
                #tampilkan link
                # print(full_link)

                #waktu post
                datetime_post = detail_post[3].find("time")
                if datetime_post:
                    dt_detail = datetime_post.attrs['datetime']
                    date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
                    time_pattern = re.compile(r'\d{2}:\d{2}:\d{2}')
                    date_post = re.search(date_pattern, dt_detail)
                    time_post = re.search(time_pattern, dt_detail)     
                    released = f"{date_post[0]} {time_post[0]}"         
                    #tampilkan date time
                    # print(released+ " (GMT+0)")
                # print('\n')

            except IndexError:
                tweet = '(ditangguhkan sistem)'
                full_link = None
                released = ''

            report = {
                'tweet' : tweet,
                'post_link' : full_link,
                'datetime_(GMT+0)' : released
            }            
            if report['datetime_(GMT+0)'] not in list_tweet or report['datetime_(GMT+0)'] == '':    
                tweets.append(report)
                list_tweet = list(map(lambda twit: twit["datetime_(GMT+0)"], tweets))                
                # print(f'jumlah tweet masuk: {len(tweets)}')                                       
                print(f"({a}) {tweets[-1]}")
                # if a==80:
                #     c=0
                #     for ss in tweet_1:
                #         print(f'({c}) {ss}')
                #         c=c+1
                a=a+1  
                ping =0
            else:
                ping = ping +1

        coord_y = position_y()
        y_axis = y_axis - coord_y['y']         
        # print(f'koordinat y :{y_axis}')
                    
    time.sleep(0.5)

time.sleep(5)
driver.delete_all_cookies()

driver.quit()
print(f'total twit: {len(tweets)}')
# for x in tweets:
#     print(x)

csv_files = pd.DataFrame(tweets)

# csv_files.to_csv("Tweets_ku.csv")
csv_files.to_csv(f"{file_name}.csv")
print(csv_files)
print('Finished ...')

