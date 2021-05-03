from hashlib import md5

def get_hashed_str(txt: str, method: str = "MD5"):

    if method == "MD5":
        hashed = md5(txt.encode())
    else:
        raise NotImplementedError

    return hashed.hexdigest()


def capitalize_first_letter(txt: str) -> str:
    if len(txt) > 0:
        txt = f'{txt[0].upper()}{txt[1:]}'
    return txt

def clean_text(txt:str):

    tokens2remove = ('-','/',';',',','.','*','!','?','%','$','@','#')

    for t in tokens2remove:
        txt = txt.replace('-',' ')

    return txt.replace('  ',' ')