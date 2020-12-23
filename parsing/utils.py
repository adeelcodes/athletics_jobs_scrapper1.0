import os
import smtplib
import environ

from datetime import datetime
from typing import NoReturn

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
path_env = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
environ.Env.read_env(path_env)


def get_current_folder() -> str:
    """Get and return current folder"""
    return str(os.path.dirname(os.path.realpath(__file__)))


def get_current_date_with_postfix() -> str:
    """Get and return current date with postfix"""
    current_datetime = datetime.now().date()
    return f'{str(current_datetime)}_success'


def create_new_file(directory: str, file_name: str, extension: str = '.txt') -> NoReturn:
    """Create a new file with some name and path..."""
    file = open(f'{directory}/{file_name}{extension}', 'w+')
    file.close()


def remove_file(directory: str, file_name: str, extension: str = '.txt') -> NoReturn:
    """Create a new file with some name and path..."""
    os.remove(f'{directory}/{file_name}{extension}')


def remove_file_with_current_date() -> NoReturn:
    """Create new date into current folder with like name `2020-12-08_success.txt`"""
    path = get_current_folder()
    remove_file(
        directory=path,
        file_name=get_current_date_with_postfix()
    )


def create_new_file_with_current_date() -> NoReturn:
    """Create new date into current folder with like name `2020-12-08_success.txt`"""
    path = get_current_folder()
    create_new_file(
        directory=path,
        file_name=get_current_date_with_postfix()
    )


def send_email_with_some_error() -> NoReturn:
    """Send some email if was happened some errors"""

    gmail_user = env.str('GMAIL_USER')
    gmail_password = env.str('GMAIL_PASSWORD')

    sent_from = gmail_user
    to = ['recipient@gmail.com', 'another_recipient@gmail.com']
    subject = 'SOS, an error occurred'
    body = 'An error occurred that needs human attention'

    message = 'Subject: {}\n\n{}'.format(subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, message)
        server.close()

        print('Email sent!')
    except Exception as ex:
        print(f'Something went wrong... {ex}')
