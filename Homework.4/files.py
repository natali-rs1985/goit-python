import sys
from pathlib import Path


IMAGES = ['JPEG', 'PNG', 'JPG']
VIDEO = ['AVI', 'MP4', 'MOV']
DOCUMENTS = ['DOC', 'DOCX', 'TXT']
MUSIC = ['MP3', 'OGG', 'WAV', 'AMR']
ARCHIVES = ['ZIP', 'GZ', 'TAR']

images_list = []
video_list = []
documents_list = []
music_list = []
archives_list = []
another = []

extensions = set()
unknown_extensions = set()


def find_files(path):
    files = []
    if path.exists():
        for file in path.iterdir():
            if file.is_file():
                files.append(file.name)
            else:
                files.extend(find_files(file))

    return files


def sort_by_extension(files):

    for file in files:
        if file.split('.')[-1].upper() in IMAGES:
            images_list.append(file)
        elif file.split('.')[-1].upper() in VIDEO:
            video_list.append(file)
        elif file.split('.')[-1].upper() in DOCUMENTS:
            documents_list.append(file)
        elif file.split('.')[-1].upper() in MUSIC:
            music_list.append(file)
        elif file.split('.')[-1].upper() in ARCHIVES:
            archives_list.append(file)
        else:
            another.append(file)

    print(f'Imege files {images_list}')
    print(f'Video files {video_list}')
    print(f'Document files {documents_list}')
    print(f'Music files {music_list}')
    print(f'Archive files {archives_list}')
    print(f'Another files {another}')


def find_extension(files):

    for file in files:
        if file.split('.')[-1].upper() in (IMAGES + VIDEO + DOCUMENTS + MUSIC + ARCHIVES):
            extensions.add(file.split('.')[-1].upper())
        else:
            unknown_extensions.add(file.split('.')[-1].upper())
    print(f'Extensios in folder: {extensions}')
    print(f'Unknown extensios in folder: {unknown_extensions}')


def run_script():
    if find_files(path):
        files = find_files(path)
        sort_by_extension(files)
        find_extension(files)

    else:
        print('Path does not exist')


if __name__ == '__main__':

    path = Path(r'C:\GOIT-Python\goit-python\Homework.4\Files')

    #path = sys.argv[1]
    #path = Path(path)

    run_script()
