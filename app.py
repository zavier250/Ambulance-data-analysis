# Author: Zavier
from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import numpy as np
from Kmeans import *
from distribution import *

# Publish on Git on July.19th, 2020.

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:demo@localhost:3306/ambulance_data'

db = SQLAlchemy(app)
migrate = Migrate(app,db)

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(64),index = True, unique=True, nullable=False)

    def __repr__(self):
        return f'<{self.name}>'

class Final_Assessment_Count(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    FA_Code = db.Column(db.String(64),index = True, unique = False, nullable = False)
    FA_desc = db.Column(db.String(300),index = True, unique = False, nullable = True)
    Count = db.Column(db.Integer, index = True)


class Response_Time_Count(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Class = db.Column(db.String(300),index= True, unique = False, nullable = False)
    Count = db.Column(db.Integer, index = True)

class Overtime_Response_FA(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Response_Time_Class = db.Column(db.String(300),index= True, unique = False, nullable = False)
    FA_Code = db.Column(db.String(64),index = True, unique = False, nullable = False)
    Count = db.Column(db.Integer, index=True)

class Response_Finalass_Addr(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    EARF_Number = db.Column(db.Integer, index=True, unique=False, nullable = False)
    Year = db.Column(db.Integer, index = True, unique = False, nullable = True)
    Response_Time_Class = db.Column(db.String(300), index=True, unique=False, nullable=False)
    Street_Name = db.Column(db.String(500), index=True, unique=False, nullable=True)
    Suburb = db.Column(db.String(300), index=True, unique=False, nullable=True)
    Lat = db.Column(db.Float, index=True, unique=False, nullable=True)
    Lon = db.Column(db.Float, index=True, unique=False, nullable=True)
    FA_Code = db.Column(db.String(64), index=True, unique=False, nullable=False)

class Centroids_Count(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Lat = db.Column(db.Float, index=True, unique=False, nullable=True)
    Lon = db.Column(db.Float, index=True, unique=False, nullable=True)
    Count = db.Column(db.Integer, index=True)

@app.route('/home',methods=['GET','POST'])
def home():
    # GET
    name = request.form.get('name')
    if name:
        user = User(name=name)
        db.session.add(user)
        db.session.commit()

    users = User.query.order_by(User.name).all()
    print(type(users))
    print(users)
    return render_template('index.html',users = users)

def load_data(filename):
    data = np.genfromtxt(filename,delimiter=',')
    data = data.tolist()
    return data

@app.route('/upload_fac')
def upload_final_assessment_count():
    final_assess_count = load_csv('final_assessment_count.csv')
    final_assess_count = final_assess_count.values.tolist()
    for pair in final_assess_count:
        pair = Final_Assessment_Count(FA_Code=pair[1],FA_desc=pair[2],Count=pair[3])
        db.session.add(pair)
    db.session.commit()
    print('CSV file uploaded.')

@app.route('/upload_rsc')
def upload_response_time_count():
    data = load_csv('response_time_count.csv')
    data = data.values.tolist()
    for pair in data:
        tuple = Response_Time_Count(Class=pair[1],Count=pair[2])
        db.session.add(tuple)
    db.session.commit()
    print('CSV file uploaded.')

@app.route('/upload_rfc')
def upload_response_finalass_count():
    data = load_csv('response_finalass_count.csv')
    data = data.values.tolist()
    for pair in data:
        tuple = Overtime_Response_FA(Response_Time_Class=pair[1], FA_Code=pair[2], Count=pair[3])
        db.session.add(tuple)
    db.session.commit()
    print('CSV file uploaded.')

@app.route('/upload_rfa')
def upload_response_finalass_addr():
    print('Begin.....')
    data = load_csv('response_finalass_addr.csv')
    data = data.values.tolist()
    for pair in data:
        pair[4]=str(pair[4])
        tuple = Response_Finalass_Addr(EARF_Number=pair[1], Year=pair[2], Response_Time_Class=pair[3], Street_Name=pair[4],
                                       Suburb=pair[5], Lat=pair[6], Lon=pair[7], FA_Code=pair[8])
        db.session.add(tuple)
        # print(type(pair[4]))
    db.session.commit()
    print('CSV file uploaded.')

@app.route('/upload_cc')
def upload_centroids_count():
    data = load_csv('centroids_count.csv')
    data = data.values.tolist()
    for pair in data:
        # if pair[1]!=nan and pair[2]!=nan:
        tuple = Centroids_Count(Lat=pair[1], Lon=pair[2], Count=pair[3])
        db.session.add(tuple)
    db.session.commit()
    print('CSV file uploaded.')

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/map')
def map():
    # dataMat = get_accident_loc('earf.csv',200)
    # dataMat = dataMat[:, 1:]
    # centroids, clusterAssment = kMeans(dataMat, 8)
    # centroids_list = centroids.tolist()
    # print(centroids_list)
    # return render_template('map.html',data=centroids_list)
    # addr_list = load_finalass_addr('response_finalass_addr.csv')
    # addr_list = np.mat(addr_list)
    # centroids,clusterAssment = kMeans(addr_list,200)
    # centroids_list = centroids.tolist()
    centroids_list = load_centroid_count('centroids_count.csv')
    return render_template('map.html',data=centroids_list)

@app.route('/dashboard')
def dashboard():
    #pie chart
    final_assess_dic = load_pie_data('final_assessment_count.csv')
    whole_final = load_whole_final('final_assessment_count.csv')
    response_count = load_response_count('response_time_count.csv')
    response_finalass_count = load_response_finalass_count('response_finalass_count.csv')
    data_dic={}
    data_dic['final_assess_count']=final_assess_dic
    data_dic['whole_final']=whole_final
    data_dic['response_count']=response_count
    data_dic['response_finalass_count']=response_finalass_count
    # dataMat = get_accident_loc('earf.csv', 50)
    # dataMat = dataMat[:, 1:]
    # centroids, clusterAssment = kMeans(dataMat, 4)
    # centroids_list = centroids.tolist()
    # print(centroids_list)
    # return render_template('dashboard.html', data=centroids_list)
    return render_template('dashboard.html',data=data_dic)

@app.route('/heatmap')
def heatmap():
    list = load_finalass_addr('response_finalass_addr.csv')
    return render_template('heatmap.html',data=list)

@app.route('/dashboard2')
def dashboard2():
    #pie chart
    # final_assess_dic = load_pie_data('final_assessment_count.csv')
    # whole_final = load_whole_final('final_assessment_count.csv')
    whole_final2 = Final_Assessment_Count.query.all()
    print(type(whole_final2))
    print(len(whole_final2))
    print(whole_final2[0].Count)
    # response_count = load_response_count('response_time_count.csv')
    response_count = Response_Time_Count.query.all()
    response_finalass_count = load_response_finalass_count('response_finalass_count.csv')
    # response_finalass_count = Overtime_Response_FA.query.all()

    rfc_code = db.session.query(Overtime_Response_FA.FA_Code).distinct().all()
    print(rfc_code)


    # addr_list = load_finalass_addr('response_finalass_addr.csv')
    addr_list = db.session.query(Response_Finalass_Addr.Lat,Response_Finalass_Addr.Lon).all()
    # centroids_list = load_centroid_count('centroids_count.csv')
    centroids_list = db.session.query(Centroids_Count).all()

    data_dic={}
    # data_dic['final_assess_count']=final_assess_dic
    data_dic['whole_final']=whole_final2
    data_dic['response_count']=response_count
    data_dic['response_finalass_count']=response_finalass_count
    data_dic['rfc_code']=rfc_code
    data_dic['addr_list']=addr_list
    data_dic['centroid_count']=centroids_list

    # print(centroids_list)
    # dataMat = get_accident_loc('earf.csv', 50)
    # dataMat = dataMat[:, 1:]
    # centroids, clusterAssment = kMeans(dataMat, 4)
    # centroids_list = centroids.tolist()
    # print(centroids_list)
    # return render_template('dashboard.html', data=centroids_list)
    return render_template('dashboard2.html',data=data_dic)

if __name__=='__main__':
    # print(load_data('geo2.csv'))
    # print(type(load_data('geo2.csv')))
    app.run(debug=True)

    # flask db init
    # flask db migrate
    # flask db upgrade

    # Error 48
    # sudo lsof -i:5000
    # kill pid
