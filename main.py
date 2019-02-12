import qrcode
import os,tkinter,tkinter.filedialog
import pathlib
from PIL import ImageTk,Image
import readqr

fTyp = [("","*")]
iDir = os.path.abspath(os.path.dirname(__file__))
img_tk=0;
def select_file(_window):#画像選択関数
	global img_tk;
	cv=tkinter.Canvas(_window,width=290,height=290,bg='black')
	file = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)#画像を選択させて絶対パスを取得
	file_path=pathlib.Path(file)
	print(file_path.relative_to(file_path.cwd()))
	book_img=Image.open(file_path.relative_to(file_path.cwd()))#画像の絶対パスを相対パスに変換して画像読み込み
	img_tk=ImageTk.PhotoImage(book_img)
	
	cv.create_image(0,0,image=img_tk,anchor=tkinter.NW)#画像描画
	cv.pack()


def QRcreatefun(_window,_name):#QRコード作成よう関数
	img=qrcode.make(_name.get())#QRコード作成
	img.save(_name.get()+'.png')
	_window.destroy()#QRコード作成ウィンドウ削除

def borrow(_window,name,_bookname):
	#借入用
	_name=name.get();
	booksdata=readqr.load_data();
	booksvalue=readqr.get_booksvalue()
	readflg=0;
	print("\n\n",_name)
	for i in range(booksvalue):
		if _bookname==booksdata[i][0] and booksdata[i][1]=="0":
			readqr.write(_bookname,"1",_name);
			print("正常に借入が完了しました")
			readflg=1;
			break;
		elif _bookname==booksdata[i][0] and booksdata[i][1]=="1":
			print("誰かが借りています\n借りている人は",booksdata[i][2],"です")
			readflg=1;
			break;

	if readflg==0:
		print("そのような本は見つかりませんでした");

	_window.destroy();

def Borbtn_click():
	print("Return");
	Borr=tkinter.Toplevel()#QRコード作成用ウィンドウ生成
	Borr.title(u"返却")
	name=tkinter.Entry(Borr,width=30)
	name.place(x=50,y=100)
	Borr.geometry("300x300")
	print("準備完了という文字が出力されたら\n借りたい本のQRコードをカメラの前にかざしてください\n\n")
	book=readqr.read()
	print("読み取ったデータは",book,"です")
	print("あなたの名前を半角で入力してください")
	booksdata=readqr.load_data();
	booksvalue=readqr.get_booksvalue()
	readflg=0;

	QRcreate=tkinter.Button(Borr,text=u"借りる",command=lambda:borrow(Borr,name,book))#QRコードを作成する関数にとぶボタン

	QRcreate.pack()

def Re_btn_click():
	print("Return");
	book=readqr.read()
	booksdata=readqr.load_data();
	booksvalue=readqr.get_booksvalue()
	readflg=0;
	print("準備完了という文字が出力されたら\n返したい本のQRコードをカメラの前にかざしてください\n\n")
	print("読み取ったデータは",book,"です")
	for i in range(booksvalue):
		if book==booksdata[i][0] and booksdata[i][1]=="1":
			readqr.write(book,"0","none");
			print("正常に返却が完了しました")
			readflg=1;
			break;
		elif book==booksdata[i][0] and booksdata[i][1]=="0":
			print("そもそも誰も借りていません\n")
			readflg=1;
			break;

	if readflg==0:
		print("そのような本は見つかりませんでした");


def createbtn_click():
	print("Create")
	Create_win=tkinter.Toplevel()#QRコード作成用ウィンドウ生成
	Create_win.title(u"Create QRcode Window")
	Create_win.geometry("700x700")
	#QR作成用関数
	name=tkinter.Entry(Create_win,width=20)#QRコード名をうちこませる
	name.place(x=50,y=100)
	Fileselectbtn=tkinter.Button(Create_win,text=u"File Select",command=lambda:select_file(Create_win))#ファイル選択させる関数にとぶボタン
	Fileselectbtn.pack()
	QRcreate=tkinter.Button(Create_win,text=u"Create QRcode",command=lambda:QRcreatefun(Create_win,name))#QRコードを作成する関数にとぶボタン
	QRcreate.pack()

window=tkinter.Tk()#mainWindow
window.title(u"Hello,world!!")
window.geometry("300x300")
Read_button=tkinter.Button(window,text=u"本を借りる",command=Borbtn_click)#本借用ウィンドウにとぶボタン
Make_button=tkinter.Button(window,text=u"本登録",command=createbtn_click)#本登録ウィンドウにとぶボタン
Re_button=tkinter.Button(window,text=u"本返却",command=Re_btn_click)#本返却ウィンドウにとぶボタン

Read_button.pack()
Make_button.pack()
Re_button.pack()
window.mainloop()