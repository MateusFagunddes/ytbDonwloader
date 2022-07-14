from time import sleep
from pytube import YouTube, Playlist, request
from tqdm import tqdm
from colorama import init, Fore

init(autoreset=True)

def getFormat():
    format = input('Insert the file format (.mp3, .mp4) REMEMBER THE DOT: ')
    return format

def obMsg(download: bool):
    phrases = ['CONNECTING WITH YOUTUBE API', 'DOWNLOADING VIDEO']
    phrase = phrases[0] if download else phrases[1]
    cor = Fore.YELLOW if download else Fore.BLUE
    for i in phrase:
        print(f'{cor}{i}', end='', flush=True)
        sleep(0.01)
    print('')

def download_video(link, format:str = '.mp4'):
    obMsg(False)
    def progress_bar(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        downloaded = total_size - bytes_remaining
        percent = (downloaded / total_size) * 100
        print(f'{Fore.YELLOW}|\r', end='', flush=True)   
        tqdm.write(f' {Fore.MAGENTA}{round(percent,2)}%', end='\r\r')
    if format:
        pass
    else:
        format = '.mp4'
    path = r'videos/'
    youtube = YouTube(link, on_progress_callback= progress_bar)
    lengthVideo = youtube.length /60
    video = youtube.streams.get_highest_resolution()
    if format == '.mp3':
        video = youtube.streams.get_audio_only()
        path = r'audio/'    
    print(f'{Fore.YELLOW}┌' + f'{Fore.YELLOW}─' * (len(video.title) + 42) + f'{Fore.YELLOW}┐')
    print(f'{Fore.YELLOW}| NAME: ', video.title, ' '*32,f"{Fore.YELLOW}|")
    print(f'{Fore.YELLOW}| SIZE: ', round((video.filesize / (1024**2)),2), 'MB')
    print(f'{Fore.YELLOW}| ', end='')
    video.download(filename= f"{youtube.title}{format}", output_path= path, )
    print(f'\n{Fore.YELLOW}|{Fore.GREEN} DOWNLOAD CONCLUDED!', " " *(len(video.title)+20), f'{Fore.YELLOW}|')
    print(f'{Fore.YELLOW}└' + f'{Fore.YELLOW}─' * (len(video.title) + 42) + f'{Fore.YELLOW}┘')

def download_from_txt(file, format:str = '.mp4'):
    videoList = []   
    with open(file, 'r') as f:
        for line in f:
            videoList.append(line)
    for i in videoList: 
        download_video(i, format)
    
def playlistInfo(format:str = '.mp4'):
    def download_playlist(playlist_url, format:str = '.mp4'):
        playlist = Playlist(playlist_url)
        for video in videoUrl:
            download_video(video, format) 
    url = input('INSERT PLAYLIST URL: ')
    obMsg(True)
    playlist = Playlist(url)
    playlistTitle = playlist.title
    countVideos = playlist.length
    videoUrl = playlist.video_urls
    videoName = []
    for i, l in enumerate(videoUrl):
        videoName.append(YouTube(videoUrl[i]).title)
    print(f'{Fore.BLUE}PLAYLIST NAME:', {playlistTitle}, f'\n{Fore.BLUE}NUMBER OF VIDEOS IN THE PLAYLIST:', countVideos)
    if countVideos <= 5:
        for i, name in enumerate(videoName):
            print(f'{Fore.BLUE}NAME OF #{i+1} VIDEO: ', name, 
            f'{Fore.BLUE}  SIZE: ', round((YouTube(videoUrl[i]).streams.get_highest_resolution().filesize / (1024**2)),2), 'MB')
    else:
        for i, name in enumerate(videoName):
            if i < 5:
                print(f'{Fore.BLUE}NAME OF #{i+1} VIDEO: ', name, 
                f'{Fore.BLUE}  SIZE: ', round((YouTube(videoUrl[i]).streams.get_highest_resolution().filesize / (1024**2)),2), 'MB')
            else:
                print(f'{Fore.BLUE}AND MORE {countVideos - 5} VIDEOS')
                break
    download = input('\n\nDOWNLOAD? (Y/N) ')
    if download == 's':
        download_playlist(url, format)

def onlyPlaylistDownload(format:str = '.mp4'):
    url = input('INSERT PLAYLIST URL')
    playlist = Playlist(url)
    videoUrl = playlist.video_urls
    for i, l in enumerate(videoUrl):
        download_video(videoUrl[i], format)

while True:
    op = input(f'{Fore.GREEN} 1 - DOWNLOAD A SINGLE VIDEO\n2 - DOWNLOAD A PLAYLIST\n3 - DOWNLOAD VIDEOS FROM A TXT FILE \n{Fore.RESET}YOUR CHOICE: ')
    if op == '1':
        link = input('VIDEO URL: ')
        download_video(link, getFormat())
    elif op == '2':      
        info = input(f'{Fore.GREEN}1 - KNOW MORE INFOS ABOUT THE PLAYLIST\n2 - JUST DOWNLOAD\n{Fore.RESET}YOUR CHOICE: ')
        if info == '1':
            playlistInfo(getFormat())
        elif info == '2':
            onlyPlaylistDownload(getFormat())    
    elif op == '3':
        file = input('NAME OF THE TXT FILE (REMEMBER OF THE DOT): ')
        download_from_txt(file, getFormat())

    continueQ = input(f'{Fore.GREEN}CONTINUE? (Y/N) ').lower()
    if continueQ == 'n':
        break           