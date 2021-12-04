import os

from django.core.exceptions import ValidationError

MAX_FILE_SIZE = 1073741824
ALLOWED_EXTENSIONS = ['.mp4', '.3gp', '.mkv']


def validate_size(value):
    if value.size > MAX_FILE_SIZE:
        raise ValidationError(f'Maximum file size is: {MAX_FILE_SIZE} Bytes')


def validate_extension(value):
    split_ext = os.path.splitext(value.name)

    if len(split_ext) > 1:
        ext = split_ext[1]
        if ext.lower() not in ALLOWED_EXTENSIONS:
            raise ValidationError(f'File not allowed, valid extensions: {ALLOWED_EXTENSIONS}')
