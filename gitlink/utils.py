from sys import getdefaultencoding, version_info
from subprocess import Popen, PIPE


basestr = (str, unicode) if version_info[0] == 2 else (str,)
default_encoding = getdefaultencoding()

def run(*args, **kw):
    p = Popen(stdout=PIPE, stderr=PIPE, shell=True, *args, **kw)
    out, err = p.communicate()
    ret = p.poll()

    if ret:
        cmd = kw.get('args')
        if cmd is None:
            cmd = args[0]

    if out:
        out = out.decode(default_encoding)
        out = out.rstrip('\n')

    return ret, out

def to_clipboard(s):
    '''Send string to clipboard.'''
    try:
        from . pyperclip import copy
    except:
        raise Exception('warning: xclip or xsel must be installed for copying to work')
    copy(s)

def shorten_hashes(res, length=7):
    for key in 'sha', 'tree_sha', 'object', 'commit_sha', 'top_tree_sha':
        if key in res and isinstance(res[key], basestr):
            res[key] = res[key][:length]
