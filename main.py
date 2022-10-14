import tarfile
import re
import io
import time

tar = tarfile.open('./enron_mail_20150507.tar.gz', mode='r:gz')

NO_OF_CHARS = 256
def badCharHeuristic(string, size):
	badChar = [-1]* NO_OF_CHARS
	for i in range(size):
		badChar[ord(string[i])] = i
	return badChar

def boyerMoore(txt, pat):
    m = len(pat)
    n = len(txt)
    badChar = badCharHeuristic(pat, m)
    s = 0
    while(s <= n-m):
        j = m-1
        while j>=0 and pat[j] == txt[s+j]:
            j -= 1
        if j<0:
            return True
        else:
            s += max(1, j-badChar[ord(txt[s+j])])

# itens A, B e D
def func1():
    regexCountries = re.compile('[^A-Za-z](AF|AX|AL|DZ|AS|AD|AO|AI|AQ|AG|AR|AM|AW|AU|AT|AZ|BS|BH|BD|BB|BY|BE|BZ|BJ|BM|BT|BO|BQ|BA|BW|BV|BR|IO|BN|BG|BF|BI|KH|CM|CA|CV|KY|CF|TD|CL|CN|CX|CC|CO|KM|CG|CD|CK|CR|CI|HR|CU|CW|CY|CZ|DK|DJ|DM|DO|EC|EG|SV|GQ|ER|EE|ET|FK|FO|FJ|FI|FR|GF|PF|TF|GA|GM|GE|DE|GH|GI|GR|GL|GD|GP|GU|GT|GG|GN|GW|GY|HT|HM|VA|HN|HK|HU|IS|IN|ID|IR|IQ|IE|IM|IL|IT|JM|JP|JE|JO|KZ|KE|KI|KP|KR|KW|KG|LA|LV|LB|LS|LR|LY|LI|LT|LU|MO|MK|MG|MW|MY|MV|ML|MT|MH|MQ|MR|MU|YT|MX|FM|MD|MC|MN|ME|MS|MA|MZ|MM|NA|NR|NP|NL|NC|NZ|NI|NE|NG|NU|NF|MP|NO|OM|PK|PW|PS|PA|PG|PY|PE|PH|PN|PL|PT|PR|QA|RE|RO|RU|RW|BL|SH|KN|LC|MF|PM|VC|WS|SM|ST|SA|SN|RS|SC|SL|SG|SX|SK|SI|SB|SO|ZA|GS|SS|ES|LK|SD|SR|SJ|SZ|SE|CH|SY|TW|TJ|TZ|TH|TL|TG|TK|TO|TT|TN|TR|TM|TC|TV|UG|UA|AE|GB|US|UM|UY|UZ|VU|VE|VN|VG|VI|WF|EH|YE|ZM|ZW|AFG|ALB|DZA|ASM|AND|AGO|AIA|ATA|ATG|ARG|ARM|ABW|AUS|AUT|AZE|BHS|BHR|BGD|BRB|BLR|BEL|BLZ|BEN|BMU|BTN|BOL|BIH|BWA|BVT|BRA|IOT|VGB|BRN|BGR|BFA|BDI|KHM|CMR|CAN|CPV|CYM|CAF|TCD|CHL|CHN|CXR|CCK|COL|COM|COD|COG|COK|CRI|CIV|CUB|CYP|CZE|DNK|DJI|DMA|DOM|ECU|EGY|SLV|GNQ|ERI|EST|ETH|FRO|FLK|FJI|FIN|FRA|GUF|PYF|ATF|GAB|GMB|GEO|DEU|GHA|GIB|GRC|GRL|GRD|GLP|GUM|GTM|GIN|GNB|GUY|HTI|HMD|VAT|HND|HKG|HRV|HUN|ISL|IND|IDN|IRN|IRQ|IRL|ISR|ITA|JAM|JPN|JOR|KAZ|KEN|KIR|PRK|KOR|KWT|KGZ|LAO|LVA|LBN|LSO|LBR|LBY|LIE|LTU|LUX|MAC|MKD|MDG|MWI|MYS|MDV|MLI|MLT|MHL|MTQ|MRT|MUS|MYT|MEX|FSM|MDA|MCO|MNG|MSR|MAR|MOZ|MMR|NAM|NRU|NPL|ANT|NLD|NCL|NZL|NIC|NER|NGA|NIU|NFK|MNP|NOR|OMN|PAK|PLW|PSE|PAN|PNG|PRY|PER|PHL|PCN|POL|PRT|PRI|QAT|REU|ROU|RUS|RWA|SHN|KNA|LCA|SPM|VCT|WSM|SMR|STP|SAU|SEN|SCG|SYC|SLE|SGP|SVK|SVN|SLB|SOM|ZAF|SGS|ESP|LKA|SDN|SUR|SJM|SWZ|SWE|CHE|SYR|TWN|TJK|TZA|THA|TLS|TGO|TKL|TON|TTO|TUN|TUR|TKM|TCA|TUV|VIR|UGA|UKR|ARE|GBR|UMI|USA|URY|UZB|VUT|VEN|VNM|WLF|ESH|YEM|ZMB|ZWE)[^A-Za-z]')
    regexDollar = re.compile('(\$[0-9]+([.,][0-9]+)?\s?((B|[Bb]illions?)?|(MM|[Mm]illions?)?|([Kk]|M)?)?\s)')
    regexUrl = re.compile('((http://|https://)?(www.)([a-zA-Z])+.[a-z]+(.[a-z]+)+)')
    countries = []
    maxValue = 0
    maxValueStr = ''
    maxValueMember = None
    addrAmount = {}
    for member in tar.getmembers():
        fileBin = tar.extractfile(member)
        if fileBin:
            file = io.TextIOWrapper(fileBin)
            for line in file.readlines():
                matchCountries = regexCountries.findall(str(line.strip()))
                for match in matchCountries:
                    if not match[0] in countries:
                        countries.append(match[0])
                matchDollar = regexDollar.findall(str(line.strip()))
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
                matchURL = regexUrl.findall(str(line.strip()))
                for match in matchURL:
                    if match[0] in addrAmount:
                        addrAmount[match[0]] +=1
                    else:
                        addrAmount[match[0]] = 1

    sortedAddrAmount = {k: v for k, v in sorted(addrAmount.items(), key=lambda item: item[1], reverse=True)}
    # a)
    print(f"Número total de países: {len(countries)}")
    # b)
    print(f"Maior valor em dólar de {maxValueStr} encontrado no arquivo {maxValueMember.name}")
    # d)
    print(f"""URLs mais frequentes:
    {list(sortedAddrAmount.keys())[0]}: {list(sortedAddrAmount.values())[0]} correspondências
    {list(sortedAddrAmount.keys())[1]}: {list(sortedAddrAmount.values())[1]} correspondências
    {list(sortedAddrAmount.keys())[2]}: {list(sortedAddrAmount.values())[2]} correspondências
    {list(sortedAddrAmount.keys())[3]}: {list(sortedAddrAmount.values())[3]} correspondências
    {list(sortedAddrAmount.keys())[4]}: {list(sortedAddrAmount.values())[4]} correspondências
    """)
    return True

