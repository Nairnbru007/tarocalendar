import calendar
from .models import Calendata
from datetime import datetime, date, timedelta

path_to_tmps_ru={
'acc_active_email':'ru/acc_active_email.html',#+
'agreement':'ru/agreement.html',#+
'algorithm':'ru/algorithm.html',#+
'commercial':'ru/commercial.html',#+
'confirmation_acc':'ru/confirmation_acc.html',#+
'contacts':'ru/contacts.html',#+
'description':'ru/description.html',#+
'instruction':'ru/instruction.html',
'favorites':'ru/favorites.html',#+
'menu_footer':'ru/menu_footer.html',#+
'offer':'ru/offer.html',#+
'password_reset_confirm':'ru/password_reset_confirm.html',#-
'password_reset_mail':'ru/password_reset_mail.html',#+
'tarif':'ru/tarif.html',#+
'video':'ru/video.html',#+
}

path_to_tmps_en={
'acc_active_email':'en/acc_active_email.html',#+
'agreement':'en/agreement.html',#+
'algorithm':'en/algorithm.html',#+
'commercial':'en/commercial.html',#+
'confirmation_acc':'en/confirmation_acc.html',#+
'contacts':'en/contacts.html',#+
'description':'en/description.html',#+
'instruction':'en/instruction.html',
'favorites':'en/favorites.html',#+
'menu_footer':'en/menu_footer.html',#+
'offer':'en/offer.html',#+
'password_reset_confirm':'en/password_reset_confirm.html',#-
'password_reset_mail':'en/password_reset_mail.html',#+
'tarif':'en/tarif.html',#+
'video':'en/video.html',#+
}

months_num_ru={
    1:"Январь",
    2:"Февраль",
    3:"Март",
    4:"Апрель",
    5:"Май",
    6:"Июнь",
    7:"Июль",
    8:"Август",
    9:"Сентябрь",
    10:"Октябрь",
    11:"Ноябрь",
    12:"Декабрь",
    "Январь":1,
    "Февраль":2,
    "Март":3,
    "Апрель":4,
    "Май":5,
    "Июнь":6,
    "Июль":7,
    "Август":8,
    "Сентябрь":9,
    "Октябрь":10,
    "Ноябрь":11,
    "Декабрь":12,
}
months_num_en={
    1:"January",
    2:"Februare",
    3:"March",
    4:"April",
    5:"May",
    6:"June",
    7:"July",
    8:"August",
    9:"September",
    10:"October",
    11:"November",
    12:"December",
    "January":1,
    "Februare":2,
    "March":3,
    "April":4,
    "May":5,
    "June":6,
    "July":7,
    "August":8,
    "September":9,
    "October":10,
    "November":11,
    "December":12,
}

# (start(day, month), end(day, month))
sign_dates = (
    ((20, 3), (19, 4)),  # Aries
    ((20, 4), (20, 5)),
    ((21, 5), (20, 6)),
    ((21, 6), (22, 7)),
    ((23, 7), (22, 8)),
    ((23, 8), (22, 9)),
    ((23, 9), (22, 10)),
    ((23, 10), (21, 11)),
    ((22, 11), (21, 12)),
    ((22, 12), (19, 1)),
    ((20, 1), (17, 2)),
    ((18, 2), (19, 3)),  # Pisces
)

# English
en_dict = (
    (0, "Aries"),
    (1, "Taurus"),
    (2, "Gemini"),
    (3, "Cancer"),
    (4, "Leo"),
    (5, "Virgo"),
    (6, "Libra"),
    (7, "Scorpio"),
    (8, "Sagittarius"),
    (9, "Capricorn"),
    (10, "Aquarius"),
    (11, "Pisces"),
)

# Russian
ru_dict = (
    (0, "Овен"),
    (1, "Телец"),
    (2, "Близнецы"),
    (3, "Рак"),
    (4, "Лев"),
    (5, "Дева"),
    (6, "Весы"),
    (7, "Скорпион"),
    (8, "Стрелец"),
    (9, "Козерог"),
    (10, "Водолей"),
    (11, "Рыбы"),
)

# Num
num_dict = (
    (0, "1"),
    (1, "2"),
    (2, "3"),
    (3, "4"),
    (4, "5"),
    (5, "6"),
    (6, "7"),
    (7, "8"),
    (8, "9"),
    (9, "10"),
    (10, "11"),
    (11, "12"),
)

images = {
    'fire':'images/fire.png',
    'earth':'images/earth.png',
    'water':'images/water.png',
    'air':'images/air.png',
    'empty':'images/Empty.png',
}

language_dict = {
    'en_US': en_dict,
    'ru_RU': ru_dict,
    'num': num_dict,
    None: num_dict
}

tariff_dict={
    'Start':1,
    'Standart':2,
    'Full':3
}

def save_render(data):
    arr={}
    for i in data:
        if i!="csrfmiddlewaretoken":
            arr[i]=data[i]
    return arr



def algorithm_run_left(left_arr,the_date_str):
    temp=algorithm_run_glob(the_date_str)
    for i in range(1,9):
        left_arr['x1'+str(i)]=str(temp[i-1])
    return [{**left_arr},temp]

