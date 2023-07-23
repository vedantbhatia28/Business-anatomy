from flask import Flask, render_template, request, redirect, session, url_for, flash
from pip import main
from sqlalchemy import true
# from second import second
# from analytics import analytics
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from config import mail_username, mail_password
from datetime import timedelta
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
# import mysql
# import cursor
import sqlite3
# import stripe


app = Flask(__name__)

connection = mysql.connector.connect(
    host='localhost', 
    user='root', 
    passwd='Admin@123',
    database='businessanatomy')

app.secret_key ="4321"

cursor = connection.cursor()


sales = pd.read_csv('static/csv/supermarket_sales.csv')

Mum = pd.read_csv('static/csv/Mumbai Sales_Analysis.csv')

Del = pd.read_csv('static/csv/Delhi Sales_Analysis.csv')

Bang = pd.read_csv('static/csv/Bangalore Sales_Analysis.csv') 


# app.register_blueprint(second,url_prefix="")
# app.register_blueprint(second1,url_prefix="")


app.config['MAIL_SERVER'] = "smtp-mail.outlook.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSl'] = False
app.config['MAIL_USERNAME'] = mail_username
app.config['MAIL_PASSWORD'] = mail_password


mail = Mail(app)


# YOUR_DOMAIN = "http://localhost:5000"

# @app.route("/payment",methods=["POST"])
# def payment():
#     try:
#         checkout_session = stripe.checkout.Session.create(

#             line_items= [
#             {
#                 'price':'price_1MhDLrSBfos2gVULR6W0fURs',
#                 'quantity':1
#             }
#             ],
#             mode = "subscription",
#             success_url= YOUR_DOMAIN+"./dashboard",
#             cancel_url= YOUR_DOMAIN+ "./index"


#         )

#     except Exception as e:
#         return str(e)

#     return redirect(checkout_session.html,code=303)  

@app.route("/", methods = ['GET'])
@app.route("/index", methods = ['GET'])
def HomePage():
    return render_template('index.html')   

@app.route("/contactForm", methods = ['GET' , 'POST'])
def contactForm():
    if request.method == "POST":
        name = request.form.get('Name')
        email = request.form.get('Email')
        phone = request.form.get('Phone')
        message = request.form.get('Message')

        msg = Message(subject=f"Mail from{name}", body=f"Name: {name}\nE-Mail: {email}\nPhone: {phone}\n\n\n{message}", sender="oppanchayat5@outlook.com", recipients=['oppanchayat5@gmail.com'])
        mail.send(msg)
        return render_template("contactForm.html", success=True)

    return render_template('contactForm.html')


@app.route("/services")
def services():
    return render_template('services.html')   

@app.route("/Premium")
def Pro():
    return render_template('Pro.html')  

@app.route("/SignUp")
def SignUp():
    return render_template('SignUp.html')  

# @app.route("/aboutus")
# def aboutUs():
#     return render_template('aboutUs.html')    

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user_id = request.form['user_id']
        password = request.form['password']

        LogIn = "SELECT user_id, password from businessanatomy.login WHERE user_id = '"+user_id+"' AND password = '"+password+"'"
        cursor.execute(LogIn)
        user = cursor.fetchone()

        if user:
            session['loggedin'] = True
            session['user_id'] = user[1]
            session['name'] = user_id

            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for("login")) 
    return render_template('Login.html')

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
        return render_template('dashboard.html', Q1 ='static/graph_Img/Total_Sales/Month.png', Q2 = 'static/graph_Img/Total_Sales/City.png', Q3 = 'static/graph_Img/Total_Sales/Time.png', 
        Q4 = 'static/graph_Img/Total_Sales/Product.png' ,Q5 = 'static/graph_Img/Total_Sales/Customer.png',Q6 = 'static/graph_Img/Total_Sales/Payment.png'
        ,ProductLine = bpl, BestMonth = bms, BestCity = bcs, Member = mvn, Payment = ppm, SalesByH = sbh_s)
        

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 



Total_Sales = sales.groupby('Month').Total.sum()
months = range(1,4)
        
plt.figure(figsize=(10,7))
colors = ['#e01616', '#612f75', '#db3d7a']
        
plt.bar(months, Total_Sales, color = colors)
        
plt.title('Sales By Month', fontdict= {'fontname': 'Georgia','fontsize': 20 })
        
labels = ['Jaunuary', 'February', 'March']
plt.xticks(months, size = 14, labels = labels)
plt.yticks(size=14)
        
