#!/usr/bin/env python
# coding: utf-8

# # Исследование объявлений о продаже квартир
# ## Цель исследования:
#         Провести иследование данных о квартирах в Иркутске предоставленных сайтом Циан.
# ## Задачи исследования:
#         Выявить выгодные варианты объявлений по цене и району 
#         Доказать, что цена за квадратный метр зависит от района продажи квартиры 
# ## Декомпозиция работы:
#         1. Подготовка данных 
#         2. Предобработка данных
#         3. Анализ данных
#         4. Визуализация данных
#         5. Вывод о задачах исследования

# ### 1. Подготовка данных 

# In[1]:


#Импортируем библиотеки
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

#показывать всю информацию в колонках 
pd.set_option('display.max_colwidth', None)

#Загружаем данные 
data = pd.read_csv('C:/Users/admin/all/flat_3.csv', sep=';')

display(data.head())


# In[2]:


# переименование столбцов для удобного использования 
data = data.rename(columns={'Количество комнат': 'rooms', 
                               'Тип': 'type', 
                               'район': 'district', 
                               'Адрес': 'address', 
                               'Площадь, м2': 'area',
                               'Этаж': 'floor', 
                               'Цена': 'price', 
                               'Ремонт': 'repair', 
                               'Ссылка на объявление': 'link'})
# смотрим основную информацию о датафрейме
display(data.info())


# In[3]:


display(data['rooms'].unique())
display(data['type'].unique())
display(data['district'].unique())
display(data['repair'].unique())


# In[4]:


# изменим столбец с данными о колве квартир - уберем лишнюю информацию
data['rooms'] = data['rooms'].str.replace(',', ' ').str.replace('\D', '', regex=True) # удаляет данные в ячейке после ","
data.sample(5)


# ### 2. Предобработка данных
# Перед работой с данными необходимо произвести следующие изменения и анализ данных:
# ##### 1. Создадим дополнительные столбцы 
# Добавим столбцы "Этажей в доме" и столбец "Цена за квадратный метр":
# 1. Разделим столбец "floor": Возьмем из столбца "floor" информацию за знаком "/" и добавим столбец "floor_all" с данными о количестве этажей в доме
# 2. Добавим данные о цене за квадратный метр в новый столбец "price_square"
# 
# 
# ##### 2. Изменим типы объектов в следующих столбцах:
# *rooms* - изменить на тип объекта int\
# *floor* - изменить на int 
# 
# ##### 3. Работа с пропусками и дубликатами в данных. 
# 1. Определим количество пропущенных значениях в столбцах и если есть пропуски, то для дальнейшей работы необходимо их убрать, заменив их на подходящие по логике данные. 
# 2. Проверим данные на дубликаты по столбцам "Адрес" и "ID" - там не должны быть дубли, если они будут то строки необходимо удалить

# #### Разделим столбец "floor" и добавим столбец "price_square" с данными о цене за квадратный метр 

# data['floor_all'] = data['floor'].str.split('/').str.get(1)
# 

# data['floor'] = data['floor'].str.split('/').str.get(0)

# data.sample(5) 

# In[5]:


# добавим столбец 'floor_all'
data['floor_all'] = data['floor'].str.split('/').str.get(1)
data['floor'] = data['floor'].str.split('/').str.get(0)
data['price_square'] = (data['price'] / data['area'])/1000 # создадим столбец "price_square" с данными о цене за кв.м. и 
data['price'] = data['price']/1000000  # поделим результат на 100 для лучшего восприятия цены


# In[6]:


data['price'] = data['price'].round(1) #  округлим числа до десятых
data['price_square'] = data['price_square'].round(1)
data.sample(5) 


# Теперь данные в столбце "price" отображаются в млн., а данные в столбце "price_square" в тыс./за кв.м.

# #### 2. Изменим типы объектов 

# In[7]:


# изменим тип данных для дальнейшего исследовани
data['rooms'] = data['rooms'].fillna(0).astype('int')
data['floor'] = data['floor'].fillna(0).astype('int')


# In[8]:


display(data.sample(5))  # проверим изменненые данные
display(data.info())


# #### 3. Определим количество пропущенных значениях и исследуем на дубликаты в столбцах

# In[9]:


# посчитаем пропуски
print('Количество дубликатов:', data.duplicated().sum())
print('Количие пропусков:')
data.isnull().sum() 


# Дубликатов данных нет. 
# Пропуски в столбце с ремонтом и кол-вом комнат из-за отсутсивия информации - для работы с эти столбцом необходимо заменить пропущенные значения на 0 - как "нет информации о ремонте/комнатах":

# In[10]:


# замена пропусков
data['repair'] = data['repair'].fillna(0)


# ## Анализ данных
# ### Исследуем количество объектов по категориям: район продаж, количество комнат, площадь, цена за квадратный метр. Построим визуализации. 

# In[11]:


# районы
display(data['district'].value_counts())
data['district'].hist();


