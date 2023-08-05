#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilities to break time correlation of features and create dataset
to look back N time steps (window_size) and predict up to the K-th time steps 
into the future (horizon_size) at a starting point O (offset) in the future.
"""

import numpy as np
import pandas as pd


''' For now lets simplify:
Simple Window Slider
--------------------

- We assume ∆T is constant 
- R = 1 -> We just produce 1 horizon of predictions.
- L = 1 -> We slide the window 1 step at a time

'''

class WindowSlider(object):
    ''' Window Slider to break Time Correlations 

    This method wrangles with an input time-series 
    data of X features and a y response.

    Given a Window Size, it creates a row for each
    prediction y, given the window of itself and the
    rest of the variables as independent predictors.

                
    Example
    -------

    import numpy as np
    import pandas as pd
    from window import WindowSlider
    
    X = pd.DataFrame(
            np.array([[1, 1, 2], [3, 0, 7], [8, 8, 1], [5, 1, 8], [8, 8, 1]]), 
            columns=['X1','X2','Y'])
    
    window_generator = WindowSlider(window_size=2, horizon_size=1)
    RES = window_generator.collect_windows(data=X)

    print(X)

       X1  X2  Y
    0   1   1  2
    1   3   0  7
    2   8   8  1
    3   5   1  8
    4   8   8  1
    
    print(RES)
        
       X1(t-1)  X1(t-2)  X2(t-1)  X2(t-2)  Y(t-1)  Y(t-2)  Y
    0        1        3        1        0       2       7  1
    1        3        8        0        8       7       1  8
    2        8        5        8        1       1       8  1

    '''

    def __init__(self, window_size=2, horizon_size=1):        

        self.W = window_size
        self.K = horizon_size
        self.R = 1
        # self.cols= cols
    
    def collect_windows(self, data, prev_y=True):
        '''
        Input:
            data: pd.Dataframe  
                Features and the response [Xy]
                Respone must be the last of the columns

        Returns:
            X: Pandas dataframe with the collected windows
        '''
        # output_shape = f(input_shape, window, stride)
        ix = data.index[self.W:]
        x = data.values
        N, C = data.shape
        L = N - self.W # TODO: self.R 
        
        # Apend t-lag to column name
        cols = list()
        for j, col in enumerate(data.columns):                        
            for i in range(self.W):
                cols.append(col + ('(t-{})'.format(i+1)))
        cols.append('Y')

        # Reshape to desired dataframe
        X = list() 
        for i in range(L):
            X_row = list()
            for j in range(C):
                for k in range(self.W):
                    X_row.append(x[i+k,j])
            X_row.append(x[i+self.W,-1])
            X.append(X_row)
        
        return pd.DataFrame(X,columns=cols,index=ix)


if __name__ = '__main__':
    pass