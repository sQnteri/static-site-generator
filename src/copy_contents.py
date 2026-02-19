import os
import shutil

def copy_contents(source, destination):
    if not os.path.exists(destination):
        os.makedirs(destination)

    for item in os.listdir(source):
        path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)
        
        if os.path.isdir(path):
            copy_contents(path, dest_path)
        else:
            shutil.copy(path, dest_path)
            print(f'Copying {path} to {dest_path}')
