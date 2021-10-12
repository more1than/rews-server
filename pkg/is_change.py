import hashlib


def is_change(body_hash, *args):
    string1 = ""
    for i in args:
        string1 += str(i)
    hash_before = hashlib.sha256(string1.encode("utf-8")).hexdigest()
    if hash_before == body_hash:
        return False, hash_before
    return True, hash_before
