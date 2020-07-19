import pandas as pd

# Final Assessment
def load_pie_data(filename):
    df = pd.read_csv(filename,encoding="ISO-8859-1")
    df = df.head(6)
    top_dic = {}
    for i in range(df.shape[0]):
        top_dic[df['Final Assessment Code'][i]]=int(df['Count'][i])
    return top_dic

# dic = load_pie_data('final_assessment_count.csv')
# print(dic)

def load_whole_final(filename):
    df = pd.read_csv(filename, encoding="ISO-8859-1")
    return df

# Response Time
def response_time_count(filename):
    df = pd.read_csv(filename,encoding="ISO-8859-1")
    print(df['Class'].unique())
    df2 = pd.DataFrame(columns=('Class','Count'))
    df2 = df2.append(
        pd.DataFrame(
            {'Class': 'Less than 7 min', 'Count': [df[df['Class'] == '<7min'].shape[0]]})
    )
    df2 = df2.append(
        pd.DataFrame(
            {'Class': '7min - 10 min', 'Count': [df[df['Class'] == '7min-10min'].shape[0]]})
    )
    df2 = df2.append(
        pd.DataFrame(
            {'Class': '10min - 20min', 'Count': [df[df['Class'] == '10min-20min'].shape[0]]})
    )
    df2 = df2.append(
        pd.DataFrame(
            {'Class': '20min - 30min', 'Count': [df[df['Class'] == '20min-30min'].shape[0]]})
    )
    df2 = df2.append(
        pd.DataFrame(
            {'Class': '30min - 60min', 'Count': [df[df['Class'] == '30min-60min'].shape[0]]})
    )
    df2 = df2.append(
        pd.DataFrame(
            {'Class': 'Longer than 60min', 'Count': [df[df['Class'] == '>60min'].shape[0]]})
    )

    df2.to_csv('response_time_count.csv')

# response_time_count('response_time.csv')

def load_response_count(filename):
    df = pd.read_csv(filename, encoding="ISO-8859-1")
    dic = {}
    for i in range(df.shape[0]):
        dic[df['Class'][i]]=int(df['Count'][i])
    return dic

def load_response_finalass_count(filename):
    df = pd.read_csv(filename, encoding="ISO-8859-1")
    # print(df[(df['Response Time Class']=='10min - 20min')&(df['Final Assessment Code']=='PAIN')]['Count'].values[0])
    dic = {}
    for i in df['Final Assessment Code'].unique():
        dic[i]={}
        for j in df['Response Time Class'].unique():
            dic[i][j]=df[(df['Final Assessment Code']==i)&(df['Response Time Class']==j)]['Count'].values[0]
    return dic


# dic = load_response_finalass_count('response_finalass_count.csv')
# print(dic)

def load_finalass_addr(filename):
    df = pd.read_csv(filename, encoding="ISO-8859-1")
    list = []
    for i in range(df.shape[0]):
        # if df['Final Assessment Code'][i]=='ABRASGRAZ':

        list.append([df['Lat'][i],df['Lon'][i]])
    return list

def load_centroid_count(filename):
    df = pd.read_csv(filename,encoding="ISO-8859-1")
    list = []
    for i in range(df.shape[0]):
        if df['Count'][i]!=0:
            list.append([df['Lat'][i],df['Lon'][i],df['Count'][i]])
    return list

# print(load_finalass_addr('response_finalass_addr.csv'))