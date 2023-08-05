# THIS FILE IS GENERATED FROM PADDLEPADDLE SETUP.PY
#
full_version    = '1.6.1'
major           = '1'
minor           = '6'
patch           = '1'
rc              = '0'
istaged         = False
commit          = '53f1e024d4dcffe76d5b8b7a996eb7ed2ac802cd'
with_mkl        = 'ON'

def show():
    if istaged:
        print('full_version:', full_version)
        print('major:', major)
        print('minor:', minor)
        print('patch:', patch)
        print('rc:', rc)
    else:
        print('commit:', commit)

def mkl():
    return with_mkl
