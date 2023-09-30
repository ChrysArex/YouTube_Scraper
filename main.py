import youtube_scraping as ys
from datetime import datetime
import frontend_tk as f
import os 
import sqlite3
#creation du connecteur youtube
logger = ys.youtube

#verification de l'existence de la base de données et création en cas d'innexistence
chemin = os.getcwd()+"/BD_inf_resultat.sq3"
try:
    conn = sqlite3.connect(chemin, check_same_thread=False)
    curseur = conn.cursor()
except sqlite3.OperationalError:
    print("Erreur de connection a la database")
if __name__=='__main__':
    app = f.scraper(curseur=curseur, connection=conn)
    app.mainloop()
    conn.close()