plt.ylabel('Sales of each Month', fontdict= {'fontname': 'Georgia','fontsize': 20 })
plt.xlabel('Months', fontdict= {'fontname': 'Georgia','fontsize': 20 })
        
plt.savefig('static/graph_Img/Total_Sales/Month.png')


##################################### QUERY 2 #################################


# Delhi = sales.loc[sales['City'] == 'DELHI'].count()[0]
# Mumbai = sales.loc[sales['City'] == 'MUMBAI'].count()[0]
# Bangalore = sales.loc[sales['City'] == 'BANGALORE'].count()[0]

Mumbai = sales.loc[sales['City'] == 'MUMBAI'].Total.sum().astype(int)
Delhi = sales.loc[sales['City'] == 'DELHI'].Total.sum().astype(int)
Bangalore = sales.loc[sales['City'] == 'BANGALORE'].Total.sum().astype(int)

labels = ['Mumbai', 'Delhi', 'Bangalore']
colors = ['#4755a6', '#6da32f']
explode = (0.1,0.1,0.1)

plt.pie([Delhi,Mumbai,Bangalore], labels = labels, explode = explode, autopct = '%.2f %%', radius=1.5,textprops={'fontsize': 15} )

plt.savefig('static/graph_Img/Total_Sales/City.png')



##################################### QUERY 3 #################################



sales['Hour'] = pd.to_datetime(sales['TIME']).dt.hour
sales['Minute'] = pd.to_datetime(sales['TIME']).dt.minute
sales['Count'] = 1

keys = [pair for pair, df in sales.groupby(['Hour'])]

plt.figure(figsize=(9,6))

plt.title('Sales By Hour', fontdict= {'fontname': 'Georgia','fontsize': 20 })

plt.plot(keys, sales.groupby(['Hour']).count()['Count'], color='#32b865')

plt.xticks(keys,size = 13)
plt.yticks(size = 13)

plt.ylabel('Sales', fontdict= {'fontname': 'Georgia','fontsize': 20 })
plt.xlabel('Time in Hours', fontdict= {'fontname': 'Georgia','fontsize': 20 })

plt.grid()
plt.savefig('static/graph_Img/Total_Sales/Time.png')



##################################### QUERY 4 #################################



Total_Sales = sales.groupby('Product line').Total.sum()

Product = sales.groupby('Product line')
keys = [pair for pair, df in Product]

plt.figure(figsize=(14,9))

plt.title('Sales Of Product', fontdict= {'fontname': 'Georgia','fontsize': 20 })
colors = ['#4755a6', '#6da32f', '#ad283e', '#d6d01e', '#913d5b', '#5b7fe3']

plt.bar(keys, Total_Sales, color = colors)

plt.xticks(keys, size=12)
plt.yticks(size = 14)

plt.ylabel('Sales', fontdict= {'fontname': 'Georgia','fontsize': 25 })
plt.xlabel('Product Line', fontdict= {'fontname': 'Georgia','fontsize': 25 })

#     # quantity_ordered = Product.sum()['Quantity']

#     # fig, ax1 = plt.subplots()

#     # ax2 = ax1.twinx()

#     # ax1.bar(keys, Total_Sales, color='g')
#     # ax2.plot(keys, quantity_ordered, color='b')

#     # # plt.figure(figsize=(8,4))

#     # ax1.set_xlabel('Product Line', size=20)
#     # ax1.set_ylabel('Sales', color='g', size=20)
#     # ax2.set_ylabel('Quantity', color='b',size=20)
#     # ax1.set_xticklabels(keys, rotation='vertical', size=15)
#     # plt.yticks(size = 13)

plt.savefig('static/graph_Img/Total_Sales/Product.png')



##################################### QUERY 5 #################################



# normal = sales.loc[sales['Customer type'] == 'Normal'].count()[0]
# member = sales.loc[sales['Customer type'] == 'Member'].count()[0]

# labels = ['Normal', 'Member']
# colors = ['#6097a8', '#ab8c26']
# explode = (0.13,0.13)

# plt.pie([normal,member],labels = labels, colors = colors, explode = explode, autopct = '%.2f %%', radius=1.2 ,textprops={'fontsize': 16})

# plt.savefig('static/graph_Img/Total_Sales/Customer.png')



# #################################### QUERY 6 #################################



