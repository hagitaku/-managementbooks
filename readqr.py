from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
import cv2
import numpy as np

def check():
    bookname=read()
    booksdata=load_data();
    booksvalue=get_booksvalue();
    readflg=0;

    for i in range(booksvalue):
        if bookname==booksdata[i][0] and booksdata[i][1]=="0":
            print("借りることができます");
            readflg=1;
            break;
            
    if readflg==0:
        print("見つかりませんでした");
    return 0;

def edit_contrast(image, gamma):
    """コントラクト調整"""
    look_up_table = [np.uint8(255.0 / (1 + np.exp(-gamma * (i - 128.) / 255.)))
        for i in range(256)]
 
    result_image = np.array([look_up_table[value]
                             for value in image.flat], dtype=np.uint8)
    result_image = result_image.reshape(image.shape)
    return result_image
 
def read():
    print("カメラ起動中");
    if __name__ == "readqr":
        capture = cv2.VideoCapture(0)
        if capture.isOpened() is False:
            raise("IO Error")
    print("準備完了");
    while True:
        ret, frame = capture.read()
        if ret == False:
            continue
        # グレースケール化してコントラクトを調整する
        gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        image = edit_contrast(gray_scale, 5)
     
        # 加工した画像からフレームQRコードを取得してデコードする
        codes = decode(image)
        if len(codes) > 0:
            return codes[0][0].decode('utf-8', 'ignore')

def get_booksvalue():
    filename="bookstates.csv";
    fp=open(filename,"rt",encoding="utf-8");
    tsv=fp.read();

    rows=tsv.split("\n");
    result=[];
    for line in rows:
        cols=line.split(",");
        if len(cols)<=1:break;
        result.append(cols);

    return len(result);

def load_data():
    filename="bookstates.csv";
    fp=open(filename,"rt",encoding="utf-8");
    tsv=fp.read();

    rows=tsv.split("\n");
    result=[];
    for line in rows:
        cols=line.split(",");
        if len(cols)<=1:break;
        result.append(cols);

    return result;