def algorithm_run_right(right_arr,the_date_str):
    temp=algorithm_run_glob(the_date_str)
    for i in range(1,9):
        right_arr['x2'+str(i)]=str(temp[i-1])
    return [{**right_arr},temp]

def algorithm_run_center(left_arr,center_arr,right_arr,left,right,the_date_str):
    temp=algorithm_run_glob(the_date_str)
    if left!=True:
        for i in range(1,9):
            left_arr['x1'+str(i)]=''
    if right!=True:
        for i in range(1,9):
            right_arr['x2'+str(i)]=''
    if left==True or right==True:
        for i in range(1,9):
            center_arr['x3'+str(i)]=str(temp[i-1])
    else:
        for i in range(1,9):
            center_arr['x3'+str(i)]=''
    return {**left_arr,**center_arr,**right_arr}

def sum_digits(n):
    s = 0
    while n:
        s += n % 10
        n //= 10
    return s

def algorithm_run_glob(the_date_str):
    # d.m.q.b.e.f.k.l
    # 1.2.3.4.5.6.7.8
    temp=the_date_str.split('.')

    d=int(temp[0])
    while d>22:
        d=sum_digits(d)
    m=int(temp[1])
    y=int(temp[2])
    q=y
    while q>22:
        q=sum_digits(q)
    b=d+m
    while b>22:
        b=sum_digits(b)
    e=d+q
    while e>22:
        e=sum_digits(e)
    f=m+q
    while f>22:
        f=sum_digits(f)
    #k=sum_digits(d)+sum_digits(m)+sum_digits(q)
    k = d + m + q
    l = sum_digits(k)
    if k>22:
        k="-"
    #if l<10:
    #    k='-'
    while l>9:
        l=sum_digits(l)

    if d == 22: d = 0
    if m == 22: m = 0
    if q == 22: q = 0
    if b == 22: b = 0
    if e == 22: e = 0
    if f == 22: f = 0
    if k == 22: k = 0
    if l == 22: l = 0
    temp=[d,m,q,b,e,f,k,l]
    return temp

def _(word_index, language=None):
    if language is not None:
        return language_dict.get(language)[word_index][1]
    language = locale.getlocale()
    return language_dict.get(language[0], language_dict.get('en_US'))[word_index][1]

def get_zodiac_sign(d, month=None, language=None):
    # params
    if month is None:
        month = int(d.month)
        day = int(d.day)
    else:
        day = int(d)
        month = int(month)
    # calculate
    for index, sign in enumerate(sign_dates):
        if (month == sign[0][1] and day >= sign[0][0]) or (month == sign[1][1] and day <= sign[1][0]):
            return _(index, language)
    return ''

def get_images_by_zod(zod_num_get):
    temp=""
    if zod_num_get in ["1","5","9"]:
        temp="fire"
    if zod_num_get in ["2","6","10"]:
        temp="earth"
    if zod_num_get in ["3","7","11"]:
        temp="air"
    if zod_num_get in ["4","8","12"]:
        temp="water"
    return images[temp]

alphabet={
    'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,
    'g':7,'h':8,'i':9,'j':10,'k':11,'l':12,
    'm':13,'n':14,'o':15,'p':16,'q':17,'r':18,
    's':19,'t':20,'u':21,'v':22,'w':23,'x':24,'y':25,'z':26,

    'а':1,'б':2,'в':3,'г':4,'д':5,'е':6,'ё':7,
    'ж':8,'з':9,'и':10,'й':11,'к':12,'л':13,
    'м':14,'н':15,'о':16,'п':17,'р':18,'с':19,
    'т':20,'у':21,'ф':22,'х':23,'ц':24,'ч':25,
    'ш':26,'щ':27,'ъ':28,'ы':29,'ь':30,'э':31,'ю':32,'я':33,
}
def fio_to_num(fio_str:str,index:str):
    summ1 = 0
    summ2 = 0
    summ3 = 0
    fio_temp = fio_str.replace('-','').lower()
    fio_temp=fio_temp.split(' ')
    #print(fio_temp)
    try:
        for i in fio_temp[0]:
            if i in alphabet:
                summ1=summ1+alphabet[i]
    except:
        print('error fio '+index+' [0]')
        pass
    try:
        #for i in ''.join(fio_temp[1:]):
        for i in fio_temp[1]:
            if i in alphabet:
                summ2=summ2+alphabet[i]
                #print(i)
    except:
        print('error fio '+index+' [1]')
        pass


    while summ1 > 22:
        summ1 = sum_digits(summ1)
    while summ2 > 22:
        summ2 = sum_digits(summ2)

    summ3 = summ1 + summ2
    while summ3 > 22:
        summ3 = sum_digits(summ3)

    if summ1 == 0: summ1 = '-'
    if summ2 == 0: summ2 = '-'
    if summ2 == '-': summ3 = '-'

    if summ1 == 22: summ1 = 0
    if summ2 == 22: summ2 = 0
    if summ3 == 22: summ3 = 0

    temp={}
    temp['fio'+index+'1'] = str(summ1)
    temp['fio'+index+'2'] = str(summ2)
    temp['fio'+index+'3'] = str(summ3)
    #print(temp)
    return temp