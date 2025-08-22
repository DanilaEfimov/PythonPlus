import pathlib
import io
import tokenize


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

def remove_empty_lines(source: list[str]) -> list[str]:
    return [line for line in source if line.strip()]

def remove_comments(source: list[str]) -> list[str]:
    source_code = ''.join(source)
    result_tokens = []
    tokens = tokenize.tokenize(io.BytesIO(source_code.encode('utf-8')).readline)

    for token in tokens:
        if token.type == tokenize.COMMENT or token.type == tokenize.ENCODING:
            continue
        result_tokens.append(token)

    new_code = tokenize.untokenize(result_tokens)
    return new_code.splitlines(keepends=True)


from handlers import is_directive