# Credit_card = sales.loc[sales['Payment'] == 'Credit card'].count()[0]
# Cash = sales.loc[sales['Payment'] == 'Cash'].count()[0]
# Ewallet = sales.loc[sales['Payment'] == 'Ewallet'].count()[0]

# labels = ['Credit card', 'Cash', 'Ewallet']
# colors = ['#4755a6', '#6da32f','#c24127']
# explode = (0.1,0.1,0.1)

# plt.pie([Credit_card, Cash, Ewallet], labels = labels,explode = explode, colors = colors, autopct = '%.2f %%', radius=1.3,textprops={'fontsize': 14})

# plt.savefig('static/graph_Img/Total_Sales/Payment.png')

mm=dict()
# best product line--------------------------------------
ea=Bang[Bang['Product line']=='Electronics accessories']['Quantity'].sum()
fa=Bang[Bang['Product line']=='Fashion ccessories']['Quantity'].sum()
fb=Bang[Bang['Product line']=='Food and beverages']['Quantity'].sum()
hb=Bang[Bang['Product line']=='Health and beauty']['Quantity'].sum()
hl=Bang[Bang['Product line']=='Home and lifestyle']['Quantity'].sum()
sp=Bang[Bang['Product line']=='Sports and travel']['Quantity'].sum()
pl={'electronics accessories':ea,'Fashion accessories':fa,'food and beverages':fb,'health and beauty':hb,'home and lifestyle':hl,'sports and travel':sp}
bpl=max(pl,key=pl.get)
# print(f"{bpl}")


#best month----------------------------------
jan=sales[sales['Month']=='January']['Total'].sum()
feb=sales[sales['Month']=='February']['Total'].sum()
mar=sales[sales['Month']=='March']['Total'].sum()
monthlysalesdict={'January':jan,'february':feb,'march':mar}
bms=max(monthlysalesdict,key=monthlysalesdict.get)
# print(f"{bms}")  

#best city---------------------------------------------
mum=sales[sales['City']=='MUMBAI']['Total'].sum()
delh=sales[sales['City']=='DELHI']['Total'].sum()
blr=sales[sales['City']=='BANGALORE']['Total'].sum()
citysalesdict={'MUMBAI':mum,'DELHI':delh,'BANGALORE':blr}
bcs=max(citysalesdict,key=citysalesdict.get)
# print(f'{bcs}')

#membersVnormal---------------------------------------
mem=sales[sales['Customer type']=='Member']['Total'].sum()
non=sales[sales['Customer type']=='Normal']['Total'].sum()
memvsnordict={'Member':mem,'Normal':non}
mvn=max(memvsnordict,key=memvsnordict.get)
# print(f'MOST CUSTOMER WERE:{mvn}')

#preferablepaymentmode--------------------------------
cc=sales[sales['Payment']=='Credit Card']['Total'].sum()
cash=sales[sales['Payment']=='Cash']['Total'].sum()
ew=sales[sales['Payment']=='Ewallet']['Total'].sum()
paymentmodedict={'credit card':cc,'cash':cash,'Ewallet':ew}
ppm=max(paymentmodedict,key=paymentmodedict.get)
# print(f'most preferred payment mode:{ppm}')

#salesbyhour----------------------------------------
sales['Hour']=pd.to_datetime(sales['TIME']).dt.hour
sales['Minute']=pd.to_datetime(sales['TIME']).dt.minute
sales['Count']=1
ten=sales[sales['Hour']==10]['Total'].sum()
elv=sales[sales['Hour']==11]['Total'].sum()
twl=sales[sales['Hour']==12]['Total'].sum()
thr=sales[sales['Hour']==13]['Total'].sum()
frt=sales[sales['Hour']==14]['Total'].sum()
fif=sales[sales['Hour']==15]['Total'].sum()
six=sales[sales['Hour']==16]['Total'].sum()
svn=sales[sales['Hour']==17]['Total'].sum()
eig=sales[sales['Hour']==18]['Total'].sum()
nin=sales[sales['Hour']==19]['Total'].sum()
twn=sales[sales['Hour']==20]['Total'].sum()
salesbyhourdict={'10am':ten,'11am':elv,'12pm':twl,'1pm':thr,'2pm':frt,'3pm':fif,'4pm':six,'5pm':svn,'6pm':eig,'7pm':nin,'8pm':twn}
sbh_s=max(salesbyhourdict,key=salesbyhourdict.get)
# print(f'best time for sales:{sbh}')



