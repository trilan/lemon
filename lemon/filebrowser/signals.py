from django.dispatch import Signal


filebrowser_pre_createdir = Signal(providing_args=['path', 'dirname'])
filebrowser_post_createdir = Signal(providing_args=['path', 'dirname'])

filebrowser_pre_delete = Signal(providing_args=['path', 'filename'])
filebrowser_post_delete = Signal(providing_args=['path', 'filename'])

filebrowser_pre_rename = Signal(
    providing_args=['path', 'filename', 'new_filename'])
filebrowser_post_rename = Signal(
    providing_args=['path', 'filename', 'new_filename'])
