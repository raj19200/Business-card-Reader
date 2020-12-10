import re
from difflib import SequenceMatcher

# def is_website(txt):
#     isemail = False
#     subtokens = [tok.lower() for tok in txt.split()]
#     for subtoken in subtokens:
#         if(isemail):
#             return subtoken
#         a = SequenceMatcher(None, subtoken, 'web').ratio()
#         b = SequenceMatcher(None, subtoken, 'website').ratio()
#         c = SequenceMatcher(None, subtoken, 'www').ratio()
#         if(max(a,b,c)>0.9):
#             isemail = True

#     txt = txt.lower()
#     w = re.findall(r'(^(?:http\:\/\/|https\:\/\/)?(?:[a-z0-9][a-z0-9\-]*\.?)+[a-z0-9][a-z0-9\-]*$)',txt)
#     return w

def is_website(txt):
    # txt = txt.lower()
    W=[]
    w = re.findall(
    r'((?:https?:\/\/)?(?:www\.)[-a-zA-Z0-9:%._\+~#=]{2,256}\.[a-z]{2,4}\b(?:[-a-zA-Z0-9@:%_\+.~#?&//=]*)|(?:https?:\/\/)?(?:www\.)?(?!ww)[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,4}\b(?:[-a-zA-Z0-9@:%_\+.~#?&//=]*))',txt)
    for s in w:
        if '@' not in s:
            W.append(s)
    # if(txt.find("\\\\") >= 0 or txt.find("www") >= 0 or txt.find('web') >= 0 or txt.find('http') >= 0):
    #     return txt
    # else:
    #     return ' '
    return W


if __name__ == "__main__":
    print(is_website("web : mkumarhub.com ¢ E-mail Id: mkumarhub@gmail.com"))