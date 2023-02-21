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

    Returns: None, writes the pulled data as a csv file in the provided path at
            zip code level demographics for Illinois.
    """

    acs_var = censusdata.download('acs5/subject', 2019, censusdata.censusgeo(
        [('zip%20code%20tabulation%20area', '*')]),
        ['S0601_C01_047E', 'S1901_C01_013E', 'S1501_C02_009E', 
         'S1501_C02_012E', 'S2301_C04_001E', 'S0101_C01_001E',
         'S0101_C01_002E', 'S0101_C01_003E', 'S0101_C01_004E',
         'S0101_C01_005E', 'S0101_C01_006E', 'S0101_C01_007E',
         'S0101_C01_008E', 'S0101_C01_009E', 'S0101_C01_010E',
         'S0101_C01_011E', 'S0101_C01_012E', 'S0101_C01_013E',
         'S0101_C01_014E', 'S0101_C01_015E', 'S0101_C01_016E',
         'S0101_C01_017E', 'S0101_C01_018E', 'S0101_C01_019E',
         'S0601_C01_014E', 'S0601_C01_015E', 'S0601_C01_016E',
         'S0601_C01_017E', 'S0601_C01_021E', 'STATE', 
         'ZCTA'])
    
    acs_var = acs_var[acs_var.STATE == 17]
    acs_var = acs_var.drop('STATE', axis=1)
    
    acs_var.columns = ['hh_median_income', 'hh_mean_income', 'perc_educ_highschool',
                        'perc_educ_bachelor', 'unemployment_rate', 'total_population',
                        'age_under_5', 'age_5_to_9', 'age_10_to_14',
                        'age_15_to_19', 'age_20_to_24', 'age_25_to_29',
                        'age_30_to_34', 'age_35_to_39', 'age_40_to_44',
                        'age_45_to_49', 'age_50_to_54', 'age_55_to_59',
                        'age_60_to_64', 'age_65_to_69', 'age_70_to_74',
                        'age_75_to_79', 'age_80_to_84', 'age_85_up',
                        'pop_white', 'pop_black', 'pop_native',
                        'pop_asian', 'pop_latino', 'zip_code']

    acs_var.to_csv('data_bases/acs_data.csv')