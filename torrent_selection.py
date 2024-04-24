import libtorrent as lt
import os
from tqdm import tqdm
from multiprocessing import Pool

def download_file(args):
    torrent_file, file_path, file_index = args
    download_torrent_file(torrent_file, file_path, file_index)

def download_torrent_file(torrent_file, save_path, file_index):
    ses = lt.session()
    info = lt.torrent_info(torrent_file)
    params = {
        'save_path': save_path,
        'storage_mode': lt.storage_mode_t(2),  # 设置存储模式为存储所有文件
        'ti': info
    }
    handle = ses.add_torrent(params)
    files = handle.get_torrent_info().files()
    for i, file in enumerate(files):
        if file.path[8:] == file_index:
            handle.file_priority(i, 1)
        else:
            handle.file_priority(i, 0)


    # 等待种子下载完成
    count = 0
    while not handle.is_seed():
        count += 1
        s = handle.status()
        if count % 50000 == 0:
            print('Downloading: {}% complete (down: {} kB/s up: {} kB/s peers: {} count: {})'.format(
                s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, count))
        if (s.progress == 1) or (s.progress == 0 and count > 1000000) or (s.download_rate == 0 and count > 10000000):
            break

    ses.remove_torrent(handle)

# 示例用法
file_path_format = './textbook/{}/'
torrent_file_format = './torrent/{}'
download_args = []

for i in range(22, 32): #下载22页-32页的书籍
    filelist = os.listdir(torrent_file_format.format(i))
    for file in tqdm(filelist):
        if file == 'error.txt':
            continue
        file_path = file_path_format.format(i)
        torrent_file = torrent_file_format.format(i) + '/' + file
        file_index = file[0:32]
        download_args.append((torrent_file, file_path, file_index))

with Pool(processes=2) as pool:  # 这里的2是进程数，你可以根据你的实际情况来修改这个值
    pool.map(download_file, download_args)
