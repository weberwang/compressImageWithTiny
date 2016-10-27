
import tinify
import sys
import os
import hashlib
import json
tinify.key = 'your key'

compressedfiles_data = None

def filemd5(file):
    with open(file, 'rb') as compressed:
        compressed_data = compressed.read()
        m2 = hashlib.md5()   
        m2.update(compressed_data)   
        return m2.hexdigest()

def compressimg(file):
    m5 = compressedfiles_data.get(file)
    print('before compress', m5)
    if  m5 != None and filemd5(file) == m5:
        return
    sourcefile = tinify.from_file(file)
    sourcefile.to_file(file)
    m5 = filemd5(file)
    print(m5)
    compressedfiles_data[file] = m5
    pass
    
def findfile(path):
    if path.find('.') == 0:
        return
    if os.path.isdir(path):
        listdir = os.listdir(path)
        for path in listdir:
            if os.path.isfile(path) and (path[path.rfind('.')+1:] in ['png','jpg']):
                compressimg(path)
            else :
                findfile(path)
    pass

if __name__ == '__main__':
    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        root = os.getcwd()
    global compressedfiles_data
    with open(os.path.join(root,'compressed.json'),'r') as compressedfiles:
        filedata = compressedfiles.read()
        if len(filedata) > 0:
            compressedfiles_data = json.loads(filedata)
        else :
            compressedfiles_data = {}
    findfile(root)
    with open('compressed.json','w') as compressedfiles:
        compressedfiles.write(json.dumps(compressedfiles_data))
