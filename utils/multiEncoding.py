# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 10:48:05 2021

@author: gabri
"""

import pandas as pd

def encode(db_to_encode):
    
    df = pd.read_csv(db_to_encode)
   # df=df.drop(["Name"] ,axis=1)
   # print(df)
    
    from sklearn.preprocessing import OneHotEncoder
    ohe = OneHotEncoder(categories='auto')
    
    """I'm creating a variable which will contain all the name of the columns that don't have integers as attributes"""
    obj_columns = list(df.select_dtypes(include=['object']).columns)
    print(obj_columns)
    
    """I'm creating a list which will be more efficient to create a DataFrame after the for instead of concateneting 
        all the DataFrames"""
    pdList = [df]
    
    """I'm encoding one column at a time and I need the realName to create columns in the DataFrame with the correct
        name of the attribute, I then append the new dataframe in the list create before"""
    for string in obj_columns:
        X = ohe.fit_transform(df[[string]]).toarray()
        Z = pd.DataFrame(X,columns = ohe.categories_,dtype='int64')
        #realName = Z.columns.get_level_values(0)
        realName = string+"*"+Z.columns.get_level_values(0)  #this would safe the name of the columns plus the name of the attribute
        realDf = pd.DataFrame(X,columns = realName,dtype='int64')
        pdList.append(realDf)
        
    """I'm concateneting all the dataFrames in the list to create a single dataFrame"""
    new = pd.concat(pdList,axis='columns')
    #print(new)
    
    """I'm dropping the initial columns which had object values"""
    for string in obj_columns:
        new = new.drop([string],axis='columns')
    #print(new)
    
    return new

def encodeBig(db_to_encode):
    
    df = pd.read_csv(db_to_encode)
    df=df.drop(["Id","Release Date","RatingValue","RatingCount","ReviewCount","Filming Locations","Description"],axis=1)
    df= df.loc[df["Year"]>=2000]
    df = df.reset_index(drop=True)
    final=df.dropna()
    final=final.reset_index(drop=True)
    print(final)
   # print(df)
        
    from sklearn.preprocessing import OneHotEncoder
    ohe = OneHotEncoder(categories='auto')
    
    """I'm creating a variable which will contain all the name of the columns that don't have integers as attributes"""
    obj_columns = list(final.select_dtypes(include=['object']).columns)
    print(obj_columns)
    
    """I'm creating a list which will be more efficient to create a DataFrame after the for instead of concateneting 
        all the DataFrames"""
    pdList = [final]
    
    """I'm encoding one column at a time and I need the realName to create columns in the DataFrame with the correct
        name of the attribute, I then append the new dataframe in the list create before"""
    for string in obj_columns:
        X = ohe.fit_transform(final[[string]]).toarray()
        Z = pd.DataFrame(X,columns = ohe.categories_,dtype='int64')
        #realName = Z.columns.get_level_values(0)
        realName = string+"*"+Z.columns.get_level_values(0)  #this would safe the name of the columns plus the name of the attribute
        realDf = pd.DataFrame(X,columns = realName,dtype='int64')
        pdList.append(realDf)
        
    """I'm concateneting all the dataFrames in the list to create a single dataFrame"""
    new = pd.concat(pdList,axis='columns')
    #print(new)
    
    """I'm dropping the initial columns which had object values"""
    for string in obj_columns:
        new = new.drop([string],axis='columns')
    
    return new

"""With this function I'm able to retrieve the name of the columns requested by the example, a sort of inverse encoding"""
# def inverse(schema_to_inverse):
    
    
    # objList=[]
    # for string in schema_to_inverse:
    #     if not objList:
    #         a = string.find('_')
    #         if( a != -1 ):
    #             copy = string[0:a]
    #             objList.append(copy)
    #     else:
    #         a=string.find('_')
    #         if( a!=-1):
    #             copy = string[0:a]
    #             if(copy!=objList[-1]):
    #                 objList.append(copy)
    
#     return objList
    