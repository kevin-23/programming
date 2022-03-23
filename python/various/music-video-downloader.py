'''Music and videos downloader. Python 3.7.3 is required to run the script.
   I recommend execute the first time the option 1.
   This script runs on Debian Buster.'''

import os
from tkinter import filedialog
from tkinter import *

#This function contains the name of the program.
def program_name():
    os.system('clear')
    print('˖ ˖ ˖   MUSIC AND VIDEO DOWNLOADER   ˖ ˖ ˖\n')

#This function installs the requeriments.
def requeriments():
    while True:
        program_name()
        print('To run the script you need youtube-dl and ffmpeg.\
              \nDo you want to install them? Superuser privileges is required. y/N')
        option = input('\n--> ')
        option = option.lower()
        if option == 'y' or option == 'yes':
            os.system('sudo apt-get update \
                       && sudo apt-get -y install \
                       youtube-dl \
                       ffmpeg')
            input('\nPress ENTER to continue!')
            break
        elif option == 'n' or option == 'no':
            break
        else:
            input('Error! Press ENTER to continue.')
            program_name()

#This function downloads links as music.
def download_music(save_folder, links_file):
    os.system(f"clear\
               && cd {save_folder} \
               && youtube-dl --geo-bypass -x --audio-format mp3 \
               -o '%(title)s.%(ext)s' -a {links_file}")

#This function downloads links as video.
def download_video(save_folder, links_file):
    os.system(f"clear\
               && cd {save_folder} \
               && youtube-dl --geo-bypass --yes-playlist \
               -o '%(title)s.%(ext)s' -f best -a {links_file}")

#Menu with options.
def menu():
    #Start the save directory and select the link file.
    root = Tk()
    root.withdraw()
    program_name()

    #Select the save directory.
    print('Select the save directory.')
    folderSelected1 = filedialog.askdirectory()
    os.chdir(folderSelected1)

    #Select the file that contains the links.
    print('Select the file that contains the links.')
    fileSelected1 = filedialog.askopenfilename()
    program_name()
    while True:
        print('What do you want? \n\
               \n1. Install requeriments.\n2. Download as music.\n3. Download as video.\
               \n4. Exit')
        option = input('\n--> ')
        if option == '1':
            requeriments()
            program_name()
        elif option == '2':
            download_music(folderSelected1, fileSelected1)
            break
        elif option == '3':
            download_video(folderSelected1, fileSelected1)
            break
        elif option == '4':
            print('Exiting...')
            break
        else:
            input('\nERROR! press ENTER to continue.')
            program_name()

menu()
