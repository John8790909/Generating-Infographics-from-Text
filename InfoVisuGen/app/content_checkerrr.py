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


'''
idx is for index. tld for top level domains
for tld in the variable containing a bunch of
top level domains, get me the index of the
top level domain in the raw text. whether its .com .org .gov .co.uk
i don't know, but if a top level domain from the
TLD variable is in this text, then look for it, 
and give me its location. this location is referred to
as the index. remember that strings are arrays,
so doing  my_string[4] is perfectly fine. 
strings have a function called .index() which will
give you the index of an element. elements are the values inside an array
so anyways, raw_text.index(tld) this will give me the
index or the location of this tld string. and then im saving that
to a variable called idx. so idx is the index of that tld.
url.append(raw_text[:idx + len(tld)])
raw_text[:4] means, give me everything from the start up until the
4th character in this string. this is called string slicing
in the code below, I'm doing raw_text[:idx + len(tld)]
what this means is, get me everything from the start up until idx
which idx is the location of the top level domain. so get me everything,  up until
that point. so if i have google.com,  get me the start up until the location of the tld
so.... i will get google  but i want to include the top level domain,  so i specify
idx + len(tld)  so if the tld has a length of 4, it will give me
up until idx, and then 4 more. so this will include the whole thing, which... is a url
so i will get google.com
the reason im doing this is because, well... i want to remove every single url in the text
it's, not needed imo. so im trying to trim the text as much as i can. part of it is
removing all the urls inside of it. well, there's still more code.
return raw_text[idx + len(tld):]
this means, return everything, from the location of the tld, + its length
and return everything after that. usually text would combine and stuff. google.comwas made by ...
so it will remove google.com and say just,  was made by ... it isn't foolproof, there will be some misses
but i think it should work most of the time
'''
def extract_url(raw_text):
    for tld in TLD:
        try:
            idx = raw_text.index(tld)
            URL.append(raw_text[:idx + len(tld)])
            return raw_text[idx + len(tld):]
        except Exception:
            pass
    return raw_text


def cleanup(raw_text):
    if type(raw_text) != str:
        print(f"cleanup(): string expected. got <{type(raw_text).__name__}>")
        return

    start = 0
		
    '''
    i + 1 >= len(raw_text) is, pretty much just making sure that i dont get an IndexError, because i will be
    doing a lot of i + 1 stuff, which will give me an IndexError if im not careful so thats there to prevent that
    start is the start of the word, and end is the end of the word. so it will append the whole word. but also im extracting any urls that may be inside of it
    suppose the word is combined together with a url
    '''
    for i in range(len(raw_text)):
        if i + 1 >= len(raw_text):
            end = i + 1
            CLEAN_WORDS.append(extract_url(raw_text[start:end]))
				
        elif raw_text[i] == " ":
            ''' if there's a space, assume thats the end of the word and a new word is about to come up. so we can conclude the word here
            and then append it to the clean_words variable. and then we are setting the start variable to the new position of, what i assume will be the next word
            and carry on from there. so if there's a space, assume the word has ended, set end whatever i is, and append the current start position to the end position,
            and then let start be the start of the next word. i guess i could have also just .split() but at the time i was kinda, crazy about controlling each single character
            '''
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

    ''' stripped_text is the version of the text except, smaller. after everything has been extracted.
    ~ but now i want to remove even more from it. i want to remove every symbol that isnt in the accepted_symbols variable.
    ~ i want to keep every comma, period, hyphen, single quote, ampersand, colon i think those are important
    ~ for example, someone's name may be, anne-marie claire or something like that. commands and periods are important to keep too imo
    ~ so basically remove every other symbol that isnt part of the accepted_symbols list '''
    for i in range(len(stripped_text)):
      
        ''' this is the part of the loop that actually removes any weird symbols other than the ones specified in the above list '''
        if stripped_text[i] in ACCEPTED_SYMBOLS:
            clean_text += stripped_text[i]
            continue
				
        elif not stripped_text[i].isalnum():
            clean_text += " "
            continue

        '''
        i + 1 < len(stripped_text) is just to make sure i dont get IndexError while performing these operations
        this statement just separates words that may have been combined together. so again, im trying to control, everyyyyy single character
        i think it's the safest way to do this. so im comparing each character and checking these conditions: if the current character is a digit, 
        and the next character is alphabetical, add a space right after the current character. then im doing the inverse. if current character is alphabetical
        and the next character is a digit, add a space after the current character. this is to help separate things that may have been combined together
        then im checking, if the current character is lowercase and the next character is uppercase, add a space in between them. so like this
        and thenJohn went to school.  it should read,  and then John went to school. so thats what that does. and, i think the last elif is doing the same 
        exact thing tbh... i don't remember if i tested that. but basically, if the current character is uppercase, and the next letter is lowercase,
        add a space before the uppercased letter. so...... and thenJohn went to school  will become  and then John went to school. but also if i did
        and thenUSA won the olympics. hmmmmm, honestly i think i can remove that last elif. i dont know how the results will be affected. i know if i put it there
        it must have been because i saw something, and decided to keep it there. but i dont remember what exactly i saw that made me want to write that line. 
        to my understanding, it does essentially the same thing the previous elif does. but idk. 
        '''
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
    
    '''
    and last but not least, stop words. trying to strip as much as i can from the text. the smaller the text, the better. so im trying to
    remove everything that isnt needed. stopwords is the last step in this function. im removing words that are found in spacy's stop words and also
    nltk's stopwords. i made a big stopwords list above. i basically have spacy's stop words and some more stuff that i felt weren't needed
    and im appending every word that isnt in either stopword lists. honestly this code overall looks bad. i feel that it can be more legible if i changed
    the way i did things and the way i named them
    '''
    for word in clean_text:
        if word.lower() not in spacy_stopwords and word.lower() not in nltk_stopwords:
            cleaner_text += word + " "

    return cleaner_text