# make initial data that we can structure visualiztions on
import pandas as pd
import numpy as np

def make_dummy_data():
    '''
    MAKE DOC STRING
    '''
    NUM_ROWS = 59

    # Disparity index inputs
    df = pd.DataFrame(np.random.randint(0, 100, size=(NUM_ROWS, 4)), columns=['x1','x2','x3','x4'])
    
    # Columns we know we'll have
    df['zipcode'] = np.array(['60601', '60602', '60603', '60604',
                               '60605', '60606', '60607', '60608',
                               '60609', '60610', '60611', '60612',
                               '60613', '60614', '60615', '60616',
                               '60617', '60618', '60619', '60620',
                               '60621', '60622', '60623', '60624',
                               '60625', '60626', '60628', '60629',
                               '60630', '60631', '60632', '60633',
                               '60634', '60636', '60637', '60638',
                               '60639', '60640', '60641', '60642',
                               '60643', '60644', '60645', '60646',
                               '60647', '60649', '60651', '60652',
                               '60653', '60654', '60655', '60656',
                               '60657', '60659', '60660', '60661',
                               '60666', '60707', '60827'])

    df['num_evictions'] = np.random.randint(0,10000,size=(NUM_ROWS, 1))
    df['disparity_index'] = np.random.rand(NUM_ROWS, )

    return df

    