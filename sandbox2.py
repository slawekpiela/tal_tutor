import os
import requests
import json
import magic
import streamlit as st

from configuration import whereby_api_key, tiny_api_key
import whisper
import re
from moviepy.editor import VideoFileClip
from datetime import timedelta, datetime
import subprocess
import shutil
import os

# Define the current path of the file and the new directory path
current_file_path = 'data/'
new_directory_path = 'data_repo/'

# Ensure the new directory exists
if not os.path.exists(new_directory_path):
    os.makedirs(new_directory_path)

# Move the file
new_file_path = shutil.move(current_file_path, new_directory_path)

print(f'File moved to: {new_file_path}')
