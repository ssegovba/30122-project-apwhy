import pandas as pd

### To run, we have to instantiate the following global parameters###

# 1) thresholds represent pre-defined cutoffs obtained from our literature review
thresholds = {
'type I crime': 10,
'type II crime': 30,
'rental affordability': 0.3,
'house price affordability': 4,
'time to cbd': 30,
'distance to cbd': 5000}

# 2) specify fixed cutoff as specified in AF method. 
#    Criteria is to censor data for non-deprived neighborhoods
k = 2

# 3) path to clean data (currently synthetic as we are still merging our dataset)
cleaned_data = ""

class MultiDimensionalDeprivation:
    def __init__(self, k, cleaned_data, thresholds):
        '''
        constructor
        '''
        self.k = k
        self.data = pd.read_csv(cleaned_data)
        self.thresholds = thresholds
        self.indicators = list(thresholds.keys())
        
    def deprivation_matrix(self):
        '''
        This function computes a matrix of deprivation scores for n zipcodes (rows)
        in d dimensions (columns)
        Inputs:
        cleaned_data    : takes in cleaned processed data
        k               : fixed cutoff in AF method
        
        Returns wellbeing scores as a pandas dataframe
        '''
        #Generate binary matrix y
        mat_y = pd.DataFrame(index=self.data.index, columns=self.indicators)
        self.data['deprivation_share'] = 0
        for ind in self.indicators:
            mat_y[ind] = (self.data[ind] >= self.thresholds[ind]).astype(int)
            self.data['deprivation_share'] += mat_y[ind]

        # for all zipcodes that has less than k deprivations assign all elements to
        # be 0
        mat_y[self.data['deprivation_share'] <= self.k] = 0
        
        return mat_y

    def normalized_gap(self):
        '''
        Computes the normalized gap - Matrix g^1 in AF method
        Represents the extent of deprivation in distance relative to thresholds
        Some prefer this matrix as this satisfies monotonicity

        Input: Matrix Y from fn:deprivation_matrix()
        Returns: Matrix g^1(k) as a pandas dataframe
        '''
        mat_y = self.deprivation_matrix()
        
        # Compute the normalized gap
        mat_g1 = pd.DataFrame(index=self.data.index, columns=self.indicators)
        for ind in self.indicators:
            mat_g1[ind] = (self.data[ind] - self.thresholds[ind]) / self.thresholds[ind]
        
        # Replace NaN values and negative values with 0 
        mat_g1 = mat_g1.fillna(0)
        mat_g1[mat_g1 < 0] = 0
        
        # Apply mat_y to g1
        for ind in self.indicators:
            mat_g1[ind] *= mat_y[ind]

        return mat_g1

    def power_gap(self, n):
        '''
        Computed power gap - Matrix g^alpha (n = alpha).
        This matrix is used by policymakers to target the most deprived 
        neighborhoods first

        Input: Matrix g^1(k) from fn: normalized_gap()
        Returns: Matrix g^alpha(k) as a pandas dataframe
        '''
        mat_g2 = self.normalized_gap() ** n
        return mat_g2