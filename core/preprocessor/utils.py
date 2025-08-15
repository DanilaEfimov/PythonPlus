import pathlib


def replace_extension(filename: str, new_suffix: str) -> str:
    path = pathlib.Path(filename)
    if not new_suffix.startswith('.'):
        new_suffix = '.' + new_suffix
    new_filename = path.with_suffix(new_suffix)
    return str(new_filename)

def search_end(source: list[str], line_from: int) -> int:
    for i in range(line_from, len(source)):
        if is_directive(source[i].strip(), 'end'):
            return i
    return -1

from handlers import is_directive