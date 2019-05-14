import gzip

conf = None

def gzipOpen(fileName, mode='r'):
    if fileName.endswith('gz'):
        return gzip.open(fileName, '%sb' % mode)
    return open(fileName, mode)

