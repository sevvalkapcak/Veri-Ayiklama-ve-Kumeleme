from clusters import hcluster, kcluster
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as msgbox
import tkinter.scrolledtext as tkst
from terminal2tkintertext import print_terminalden, printcluster_terminalden


def matrise_cevir(data:dict):
    data_matrix = []
    satirlar = []
    tum_sutunlar = {item for sublist in [list(x.keys()) for x in data.values()] for item in sublist}

    for key, values in data.items():
        data_matrix.append([])
        satirlar.append(key)
        for sutun in tum_sutunlar:
            if sutun in values.keys():
                data_matrix[-1].append(values[sutun])
            else:
                data_matrix[-1].append(0)

    return data_matrix, satirlar, tum_sutunlar


class KumelemeEkrani(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initGui()
        self.pack()

    def initGui(self):

        # Frame 1 : Txt dosyasi yukleme
        frame1 = tk.Frame(self)

        fr1_label = tk.Label(
            frame1, text="Yandaki butonu kullanarak verilen dosyayi girebilirsiniz")
        fr1_buton = tk.Button(
            frame1, text="Txt Dosya Sec", command=self.aktar)

        fr1_label.pack(side=tk.LEFT)
        fr1_buton.pack(side=tk.RIGHT)
        frame1.pack()
        #########

        # Frame 2: Kategorileri sectirme ve kumeleme belirleme ve kumele butonu
        frame2 = tk.Frame(self)
        fr2_label1 = tk.Label(frame2, text = "2 Adet Kategori Secin:")
        self.fr2_listbox1 = tk.Listbox(
            frame2, width=40, selectmode="multiple", exportselection=0)
  
        ana_label = tk.Label(
            frame2, text="Kumeleme Ekrani", font='Helvetica 18 bold')
        self.hiyerarsik_secili = tk.BooleanVar()

        true_button = tk.Radiobutton(frame2,
                                     text="Hiyerarsik Kumeleme",
                                     variable=self.hiyerarsik_secili,
                                     value=True
                                     )

        false_button = tk.Radiobutton(frame2,
                                      text="KMeans Kumeleme",
                                      variable=self.hiyerarsik_secili,
                                      value=False
                                      )

        fr2_label2 = tk.Label(frame2, text="KMeans Kume Sayisi")

        self.kmeans_kumeno = tk.IntVar()
        fr2_entry1 = tk.Entry(
            frame2, textvariable=self.kmeans_kumeno)

        fr2_buton1 = tk.Button(frame2, text="Kumele !", command=self.kumele)

        ana_label.grid(row=0, column=0, columnspan=4)

        fr2_label1.grid(row= 1, column = 0)
        self.fr2_listbox1.grid(row=2, column=0, rowspan=4)
        
        true_button.grid(row=2, column=1, sticky='w')
        false_button.grid(row=3, column=1, sticky='w')
        
        fr2_label2.grid(row=2, column=2)
        fr2_entry1.grid(row=3, column=2)
        
        fr2_buton1.grid(row=2, column=3, rowspan=2, padx=30)

        frame2.pack()
        #############


        # Frame 3: Goruntu ekrani
        frame3 = tk.Frame(self)
        # Burda bir buton widgetı oluşturuyoruz, seçeneklerini belirliyoruz ve pencerimizde yerini belirliyoruz.
        self.Textbox1 = tkst.ScrolledText(frame3, font="Italic 13 bold", width=80, height=20, relief="sunken",
                       bd="5px")
      
        self.Textbox1.pack()
        frame3.pack()
        ###########

    def kumele(self):
        ''' Dosyayi okumak icin gerekli fonksiyonlari cagirir ve secili opsiyona gore kumeleme islemini yapar. 
        '''

        self.degerler = self.dosya_oku()
        self.matris, self.satirlar, self.sutunlar = matrise_cevir(self.degerler)

        # Textbox i temizle (daha onceden yazili olanlari sil)
        self.Textbox1.delete('1.0', tk.END)

        # Kumele
        if self.hiyerarsik_secili.get():
            self.siniflar = hcluster(self.matris)
            contents = printcluster_terminalden(self.siniflar, self.satirlar)
        else:

            kmeans_kume=4
            if self.kmeans_kumeno.get()>0:
                kmeans_kume = self.kmeans_kumeno.get()
                
            self.siniflar = kcluster(self.matris, k=kmeans_kume)

            # Ekrana basili olan kodu text ekranina yazilacak contents listesine ekle
            contents = []
            for sinif in range(len(self.siniflar)):
                contents.append(print_terminalden(
                    sinif, [self.satirlar[r] for r in self.siniflar[sinif]]))

        for c in contents:
            self.Textbox1.insert(tk.END, c)

    def aktar(self):
        self.dosya_ismi = fd.askopenfilename()
        with open(self.dosya_ismi) as dosya:
            basliklar = dosya.readline().split(',')
            self.basliklar = [item.strip() for item in basliklar]
        
        for baslik in self.basliklar:
            self.fr2_listbox1.insert(tk.END, baslik)


    def dosya_oku(self):
        if not len(self.fr2_listbox1.curselection()) ==2 :
            msgbox.showerror(title="Secim hatasi",
                             message="Tam olarak iki kategori secilmeli")
            return

        satir_ismi = self.basliklar[self.fr2_listbox1.curselection()[0]]
        sutun_ismi = self.basliklar[self.fr2_listbox1.curselection()[1]]


        deger_sozluk = dict()

        with open(self.dosya_ismi) as dosya:

            bIlkSatirOkundu = False
            for line in dosya:
                line = line.split(",")
                # satir sonundaki newline'dan kurtulalim
                line = [item.strip() for item in line]
                if not bIlkSatirOkundu:
                    satir_indeks = self.basliklar.index(satir_ismi)
                    sutun_indeks = self.basliklar.index(sutun_ismi)
                    bIlkSatirOkundu  = True
                else:
                    satir_kategori = float(line[satir_indeks])
                    sutun_kategori = float(line[sutun_indeks])
                    deger_sozluk.setdefault(satir_kategori, {})
                    deger_sozluk[satir_kategori].setdefault(sutun_kategori, 0)
                    deger_sozluk[satir_kategori][sutun_kategori] += 1

        return deger_sozluk


root = tk.Tk()
root.title("Veri Ayiklama ve Kumeleme")
#root.geometry("650x650+400+100")

KumelemeEkrani(root)
root.mainloop()
