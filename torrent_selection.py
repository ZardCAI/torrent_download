import libtorrent as lt
import os

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
    while not handle.is_seed():
        s = handle.status()
        print('Downloading: {}% complete (down: {} kB/s up: {} kB/s peers: {})'.format(
            s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers))
        if s.progress == 1:
            break

    ses.remove_torrent(handle)

# 示例用法
file_path_format = './textbook/{}/'
torrent_file_format = './torrent/{}'
for i in range(1, 2):
    filelist = os.listdir(torrent_file_format.format(i))
    for file in filelist:
        file_path = file_path_format.format(i)
        torrent_file = torrent_file_format.format(i) + '/' + file
        file_index = file[0:32]
        print(torrent_file)
        print(file_path)
        print(file_index)
        download_torrent_file(torrent_file, file_path, file_index)
# torrent_file = '5c3b2e74c15fd0b911b652dcbc3f7441.torrent'  # 种子文件路径
# save_path = './'  # 下载保存路径
# file_index = '5c3b2e74c15fd0b911b652dcbc3f7441'   # 要下载的文件索引

# download_torrent_file(torrent_file, save_path, file_index)