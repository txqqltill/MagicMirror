import os

def find_users(image_path):
    return [
        f.removesuffix("-id.jpg")
        for f in os.listdir(image_path)
        if f.endswith("-id.jpg")
    ] + ["Guest"]
