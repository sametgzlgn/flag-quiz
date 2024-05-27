from PIL import Image,ImageTk
from ttkbootstrap.constants import *
from tkinter.simpledialog import askstring
from tkinter.simpledialog import askinteger
import tkinter as tk
import ttkbootstrap as ttk
import simpleaudio as sa
import random
import sys

ulke_bilgileri = []
siklar = []
dogru_cevap = ""
width,height = 0,0
dizin = "res/"
puan = 0
dogru = sa.WaveObject.from_wave_file("res/dogru.wav")
yanlis = sa.WaveObject.from_wave_file("res/yanlis.wav")

def init(total_soru,seviye):
    global ulke_bilgileri
    csv_dosyasi = open("ulkeler.csv","r")
    ulkeler = csv_dosyasi.readlines()
    while len(ulke_bilgileri) < total_soru:
       ulke = str(random.choice(ulkeler))[:-1].split(",")
       if ulke not in ulke_bilgileri and seviye == ulke[2]:
           ulke_bilgileri.append(ulke)
    csv_dosyasi.close()

def yeni_soru():
    global bayrak_lbl,siklar,dogru_cevap,buton1,buton2,buton3
    csv_dosyasi = open("ulkeler.csv","r")
    ulkeler = csv_dosyasi.readlines()
    siklar = []
    try:
        bayrak_dosyasi = Image.open("{}{}".format(dizin,ulke_bilgileri[0][0]))
    except IndexError:
        sys.exit()
    dogru_cevap = ulke_bilgileri[0][1]
    siklar.append(ulke_bilgileri[0][1])
    while len(siklar) < 3:
        ulke_adlari = str(random.choice(ulkeler))[:-1].split(",")
        siklar.append(ulke_adlari[1])
    random.shuffle(siklar)
    csv_dosyasi.close()
    bayrak_img = ImageTk.PhotoImage(bayrak_dosyasi.resize((round(width * 0.7),round(height * 0.7))))
    bayrak_lbl.image = bayrak_img
    bayrak_lbl["image"] = bayrak_img
    buton1["text"] = siklar[0].title()
    buton2["text"] = siklar[1].title()
    buton3["text"] = siklar[2].title()

def cevap(indis):
    global ulke_bilgileri,puan,puan_lbl
    if siklar[indis] == dogru_cevap:
        puan += 10
        dogru.play()
        puan_lbl["text"] = "Puan: {}".format(puan)
        ulke_bilgileri.pop(0)
        yeni_soru()
    else:
        yanlis.play()
        ulke_bilgileri.pop(0)
        yeni_soru()

pencere = tk.Tk()
init(askinteger("Flag Quiz","Kaç soru sorulsun?"),askstring("Flag Quiz","easy/medium/hard?"))
width, height = round(pencere.winfo_screenwidth() * 0.85),round(pencere.winfo_screenheight() * 0.85)
pencere.title("Flag Quiz")
pencere.geometry("{}x{}".format(width,height))
pencere.resizable(0,0)
ttk.Style("superhero")
bayrak_lbl = ttk.Label()
bayrak_lbl.pack(side=TOP,pady=10)
puan_lbl = ttk.Label(text="Puan: ")
puan_lbl.place(x=round(width * 0.9),y=round(height * 0.9))

buton1 = ttk.Button(text="Şık 1",width=20,bootstyle="success-outline",command=lambda:cevap(0))
buton1.place(x=round(width * 0.22),y=round(height * 0.8))
buton2 = ttk.Button(text="Şık 2",width=20,bootstyle="success-outline",command=lambda:cevap(1))
buton2.place(x=round(width * 0.44),y=round(height * 0.8))
buton3 = ttk.Button(text="Şık 3",width=20,bootstyle="success-outline",command=lambda:cevap(2))
buton3.place(x=round(width * 0.66),y=round(height * 0.8))
yeni_soru()
pencere.mainloop()