# ### Больше всего продаются квартиры в Октябрьском районе

# In[12]:


data['type'].unique() # посмотрим данные о типе квартир


# Изменим столбец с данными о типе квартиры: заменим данные на "second" - вторичное жилье и "new" - новостройка.

# In[13]:


data['type']
data = data.replace({'type':{'Продажа квартиры в новостройке':"new", 'Продажа квартиры': "second"}})
data.head()


# In[14]:


data['rooms'].unique()


# In[15]:


data[data['rooms'] == 0] 


# По полученным данным большенство квартир с кол-вом комнат = 0 это новостройки без ремонта. Остальные 5 квартир имеют площадь менее 31 квадрата - значит это студии. Оставим как есть.
display(data['rooms'].value_counts()) #посчитаем количество квартир в зависимости от количества комнат
data['rooms'].hist(figsize=(4,4)) #построим диаграмму 
# In[16]:


data_district = data.pivot_table(index = 'district', values = 'ID', columns='rooms', aggfunc = 'count').reset_index().fillna(0)
display(data_district) 
display(data_district.info())


# In[17]:


# строим гистограммы 

fig = px.histogram(data_district, # загружаем данные 
                   x=[0, 1, 2, 3, 4, 5], # указываем столбец с данными для оси X 
                   y= 'district',
                   title='Распределение') # указываем заголовок 
fig.update_layout(yaxis_title ='Районы') # подпись для оси X 
fig.update_layout(xaxis_title ='Количество комнат') # подпись для оси Y 
fig.show(); # выводим график


# В полученном результате видим преобладание однокомнатных квартир в любом из районов

# In[32]:


# можем посмотреть колличество каких квартир продается, 
# новостроек или вторичного жилья, по районам
data_price4 = data.pivot_table(index = 'district', values = 'ID', columns='type', aggfunc = 'count').reset_index()
data_price4['%_new'] = 100*(data_price4['new'] / data_price4['new'].sum()).round(3)
data_price4['%_second'] = 100*(data_price4['second'] / data_price4['second'].sum()).round(3)

data_price4


# Новостроек много в Правобережном районе - 28%. А объявлений вторичного жилья больше в Ленинском районе - 32,4%.

# In[34]:


# можем посмотреть колличество скольки комнатных квартир, 
# новостроек или вторичного жилья, в каких районах продается больше чем в остальных
data_price2 = data.pivot_table(index = ['district', 'rooms'], values = 'ID', columns='type', aggfunc = 'count')
data_price2


# ### Посмотрим заполнение данных в столбце с данными - цена за кв.метр

# In[42]:


# цена за квартиру
data['price'].describe().round(3)


# In[24]:


# цена за квадратный метр
display(data['price_square'].describe().round(1))
data['price_square'].hist(bins=100)  


#    Средняя цена за квадратный метр - 67.3 т.р./кв. А максиматльная сумма за квадрат - 346.2 т.р./кв Посмотрим эти объявления:

# In[25]:


data[data['price_square'] == 67.3] 


# In[26]:


data[data['price_square'] == 346.2] 


# Создам категории в датафрейме data - столбец cat_pricesquare с категориями:
# 
# 0–119 — 'менее 119 т.р за кв.м';\
# 120–140 — 'от 120 до 140 т.р за кв.м';\
# 141–152 — 'от 141 до 152 т.р за кв.м';\
# 152 и выше — 'свыше 152 т.р за кв.м'.

# In[45]:


def cat_pricesquare(income):
    try:
        if 0 <= income <= 119:
            return 'менее 119 т.р за кв.м'
        elif 120 <= income <= 140:
            return 'от 120 до 140 т.р за кв.м'
        elif 141 <= income <= 152:
            return 'от 141 до 152 т.р за кв.м'
        elif income >= 153:
            return 'свыше 152 т.р за кв.м'
    except:
        pass


# In[49]:


data['cat_pricesquare'] = data['price_square'].apply(cat_pricesquare)
display(data.sample(5)) 


# In[50]:


#  
# 
data_price5 = data.pivot_table(index = 'district', values = 'ID', columns='cat_pricesquare', aggfunc = 'count').reset_index()
# data_price5['%_new'] = 100*(data_price5['new'] / data_price5['new'].sum()).round(3)
# data_price5['%_second'] = 100*(data_price5['second'] / data_price5['second'].sum()).round(3)

data_price5


# In[51]:


# строим гистограммы 

fig = px.histogram(data_price5, # загружаем данные 
                   x=["менее 119 т.р за кв.м", "от 120 до 140 т.р за кв.м", "от 141 до 152 т.р за кв.м", "свыше 152 т.р за кв.м"], # указываем столбец с данными для оси X 
                   y= 'district',
                   title='Распределение') # указываем заголовок 
fig.update_layout(yaxis_title ='Районы') # подпись для оси X 
fig.update_layout(xaxis_title ='Количество комнат') # подпись для оси Y 
fig.show(); # выводим график


# In[ ]:




