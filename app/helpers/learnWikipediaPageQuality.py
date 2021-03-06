# -*- coding: utf-8 -*-
"""
learnWikipediaPageQuality.py
Created on Wed Jun 11 17:16:22 2014
Learn to predict the quality of Wikipedia pages

@author: ahna
"""

import pandas as pd
import numpy as np
import sklearn
import sklearn.linear_model
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing
from sklearn.pipeline import Pipeline
from sklearn.metrics import recall_score, precision_score
import pickle
#import qualityPredictor
from app.helpers.qualityPredictor import qualPred

def optimizeRegConstant(logres):
    # determine regularization constant. TO DO: make it so it returns best C. also might need to save and restore original C
    Cs = np.linspace(0.01,0.6,20)
    scores = []
    for c in Cs:
        logres.set_params(clf__C=c).fit(X_train, y_train)
        scores.append(logres.score(X_test,y_test))
    print(np.array([Cs,scores]))
    plt.plot(Cs,scores)



def main():
    qp = qualPred() 
    
    ##############################################
    # file names
    featured_csvfilename = '/Users/ahna/Documents/Work/insightdatascience/project/wikiphilia/data/featured.csv'
    flagged_csvfilename = '/Users/ahna/Documents/Work/insightdatascience/project/wikiphilia/data/flagged.csv'
    #qualityPredictorFile = '/Users/ahna/Documents/Work/insightdatascience/project/wikiphilia/data/qualityPredictor.p'
    qualityPredictorFile = '/Users/ahna/Documents/Work/insightdatascience/project/insightfl/app/helpers/qualityPredictorFile.p'
        
    ##############################################
    # load data
    featuredDF = pd.DataFrame().from_csv(featured_csvfilename) # load existing dataframe from file and append to it
    flaggedDF = pd.DataFrame().from_csv(flagged_csvfilename) # load existing dataframe from file and append to it
    flaggedDF['featured']=False
    featuredDF['flags']='NA'
    featuredDF['flagged']=0
    featuredDF['featured']=True
    DF = pd.concat([featuredDF,flaggedDF])
    
    ##############################################
    # set up data matrices
    # features are length, nextlinks, nimages, nlinks
    X = DF[qp.featureNames].values.astype('float')
    #X_scaled = preprocessing.scale(X) # feature normalization, save noralization info!
    
    # labels are 1 if featured is True, 0 if flagged is True
    y = DF['featured'].values
    
    ##############################################
    
    ##############################################
    # divide into training set and test set
    np.random.seed()    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=qp.testPropor, train_size=1-qp.testPropor, random_state=np.random.random_integers(100))
        
    ##############################################
    # build learning pipeline for logistic regression
    clf = sklearn.linear_model.LogisticRegression(C=0.35) 
    qp.logres = Pipeline([("scaler", preprocessing.StandardScaler()), ("clf", clf)])
    qp.logres.fit(X_train, y_train)
    qp.clf = clf
#    qp.logres.score(X_test,y_test)

    ##############################################
    # save results
    pickle.dump(qp,open(qualityPredictorFile, 'wb'))
    print clf.raw_coef_
    qp2 = pickle.load(open(qualityPredictorFile, 'rb'))
    print("Found: " + str(qp2))

    ##############################################
    # caculate accuracy on test set
    print("Score on training data: " + str(qp.logres.score(X_train, y_train)))
    print("Score on test data: " + str(qp.logres.score(X_test, y_test)))
    preds = qp.logres.predict(X_test)
    print("Recall score on test data: " + str(recall_score(y_test, preds)))
    print("Precision score on test data: " + str(precision_score(y_test, preds)))
    # Prec = 1, recall = 0.68 means no false negatives, erring on the side of labelling 1 (high quality)    
    
    ##############################################
    # determine which features matter and drop the ones that don't
    
    ##############################################
    # deploy to unlabelled data
    # for final app, ideally i'd compute this index on all of wikipedia
    #sklearn.linear_model.LogisticRegression.predict()    


if __name__ == '__main__': main()