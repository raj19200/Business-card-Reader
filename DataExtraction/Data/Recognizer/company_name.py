import os
path = os.path.dirname(os.path.abspath(__file__))

common_company_tokens = []

with open(path + '/../Dataset/common_prefix_suffix_company.txt') as company_tokens:
    for token in company_tokens:
        comp_token = token.strip().lower()
        if len(comp_token) > 0:
            common_company_tokens.append(comp_token)


def is_company_name(line):
    line = line.lower().split(' ')
    for token in common_company_tokens:
        if line.__contains__(token):
            return True
    return False
