import pandas as pd
import pathlib
import argparse

# Take in arguments from the Command Line:
parser = argparse.ArgumentParser(description = "Input and output directories.")
parser.add_argument('inputFileName', nargs = 1, type = str, \
                    help = "The filename of the input `__nodes.csv` file.")
parser.add_argument('outputFileName', nargs = 1, type = str, \
                    help = "The filename of the output `__nodesTagged.csv` file.")
args = parser.parse_args()


# Read `__nodes.csv` to a DataFrame:
nodes_df = pd.read_csv('{}.csv'.format(args.inputFileName[0]))

def typeGeneral(type):
    if not isinstance(type, str):
        return 'No data'
    elif type in ('Corporate Pension', 'Public Pension Fund', \
                'Union Pension Fund'):
        return 'Pensions'
    elif type in ('Fund of Funds', 'Money Management Firm', \
                'Wealth Management Firm', 'Investment Advisor', \
                'Private Investment Fund'):
        return 'Investment Managers'
    elif type in ('Banking Institution', 'Corporation', 'Insurance Company', \
                'Real Estate Investment Company'):
        return 'Asset Managers'
    elif type in ('Family Office (Multi)', 'Family Office (Single)', \
                'High-net-worth investor'):
        return 'Family Offices'
    elif type in ('Endowment', 'Foundation', 'Government Agency', \
                'Economic Development Agency', 'Sovereign Wealth Fund'):
        return 'Patient Capital'
    else:
        return 'Other'

eurList = ['Albania', 'Andorra', 'Armenia', 'Austria', 'Azerbaijan', \
            'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria', \
            'Croatia', 'Cyprus', 'Czechia', 'Czech Republic', 'Denmark', \
            'Estonia', 'Finland', 'France', 'Georgia', 'Germany', 'Greece', \
            'Hungary', 'Iceland', 'Ireland', 'Italy', 'Kazakhstan', 'Kosovo', \
            'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malta', \
            'Moldova', 'Monaco', 'Montenegro', 'Netherlands', \
            'North Macedonia', 'Norway', 'Poland', 'Portugal', 'Romania', \
            'Russia', 'San Marino', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', \
            'Sweden', 'Switzerland', 'Turkey', 'Ukraine', 'United Kingdom', \
            'Vatican City', 'Holy See']

def location(country):
    if not isinstance(country, str):
        return 'No data'
    elif 'United States' in country:
        return 'United States'
    elif country in eurList:
        return 'Europe'
    else:
        return 'Other'

# Insert new 'location' column after 'country' column:
nodes_df.insert(list(nodes_df.columns).index('country') + 1, 'location', \
                nodes_df.apply(lambda x: location(x['country']), axis = 'columns'))

# Insert new 'typeGeneral' column after 'location' column:
nodes_df.insert(list(nodes_df.columns).index('location') + 1, 'typeGeneral', \
                nodes_df.apply(lambda x: typeGeneral(x['type']), axis = 'columns'))




# Save the .csv file (note that file name has to be an absolute path):
nodes_df.to_csv("{}.csv".format(args.outputFileName[0]), index = False)
