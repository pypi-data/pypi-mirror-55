import hashlib

# Download module list with hash
module_hashes = {
        'nircmd.exe': 'ea448e2d5be3197a422ad413598c6c43',
        'webcam.exe': 'ea678b48940aebe8fbf9a189949fc4a3',
        }

def md5(file):
    ##|
    ##| Get file md5
    ##|
    hash_md5 = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()