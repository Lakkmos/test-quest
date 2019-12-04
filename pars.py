import requests,lxml
from bs4 import BeautifulSoup

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36', 'x-requested-with':'XMLHttpRequest'}
session = requests.Session()
gender = "Мужской"
lenX = 0
print('Введите логин:')
login = input()
#login = 'aleksandra.grinina@mail.ru' #Оставлю тестовый логин, на случай тестирования
print('Введите пароль:')
password = input()
#password = 'Fixprice123' #и пароль. Руками вводить тяжелее

params = {
    'login': login,
    'password': password,
    'AUTH_FORM': 'Y',
    'TYPE': 'AUTH',
    'backurl': '/personal/'
          }

session.post('https://fix-price.ru/ajax/auth_user.php', data=params, headers=headers)

url = 'https://fix-price.ru/personal/'
personal_data = session.get(url)
soup = BeautifulSoup(personal_data.text, 'lxml')

pdata = soup.find('div', class_='client-name')

pdata = soup.select('input[placeholder="*Фамилия"]')
print (pdata[0]['value'])
res = pdata[0]['value']
res = res+'\n'
pdata = soup.select('input[placeholder="*Имя"]')
print (pdata[0]['value'])
res = res+pdata[0]['value']
res = res+'\n'
pdata = soup.select('input[placeholder="*Отчество"]')
print (pdata[0]['value'])
res = res+pdata[0]['value']
res = res+'\n'
pdata = soup.select('input[placeholder="*EMAIL"]')
print (pdata[0]['value'])
res = res+pdata[0]['value']
res = res+'\n'
pdata = soup.select('input[placeholder="*Дата рождения"]')
print (pdata[0]['value'])
res = res+pdata[0]['value']
res = res+'\n'
pdata = soup.select('input[name="PERSONAL_GENDER"]')
try:
    if pdata[0]['checked']:
       gender = 'Женский'
except:
    gender=gender
print ('Пол: ',gender)
res = res+'Пол: '+gender
res = res+'\n'
pdata = soup.select('option[selected=""]')
print (pdata[0]['value'],', ', pdata[1]['value'])
res = res+pdata[0]['value']+', '+ pdata[1]['value']
res = res+'\n'
pdata = soup.select('input[class="checkbox"]')
try:
    if pdata[0]['checked']:
        print ('Email подписка')
        res = res+'Email подписка'
        res = res + '\n'
except:
    gender = gender
try:
    if pdata[1]['checked']:
        print('SMS подписка')
        res = res + 'SMS подписка'
        res = res + '\n'
except:
    gender = gender
pdata = soup.find_all('div', class_="personal-card__number")
pdata = str(pdata[0])
pdata = pdata.replace('<div class="personal-card__number">', '')
pdata = pdata.replace("</div>", '')
print ("Номер карты: ", pdata)
res = res +"Номер карты: "+pdata
res = res+'\n'+'\n'
res = res +'_________В_избранном_________'+'\n'+'\n'
pdata = soup.find_all('a',  class_="product-card__title")

for i in (range(len(pdata))):
    lenX = lenX + 1
    z = ''
    print (pdata[i].text.strip(),'\t\t\t\t\tfix-price.ru'+str(pdata[i]['href']))
    res = res + pdata[i].text.strip()+'\t\t\t\t\tfix-price.ru'+str(pdata[i]['href'])
    res = res + '\n'
    url = 'https://fix-price.ru'+str(pdata[i]['href'])
   # print (url)
    prod = session.get(url)
    prod_soup = BeautifulSoup(prod.text, 'lxml')
    pprod = prod_soup.find_all('div', itemprop="description")
    print(pprod[0].text.strip())
    res = res +pprod[0].text.strip()
    res = res + '\n'
    pprod = prod_soup.find_all('div', class_="tabs__params")
    for j in (range(len(pprod))):
        z = z+' '+str(pprod[j].text).replace("  ",'')+' '

    print (z.replace("\n",' '))
    res = res +z.replace("\n",' ')
    res = res + '\n'
    pprod = prod_soup.find_all('span', itemprop="price")
    print(pprod[0].text.strip(), "РУБ.")
    res = res +pprod[0].text.strip()+" РУБ."
    res = res + '\n'
    print ('_________________________________'+'\n')
    res = res +'_________________________________'+'\n'
    res = res + '\n'
ppage = soup.find('ul',  class_="paging__list")
ppage = ppage.find_all('a')
for b in (range(len(ppage))):
    url = 'https://fix-price.ru'+str(ppage[b]['href'])
    print(url+'\n')
    personal_data = session.get(url)
    soup = BeautifulSoup(personal_data.text, 'lxml')
    pdata = soup.find_all('a', class_="product-card__title")

    for i in (range(len(pdata))):
        lenX = lenX + 1
        z = ''
        print(pdata[i].text.strip(), '\t\t\t\t\tfix-price.ru' + str(pdata[i]['href']))
        res = res +pdata[i].text.strip()+ '\t\t\t\t\tfix-price.ru' + str(pdata[i]['href'])
        res = res + '\n'
        url = 'https://fix-price.ru' + str(pdata[i]['href'])
        # print (url)
        prod = session.get(url)
        prod_soup = BeautifulSoup(prod.text, 'lxml')
        pprod = prod_soup.find_all('div', itemprop="description")
        print(pprod[0].text.strip())
        res = res +pprod[0].text.strip()
        res = res + '\n'
        pprod = prod_soup.find_all('div', class_="tabs__params")
        for j in (range(len(pprod))):
            z = z + ' ' + str(pprod[j].text).replace("  ", '') + ' '

        print(z.replace("\n", ' '))
        res = res +z.replace("\n", ' ')
        res = res + '\n'
        pprod = prod_soup.find_all('span', itemprop="price")
        print(pprod[0].text.strip(), "РУБ.")
        res = res + pprod[0].text.strip()+ "РУБ."
        res = res + '\n'
        print('_________________________________'+'\n')
        res = res +'_________________________________'+'\n'
        res = res + '\n'

print ('Всего товаров в избранном:',lenX)
res = res + 'Всего товаров в избранном: '+str(lenX)+'\n'+'\n'

print ('Акции')
res = res + '____________Акции____________'

url = "https://fix-price.ru/actions/"
personal_data = session.get(url)
soup = BeautifulSoup(personal_data.text, 'lxml')
pdata = soup.find('ul', class_='paging__list')
last_link = pdata.find_all('li', class_='paging__item')
last_link = last_link[3].find('a')
z = last_link['href']
z = z.replace("/actions/?PAGEN_2=",'')
z = int(z)
pdata = soup.find_all('div', class_="action-card__desc")
for i in (range(len(pdata))):
    lenX = pdata[i].text.replace ('  ','')
    if lenX.find("акция завершена") ==-1:
        print(lenX)
        res = res + lenX
        print('---------------------------')
        res = res + '\n'
        res = res + '---------------------------'
        res = res + '\n'

for b in range(z-1):
    url = 'https://fix-price.ru/actions/?PAGEN_2='+str(b+2)

    personal_data = session.get(url)
    soup = BeautifulSoup(personal_data.text, 'lxml')
    pdata = soup.find_all('div', class_="action-card__desc")
    for i in (range(len(pdata))):
        lenX = pdata[i].text.replace('  ', '')
        if lenX.find("акция завершена") == -1:
            print(lenX)
            res = res + lenX
            print('---------------------------')
            res = res + '\n'
            res = res + '---------------------------'
            res = res + '\n'


with open('result.txt', 'w') as output_file:
  output_file.write(res)
session.close()
