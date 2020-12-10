def is_pincode2(token):
    sub_tokens = [tok.lower() for tok in token.split(",")]
    print(sub_tokens)
    # p = ''.join(e for e in token if e.isalnum() and e.isdigit())
    # return p
    a = ''.join(e for e in sub_tokens[-1] if e.isalnum() and e.isdigit())
    return a

if __name__ == "__main__":
    print(is_pincode2('27,CamaCommercialCentre,Opp.MirzapurCourt,|-Mirzapur,Ahmedabad-1.'))