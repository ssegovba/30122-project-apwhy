#make sure to install these packages before running:
# pip install censusdata
# pip install csv
# pip install pandas

import censusdata

def pull_acs_data():
    """
    Retrieves 2019 data of the American Census Survey
        from the US Census API

    Input: None

    Returns (pd.DataFrame): zip code level demographics
    """

    acs_var = censusdata.download('acs5/subject', 2019, censusdata.censusgeo(
        [('zip%20code%20tabulation%20area', '*')]),
        ['S0601_C01_047E', 'S1901_C01_013E',
         'S1501_C02_009E', 'S1501_C02_012E',
         'S2301_C04_001E'])
    
    acs_var.columns = ['hh_median_income', 'hh_mean_income',
                        'perc_educ_highschool', 'perc_educ_bachelor',
                        'unemployment_rate']
    
    return acs_var