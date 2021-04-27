# *-* coding: utf-8 *-*
import spacy
URL = []
CLEAN_WORDS = []
ACCEPTED_SYMBOLS = { ",", ".", "-", "'", "&", ":" }
TLD = { ".com", ".org", ".net", ".edu", ".gov", ".co.", ".io" }

sp = spacy.load("en_core_web_sm")
spacy_stopwords = sp.Defaults.stop_words
nltk_stopwords = { "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers",
"herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be",
"been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for",
"with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
"further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only",
"own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now" }

def extract_url(raw_text):
    for tld in TLD:
        try:
            idx = raw_text.index(tld)
            URL.append(raw_text[:idx + len(tld)])
            return raw_text[idx + len(tld):]
        except Exception:
            pass
    return raw_text


''' Refines the raw data collected from websites '''
def refine_text(raw_text):
    if type(raw_text) != str:
        print(f"cleanup(): string expected. got <{type(raw_text).__name__}>")
        return

    start = 0

    ''' Separates words that are together in a string text, iterating through each characters '''
    for i in range(len(raw_text)):
        if i + 1 >= len(raw_text):
            end = i + 1
            CLEAN_WORDS.append(extract_url(raw_text[start:end]))

        elif raw_text[i] == " ":
            end = i
            CLEAN_WORDS.append(extract_url(raw_text[start:end]))
            start = end + 1

        try:
            CLEAN_WORDS.remove("")
            CLEAN_WORDS.remove(" ")
        except Exception:
            pass

    stripped_text = " ".join(CLEAN_WORDS)
    clean_text, cleaner_text = "", ""


    for i in range(len(stripped_text)):
        if stripped_text[i] in ACCEPTED_SYMBOLS:
            clean_text += stripped_text[i]
            continue

        elif not stripped_text[i].isalnum():
            clean_text += " "
            continue
        
        ''' Checks two characters: the current [i] and the one in front of (after) it '''
        if i + 1 < len(stripped_text):
            if stripped_text[i].isdigit() and stripped_text[i+1].isalpha():
                clean_text += stripped_text[i] + " "

            elif stripped_text.isalpha() and stripped_text[i+1].isdigit():
                clean_text += stripped_text[i] + " "

            elif stripped_text[i].islower() and stripped_text[i+1].isupper():
                clean_text += stripped_text[i] + " "

            elif stripped_text[i].isupper() and stripped_text[i+1].islower():
                clean_text += " "  + stripped_text[i]

            else:
                clean_text += stripped_text[i]
        else:
            clean_text += stripped_text[i]

    clean_text = clean_text.split()
    for word in clean_text:
        if word.lower() not in spacy_stopwords and word.lower() not in nltk_stopwords:
            cleaner_text += word + " "

    return cleaner_text