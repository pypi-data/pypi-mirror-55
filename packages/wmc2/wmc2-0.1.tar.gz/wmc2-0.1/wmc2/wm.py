class wm:
 encoding="""import math

def gamma(m):
    return ((len(str(bin(m)[2:]))-1)*'0')+bin(m)[2:]

def delta(m):
    n = 1 + math.floor(math.log(m,2))
    return gamma(n)+bin(m)[3:]

def goulomb(m,b):
    q = m//b
    q1 = q*'0'+str(1)
    i = math.floor(math.log(b,2))
    r = m - q*b
    d = int(math.pow(2,i+1) - b)
    if r<d:
        r1 = bin(r)[2:2+i+1]
        if(len(r1)<i):
            r1 = '0'*(i-len(r1)) + str(r1)
    else:
        r1 = bin(r+d)[2:2+i+2]
        if(len(r1)<i+1):
            r1 = '0'*(i-len(r1)+1) + str(r1)
    return q1+r1

for i in range(1,31):
    print(i,end=" ")
    print(gamma(i),end=" ")
    print(delta(i),end=" ")
    print(goulomb(i,10),end=" ")
    print()"""

 inverted_index="""from nltk import word_tokenize
from nltk import sent_tokenize
from nltk import FreqDist
import pandas as pd

sl = ["Oh wow lookie here here.","Holy crap lookie here, this is beautiful","Tushar is the opposite of beautiful here"]

stpwrds = [",",".","!","?","'"]

ml = []
h = []

for i in sl:
    l = []
    for j in word_tokenize(i):
        if j not in stpwrds:
           l.append(j.lower())
           h.append(j.lower())
    ml.append(l)

di = dict(FreqDist(h))

ans = []

for i in list(di.keys()):
    lt = []
    c = 1
    for j in ml:
        ltt = []
        ltt.append("Doc: "+str(c))
        if i in j:
            ltt.append("Count: "+str(j.count(i)))
        else:
            ltt.append(0)
        for k in range(len(j)):
            if i==j[k]:
                ltt.append(k+1)
        lt.append(ltt)
        c = c+1
    ans.append(lt)

d = 0
for i in list(di.keys()):
    print(i,end="          ")
    print(ans[d])
    print()
    d = d + 1

m = input("enter word plssss")
d = 0
for i in list(di.keys()):
    if i==m:
        print(i,end="          ")
        print(ans[d])
    d = d+1"""

 pagerank="""import numpy as np
a = [[0,0,1,0,0,0],[0.5,0,0.5,0,0,0],[1,0,0,0,0,0],[0,0,0,0,0.5,0.5],[0,0,0.5,0.5,0,0],[0,0,0,0.5,0.5,0]]
M = np.array(a)
H = np.transpose(a)
N = np.array([0.85,0.85,0.85,0.85,0.85,0.85])
res = N
ans = []
for i in range(7):
    print("iteration",i+1)
    res = np.dot(H,res)
    if(i==0):
        c = res
    print(res)
v = c.tolist()
v.sort(reverse=True)
o = c.tolist()
for i in range(6):
    print("The rank of page number "+str(i+1)+" is "+str(v.index(o[i])+1))"""

 scraping="""from bs4 import BeautifulSoup
import requests
import warnings
import tkinter as tk
from PIL import ImageTk, Image
import os
from io import BytesIO

url = "https://www.snapdeal.com/products/mobiles-mobile-phones/filters/Form_s~Smartphones"
warnings.filterwarnings("ignore")


page_response = requests.get(url,verify = False, timeout=5)

page_content = BeautifulSoup(page_response.content,"html.parser")

product_price = page_content.find_all('span',class_='lfloat product-price')

product_name = page_content.find_all('p',class_='product-title')

product_discount = page_content.find_all('div',class_='product-discount')

test = page_content.find_all('img',class_='product-image')


    

for i in range(len(product_name)):
    s = product_name[i].text
    s = s.lstrip()
    s = s.rstrip()
    print('PRODUCT '+str(i+1)+' :')
    print('PRODUCT NAME : ' + s)

    dis = product_price[i].text
    dis = dis.lstrip()
    dis = dis.rstrip()
    print('PRODUCT PRICE : ' + dis)

    n = product_discount[i].text
    n = n.lstrip()
    n = n.rstrip()
    print('PRODUCT DISCOUNT : '+ n)
    try:
        url = test[i]['src']
    except:
        url = test[i]['data-src']
    root = tk.Tk()
    response = requests.get(url)
    img_data = response.content
    img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
    panel = tk.Label(root, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")
    root.mainloop()
    print('')"""

 tf_idf="""from nltk import word_tokenize
import math
import pandas as pd

sl = ["Oh wow lookie here here.","Holy crap lookie here, this is beautiful! Tushar ke bubs","oh wow Tushar is the opposite of beautiful here"]
stpwrds = [",",".","!","?","'"]

ml = []
h = []

for i in sl:
    l = []
    for j in word_tokenize(i):
        if j not in stpwrds:
           l.append(j.lower())
           h.append(j.lower())
    ml.append(l)

h = set(h)
h = list(h)

tfm = []

for i in ml:
    tf = dict()
    ch = []
    for j in i:
        if j not in ch:
            ch.append(j)
            tf[j] = i.count(j)/len(set(i))
    tfm.append(tf)

idf = dict()

for i in h:
    c = 0
    for j in ml:
        if i in j:
            c = c+1
    idf[i] = math.log((1+len(sl))/c)


cnt = 1
for i in tfm:
    ans = pd.DataFrame(columns=['Term','TF','IDF','TF*IDF'])
    print("----------------DOCUMENT"+str(cnt)+"-------------------------")
    for j in list(i.keys()):
        l = []
        l.append(str(j))
        l.append(str(i[j]))
        l.append(str(idf[j]))
        l.append(str(i[j]*idf[j]))
        ans = ans.append(pd.Series(l,index=['Term','TF','IDF','TF*IDF']),ignore_index=True)
    cnt = cnt +1
    print(ans)"""

 elbow="""from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pyplot as plt

x1 = np.array([3, 1, 1, 2, 1, 6, 6, 6, 5, 6, 7, 8, 9, 8, 9, 9, 8])
x2 = np.array([5, 4, 5, 6, 5, 8, 6, 7, 6, 7, 1, 2, 1, 2, 3, 2, 3])

plt.plot()
plt.xlim([0, 10])
plt.ylim([0, 10])
plt.title('Dataset')
plt.scatter(x1, x2)
plt.show()

# create new plot and data
plt.plot()
X = np.array(list(zip(x1, x2))).reshape(len(x1), 2)
colors = ['b', 'g', 'r']
markers = ['o', 'v', 's']

# k means determine k
distortions = []
K = range(1,10)
for k in K:
    kmeanModel = KMeans(n_clusters=k).fit(X)
    kmeanModel.fit(X)
    distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0])

# Plot the elbow
plt.plot(K, distortions, 'bx-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('The Elbow Method showing the optimal k')
plt.show()"""

 apriori="""import numpy as np
import pandas as pd
from apyori import apriori

store_data = pd.read_csv('Day1.csv',header=None)

records = []

for i in range(0,22):
    records.append([str(store_data.values[i,j]) for j in range(0,6)])

association_rules = apriori(records,min_support=0.50,min_confidence=0.7,min_lift=1.2,min_length=2)
association_results = list(association_rules)

print(association_results)"""

