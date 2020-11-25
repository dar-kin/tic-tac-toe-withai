from datetime import datetime


def get_release_date(release_str):
    release_str = release_str.replace("Day of release: ", "")
    return datetime.strptime(release_str, "%d %B %Y").strftime("%Y-%m-%d %H:%M:%S")
