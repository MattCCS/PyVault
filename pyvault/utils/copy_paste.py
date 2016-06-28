import subprocess

def write_to_clipboard(text):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(text.encode('utf-8'))

# def read_from_clipboard():
#     return subprocess.check_output(
#         'pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')
