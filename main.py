import tarfile
import re

tar = tarfile.open('./enron_mail_20150507.tar.gz', mode='r:gz')
regexDollar = re.compile('(\$[0-9]+([.,][0-9]+)?\s?((B|[Bb]illions?)?|(MM|[Mm]illions?)?|([Kk]|M)?)?\s)')

maxValue = 0
maxValueStr = ''
maxValueMember = None

for member in tar.getmembers():
    file = tar.extractfile(member)
    if file:
        f = file.read()
        matchDollar = regexDollar.findall(str(f.strip()))
        for match in matchDollar:
            value = re.search('[0-9]+(.[0-9]+)?', match[0]).group().replace(',','')
            if match[3] != '':                  #bilhão
                value = float(value)*pow(10,9)
            elif match[4] != '':                #milhão
                value = float(value)*pow(10,6)
            elif match[5] != '':                #milhar
                value = float(value)*pow(10,3)
            else: value = float(value)
            if value > maxValue:
                maxValue = value
                maxValueStr = match[0]
                maxValueMember = member

print(f"Maior valor em dólar de {maxValueStr} encontrado no arquivo {maxValueMember.name}")
