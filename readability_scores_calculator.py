"""Modules providing regular expression matching operations, simple modal dialog to 
get a value from the user and a function ti calculate the square root of a given number"""
import re
from math import sqrt
from tkinter import filedialog


# Text analysis with RegEx

def caracteres(txt):
    """Counts the number of characters"""
    return len(re.findall(r'\w', txt))

def voyelles(txt):
    """Counts the number of vowels"""
    return len(re.findall(r'[aeiouœéèàâûù]', txt, re.I))

def digrammes(txt):
    """Counts the number of vowel digraphs"""
    return len(re.findall(r'(au)|(eu)|(ou)|(oû)|(où)|(oi)|(œu)|(ei)|(ai)|(ée)|(ue)|(ui)|(ua)', txt, re.I))

def trigrammes(txt):
    """Counts the number of vowel trigraphs"""
    return len(re.findall(r'(eau)|(oue)|(aie)', txt, re.I))

def syllabes_graphiques(txt):
    """Counts the number of written syllables by substracting the number of bigraphs and trigraphs from the number of vowels"""
    return voyelles(txt) - (digrammes(txt)+trigrammes(txt))

def mots(txt):
    """Counts the number of words"""
    return len(re.findall(r'\w+', txt))

def mots_plusdesixlettres(txt):
    """Counts the number of words consisting of more than six letters"""
    return len(re.findall(r'\w{7,}', txt))

def mots_plusdetroissyllabes(txt):
    """Counts the number of words consisting of more than three syllables"""
    mots_polysyllabiques = 0
    for mot in txt.split():
        if (syllabes_graphiques(mot)) >= 3 :
            mots_polysyllabiques+=1
    return mots_polysyllabiques

def phrases(txt):
    """Counts the number of sentences"""
    if len(re.findall(r'\w{2,}\s?[.?!]', txt)) == 0:
        return 1 # Prevents ZeroDivison error
    return len(re.findall(r'\w{2,}\s?[.?!]', txt))


# Readability formulas

def ari(txt):
    """Calculates the Automated Readability Index (ARI)"""
    return 4.71*(caracteres(txt)/mots(txt))+0.5*(mots(txt)/phrases(txt))-21.43

def coleman_liau(txt):
    """Calculates the Coleman-Liau index"""
    return 0.0588*((caracteres(txt)/mots(txt))*100)-0.296*((phrases(txt)/mots(txt))*100)-15.8

def fkgl(txt):
    """Calculates the Flesch-Kincaid Grade Level (FKGL)"""
    return 0.39*(mots(txt)/phrases(txt))+11.8*(syllabes_graphiques(txt)/mots(txt))-15.59

def gunning(txt):
    """Calculates the Gunning Fog index"""
    return 0.4*((mots(txt)/phrases(txt))+100*(mots_plusdetroissyllabes(txt)/mots(txt)))

def smog(txt):
    """Calculates the Simple Measure of Gobbledygook index (SMOG)"""
    return 1.043*(sqrt((mots_plusdetroissyllabes(txt)*(30/phrases(txt)))))+3.1291

def lix(txt):
    """Calculates the LIX index"""
    return mots(txt)/phrases(txt)+100*(mots_plusdesixlettres(txt)/mots(txt))

def rix(txt):
    """Calculates the RIX index"""
    return mots_plusdesixlettres(txt)/phrases(txt)


# Score analysis

def score_analysis(formula, score):
    '''Gives the reading levels corresponding to a score for each formula'''
    formula_scales = [['lix',59,50,40,30],
                        ['rix',7.1,5.3,2.9,1.8],
                        ['fkgl',15,12,5,1],
                        ['gunning',17,13,7,1],
                        ['smog',14,12,7,1],
                        ['ari',15,9,5,1],
                        ['coleman_liau',15,9,5,1]]
    for column in range(7):
        for row in range(5):
            if formula_scales[column][row] == formula :
                if score > formula_scales[column][1]:
                    return "Très difficile"
                if score > formula_scales[column][2]:
                    return "Difficile"
                if score > formula_scales[column][3]:
                    return "Intermédiaire"
                if score > formula_scales[column][4]:
                    return "Facile"
                return "Très facile"


# Print results

def print_readability_scores(txt):
    """Prints the readability scores and the grade levels corresponding"""
    return print (f'''
                La plupart des indices de lisibilité suivants ont été conçus pour l'Anglais. Les indices de lisibilité LIX
                et RIX sont les plus fiables pour évaluer le niveau de difficulté des textes français.

                INDICES DE LISIBILITE
                ---------------------
                LIX................................ {round(lix(txt), 2)} : {score_analysis('lix',lix(txt))}
                RIX................................ {round(rix(txt), 2)} : {score_analysis('rix',rix(txt))}
                Gunning fog........................ {round(gunning(txt), 2)} : {score_analysis('gunning',gunning(txt))}
                SMOG............................... {round(smog(txt), 2)} : {score_analysis('smog',smog(txt))}
                Flesch-Kincaid..................... {round(fkgl(txt), 2)} : {score_analysis('fkgl',fkgl(txt))} 
                Coleman-Liau....................... {round(coleman_liau(txt), 2)} : {score_analysis('coleman_liau',coleman_liau(txt))}
                Automated readability index........ {round(ari(txt), 2)} : {score_analysis('ari',ari(txt))}''')

def print_text_statistics(txt):
    """Prints the text stastistics that served to calculate the readability scores"""
    return print(f'''
                STATISTIQUES DU TEXTE
                ---------------------
                Caractères......................... {caracteres(txt)}
                Voyelles........................... {voyelles(txt)}
                Digrammmes......................... {digrammes(txt)}
                Trigrammes......................... {trigrammes(txt)}
                Syllabes graphiques................ {syllabes_graphiques(txt)}
                Mots............................... {mots(txt)}
                Mots Longs (>6 lettres)............ {mots_plusdesixlettres(txt)}
                Mots complexes (>2 syllabes)....... {mots_plusdetroissyllabes(txt)}
                Phrases............................ {phrases(txt)}
                ''')


# User input

def user_input():
    """User input : raw text"""
    filepath = filedialog.askopenfilename(title= "Chosissez un fichier en texte brut...",
    filetypes=[("Texte brut", "*.txt")])
    file=open(filepath, encoding="utf8", errors='ignore')
    plain_text=file.read()
    file.close()
    return plain_text


# Program

texte = user_input()
print_text_statistics(texte)
print_readability_scores(texte)
