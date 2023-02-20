# make initial data that we can structure visualizations on
import pandas as pd
import numpy as np

def make_dummy_data():
    '''
    MAKE DOC STRING
    '''
    NUM_ROWS = 70

    # Disparity index inputs
    df = pd.DataFrame(np.random.randint(0, 100, size=(NUM_ROWS, 4)), columns=['x1','x2','x3','x4'])
    
    # Columns we know we'll have
    df['zipcode'] = np.random.randint(00000,99999,size=(NUM_ROWS, 1))
    df['num_evictions'] = np.random.randint(0,10000,size=(NUM_ROWS, 1))
    df['disparity_index'] = np.random.rand(NUM_ROWS, )

    return df

    