import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import json
from folium.features import CustomIcon

path = os.getcwd()

case = pd.read_csv(path + r'\data\Case.csv')
patinfo = pd.read_csv(path + r'\data\PatientInfo.csv')
region = pd.read_csv(path + r'\data\region.csv')

import networkx as nx
from pyvis.network import Network

#집단 감염 케이스
infect_case=list(set(case['infection_case'])-set(['etc','contact with patient','overseas inflow']))
#결측치 채우기
patinfo.fillna('nan',inplace=True)
# 지역 확진번호 리스트
pat_id=list(patinfo['patient_id'])
patient_case=list(patinfo['infection_case'])
#누구로부터 감염됐는가
who=list(patinfo['infected_by'])
#결측치값을 제외, 중복제외
from_who=set(list(patinfo['infected_by']))-set(['nan'])
# 확진자 id를 정수로 변환
from_who=[int(i) for i in from_who]
#전체 확진자들 중 who가 결측 아닌 사람들 인덱스
who_index=[int(i) for i in range(len(pat_id)) if list(patinfo['infected_by'])[i] != 'nan' and who[i] in pat_id]
#감염시킨 사람 -> 감염된 확진자
new_edges=[(int(who[i]),int(pat_id[i]))for i in who_index]

#집단 감염간에는 링크가 연결되지 않는다
#감염장소 ->확진자 연결
num_case=[(patient_case[num],int(pat_id[num])) for num in range(len(pat_id)) if patient_case[num] in infect_case]
#집단감염된 확진자 리스트
patient_list=[i[1] for i in num_case]
case_list=list(set([i[0] for i in num_case]))

def get_date(pati_id):
    index=pat_id.index(pati_id)
    str_day=list(patinfo['confirmed_date'])[index]
    str_day=str_day.split('-')
    date=''.join(str_day)
    date=int(date)
    return date

new_nodes_1=[i[0] for i in new_edges if i[0] not in patient_list]
new_nodes_2=[i[1] for i in new_edges if i[1] not in patient_list]
patient_list.extend(new_nodes_1)
patient_list.extend(new_nodes_2)
patient_list=list(set(patient_list))

edge_list=list(num_case)
edge_list.extend(new_edges)

G=nx.Graph()
G.add_nodes_from(patient_list,bipartite=1)
G.add_nodes_from(case_list,bipartite=0)
G.add_edges_from(edge_list)
components_covid=[x for x in sorted(nx.connected_components(G),key=len,reverse=True)]
num_node_compo=[len(x) for x in sorted(nx.connected_components(G),key=len,reverse=True)]
first=num_node_compo.index(5)
smaller=components_covid[first:]
trash=set()
for i in smaller:
    trash=trash|i
patient_list=list(set(patient_list)-trash)
case_list=list(set(case_list)-trash)
edge_list=[i for i in edge_list if i[0] not in list(trash) and i[1] not in list(trash)]
#확진자들의 인덱스
list_ind=[pat_id.index(i) for i in patient_list]

# networkx와 연계해서 딕셔너리 형태 구하기
dict_51 = {}
for i in case_list:
    dict_51[i] = list(set(G[i]) - set(case_list))

for i in case_list:
    date = [get_date(j) for j in dict_51[i]]
    first_infected = [dict_51[i][k] for k in range(len(date)) if date[k] == min(date)]
    for k in first_infected:
        edge_list = list(set(edge_list) - set([(i, k)]))
        edge_list.append((k, i))

# pyvis 네트워크 생성
g=Network(height=800,width=1600,directed=True,notebook=True)
g.set_options("""
var options = {
  "nodes": {
    "font": {
      "size": 100,
      "strokeColor": "rgba(165,215,255,1)"}}}
""")

for i in case_list:
    g.add_node(i,title=i,color='gray',label=i,shape='star')

