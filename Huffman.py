# -*- coding: utf-8 -*-
"""
PROJ631
Compression de données par codage de Huffman
"""
#Lit un texte donne en parametre
def lireTexte(texte):
    return open(texte,'r').read()

#Regarde si un caractere se trouve dans un texte donne
def existe(cc,liste):
    #Booleen test initialise a faux
    existe = False
    for i in liste :
        #Si on a le caractere dans le texte alors le booleen passe a vrai 
           if i[0] == cc :
                existe = True
    #On retourne le booleen
    return existe
        
#On recupere toutes les lettres differentes qui apparraissent dans un texte donne et on compte le nombre de fois qu'elles apparaissent.
def recupLettres(texte):
    #On lit le texte
    phrase = lireTexte(texte)
    #On initialise la listre de lettre a retourner
    alphabet = []
    #On parcours le texte
    for i in phrase :       
        cpt = 0
        #Si une lettre n'est pas repertoriee dans la liste de lettre on compte son nombre d'apparitions
        if not existe(i,alphabet):
            for j in phrase :
                if i == j :
                    cpt += 1
            #On ajoute la lettre et son nombre d'apparitions dans le texte a la liste a retourner
            alphabet.append([i,cpt])      
    return alphabet

#Methode qui trie la liste precedente en fonction de la frequence d'apparition des lettres
def triNumAlphabet(texte):
    #On prend la liste de lettres du texte en parametre
    alphabet = recupLettres(texte)
    #On fait un tri a bulles
    for k in range(len(alphabet)):
        for i in range(len(alphabet)-1) :
            #On veut ici un ordre croissant
            if alphabet[i][1] > alphabet[i+1][1]:
                trans = alphabet[i]
                alphabet[i] = alphabet[i+1]
                alphabet[i+1] = trans
    #On renvoie la liste de depart triee
    return alphabet

#On defini ,l'alphabet ASCII que l'on stocke dans un tableau
def asciiTab():
    tab = []
    Ascii = """ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~ """
    for k in Ascii:
        tab += [k]
    return tab

#Methode qui renvoie la position d'un caractere donne dans le tableau ASCII
def ordreAsciiCaractere(cc):
    tab = asciiTab()
    for k in range(len(tab)):
        if cc == tab[k]:
            return k

#Methode qui trie les lettres du texte de meme frequence en fonction de leur position dans le tableau ASCII
def triLettreAlphabet(texte):
    #On recupere notre tableau de lettres
    liste = triNumAlphabet(texte)
    #Tri a bulles
    for k in range(len(liste)):
        for i in range(len(liste)-1):
            if liste[i][1] == liste[i+1][1]:
                #Ordre croissant
                if ordreAsciiCaractere(liste[i][0])>ordreAsciiCaractere(liste[i+1][0]):
                    trans = liste[i]
                    liste[i] = liste[i+1]
                    liste[i+1] = trans    
    #La liste est triee
    return liste

#1.48s pour le fichier texte Alice

#On cree une classe arbre 
class Arbre :
    #On prend comme sur l'enonce le label, la frequence, le fils droit et le fils gauche en parametre pour definir nos arbres
    def __init__(self,label, frequence, fg, fd):
        self.label = label
        self.frequence = frequence
        self.fg = fg
        self.fd = fd
        
#On cree nos arbres a partir de la liste triee issu d'un texte choisi
def creerArbre(texte):
    liste = triLettreAlphabet(texte)
    foret = []
    for k in range(len(liste)):
        #On incremente une liste d'arbre avec en label la lettre et en frequence le compteur du tableau defini precedemment
        foret.append(Arbre(liste[k][0],liste[k][1],None,None))    
    #On retourne un tableau d'arbres
    return foret

#On cherche les mins t1 et t2 qui vont servir a incrementer t (voir consigne)
def minimum(texte):
    arbres = creerArbre(texte)
    nouvelleForet = []
    #Tant que la liste n'est pas vide
    while len(arbres)>1:
        i = 0
        #On recup t1 et t2 facilement car le tableau est trie
        t1 = arbres[0]
        t2 = arbres[1]
        tFreq = t1.frequence + t2.frequence
        #On defini l'arbre t
        t = Arbre(None,tFreq, t1, t2)
        nouvelleForet.append(t)
         #On supprime t1 et t2 de la liste pour pouvoir traiter les suivants
        del (arbres[0])
        del (arbres[0])
        #On ajoute t a la liste en cherchant le bon endroit pour que le tableau reste trie
        while i<len(arbres) and arbres[i].frequence< t.frequence :
            i += 1
        #On  l'insere a l'emplacement i de la liste 
        arbres.insert(i,t)
        #On retourne l'arbre de la liste qui est le resultat de la combinaison des precedents
    return arbres[0]

#On applique la methode sysBinaire
def code(arbre):
    return sysBinaire(arbre,'',[])

