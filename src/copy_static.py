import shutil
import os

def copy_static(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
        print("Destination deleted!")
    os.makedirs(dst, exist_ok=True)
    print("Destination remade!")
    copy_recursive(src, dst)

def copy_recursive(src, dst):
    for name in os.listdir(src):
        src_path = os.path.join(src, name)
        dst_path = os.path.join(dst, name)
        if os.path.isdir(src_path):
            os.mkdir(dst_path)
            print(f"Made {dst_path}!")
            copy_recursive(src_path, dst_path)
            print(f"Copied into {dst_path}!")
        elif os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            print(f"File copied to {dst_path}!")