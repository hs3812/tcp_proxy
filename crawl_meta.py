import pyPdf
import urllib2
from bs4 import BeautifulSoup
from urlparse import urlsplit
import os
from PIL import Image

target = 'http://www..com'


def main():
    mylist = img_search(target)
    for item in mylist:
        filename = download_image(item)
        if filename:
            if filename.endswith('.pdf'):
                printmeta(filename)
            else:
                EXIF(filename)
    exit(0)


def printmeta(filename):
    pdf = pyPdf.PdfFileReader(open(filename, 'rb'))
    docinfo = pdf.getDocumentInfo()
    print("[*] PDF metadate for " + filename)
    for item in docinfo:
        print '[*]' + item + ':' + str(docinfo[item])


def img_search(url):
    print('searching all images on' + url)
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page)
    list_images = soup.find_all('img')
    return list_images


def download_image(images):
    try:
        print("[*] Downloading images ......")
        image_source = images['src']
        image_raw = urllib2.urlopen(image_source).read()
        iamge_name = os.path.basename(urlsplit(image_source)[2])
        with open(iamge_name, 'wb') as f:
            f.write(image_raw)
        return iamge_name
    except:
        return None


def EXIF(filename):
    try:
        data = {}
        f = Image.open(filename)
        info = f._getexif()
        if info:
            for (tag, value) in info.items():
                decoded = TAGS.get(tag, tag)  # decoding not working properly
                data[decoded] = value
            GPS = data['GPSInfo']
            if GPS:
                print('[*]' + filename + 'GPS:' + GPS)
    except:
        pass


if __name__ == '__main__':
    main()