#Methode qui prend un arbre et qui renvoie une liste comprenant le labels des noeuds et leur code en binaire trouve en fonction de leur position dans l'arbre
def sysBinaire(arbre,position,listeValeurs):  
    #Si on a un label on a donc une lettre et sa position alors on l'ajoute a la liste finale
    if arbre.label !=None :
        listeValeurs.append([arbre.label,position])
    #Sinon on explore en profondeur l'arbre par recursivite
    else :
        sysBinaire(arbre.fg,position + '0',listeValeurs)
        sysBinaire(arbre.fd,position + '1',listeValeurs)
    #On retourne la liste comprenant des tuples de chacunes des lettres du texte et leur code en binaire
    return listeValeurs

#Methode qui va permettre de creer des fichier bin ou txt ou autre a partir du nom de fichiers existants
def nouvFormat(adresse, nouvFin):
    #On parcours l'adresse a l'envers
    for i in range(len(adresse)):
        adresse[:(len(adresse)-i)]
        #On cherche la fin de l'adresse (comme un .txt ou .bin par exemple)
        if adresse[-i]== '.':
            #On remplace la fin de l'adresse par la nouvelle fin demandee
            adresse += nouvFin
            return adresse
                
#Methode qui permet de creer le fichier des frequences des lettres demandees
def fichierFreq(texte):
    #On recupere la liste triee de l'alphabet du texte et des frequences
    liste = triLettreAlphabet(texte)
    texteFreq = ""
    #On recupere les donnes de cette liste sous forme d'un chaine de caractere
    for i in liste:
        texteFreq += str(i[0]) + " " + str(i[1]) + "\n"

    #On injecte la chaine de caractere implementee precedement dans le nouveau fichier freq
    with open(nouvFormat(texte, "_frequence.txt"),"w") as fichierFreq :
        fichierFreq.write(texteFreq)
    fichierFreq.close()

#Methode qui renvoie un texte binaire a partir d'une adresse d'un texte (cc) et de son alphabet
def texteCompresse(liste, texte):
    #On  recupere le texte sous forme d'une chaine de caractere
    texte = lireTexte(texte)
    cpt = 0
    txt = ""
    for i in range(len(texte)) :
        #On verifie par precaution si la lettre a convertir existe dans l'alphabet
        if existe(texte[i],liste):
            #On cherche les meme lettres dans chaque cas et on recupere le code binaire dans l'alphabet
            for k in liste :
                if k[0] == texte[i] :
                    if cpt >= 4 :
                        cpt = 0
                        txt += k[1] + " "
                    else:
                        txt += k[1]
                cpt += 1
    return txt    

#Methode qui regroupe le code binaire d'un texte en octets
def formatCompresse(texte):
    txtTrans = ''
    txtOct = ''
    #On cree une chaine de caractere sans espaces
    for k in texte :
        if k != " ":
            txtTrans += k
    #On rajoute des espaces tous les 8 caracteres
    for i in range(len(txtTrans)):
        if (i % 8) == 0 and i != 0:
            txtOct += ' '
        txtOct += txtTrans[i]
    return txtOct

#Methode qui cree un fichier dans lequel on met la forme compressee d'un texte
def compresse(texte):
     nbr = 0
     z = 7
     txtCompresse = bytes([0])
     #On recupere le texte sous forme binaire et triee par octets
     arb = minimum(texte)
     liste = code(arb)
     texteBin = texteCompresse(liste,texte)
     texteBinTrie = formatCompresse(texteBin)
     #On converti les octets en decimal puis on applique la fonction bytes afin de recuperer une chaine de caractere du texte compresse
     for k in texteBinTrie:
         #Si espace alors fin d'octet donc on remet les compteurs a zero et on ajoute la compression au resultat
         if k == ' ':
             txtCompresse += bytes([nbr])
             nbr = 0
             z = 7
         else: 
             #Conversion en decimal si nbr binaire
             nbr += 2**(z)*int(k)
             z-=1
    #On ajoute ce texte compresse a un nouveau fichier binaire
     with open(nouvFormat(texte, "_compresse.bin"),"wb") as fichierCompresse :
         fichierCompresse.write(txtCompresse)
    #On renvoie le texte compresse sous forme d'une cc pour pouvoir le reutiliser
     return txtCompresse
         
#On calcule le taux de compression d'un texte a compresser
def tauxCompression(texte):
    #On recupere le texte compresser
    texteCompresse = compresse(texte)
    #Formule de m'enonce
    return 1-(len(texteCompresse)/len(texte))

#On calculele nombre moyen de bits de stockage par caractere dans un texte a compresser
def nbrMoyBitsStockCc(texte):
    #On recupere le texte compresse
    texteCompress = compresse(texte)
    #On recupere l'alphabet de ce texte
    alphabet = triLettreAlphabet(texte)
    #On multiplie la taille du texte compresse par 8 (car chaque caractetre est code sur un octet)
    #Et on divise par la taille du tableau comprenant les lettres et l'alphabet car on veut la valeur moyenne donc on divise par le nombre de lettres
    return 8*len(texteCompress)/len(alphabet)
