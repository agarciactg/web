import os
import uuid


def user_files_path(filename, directory=""):
    _, ext = os.path.splitext(filename)
    hash = uuid.uuid4().hex
    return f"files/users/{directory}{hash}{ext}"


def user_avatar_image_path(instance, extension="jpg"):
    return user_files_path(f"{instance.id}.{extension}", "avatars/")