for i in list_ind:
    id_pat = list(patinfo['patient_id'])[i]
    id_pat_str = str(list(patinfo['patient_id'])[i])
    age = list(patinfo['age'])[i]
    sex = list(patinfo['sex'])[i]

    if age == '0s':
        if sex == 'male':
            g.add_node(id_pat, label=[' '], shape='square', color='purple', size=12, title=id_pat_str)
        elif sex == 'female':
            g.add_node(id_pat, label=[' '], shape='dot', color='purple', size=12, title=id_pat_str)
        else:
            g.add_node(id_pat, label=[' '], shape='triangle', color='purple', size=12, title=id_pat_str)

    elif age == '10s':
        if sex == 'male':
            g.add_node(id_pat, label=[' '], shape='square', color='indigo', size=12, title=id_pat_str)
        elif sex == 'female':
            g.add_node(id_pat, label=[' '], shape='dot', color='indigo', size=12, title=id_pat_str)
        else:
            g.add_node(id_pat, label=[' '], shape='triangle', color='indigo', size=12, title=id_pat_str)

    elif age == '20s':
        if sex == 'male':
            g.add_node(id_pat, label=[' '], shape='square', color='blue', size=12, title=id_pat_str)
        elif sex == 'female':
            g.add_node(id_pat, label=[' '], shape='dot', color='blue', size=12, title=id_pat_str)
        else:
            g.add_node(id_pat, label=[' '], shape='triangle', color='blue', size=12, title=id_pat_str)
    elif age == '30s':
        if sex == 'male':
            g.add_node(id_pat, label=[' '], shape='square', color='skyblue', size=12, title=id_pat_str)
        elif sex == 'female':
            g.add_node(id_pat, label=[' '], shape='dot', color='skyblue', size=12, title=id_pat_str)
        else:
            g.add_node(id_pat, label=[' '], shape='triangle', color='skyblue', size=12, title=id_pat_str)
    elif age == '40s':
        if sex == 'male':
            g.add_node(id_pat, label=[' '], shape='square', color='green', size=12, title=id_pat_str)
        elif sex == 'female':
            g.add_node(id_pat, label=[' '], shape='dot', color='green', size=12, title=id_pat_str)
        else:
            g.add_node(id_pat, label=[' '], shape='triangle', color='green', size=12, title=id_pat_str)
    elif age == '50s':
        if sex == 'male':
            g.add_node(id_pat, label=[' '], shape='square', color='lawngreen', size=12, title=id_pat_str)
        elif sex == 'female':
            g.add_node(id_pat, label=[' '], shape='dot', color='lawngreen', size=12, title=id_pat_str)
        else:
            g.add_node(id_pat, label=[' '], shape='triangle', color='lawngreen', size=12, title=id_pat_str)
    elif age == '60s':
        if sex == 'male':
            g.add_node(id_pat, label=[' '], shape='square', color='yellow', size=12, title=id_pat_str)
        elif sex == 'female':
            g.add_node(id_pat, label=[' '], shape='dot', color='yellow', size=12, title=id_pat_str)
        else:
            g.add_node(id_pat, label=[' '], shape='triangle', color='yellow', size=12, title=id_pat_str)
    elif age == '70s':
        if sex == 'male':
            g.add_node(id_pat, label=[' '], shape='square', color='orange', size=12, title=id_pat_str)
        elif sex == 'female':
            g.add_node(id_pat, label=[' '], shape='dot', color='orange', size=12, title=id_pat_str)
        else:
            g.add_node(id_pat, label=[' '], shape='triangle', color='orange', size=12, title=id_pat_str)
    elif age == '80s':
        if sex == 'male':
            g.add_node(id_pat, label=[' '], shape='square', color='red', size=12, title=id_pat_str)
        elif sex == 'female':
            g.add_node(id_pat, label=[' '], shape='dot', color='red', size=12, title=id_pat_str)
        else:
            g.add_node(id_pat, label=[' '], shape='triangle', color='red', size=12, title=id_pat_str)
    elif age == '90s':
        if sex == 'male':
            g.add_node(id_pat, label=[' '], shape='square', color='brown', size=12, title=id_pat_str)
        elif sex == 'female':
            g.add_node(id_pat, label=[' '], shape='dot', color='brown', size=12, title=id_pat_str)
        else:
            g.add_node(id_pat, label=[' '], shape='triangle', color='brown', size=12, title=id_pat_str)
    else:
        if sex == 'male':
            g.add_node(id_pat, label=[' '], shape='square', color='black', size=12, title=id_pat_str)
        elif sex == 'female':
            g.add_node(id_pat, label=[' '], shape='dot', color='black', size=12, title=id_pat_str)
        else:
            g.add_node(id_pat, label=[' '], shape='triangle', color='black', size=12, title=id_pat_str)


# 링크 리스트 추가
for i in edge_list:
    g.add_edge(source=i[0],to=i[1])

g.show('contact_age_sex.html') # 직접 네트워크를 출력하시려면, 맨 앞에 있는 #을 제거하시면 됩니다.