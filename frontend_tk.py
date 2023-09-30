from tkinter import*
from tkinter.filedialog import *
from tkinter.ttk import Scrollbar
import threading
import sqlite3
import youtube_scraping as ys

# creation de la class graphique principal

class scraper():
    def __init__(self, curseur, connection):
        self.x, self.y = 1500, 1500
        self.connection = connection
        self.cursor = curseur
        self.cursor.execute("CREATE TABLE IF NOT EXISTS dashboard (channel VARCHAR, keyword VARCHAR, video_amount INTEGER, avg_views FLOAT, days_since_first_update SMALLINT, subscribers INTEGER, url TEXT PRIMARY KEY)")
        self.fen = Tk()
        self.fen.geometry('1500x1500')
        self.fen['bg'] = 'green'
        self.a = self.fen.winfo_children()
        self.img = PhotoImage(file='youtube-users.new.png')
        #contenue de la premiere fenetre
        self.conteneur = Frame(self.fen, width=1500, height=1500)
        self.conteneur.pack()
        self.scroll_view = Scrollbar(self.conteneur, orient=VERTICAL)
        self.scroll_view.pack(side=RIGHT, fill= Y)
        self.can = Canvas(self.conteneur, width=self.x, height=self.y, bg='white', yscrollcommand=self.scroll_view.set)
        self.can.pack(side=LEFT)
        self.scroll_view.config(command=self.can.yview)
        self.notice = self.can.create_text(640, 90, text='')
        self.image = self.can.create_image(690, 365, anchor=CENTER, image=self.img)
        self.entree = Entry(self.can, width=30, bg='pink', fg='black')
        self.can.create_window(630, 50, window=self.entree)
        self.bou_key_word = Button(self.can, text='add keyword', bg='purple', command=self.thread_utilisateur(self.entree.get()).start)
        self.can.create_window(430, 90, window=self.bou_key_word)
        self.bou_csv = Button(self.can, text='uploard', bg='purple', command=self.select_file)
        self.can.create_window(850, 90, window=self.bou_csv)
        self.frame = Frame(self.can, width=100, height=100)
        self.scroll_view_2 = Scrollbar(self.frame, orient=VERTICAL)
        self.scroll_view_2.pack(side=RIGHT, fill= Y)
        self.list_keyword = Listbox(self.frame, yscrollcommand=self.scroll_view_2.set)
        self.list_keyword.bind("<<ListboxSelect>>", self.inserer)
        self.cursor.execute("SELECT keyword FROM dashboard")
        self.r = list(self.cursor)
        self.c = 0
        for e in self.r:
            if self.c > 0 and e != self.r[self.c-1]:
                self.list_keyword.insert(0, str(e).replace("(", "").replace("'", "").replace(")", "").replace(",", ""))
            self.c += 1
        self.list_keyword.pack(side = LEFT, fill = BOTH)
        self.scroll_view_2.config(command=self.list_keyword.yview)
        self.can.create_window(640, 200, window=self.frame)
        self.first = Button(self.can, text='KeyWord', relief='flat', bg='purple', width=120, command=self.acceuil)
        self.can.create_window(375, 15, window=self.first)
        self.second = Button(self.can, text='Result', relief='flat', bg='purple', width=120, command=self.display)
        self.can.create_window(1125, 15, window=self.second)
        
        
        # fonction de netoyage de la fenetre actuelle
    def clean(self):
        for e in self.can.winfo_children():
            e.destroy()
        
        
        # fonction de retour a la fenetre d'acceuil
    def acceuil(self):
        self.clean()
        self.image = self.can.create_image(690, 365, anchor=CENTER, image=self.img)
        self.entree = Entry(self.can, width=30, bg='pink', fg='black')
        self.can.create_window(630, 50, window=self.entree)
        self.bou_key_word = Button(self.can, text='add keyword', bg='purple', command=self.thread_utilisateur(self.entree.get()).start)
        self.can.create_window(430, 90, window=self.bou_key_word)
        self.bou_csv = Button(self.can, text='uploard', bg='purple', command=self.select_file)
        self.can.create_window(850, 90, window=self.bou_csv)
        self.frame = Frame(self.can, width=100, height=100)
        self.scroll_view_2 = Scrollbar(self.frame, orient=VERTICAL)
        self.scroll_view_2.pack(side=RIGHT, fill= Y)
        self.list_keyword = Listbox(self.frame, yscrollcommand=self.scroll_view_2.set)
        self.list_keyword.bind("<<ListboxSelect>>", self.inserer)
        self.cursor.execute("SELECT keyword FROM dashboard")
        self.r = list(self.cursor)
        self.c = 0
        for e in self.r:
            if self.c > 0 and e != self.r[self.c-1]:
                self.list_keyword.insert(0, str(e).replace("(", "").replace("'", "").replace(")", "").replace(",", ""))
            self.c += 1
        self.list_keyword.pack(side = LEFT, fill = BOTH)
        self.scroll_view_2.config(command=self.list_keyword.yview)
        self.can.create_window(640, 200, window=self.frame)
        self.first = Button(self.can, text='KeyWord', relief='flat', bg='purple', width=120, command=self.acceuil)
        self.can.create_window(375, 15, window=self.first)
        self.second = Button(self.can, text='Result', relief='flat', bg='purple', width=120, command=self.display)
        self.can.create_window(1125, 15, window=self.second)
        self.can.config(scrollregion=(0, 0, 1500, 500))
        print(self.can.winfo_children())
    #cette fonction renvoie le key_word entré dans la bare de recherche
    def envoi_info(self):
        self.kw_reception = self.entree.get()
        print(self.entree.get())
        return self.kw_reception
    #cette fonction lance la bloucle principale
    def mainloop(self):
        self.fen.mainloop()
    #cette fonction recupère et analyse le contenue de la barre de recherche
    def add_keyword(self, val):
        a = ys.analytics(val)
        a.r_a_k()
        return a.valides 
    #cette fonction enrégistre le resultat de l'analyse des données dans la database
    def save(self, kw_a_analyse=False):
        self.can.itemconfig(self.notice, text="Processing the keyword please wait...")
        if kw_a_analyse:
            try:
                data = self.add_keyword(kw_a_analyse)
            except:
                data = 'Err'
        else:
            try:
                data = self.add_keyword(self.entree.get())
            except:
                data = 'Err'
            print(self.entree.get())
        if data == 'Err':
            self.can.itemconfig(self.notice, text="Request quota exceeded. Try after 24h !")
        elif data == []:
            print("pas de resultats")
            self.can.itemconfig(self.notice, text="No mathing result found!!!")
        else:
            self.can.itemconfig(self.notice, text="Saving results found...")
            for d in data:
                elements = (d['name'], d['keyword'], d['video amount'], d['Avg views'], int(d['day since first update']), d['subscribers'], d['link'])
                try:
                    self.cursor.execute('INSERT INTO dashboard VALUES(?,?,?,?,?,?,?)', elements)
                    self.connection.commit()
                except sqlite3.IntegrityError:
                    print("Informations already saved")
                    self.can.itemconfig(self.notice, text="Informations already saved!")
                self.can.itemconfig(self.notice, text="Go to result table to see !")
        self.acceuil()
    #cette fonction permet de choisir et de charger un fichier csv 
    def select_file(self):
        choice_box = askopenfilename(title='open .csv file', initialdir='/', filetypes=(('csv file', '*.csv'), ('text files', '*.txt')))
        with open(choice_box, 'r') as cb:
            print('fichier ouvert')
            for l in cb.readlines():
                print('parcour du fichier')
                csv_kw = l.split(',')
                for e in csv_kw:
                    print(e)
                    threading.Thread(target=self.special, args=(e,)).start()
    #fonction speciale contre l'erreur _tkinter.TclError: can't delete Tcl command
    def special(self, kw_a_analyse):
        self.can.itemconfig(self.notice, text="Processing the keyword please wait...")
        if kw_a_analyse:
            try:
                data = self.add_keyword(kw_a_analyse)
            except:
                print("il y a quelque chose la!!!")
                data = 'Err'
        else:
            try:
                data = self.add_keyword(self.entree.get())
            except:
                data = 'Err'
            print(self.entree.get())
        if data == 'Err':
            self.can.itemconfig(self.notice, text="Request quota exceeded. Try after 24h !")
        elif data == []:
            print("pas de resultats")
            self.can.itemconfig(self.notice, text="No mathing result found!!!")
        else:
            self.can.itemconfig(self.notice, text="Saving results found...")
            for d in data:
                elements = (d['name'], d['keyword'], d['video amount'], d['Avg views'], int(d['day since first update']), d['subscribers'], d['link'])
                try:
                    self.cursor.execute('INSERT INTO dashboard VALUES(?,?,?,?,?,?,?)', elements)
                    self.connection.commit()
                except sqlite3.IntegrityError:
                    print("Informations already saved")
                    self.can.itemconfig(self.notice, text="Informations already saved!")
                self.can.itemconfig(self.notice, text="Go to result table to see !")
    #cette fonction permet d'eviter l'utilisation d'un meme thread
    def thread_utilisateur(self, arg_c):
        t_u = threading.Thread(target=self.save, args=(arg_c,))
        return t_u
        
    #cette fontion crée une fenetre de prévisualisation des keywords déja recherchés
        
    def inserer(self, event):
        valu =  self.list_keyword.curselection()[0]
        print(valu)
        self.entree.insert(0, self.list_keyword.get(valu))

    #cette fonction affiche a l'écrant les resultats contenues dans la database
    def display(self):
        critere = self.entree.get()
        requete, donnes = "", []
        self.clean()
        self.first = Button(self.can, text='KeyWord', relief='flat', bg='purple', width=120, command=self.acceuil)
        self.can.create_window(375, 15, window=self.first)
        self.second = Button(self.can, text='Result', relief='flat', bg='purple', width=120, command=self.display)
        self.can.create_window(1125, 15, window=self.second)
        if critere == "":
            self.cursor.execute("SELECT * FROM dashboard")
            donnes = list(self.cursor)
        elif critere!= "":
            for k in critere.split(','):
                requete = "SELECT * FROM dashboard WHERE keyword="+"'"+str(k)+"'"+"ORDER BY avg_views DESC"
                try:
                    self.cursor.execute(requete)
                except:
                    print("donne inexistente")
                print(requete)
                for e in list(self.cursor):
                    donnes.append(e)
        print(donnes)
        cmp = 0
        onglets = ['channel','keyword', 'video_amount', 'avg.views', 'days_since_first_update', 'subscribers', 'urls']
        # creation des entetes
        for e in range(167, 1169, 167):
            entr = Entry(self.can, bg='white', relief='flat', fg='black')
            entr.insert(0, onglets[cmp])
            self.can.create_window(e-83.5, 40, window=entr)
            cmp += 1
        cmp = 0
        #creation de la derniere entete
        entr = Entry(self.can, bg='white', width=45, relief='flat', fg='black')
        entr.insert(0, onglets[6])
        self.can.create_window(1185.5, 40, window=entr)
        #creation du contenue des entete
        y = 63
        for i in donnes:
            print(i)
            for e in range(167, 1169, 167):
                entr = Entry(self.can, bg='white', relief='flat', fg='black')
                entr.insert(0, i[cmp])
                self.can.create_window(e-83.5, y, window=entr)
                cmp += 1
            cmp = 0
            entr = Entry(self.can, bg='white', width=45, relief='flat', fg='black')
            entr.insert(0, i[6])
            self.can.create_window(1185.5, y, window=entr)
            y += 23
        self.can.config(scrollregion=(0,0,1500,y))
        

if __name__=="__main__":
    a = scraper()
    a.mainloop()

