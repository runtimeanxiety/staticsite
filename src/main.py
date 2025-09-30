import os
import shutil

def copy_static_to_public():
    src = "static"
    dst = "public"
    if os.path.exists(dst):
        print(f"Deleting existing destination: {dst}")
        shutil.rmtree(dst)
    os.mkdir(dst)
    print(f"Created directory: {dst}")

    def recursive_copy(src_dir, dst_dir):
        for item in os.listdir(src_dir):
            src_path = os.path.join(src_dir, item)
            dst_path = os.path.join(dst_dir, item)

            if os.path.isfile(src_path):
                shutil.copy(src_path, dst_path)
                print(f"Copied file: {src_path} -> {dst_path}")
            elif os.path.isdir(src_path):
                os.mkdir(dst_path)
                print(f"Created directory: {dst_path}")
                recursive_copy(src_path, dst_path)

    recursive_copy(src, dst)

def main():
    copy_static_to_public()

if __name__ == "__main__":
    main()

