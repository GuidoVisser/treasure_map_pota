from os import path

def generate_filename(fn: str, suffix: str) -> str:
    """recursively generate a unique filename

    Args:
        fn (str): file name
        suffix (str): suffix that will increment to generate a unique file name

    Returns:
        str: file name that is unique
    """
    if path.exists(fn):
        fn, ext = path.splitext(fn)
        unique_fn = fn + " (" + str(suffix) + ")" + ext
        if path.exists(unique_fn):
            unique_fn = generate_filename(fn + ext, suffix + 1)
    else:
        return fn
    
    return unique_fn