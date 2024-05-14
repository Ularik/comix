import rarfile
import zipfile
import os


def extract_file(path, title):
    file_path = path

    open_comix_file = rarfile.RarFile
    if file_path.endswith(('cbz', 'zip')):
        open_comix_file = zipfile.ZipFile

    with open_comix_file(rf'.{file_path}', 'r') as archive:  # extract comix_file.cbr
        name_list = archive.namelist()  # get name of every page in comix
        count = -1  # count for find out page num
        dir_path_for_current_comix = f'{os.path.dirname(__file__)}/{title}'  # path: ...core/extract_comix/title
        os.mkdir(dir_path_for_current_comix)
        names_of_pages = []
        for image_name in name_list:
            if image_name.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                count += 1
                archive.extract(image_name, path=dir_path_for_current_comix)    # extract page from zipfile
                names_of_pages.append(image_name)

    return names_of_pages, count
