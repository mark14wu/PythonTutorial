from sklearn import datasets
# import joblib
# 4G 报错

# import pandas
import h5py
# 最好的是h5py

iris = datasets.load_iris()
from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb.fit(iris.data, iris.target)
y_pred = gnb.predict(iris.data)
print("Number of mislabeled points out of a total %d points : %d"
      % (iris.data.shape[0],(iris.target != y_pred).sum()))

# joblib.dump(gnb, 'model/gnb.model')

h5m = h5py.File('gnb.h5', 'w')
h5m.create_dataset('gnb', data = gnb)
h5m.create_dataset('ubm', data = iris)
h5m.close()

load = h5py.File('gnb.h5', 'r')
gnb = load.get("gnb")
#y_pred = gnb.fit(iris.data, iris.target).predict(iris.data)
#print("Number of mislabeled points out of a total %d points : %d"
      #% (iris.data.shape[0],(iris.target != y_pred).sum()))