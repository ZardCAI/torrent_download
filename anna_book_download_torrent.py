import requests
import os
import bs4
import json
from tqdm import tqdm
from time import sleep
from glob import glob
from ntpath import basename
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

def download_torrent_file(url, save_path):
    response = requests.get(url, headers={'User-Agent': random.choice(user_agent)})
    with open(save_path, 'wb') as f:
        f.write(response.content)

error_url_file_format = './torrent/{}/error.txt'

output_dir = f'./download'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# url_format = 'https://openi.nlm.nih.gov/api/search?favor=r&it=' + image_type_mapping[modality] + '&m={}&n={}'
url_root = 'https://annas-archive.org'
# https://www.pdfdrive.com/download.pdf?id=58901585&h=f674e4963f959e7abdf7e05da666c0fc&u=cache&ext=pdf
url_format = 'https://annas-archive.org{}'
download_path = './torrent/{}/{}.torrent'

meta_file_format = 'test{}.json'
book_urls = os.path.join(output_dir, 'anna_download_urls.txt')
if os.path.exists(book_urls):
    with open(book_urls, 'r') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
else:
    lines = None


for i in range(36, 37):
    error_url_file = error_url_file_format.format(i)
    os.makedirs('./torrent/{}'.format(i), exist_ok=True)
    error_lines = []
    if os.path.exists(error_url_file):
        with open(error_url_file, 'r') as f:
            error_lines = f.readlines()
        error_lines = [line.strip() for line in error_lines]

    meta_file = meta_file_format.format(i)
    with open(os.path.join(output_dir, meta_file), 'r') as f:
        meta_data = json.load(f)
    for item in tqdm(meta_data):
        cur_url = f"{url_root}{item}"
        if cur_url in error_lines:
            continue
        book_id = item[-32:]
        response = requests.get(cur_url, headers={'User-Agent': random.choice(user_agent)})
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        # button type="button" id="previewButtonMain" class="btn btn-warning btn-responsive"
        # info = soup.find('div', {"id": "md5-panel-downloads", "role": "tabpanel", "aria-labelledby": "md5-tab-downloads",})
        # x = info.find_all('a', {"class": "js-download-link"})
        info = soup.find('span', {"class": "text-sm text-gray-500",})
        # print(info)

        if info is None:
            print(f"Error: {cur_url}")
            with open(error_url_file, 'a') as f:
                f.write(cur_url + '\n')
            continue
        # data_preview = info['data-preview']
        # assert "session=" in data_preview
        # sess_id = data_preview.split('session=')[-1]
        x = info.find('a')
        down_url = url_format.format(x['href'])
        if lines is None or lines is not None and down_url not in lines:
            with open(book_urls, 'a') as f:
                f.write(down_url + '\n')
        os.makedirs('./torrent/{}'.format(i), exist_ok=True)
        download_torrent_file(down_url, download_path.format(i, book_id))
        sleep(0.5)

    
