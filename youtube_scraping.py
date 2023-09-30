from googleapiclient.discovery import build
from datetime import datetime
import json
from googleapiclient import discovery

path_json = 'rest.json'
with open(path_json, encoding="utf8") as f:
    service = json.load(f)

api_key_1 = XXX
api_key_2 = XXX
api_key_3 = XXX

youtube = discovery.build_from_document(service, developerKey=api_key_1)
youtube2 = discovery.build_from_document(service, developerKey=api_key_2)
youtube3 = discovery.build_from_document(service, developerKey=api_key_3)


#création de la class recherche permetant l'obtention des chaines relatives au topic

class recherche():
    def __init__(self, keyword, youtube_connector):
        self.connector = youtube_connector
        self.numero_key = 1
        self.keyword = keyword
        self.requete = self.connector.search().list(part='snippet', type='channel', q=self.keyword, maxResults=50)
        self.reponse = self.requete.execute()
        self.nom_de_la_chainne = []
        self.today = datetime.today()
        self.age = []
        self.id = []
        self.birth_day = None
    def tous_les_elements(self):
        for e in self.reponse['items']:
             self.nom_de_la_chainne.append(e["snippet"]['channelTitle'])
             self.birth_day = datetime.fromisoformat(e["snippet"]['publishTime'].replace('Z', ''))
             self.age.append((self.today-self.birth_day).days)
             self.id.append(e['id']['channelId'])
        print(self.nom_de_la_chainne, len(self.nom_de_la_chainne))
        print(self.age)
        print(self.id)
    def plus_de_resultats(self):
        try:
            requete2 = self.connector.search().list(part='snippet', type='channel', q=self.keyword, maxResults=50, pageToken=self.reponse['nextPageToken'])
            self.reponse = requete2.execute()
            return "parcours des pages suivantes"
        except:
            return "tous les resultats ont ete parcourus"
    def alleger(self):
        self.nom_de_la_chainne = []
        self.age = []
        self.id = []
#creation de la class canal permettant de récupérer les infos d'une chaine

class canal():
    def __init__(self, youtube_connector, canal_id, jours):
        self.youtube_connector = youtube_connector
        self.canal_id = canal_id
        self.semaine = jours/7
        self.requete = self.youtube_connector.channels().list(part="statistics", id=canal_id)
        self.reponse = self.requete.execute()
        self.stats = self.reponse['items'][0]['statistics']
        self.nbr_vue = int(self.stats['viewCount'])
        self.nbr_abo = int(self.stats['subscriberCount'])
        self.nbr_video = int(self.stats['videoCount'])
    def moy_vues(self):
        if  self.nbr_video != 0:
         return self.nbr_vue/self.nbr_video
        else:
            return 0
    def moy_post(self):
        if self.semaine != 0:
            return self.nbr_video/self.semaine
        else:
            return 0


#creation de la class analytics permettant l'analyse des topics recherchés

class analytics():
    def __init__(self, keyword):
        self.keyword= keyword
        #c'est a ce niveau que tu doit try except
        try:
            self.chercher = recherche(keyword=keyword, youtube_connector=youtube)
            self.chercher.tous_les_elements()
        except:
            try:
                self.chercher = recherche(keyword=keyword, youtube_connector=youtube2)
                self.chercher.tous_les_elements()
                print("utilisation de la clé 2")
            except:
                    self.chercher = recherche(keyword=keyword, youtube_connector=youtube3)
                    self.chercher.tous_les_elements()
                    print("utilisation de la clé 3")
        # stockage des chaine_yt récupérées
        self.nom_des_chaines = self.chercher.nom_de_la_chainne
        self.age = self.chercher.age
        self.identifiants = self.chercher.id
        self.valides = []
    #creation de la fonction de validation des chaines
    #la chaine youtube est validée si elle parvient à créer un code 5 ou 4
    def is_valide(self, age, moy_vue, total_des_vues, nbr_video, total_abo, moy_post):
        if  age <= 180:
            return True
        else:
            return False
    # creation de la fonction d'analyse
    def analyse(self):
        for e in range(len(self.nom_des_chaines)):
            #creation d'un objet canal permettant d'extraire toutes les data
            try:
                canale = canal(youtube_connector=youtube, canal_id=self.identifiants[e], jours=self.age[e])
            except:
                try:
                    canale = canal(youtube_connector=youtube2, canal_id=self.identifiants[e], jours=self.age[e])
                except:
                    canale = canal(youtube_connector=youtube3, canal_id=self.identifiants[e], jours=self.age[e])
            #analyse de la chaine_yt
            if self.is_valide(age=self.age[e], moy_vue=canale.moy_vues(), total_des_vues=canale.nbr_vue, nbr_video=canale.nbr_video, total_abo=canale.nbr_abo, moy_post=canale.moy_post()):
                self.valides.append({'name':self.nom_des_chaines[e], 'keyword':self.keyword, 'video amount': canale.nbr_video, 'Avg views':canale.moy_vues(), 'day since first update':self.age[e], 'subscribers':canale.nbr_abo, 'link':'youtube.com/channel/'+str(canale.canal_id)})
    def r_a_k(self):
        # parcours et analyse des données des chaine_yt stockées
        self.analyse()
        print(self.valides)
        # parcours des pages suivantes
        cmt = 0
        check = self.chercher.plus_de_resultats() 
        while check != "tous les resultats ont ete parcourus":
            self.chercher.alleger()
            self.chercher.tous_les_elements()
            self.nom_des_chaines = self.chercher.nom_de_la_chainne
            self.age = self.chercher.age
            self.identifiants = self.chercher.id
            self.analyse()
            print("page "+str(cmt))
            check = self.chercher.plus_de_resultats()
            cmt += 1

        
   
        

    

    
