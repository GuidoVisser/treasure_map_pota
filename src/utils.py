from os import path

def generate_filename(fn, suffix):
    """recursively generate a unique filename
    """
    if path.exists(fn):
        fn, ext = path.splitext(fn)
        unique_fn = fn + " (" + str(suffix) + ")" + ext
        if path.exists(unique_fn):
            unique_fn = generate_filename(fn + ext, suffix + 1)
    else:
        return fn
    
    return unique_fn