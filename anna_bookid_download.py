import requests
import os
import bs4
import re
import json
from tqdm import tqdm
from time import sleep
from glob import glob
from ntpath import basename
from bs4 import BeautifulSoup, Comment
import multiprocessing
import random
import sys
user_agent = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
    'Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
    'Mozilla/4.0(compatible;MSIE8.0;WindowsNT6.0;Trident/4.0)',
    'Mozilla/4.0(compatible;MSIE7.0;WindowsNT6.0)',
    'Mozilla/4.0(compatible;MSIE6.0;WindowsNT5.1)',
    'Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1',
    'Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1',
    'Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11',
    'Opera/9.80(Macintosh;IntelMacOSX10.6.8;U;en)Presto/2.8.131Version/11.11',
    'Mozilla/5.0(WindowsNT6.1;WOW64;rv:54.0)Gecko/20100101Firefox/54.0',
    'Mozilla/5.0(WindowsNT10.0;WOW64;rv:54.0)Gecko/20100101Firefox/54.0',
    'Mozilla/5.0(Macintosh;IntelMacOSX10.12;rv:54.0)Gecko/20100101Firefox/54.0',
    'Mozilla/5.0(WindowsNT6.1;WOW64;rv:55.0)Gecko/20100101Firefox/55.0',
    'Mozilla/5.0(WindowsNT10.0;WOW64;rv:55.0)Gecko/20100101Firefox/55.0',
    'Mozilla/5.0(Macintosh;IntelMacOSX10.12;rv:55.0)Gecko/20100101Firefox/55.0',
    'Mozilla/5.0(WindowsNT6.1;WOW64;rv:56.0)Gecko/20100101Firefox/56.0',
    'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Maxthon2.0)',
    'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;TencentTraveler4.0)',
    'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)',
    'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;TheWorld)',
    'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;360SE)',
    'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;AvantBrowser)',
    'Mozilla/5.0(iPhone;U;CPUiPhoneOS4_3_3likeMacOSX;en-us)AppleWebKit/533.17.9(KHTML,likeGecko)Version/5.0.2Mobile/8J2Safari/6533.18.5',
    'Mozilla/5.0(iPad;U;CPUOS4_3_3likeMacOSX;en-us)AppleWebKit/533.17.9(KHTML,likeGecko)Version/5.0.2Mobile/8J2Safari/6533.18.5',
    'Mozilla/5.0(iPod;U;CPUlikeMacOSX;en-us)AppleWebKit/420.1(KHTML,likeGecko)Version/3.0Mobile/3B48bSafari/419.3',
    'Mozilla/5.0(Linux;U;Android2.3.7;en-us;NexusOneBuild/FRF91)AppleWebKit/533.1(KHTML,likeGecko)Version/4.0MobileSafari/533.1',
    'MQQBrowser/26(Mozilla/5.0;iPhoneCPUiPhoneOS7.1.2likeMacOSX)AppleWebKit/537.51.2(KHTML,likeGecko)Mobile/11D257Safari/9537.53',
    'Mozilla/5.0(Linux;U;Android4.1.2;en-us;GT-N7100Build/JZO54K)AppleWebKit/534.30(KHTML,likeGecko)Version/4.0MobileSafari/534.30',
    'Opera/9.80(Android2.3.4;Linux;OperaMobi/build-1107180945;U;en-GB)Presto/2.8.149Version/11.10',
    'Mozilla/5.0(Macintosh;IntelMacOSX10_7_3)AppleWebKit/535.20(KHTML,likeGecko)Chrome/19.0.1036.7Safari/535.20',
    'Mozilla/5.0(Linux;U;Android3.0;en-us;XoomBuild/HRI39)AppleWebKit/534.13(KHTML,likeGecko)Version/4.0Safari/534.13',
    'Mozilla/5.0(BlackBerry;U;BlackBerry9800;en)AppleWebKit/534.1+(KHTML,likeGecko)Version/6.0.0.337MobileSafari/534.1+',
    'Mozilla/5.0(hp-tablet;Linux;hpwOS/3.0.0;U;en-US)AppleWebKit/534.6(KHTML,likeGecko)wOSBrowser/233.70Safari/534.6TouchPad/1.0',
    'Mozilla/5.0(SymbianOS/9.4;Series60/5.0NokiaN97-1/20.0.019;Profile/MIDP-2.1Configuration/CLDC-1.1)AppleWebKit/525(KHTML,likeGecko)BrowserNG/7.1.18124',
    'Mozilla/5.0(PLAYSTATION3;2.00)',
    'Mozilla/5.0(iPhone;CPUiPhoneOS7_0likeMacOSX)AppleWebKit/537.51.1(KHTML,likeGecko)Version/7.0Mobile/11A465Safari/9537.53',
    'Mozilla/5.0(compatible;MSIE9.0;WindowsPhoneOS7.5;Trident/5.0;IEMobile/9.0;HTC;Titan)',
]

error_url_file = 'error_pdfdrive_urls.txt'

output_dir = './download'
# torrent_file = '/home/yuxiang/med-llm/data_preprocess/medical_mllm/0_Dataset_Check/archive/067_MedBooks/md5_to_torrent.json'
# with open(torrent_file, 'r') as f:
#     torrent_dict = json.load(f)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

url_format = 'https://annas-archive.org/search?index=&q=medical&content=book_nonfiction&ext=pdf&sort=&page={}'

total = -1

m = 36
n = 37

for page_idx in tqdm(range(m, n)):
    # if os.path.exists(output_dir + '/test{}.json'.format(page_idx)):
    #     continue
    out_data = []
    cur_url = url_format.format(page_idx)
    response = requests.get(cur_url, headers={'User-Agent': random.choice(user_agent)})
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    divs = soup.find_all('div', {'class': 'h-[125] flex flex-col justify-center'})
    divs1 = soup.find_all('div', {'class': 'h-[125] flex flex-col justify-center js-scroll-hidden'})
    for div in divs:
        x = div.find('a')
        out_data.append(x['href'])
    for div in divs1:
        comments = div.find_all(string=lambda text: isinstance(text, Comment))
        comment = comments[0]
        x = re.findall(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"', comment)
        x = x[0]
        # x = x.replace('\'', '')
        # x = x.replace(']', '')
        # print(x)
        out_data.append(x)
    # print(len(out_data))
    sleep(1)
    output_file = output_dir + '/test{}.json'.format(page_idx)
    with open(output_file, 'w') as f:
        json.dump(out_data, f, indent=2, ensure_ascii=False)

print('Total number of items:', len(out_data))
print(f'Saved to {output_file}')