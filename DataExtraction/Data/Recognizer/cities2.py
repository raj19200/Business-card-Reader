def is_city(token):

    # address = []
    sub_tokens = [tok.lower() for tok in token.split(",")]
    print(sub_tokens)
    # for e in sub_tokens[-1]:
    #     if e.isdigit():
    #         addr = sub_tokens[-2]
    #         return addr
    # else:
    #     return addr[-1]
    # print(a)
    a = ''.join(e for e in sub_tokens[-1] if e.isalnum() and not e.isdigit())
    return a
    # for token in tokens:
    #     commas = re.findall(r'\,',token)
    #     if(len(commas)>=2):
    #         address.append(token)
    # return address

if __name__ == "__main__":
    print(is_city('Citymall-1, Opp. Ice Factory, Nr. ICICI Bank, Kalol (N.G.).'))