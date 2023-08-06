import pymysql
import pymysql.cursors
import pandas as pd
import numpy as np
import json
import sqlite3

import sqlite3
c = sqlite3.connect('data.db')
c.close()

def get_connection():
    DB = sqlite3.connect('data.db')
    return DB

def setup_db():
    try:
        con = get_connection()
        # Set table Structure
#         data = ''',img_gray,time,label,shape
# 0;"[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 38, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]";1.57215E+12;NONE;"[14, 26]"'''
#         df = pd.DataFrame([x.split(';') for x in data.split('\n')[1:]], columns=[x for x in data.split('\n')[0].split(',')])
#
        df=pd.DataFrame()
        df['img_gray']=[]
        df['img_gray'] = df['img_gray'].astype('object')
        df['time']=[]
        df['time'] = df['time'].astype('object')
        df['label']=[]
        df['label'] = df['label'].astype('object')
        df['shape']=[]
        df['shape'] = df['shape'].astype('object')
        df.to_sql('training_data_small', con=con, if_exists = 'append', index=False)

        print('Successfully setup head_controller db.')
    except Exception as e:
        print("Exeception occured:{}".format(e))
    finally:
        con.close()


def get_training_data():
    '''
    Will require further resizing, since it is recalled in a visible form (2d)

    E.g.
    X.resize(X.shape[0],(X.shape[1]*X.shape[2]))
    '''

    con = get_connection()
    df = pd.read_sql_query('''select * from training_data_small''', con)
    df['data'] = df.apply(lambda x: np.array(json.loads(x['img_gray'])),axis=1)
    df['shape_tuple'] = df.apply(lambda x: tuple(json.loads(x['shape'])),axis=1)
    df['data_resized'] = df.apply(lambda x: x['data'].resize(x['shape_tuple']),axis=1)
    X = np.array([np.array(x) for x in df['data'].values])
    y = df['label'].values
    return X,y

def cross_validation_score_from_data(X,y):

    from sklearn.model_selection import train_test_split
    from sklearn import datasets
    from sklearn import svm

    X.resize(X.shape[0],(X.shape[1]*X.shape[2]))
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.4)
    X_train.shape, y_train.shape
    X_test.shape, y_test.shape

    clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
    return clf.score(X_test, y_test)


def send_df_to_table(df,table_name,operation='fail'):
    '''
    Sends a df to the sql server.
    Expects operation to be set to 'fail', 'append', or 'replace'.

    E.g. Usage:
    import db
    db.send_df_to_table(df,'test',operation='append')
    '''

    database = 'head_controller'

    assert len(df)!=0, 'df was empty. Cannot send to db.'

    try:
        # Create a cursor object
        con = get_connection()
        df.to_sql(name=table_name, con=con, if_exists = operation, index=False)

    except Exception as e:
        print("Exception occured:{}".format(e))

    finally:
        con.close()
    return