# ##################################### MUMBAI  #################################


@app.route("/mumbai")
def mumbai():
    return render_template('mumbai.html', M1 = 'static/graph_Img/Mumbai_Graph/Month.png', M2 = 'static/graph_Img/Mumbai_Graph/Product.png', 
    M3 = 'static/graph_Img/Mumbai_Graph/Total_Time.png',MonthM = mms, ProductLineM = mmp, ByHourM = sbhm)


# ##################################### MUMBAI 1 #################################


#  sales.groupby(['Month']).sum()
Total_Sales = Mum.groupby('Month').Total.sum()

months = range(1,4)
# print(months)

plt.figure(figsize=(10,7))
color = ['#e01616', '#b4ed2d', '#9e48db']

plt.bar(months, Total_Sales, color = color)

plt.title('Sales By Month', fontdict= {'fontname': 'Georgia','fontsize': 20 })

labels = ['Jaunuary', 'February', 'March']

plt.xticks(months, size = 14, labels = labels)
plt.yticks(size=14)

plt.ylabel('Sales of each Month', fontdict= {'fontname': 'Georgia','fontsize': 20 })
plt.xlabel('Months', fontdict= {'fontname': 'Georgia','fontsize': 20 })

plt.savefig('static/graph_Img/Mumbai_Graph/Month.png')


##################################### MUMBAI 2 #################################


Total_Sales = Mum.groupby('Product line').Total.sum()

Product = sales.groupby('Product line')
keys = [pair for pair, df in Product]

plt.figure(figsize=(15,8))

plt.title('Sales Of Product', fontdict= {'fontname': 'Georgia','fontsize': 25 })
colors = ['#4755a6', '#6da32f', '#ad283e', '#d6d01e', '#913d5b', '#5b7fe3']

plt.bar(keys, Total_Sales, color = colors)

plt.xticks(keys, size=12)
plt.yticks(size = 14)

plt.ylabel('Sales', fontdict= {'fontname': 'Georgia','fontsize': 25 })
plt.xlabel('Product Line', fontdict= {'fontname': 'Georgia','fontsize': 25 })

plt.savefig('static/graph_Img/Mumbai_Graph/Product.png')



##################################### MUMBAI 3 #################################



Mum['Hour'] = pd.to_datetime(Mum['TIME']).dt.hour
Mum['Minute'] = pd.to_datetime(Mum['TIME']).dt.minute
Mum['Count'] = 1

keys = [pair for pair, df in Mum.groupby(['Hour'])]

plt.figure(figsize=(9,6))

plt.title('Sales By Hour', fontdict= {'fontname': 'Georgia','fontsize': 20 })

plt.plot(keys, Mum.groupby(['Hour']).count()['Count'], color='#32b865')

plt.xticks(keys,size = 13)
plt.yticks(size = 13)

plt.ylabel('Sales Count', fontdict= {'fontname': 'Georgia','fontsize': 20 })
plt.xlabel('Time in Hours', fontdict= {'fontname': 'Georgia','fontsize': 20 })

plt.grid()

plt.savefig('static/graph_Img/Mumbai_Graph/Total_Time.png')



#monthlysales--------------------------------------------------
mum_jan=Mum[Mum['Month']=='January']['Total'].sum()
mum_feb=Mum[Mum['Month']=='February']['Total'].sum()
mum_mar=Mum[Mum['Month']=='March']['Total'].sum()
monthly={'january':mum_jan,'february':mum_feb,'march':mum_mar}
mms=max(monthly,key=monthly.get)
# print(f'best month for sales in mumbai:{mms}')


#productline----------------------------------------------------
ea_m=Mum[Mum['Product line']=='Electronics accessories']['Quantity'].sum()
fa_m=Mum[Mum['Product line']=='Fashion accessories']['Quantity'].sum()
fb_m=Mum[Mum['Product line']=='Food and beverages']['Quantity'].sum()
hb_m=Mum[Mum['Product line']=='Health and beauty']['Quantity'].sum()
hl_m=Mum[Mum['Product line']=='Home and lifestyle']['Quantity'].sum()
sp_m=Mum[Mum['Product line']=='Sports and travel']['Quantity'].sum()
mumbaipl={'electronics accessories':ea_m,'Fashion accessories':fa_m,'food and beverages':fb_m,'health and beauty':hb_m,'home and lifestyle':hl_m,'sports and travel':sp_m}
mmp=max(mumbaipl,key=mumbaipl.get)
# print(f'the best product line is:{mmp}')