# item F
def func2():
    members = tar.getmembers()
    regexPrice = re.compile('(price)')
    initRegexTime = time.time()
    regexTime = 0
    for member in members:
        fileBin = tar.extractfile(member)
        if fileBin:
            file = io.TextIOWrapper(fileBin)
            for line in file.readlines():
                matchPrice = regexPrice.findall(str(line.strip()))
                if len(matchPrice) > 0:
                    regexTime = time.time() - initRegexTime
                    break
            else: 
                continue
            break
    initBMTime = time.time()
    BMTime = 0
    for member in members:
        fileBin = tar.extractfile(member)
        if fileBin:
            file = io.TextIOWrapper(fileBin)
            for line in file.readlines():
                bm = boyerMoore(str(line.strip()), "price")
                if bm:
                    BMTime = time.time() - initBMTime
                    break
            else: 
                continue
            break
    print(f"Tempo para achar a palavra 'price':\nRegEx: {regexTime} s\nBoyer Moore: {BMTime} s")   

# item C
def func3():
    regexEmail = re.compile('(([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+)')
    maxEmails = 0
    maxEmailsMember = None
    for member in tar.getmembers():
        fileBin = tar.extractfile(member)
        if fileBin:
            file = io.TextIOWrapper(fileBin)
            aux = 0
            for line in file.readlines():
                matchEmail = regexEmail.findall(str(line.strip()))
                aux+=len(matchEmail)
            if aux > maxEmails:
                maxEmails = aux
                maxEmailsMember = member
                print(f'RESULTADO PARCIAL: Maior quantidade de emails ({maxEmails}) no arquivo {maxEmailsMember.name}')
    print(f'Maior quantidade de emails ({maxEmails}) no arquivo {maxEmailsMember.name}')

if __name__ == '__main__':
    func1()
    func2()
    func3()