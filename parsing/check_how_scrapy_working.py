import os

from utils import get_current_folder, get_current_date_with_postfix, remove_file_with_current_date, \
    send_email_with_some_error


if __name__ == '__main__':
    current_folder = get_current_folder()
    file_name = f"{get_current_date_with_postfix()}.txt"
    res = os.walk(
        current_folder,
        topdown=False
    )
    exist_file = False
    for (dirpath, dirnames, filenames_list) in res:
        if file_name in filenames_list:
            """Everything was good working. Just remove `date_success.txt` file."""
            remove_file_with_current_date()
            exist_file = True
            break

    if not exist_file:
        """Push some email with error"""
        send_email_with_some_error()
