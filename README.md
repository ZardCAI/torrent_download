# Guidance

## Requirments
```
pip install libtorrent
pip install tqdm
```
## Usage
### Step 0
```
python anna_bookid_download.py
```
This command can download the md5 id of the books.
```
python anna_book_download_torrent.py
```
This command uses the ids to get the torrent files that contain the target books.

### Step 1
Unzip the torrent.zip doucument, and make the project directory looks like this.
```
root/
├── torrent
│   ├── 1
│   │   ├── 00da8d58144ff55c489913db76b43d48.torrent
│   │   └── ...
│   ├── 2
│   ├── 3
│   └── ...
├── textbook
├── torrent_selection.py
└── ...
```

### Step 2
Modify the line 45 (range(a, b)) in torrent_selection.py, to download the textbook from page a to page b.
Run:
```
nohup python torrent_selection.py &
```

### Step 3
Following the [link](https://zhuanlan.zhihu.com/p/608119275) to install aliyunpan. Then, use the commands to upload the downloaded textbooks to aliyunpan.
```
login -RefreshToken=xxxxxxxxxxxxxxxxxxxxxxxxxxx
upload /path/to/the/data_folder /textbook
```

## Points to note:
1. Based on my experience, currently the most stable way to download is using Codespaces. Downloading on a local computer or server results in almost zero speed.
2. Codespaces cannot use "screen," so it is preferable to run Codespaces using VSCode. This allows for longer durations, as disconnecting from Codespaces will cause the process to disappear.
