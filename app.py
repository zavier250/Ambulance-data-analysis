# Author: Zavier
from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import numpy as np
from Kmeans import *
from distribution import *

# Publish on Git on July.19th, 2020

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:demo@localhost:3306/demo'

db = SQLAlchemy(app)
migrate = Migrate(app,db)

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(64),index = True, unique=True, nullable=False)

    def __repr__(self):
        return f'<{self.name}>'

@app.route('/home',methods=['GET','POST'])
def home():
    # GET
    name = request.form.get('name')
    if name:
        user = User(name=name)
        db.session.add(user)
        db.session.commit()

    users = User.query.order_by(User.name).all()
    print(users)
    return render_template('index.html',users = users)





def load_data(filename):
    data = np.genfromtxt(filename,delimiter=',')
    data = data.tolist()
    return data

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
    final_assess_dic = load_pie_data('final_assessment_count.csv')
    whole_final = load_whole_final('final_assessment_count.csv')
    response_count = load_response_count('response_time_count.csv')
    response_finalass_count = load_response_finalass_count('response_finalass_count.csv')
    addr_list = load_finalass_addr('response_finalass_addr.csv')
    centroids_list = load_centroid_count('centroids_count.csv')
    data_dic={}
    data_dic['final_assess_count']=final_assess_dic
    data_dic['whole_final']=whole_final
    data_dic['response_count']=response_count
    data_dic['response_finalass_count']=response_finalass_count
    data_dic['addr_list']=addr_list
    data_dic['centroid_count']=centroids_list
    print(centroids_list)
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