#salesbyhour-----------------------------------------------------
Mum['Hour']=pd.to_datetime(Mum['TIME']).dt.hour
Mum['Minute']=pd.to_datetime(Mum['TIME']).dt.minute
Mum['Count']=1
tenm=Mum[Mum['Hour']==10]['Total'].sum()
elvm=Mum[Mum['Hour']==11]['Total'].sum()
twlm=Mum[Mum['Hour']==12]['Total'].sum()
thrm=Mum[Mum['Hour']==13]['Total'].sum()
frtm=Mum[Mum['Hour']==14]['Total'].sum()
fifm=Mum[Mum['Hour']==15]['Total'].sum()
sixm=Mum[Mum['Hour']==16]['Total'].sum()
svnm=Mum[Mum['Hour']==17]['Total'].sum()
eigm=Mum[Mum['Hour']==18]['Total'].sum()
ninm=Mum[Mum['Hour']==19]['Total'].sum()
twnm=Mum[Mum['Hour']==20]['Total'].sum()
salesbyhourmumbai={'10am':tenm,'11am':elvm,'12pm':twlm,'1pm':thrm,'2pm':frtm,'3pm':fifm,'4pm':sixm,'5pm':svnm,'6pm':eigm,'7pm':ninm,'8pm':twnm}
sbhm=max(salesbyhourmumbai,key=salesbyhourmumbai.get)

# print(f'best time for sales:{sbhm}')


# ##################################### DELHI #################################

@app.route("/delhi")
def delhi():
    return render_template('delhi.html',  D1 = 'static/graph_Img/delhi_Graph/Month.png', D2 = 'static/graph_Img/Delhi_Graph/Product.png', 
    D3 = 'static/graph_Img/Delhi_Graph/Total_Time.png', MonthD = dms, ProductLineD = dmp_d, ByHourD = sbhd)       



# ##################################### DELHI 1 #################################

    #  sales.groupby(['Month']).sum()
Total_Sales = Del.groupby('Month').Total.sum()

months = range(1,4)
    # print(months)

plt.figure(figsize=(10,7))
color = ['#e01616', '#b4ed2d', '#9e48db']

plt.bar(months, Total_Sales, color = color)

plt.title('Sales By Month', fontdict= {'fontname': 'Georgia','fontsize': 20 })

labels = ['Jaunuary', 'February', 'March']

plt.xticks(months, size = 14, labels = labels)
plt.yticks(size=14)

plt.ylabel('Sales of each Month', fontdict= {'fontname': 'Georgia','fontsize': 20 })
plt.xlabel('Months', fontdict= {'fontname': 'Georgia','fontsize': 20 })

plt.savefig('static/graph_Img/Delhi_Graph/Month.png')







Total_Sales = Del.groupby('Product line').Total.sum()
Product = Del.groupby('Product line')
keys = [pair for pair, df in Product]

plt.figure(figsize=(15,8))

plt.title('Sales Of Product', fontdict= {'fontname': 'Georgia','fontsize': 25 })
colors = ['#4755a6', '#6da32f', '#ad283e', '#d6d01e', '#913d5b', '#5b7fe3']
   
plt.bar(keys, Total_Sales, color = colors)
   
plt.xticks(keys, size=12)
plt.yticks(size = 14)
   
plt.ylabel('Sales', fontdict= {'fontname': 'Georgia','fontsize': 25 })
plt.xlabel('Product Line', fontdict= {'fontname': 'Georgia','fontsize': 25 })
   
plt.savefig('static/graph_Img/Delhi_Graph/Product.png')
   





Del['Hour'] = pd.to_datetime(Del['TIME']).dt.hour
Del['Minute'] = pd.to_datetime(Del['TIME']).dt.minute
Del['Count'] = 1

keys = [pair for pair, df in Del.groupby(['Hour'])]
Total_Sales = Del.groupby(['Hour']).count()['Count']

plt.figure(figsize=(9,6))

plt.title('Sales By Hour', fontdict= {'fontname': 'Georgia','fontsize': 20 })

plt.plot(keys, Total_Sales , color='#32b865')

plt.xticks(keys,size = 13)
plt.yticks(size = 13)

plt.ylabel('Sales', fontdict= {'fontname': 'Georgia','fontsize': 20 })
plt.xlabel('Time in Hours', fontdict= {'fontname': 'Georgia','fontsize': 20 })

