import gzip

def infer(iterable, file_name):
    """Uses the incoming file_name and checks the end of the string
    for supported compression types"""
    if not file_name:
        raise Exception("Need file name")

    if file_name.endswith('.tar.gz'):
        raise NotImplementedError("tar.gz not supported")
    elif file_name.endswith(".gz"):
        yield gzip.GzipFile(fileobj=iterable)
    else:
        yield iterable
