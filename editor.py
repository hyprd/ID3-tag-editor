from mutagen.id3 import ID3
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TCON, TDRC, COMM
import yt_dlp
import sys
import os
import re

TagFrames = {
    1 : "TIT2", # Title
    2 : "TPE1", # Artist
    3 : "TALB", # Album Name
    4 : "TDRC", # Date
    5 : "COMM", # Comment
    6 : "TCON"  # Genre
}

old_file = ""
final_file = ""

def rename_yt_download(download):
    if download['status'] == 'finished':
        global old_file
        old_file = download['info_dict']['filename']
               
params = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'postprocessor_hooks' : [rename_yt_download],
}

def main():
    source = sys.argv[1]
    if "mp3" in source:
        edit_mp3(source)
    else:
        download_youtube(source, params)
        
def rename_file():
    global final_file
    while True:
        change_filename = input('Do you want to rename the file? (Y/n) ')
        if re.match("[Yy]", change_filename):
            new_name = input('Enter new file name: \n')
            if not new_name.endswith('.mp3'):
                    new_name += ".mp3"          
            os.rename(old_file.replace('.webm', '.mp3'), new_name)
            final_file = new_name
            break
        if re.match("[Nn]", change_filename):
            final_file = old_file.replace('.webm', '.mp3')
            print('File name will not be changed.')
            break
        else:
            print('Try again.')
            
def edit_file():
    while True:
        change_metadata = input('Do you want to edit the file metadata? (Y/n) ')
        if re.match("[Yy]", change_metadata):
            edit_mp3(final_file)
            break
        if re.match("[Nn]", change_metadata):
            print('File metadata will not be changed.')
            break
        else:
            print('Try again.')

def download_youtube(source, params):
    with yt_dlp.YoutubeDL(params) as yt:
        yt.download({source})
        rename_file()
        edit_file()
        
def edit_mp3(file):
    audio = ID3(file)
    tag = int(input('Edit metadata?\n1 - Title\n2 - Artist\n3 - Album\n4 - Year\n5 - Comment\n6 - Genre\n0 - No changes\n'))
    if(1 <= tag <= 6):
        while True:
            new_data = input('Enter new tag information \n')
            print("Before: \n" + audio.pprint())
            match tag:
                case 1:
                    audio[TagFrames[tag]] = TIT2(text=new_data)
                case 2:
                    audio[TagFrames[tag]] = TPE1(text=new_data)
                case 3:
                    audio[TagFrames[tag]] = TALB(text=new_data)
                case 4:
                    audio[TagFrames[tag]] = TDRC(text=new_data)
                case 5:
                    audio[TagFrames[tag]] = COMM(text=new_data)
                case 6:
                    audio[TagFrames[tag]] = TCON(text=new_data)
            audio.save()
            print("After: \n" + audio.pprint())
            repeat = input('Do you want to continue editing metadata? (Y/n) ')
            if re.match("[Yy]", repeat):
                edit_mp3(final_file)
                break
            if re.match("[Nn]", repeat):
                print('Metadata editing complete.')
                break
    elif tag == 0:
        print('Metadata will not be changed.')
    else:
        print('Try again.')
        edit_mp3(file)
if __name__ == "__main__":
    main()