plt.grid()

plt.savefig('static/graph_Img/Delhi_Graph/Total_Time.png')


dmp=dict()
#monthlysales--------------------------------------------------
del_jan=Del[Del['Month']=='January']['Total'].sum()
del_feb=Del[Del['Month']=='February']['Total'].sum()
del_mar=Del[Del['Month']=='March']['Total'].sum()
monthly1={'january':del_jan,'february':del_feb,'march':del_mar}
dms=max(monthly1,key=monthly1.get)
# print(f'best month for sales in delhi:{dms}')


#productline----------------------------------------------------
ea_d=Del[Del['Product line']=='Electronics accessories']['Quantity'].sum()
fa_d=Del[Del['Product line']=='Fashion ccessories']['Quantity'].sum()
fb_d=Del[Del['Product line']=='Food and beverages']['Quantity'].sum()
hb_d=Del[Del['Product line']=='Health and beauty']['Quantity'].sum()
hl_d=Del[Del['Product line']=='Home and lifestyle']['Quantity'].sum()
sp_d=Del[Del['Product line']=='Sports and travel']['Quantity'].sum()
delhipl={'electronics accessories':ea_d,'Fashion accessories':fa_d,'food and beverages':fb_d,'health and beauty':hb_d,'home and lifestyle':hl_d,'sports and travel':sp_d}
dmp_d=max(delhipl,key=delhipl.get)
# print(f"product line with the most sales is:{dmp_d}")


#salesbyhour-----------------------------------------------------
Del['Hour']=pd.to_datetime(Del['TIME']).dt.hour
Del['Minute']=pd.to_datetime(Del['TIME']).dt.minute
Del['Count']=1
tend=Del[Del['Hour']==10]['Total'].sum()
elvd=Del[Del['Hour']==11]['Total'].sum()
twld=Del[Del['Hour']==12]['Total'].sum()
thrd=Del[Del['Hour']==13]['Total'].sum()
frtd=Del[Del['Hour']==14]['Total'].sum()
fifd=Del[Del['Hour']==15]['Total'].sum()
sixd=Del[Del['Hour']==16]['Total'].sum()
svnd=Del[Del['Hour']==17]['Total'].sum()
eigd=Del[Del['Hour']==18]['Total'].sum()
nind=Del[Del['Hour']==19]['Total'].sum()
twnd=Del[Del['Hour']==20]['Total'].sum()
salesbyhourdelhi={'10am':tend,'11am':elvd,'12pm':twld,'1pm':thrd,'2pm':frtd,'3pm':fifd,'4pm':sixd,'5pm':svnd,'6pm':eigd,'7pm':nind,'8pm':twnd}
sbhd=max(salesbyhourdelhi,key=salesbyhourdelhi.get)
# print(f'best time for sales:{sbhd}')
    


# ########################################## BANGALORE #####################################


# @app.route("/bangalore")
# def bangalore():
#     return render_template('bangalore.html',  B1 = 'static/graph_Img/Bangalore_Graph/Month.png', 
#     B2 = 'static/graph_Img/Bangalore_Graph/Product.png', B3 = 'static/graph_Img/Bangalore_Graph/Total_Time.png'
#     ,MonthB = bms, ProductLineB = dmp_b, ByHourB = bsh_b) 



# #  sales.groupby(['Month']).sum()
# # Total_Sales = Bang.groupby('Month').Total.sum()

# # months = range(1,4)
# # # print(months)

# # plt.figure(figsize=(10,7))
# # color = ['#e01616', '#b4ed2d', '#9e48db']

# # plt.bar(months, Total_Sales)
    
# # plt.title('Sales By Month', fontdict= {'fontname': 'Georgia','fontsize': 20 })

# # labels = ['Jaunuary', 'February', 'March']

# # plt.xticks(months, size = 14, labels = labels)
# # plt.yticks(size=14)

# # plt.ylabel('Sales of each Month', fontdict= {'fontname': 'Georgia','fontsize': 20 })
# # plt.xlabel('Months', fontdict= {'fontname': 'Georgia','fontsize': 20 })

# # plt.savefig('static/graph_Img/Bangalore_Graph/Month.png')





# Total_Sales = Bang.groupby('Product line').Total.sum()

# Product = Bang.groupby('Product line')
# keys = [pair for pair, df in Product]

# plt.figure(figsize=(14,8))

