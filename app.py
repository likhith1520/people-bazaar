from flask import Flask,render_template,request
import pandas as pd
import requests as rs
from bs4 import BeautifulSoup

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/',methods=['POST'])
def my_form_post():
    x=request.form['ctnumber']
    item=request.form['pname']
    pd.set_option("display.max_rows",6)
    pd.set_option('max_colwidth',100)
    cols=["Name","price"]

    df=pd.DataFrame(columns=cols)
    df1=pd.DataFrame(columns=cols)
    df2=pd.DataFrame(columns=cols)
    df3=pd.DataFrame(columns=cols)

    if x=='1':
        df1=mobile_phones(item)
        df2=paytm(item)
        df3=snapdeal(item)
    
    else:
        df1=other_products(item)
        df2=paytm(item)
        df3=snapdeal(item)
    
    return render_template("home.html", column_names=df.columns.values,row_data_1=list(df1.values.tolist()),row_data_2=list(df2.values.tolist()),row_data_3=list(df3.values.tolist()),zip=zip)

def other_products(key):
    url="https://www.flipkart.com/search?q="
    url2="&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    final_url=url+key+url2
    data=rs.get(final_url)
    soup=BeautifulSoup(data.text,'html.parser')
    namesf=[]
    pricef=[]
    for a in soup.findAll('div',attrs={'class':['_3liAhj','_3O0U0u']}):
        price=a.find('div',attrs={'class':['_1vC4OE','_1vC4OE _2rQ-NK']})
        pricef.append(price.string)
        name=a.find('a',attrs={'class':['_2cLu-l','_3wU53n']})
        namesf.append(name)
    data1_table=pd.DataFrame(list(zip(namesf,pricef)),columns=["Name","Price"])
    print("Products in Flipkart Site ")
    print(data1_table.head(5))
    return data1_table.head(5)
    
        
def mobile_phones(key):
    url="https://www.flipkart.com/search?q="
    url2="&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    final_url=url+key+url2
    data=rs.get(final_url)
    soup=BeautifulSoup(data.text,'html.parser')
    namesf=[]
    pricef=[]
    ram=[]
    rom=[]
    for line in soup.findAll('div',attrs={'class':'_3O0U0u'}):
        names=line.find('div',attrs={'class':'_3wU53n'})
        phone_name=names.string.split('(')[0];
        namesf.append(phone_name)
        names2=line.find('div',attrs={'class':'_1vC4OE _2rQ-NK'})
        pricef.append(names2.string)
        rams=line.find('li',attrs={'class':''})    
    data_table=pd.DataFrame(list(zip(namesf,pricef)),columns=["Names","Price"])
    print("Products in Flipkart Site ")
    print(data_table.head(5))
    return data_table.head(5)

def paytm(key):
    url="https://paytmmall.com/shop/search?q="
    final=url+key
    data=rs.get(final)
    soup=BeautifulSoup(data.text,'html.parser')
    namess=[]
    prices=[]
    for line in soup.findAll('div',attrs={'class':'_1fje'}):
        names=line.find('div',attrs={'class':'UGUy'})
        namess.append(names.string)
        price=line.find('div',attrs={'class':['_1kMS','dQm2']})
        prices.append(price.span.text)
    print("Items in paytm mall : ")
    data1=pd.DataFrame(list(zip(namess,prices)),columns=["Names","Prices"])
    print(data1)
    return data1.head(5)

def snapdeal(key):
    url="https://www.shopclues.com/search?q="
    url2="&sc_z=2222&z=0&count=0"
    final=url+key+url2
    data=rs.get(final)
    prices=[]
    namess=[]
    soup=BeautifulSoup(data.text,'html.parser')
    for line in soup.findAll('div',attrs={'class':['column col3 search_blocks','column col3']}):
        price=line.find('span',attrs={'class':'p_price'})
        prices.append(price.string)
        name=line.find(['span','h2'],attrs={'class':['','prod_name']})
        namess.append(name.string)
    print('Items in Snapdeal site')
    datat=pd.DataFrame(list(zip(namess,prices)),columns=["names","Prices"])
    print(datat.head(5))
    return datat.head(5)

if __name__=='main_':
    app.run(debug=True)