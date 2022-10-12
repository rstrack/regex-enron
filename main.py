import tarfile
import re
import time

tar = tarfile.open('./enron_mail_20150507.tar.gz', mode='r:gz')

regexDollar = re.compile('(\$[0-9]+([.,][0-9]+)?\s?((B|[Bb]illions?)?|(MM|[Mm]illions?)?|([Kk]|M)?)?\s)')
regexEmail = re.compile('(([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+)')
regexUrl = re.compile('((http://|https://)?(www.)([a-zA-Z])+.[a-z]+(.[a-z]+)+)')
regexPrice = re.compile('(price)')

maxValue = 0
maxValueStr = ''
maxValueMember = None

maxEmails = 0
maxEmailsMember = None
emailNumber = 0
priceNumber = 0

addrAmount = {}
# inicio = time.time()
for member in tar.getmembers():
    file = tar.extractfile(member)
    if file:
        f = file.read()
        #a
        matchEmailNumber = regexEmail.findall(str(f.strip(), 'utf-8'))
        for match in matchEmailNumber:
            print(match[0])
        emailNumber += len(matchEmailNumber)
        #Devido aos emails possuírem a terminação ".com", é impossível saber o país de residência do email.
        #Portanto, optamos por fazer uma contagem total dos emails.

        #b
        matchDollar = regexDollar.findall(str(f.strip(), 'utf-8'))
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
        #c
        # extremamente lento, devido a enorme quantidade de emails
        matchEmail = regexEmail.findall(str(f.strip(), 'utf-8'))
        if len(matchEmail) > maxEmails:
            maxEmails = len(matchEmail)
            maxEmailsMember = member
        #d
        matchURL = regexUrl.findall(str(f.strip(), 'utf-8'))
        for match in matchURL:
            if match[0] in addrAmount:
                addrAmount[match[0]] +=1
            else:
                addrAmount[match[0]] = 1

        #f
        matchPrice = regexPrice.findall(str(f.strip()))
        for match in matchPrice:
            print("Achou!")
        priceNumber += 1
        
# fim = time.time()
# tempoPrice = (fim - inicio)
sortedAddrAmount = {k: v for k, v in sorted(addrAmount.items(), key=lambda item: item[1], reverse=True)}

        
# a)
print(f"Número de emails: {emailNumber}")

# b)
print(f"Maior valor em dólar de {maxValueStr} encontrado no arquivo {maxValueMember.name}")

# c)
print(f"Maior número de emails ({maxEmails}) na mensagem {maxEmailsMember.name}")

# d)
print(f"""URLs mais frequentes:
{list(sortedAddrAmount.keys())[0]}: {list(sortedAddrAmount.values())[0]} correspondências
{list(sortedAddrAmount.keys())[1]}: {list(sortedAddrAmount.values())[1]} correspondências
{list(sortedAddrAmount.keys())[2]}: {list(sortedAddrAmount.values())[2]} correspondências
{list(sortedAddrAmount.keys())[3]}: {list(sortedAddrAmount.values())[3]} correspondências
{list(sortedAddrAmount.keys())[4]}: {list(sortedAddrAmount.values())[4]} correspondências
""")

#f)
print(f"Price(s) encontrados(s): {priceNumber}")
# print(f"Tempo total do regex: {tempoPrice}")
#durante o teste rodando apenas o regex do price os resultados obtidos foram:
# Price(s) encontrados(s): 517401
# Tempo total do regex: 58.482699155807495