#!/usr/bin/env python
import os


def zipper(src, dst):
    zf = zipfile.ZipFile("%s.zip" % (dst), "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            zf.write(absname, arcname)
    zf.close()


if __name__ == '__main__':
    zipper = 'test'
    target = '/data/Documents/bdr_test_source_dir'
    zipper(target, zipfilename)