# plt.title('Sales Of Product', fontdict= {'fontname': 'Georgia','fontsize': 25 })
# colors = ['#4755a6', '#6da32f', '#ad283e', '#d6d01e', '#913d5b', '#5b7fe3']

# plt.bar(keys, Total_Sales, color = colors)

# plt.xticks(keys, size=12)
# plt.yticks(size = 14)

# plt.ylabel('Sales', fontdict= {'fontname': 'Georgia','fontsize': 25 })
# plt.xlabel('Product Line', fontdict= {'fontname': 'Georgia','fontsize': 25 })

# plt.savefig('static/graph_Img/Bangalore_Graph/Product.png')




# Bang['Hour'] = pd.to_datetime(Bang['TIME']).dt.hour
# Bang['Minute'] = pd.to_datetime(Bang['TIME']).dt.minute
# Bang['Count'] = 1

# keys = [pair for pair, df in Bang.groupby(['Hour'])]
# Total_Sales = Bang.groupby(['Hour']).count()['Count']

# plt.figure(figsize=(9,6))

# plt.title('Sales By Hour', fontdict= {'fontname': 'Georgia','fontsize': 20 })

# plt.plot(keys, Total_Sales, color='#32b865')

# plt.xticks(keys,size = 13)
# plt.yticks(size = 13)

# plt.ylabel('Sales', fontdict= {'fontname': 'Georgia','fontsize': 20 })
# plt.xlabel('Time in Hours', fontdict= {'fontname': 'Georgia','fontsize': 20 })

# plt.grid()

# plt.savefig('static/graph_Img/Bangalore_Graph/Total_Time.png')



# bpl=dict()

# #monthlysales--------------------------------------------------
# bmp=Bang.groupby('Month')['Total'].sum()
# bms=list(bmp.keys())[0]
# # print(f'best month for sales in bangalore:{bms}')

# #productline----------------------------------------------------
# ea_b=Bang[Bang['Product line']=='Electronics accessories']['Quantity'].sum()
# fa_b=Bang[Bang['Product line']=='Fashion ccessories']['Quantity'].sum()
# fb_b=Bang[Bang['Product line']=='Food and beverages']['Quantity'].sum()
# hb_b=Bang[Bang['Product line']=='Health and beauty']['Quantity'].sum()
# hl_b=Bang[Bang['Product line']=='Home and lifestyle']['Quantity'].sum()
# sp_b=Bang[Bang['Product line']=='Sports and travel']['Quantity'].sum()
# bangalorepl={'electronics accessories':ea_b,'Fashion accessories':fa_b,'food and beverages':fb_b,'health and beauty':hb_b,'home and lifestyle':hl_b,'sports and travel':sp_b}
# dmp_b=max(bangalorepl,key=bangalorepl.get)
# # print(f'best product line in bangalore is:{dmp_b}')

# #salesbyhour-----------------------------------------------------
# Bang['Hour']=pd.to_datetime(Bang['TIME']).dt.hour
# Bang['Minute']=pd.to_datetime(Bang['TIME']).dt.minute
# Bang['Count']=1
# bsh=Bang.groupby('Hour')['Total'].sum()
# bsh_b=list(bsh.keys())[0]
# print(f'best time for sales:{bsh_b}am')


# # /////////////////////////////////////////////////////////////////////////////////////////////////////


@app.route("/settings")
def settings():
    return render_template('settings.html')



# @app.route('/test_aki')
# def chartTest():  
#     return render_template('akshit.html', name = 'new_plot', url ='static/images/Month.png')

# Total_Sales = sales.groupby('Month').Total.sum()
# months = range(1,4)
        
# plt.figure(figsize=(10,7))
# colors = ['#e01616', '#612f75', '#db3d7a']
        
# plt.bar(months, Total_Sales, color = colors)
        
# plt.title('Sales By Month', fontdict= {'fontname': 'Georgia','fontsize': 20 })
        
# labels = ['Jaunuary', 'February', 'March']
# plt.xticks(months, size = 14, labels = labels)
# plt.yticks(size=14)
        
# plt.ylabel('Sales of each Month', fontdict= {'fontname': 'Georgia','fontsize': 20 })
# plt.xlabel('Months', fontdict= {'fontname': 'Georgia','fontsize': 20 })
        
# plt.savefig('static/images/Month.png')  

if __name__ == '__main__':
    app.run(debug=False,host = '0.0.0.0')
