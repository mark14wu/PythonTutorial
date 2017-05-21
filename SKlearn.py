import h5py
from sklearn import svm
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.model_selection import KFold, cross_val_score
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier
from sklearn import tree

hfile = h5py.File('studio_songs_mfcc.h5', 'r')
X = hfile['X'][:]
Y = hfile['Y'][:]

k_fold = KFold(n_splits = 5)
model_list = []

# gnb = GaussianNB()
# model_list.append(gnb)
#
# bnb = BernoulliNB()
# model_list.append(bnb)
#
# mnb = MultinomialNB()
# model_list.append(mnb)

# svm = svm.SVC(decision_function_shape='ovo')
# model_list.append(svm)
#
# sgd = SGDClassifier(loss="hinge", penalty="l2")
# model_list.append(sgd)
#
# knc = KNeighborsClassifier(15, weights='uniform')
# model_list.append(knc)

clf = tree.DecisionTreeClassifier()
# clf = clf.fit(X, Y)
print clf
result = cross_val_score(clf, X, Y, cv=k_fold, n_jobs=-1)
print result
# model_list.append(clf)

#
# nc = NearestCentroid()
# model_list.append(nc)
#
# gpc = GaussianProcessClassifier()
# model_list.append(gpc)
#
# dtc = DecisionTreeClassifier()
# model_list.append(dtc)
#
# gbc = GradientBoostingClassifier()
# model_list.append(gbc)


# vc = VotingClassifier(estimators=[('dt', dtc), ('knn', knc), ('svc', svm)], voting='soft', weights=[2,1,2])
#
# for model in model_list:
#     print model
#     result = cross_val_score(model, X, Y, cv=k_fold, n_jobs=-1)
#     print ':::::::::', result
# vc=vc.fit(X,Y)