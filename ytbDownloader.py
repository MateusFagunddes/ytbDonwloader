from time import sleep
from pytube import YouTube, Playlist, request
from tqdm import tqdm
from colorama import init, Fore
init(autoreset=True)

def getFormat():
    formato = input('Digite o formato do arquivo (.mp3, .mp4): ')
    return formato

def obMsg(download: bool):
    frases = ['Conectando com a API do Youtube', 'Baixando o video']
    frase = frases[0] if download else frases[1]
    cor = Fore.YELLOW if download else Fore.BLUE
    for i in frase:
        print(f'{cor}{i}', end='', flush=True)
        sleep(0.01)
    print('')

def download_video(link, formato:str = '.mp4'):
    obMsg(False)
    def progress_bar(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        downloaded = total_size - bytes_remaining
        percent = (downloaded / total_size) * 100
        print(f'{Fore.YELLOW}|\r', end='', flush=True)   
        tqdm.write(f' {Fore.MAGENTA}{round(percent,2)}%', end='\r\r')
    if formato:
        pass
    else:
        formato = '.mp4'
    path = r'videos/'
    youtube = YouTube(link, on_progress_callback= progress_bar)
    lengthVideo = youtube.length /60
    video = youtube.streams.get_highest_resolution()
    if formato == '.mp3':
        video = youtube.streams.get_audio_only()
        path = r'audio/'    
    print(f'{Fore.YELLOW}┌' + f'{Fore.YELLOW}─' * (len(video.title) + 42) + f'{Fore.YELLOW}┐')
    print(f'{Fore.YELLOW}| nome: ', video.title, ' '*32,f"{Fore.YELLOW}|")
    print(f'{Fore.YELLOW}| tamanho: ', round((video.filesize / (1024**2)),2), 'MB')
    print(f'{Fore.YELLOW}| ', end='')
    video.download(filename= f"{youtube.title}{formato}", output_path= path, )
    print(f'\n{Fore.YELLOW}|{Fore.GREEN} Download concluído!', " " *(len(video.title)+20), f'{Fore.YELLOW}|')
    print(f'{Fore.YELLOW}└' + f'{Fore.YELLOW}─' * (len(video.title) + 42) + f'{Fore.YELLOW}┘')

def download_from_txt(file, formato:str = '.mp4'):
    listaVideos = []   
    with open(file, 'r') as f:
        for line in f:
            listaVideos.append(line)
    for i in listaVideos: 
        download_video(i, formato)
    
def playlistInfo(formato:str = '.mp4'):
    def download_playlist(playlist_url, formato:str = '.mp4'):
        playlist = Playlist(playlist_url)
        for video in videoUrl:
            download_video(video, formato) 
    url = input('Digite a url da playlist: ')
    obMsg(True)
    playlist = Playlist(url)
    playlistTitle = playlist.title
    countVideos = playlist.length
    videoUrl = playlist.video_urls
    videoName = []
    for i, l in enumerate(videoUrl):
        videoName.append(YouTube(videoUrl[i]).title)
    print(f'{Fore.BLUE}Nome da Playlist:', {playlistTitle}, f'\n{Fore.BLUE}numero de videos na Playlist:', countVideos)
    if countVideos <= 5:
        for i, nome in enumerate(videoName):
            print(f'{Fore.BLUE}Nome do #{i+1} video: ', nome, 
            f'{Fore.BLUE}  tamanho: ', round((YouTube(videoUrl[i]).streams.get_highest_resolution().filesize / (1024**2)),2), 'MB')
    else:
        for i, nome in enumerate(videoName):
            if i < 5:
                print(f'{Fore.BLUE}Nome do #{i+1} video: ', nome, 
                f'{Fore.BLUE}  tamanho: ', round((YouTube(videoUrl[i]).streams.get_highest_resolution().filesize / (1024**2)),2), 'MB')
            else:
                print(f'{Fore.BLUE}e mais {countVideos - 5} videos')
                break
    download = input('\n\nDeseja baixar a playlist? (s/n) ')
    if download == 's':
        download_playlist(url, formato)

def onlyPlaylistDownload(formato:str = '.mp4'):
    url = input('Digite a url da playlist: ')
    playlist = Playlist(url)
    videoUrl = playlist.video_urls
    for i, l in enumerate(videoUrl):
        download_video(videoUrl[i], formato)

while True:
    op = input(f'{Fore.GREEN}1 - Para baixar um video\n2 - Para baixar uma playlist\n3 - Para baixar uma serie de videos de um arquivo .txt\n{Fore.RESET}Sua escolha: ')
    if op == '1':
        link = input('Digite a url do video: ')
        download_video(link, getFormat())
    elif op == '2':      
        info = input(f'{Fore.GREEN}1 - Saber informações da playlist\n2 - Baixar playlist\n{Fore.RESET}Sua escolha: ')
        if info == '1':
            playlistInfo(getFormat())
        elif info == '2':
            onlyPlaylistDownload(getFormat())    
    elif op == '3':
        file = input('Digite o nome do arquivo .txt: ')
        download_from_txt(file, getFormat())

    desejaContinuar = input(f'{Fore.GREEN}Deseja continuar? (s/n) ')
    if desejaContinuar == 'n':
        break            