# Take JSON file, import select records
import json
import pandas as pd

    
def populate(filename):
    # Import data
    data = []
    i = 0
    with open(filename) as file:
        #data = json.load(file)
        for line in file:
            data.append(json.loads(line))
            i += 1
    return data

if __name__ == '__main__':
    import re
    from bs4 import BeautifulSoup # to parse html
    from operator import itemgetter
    filename = 'data/ufodata.json'
    data = populate(filename)
    incoming = dict()
    df = pd.DataFrame()
    for i in range(len(data)):
        temp = pd.Series()
        soup = BeautifulSoup(data[i]['html'], 'html.parser')
        incoming[i] = [text for text in soup.stripped_strings][12:-1]
        try:
            occ, rep, loc, sha = itemgetter(0, 1, 3, 4)(incoming[i])
            try:
                temp['occur'] = re.findall('(\d*/\d*/\d*\ )', occ)[0]
            except IndexError:
                continue
            try:
                temp['reported'] = re.findall('(\d*/\d*/\d*\ \d*:\d*:\d*\ (A|P)+M)', rep)[0][0]
            except IndexError:
                continue
            try:
                temp['location'] = re.findall('[A-Z]{2}', loc)[0]
            except IndexError:
                continue
            try:
                temp['shape'] = re.findall('[a-zA-Z]*$', sha)[0]
            except IndexError:
                continue
            temp['document'] = ' '.join(incoming[i][6:])
            df = df.append(temp, ignore_index = True)
        except IndexError:
            continue
    df.to_csv('data/df.csv')
    

