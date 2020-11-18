import pandas as pd

income = pd.read_csv(
    "./data/Farmers Markets in the United States/wiki_county_info.csv")
election = pd.read_csv("./data/election/president_county_candidate.csv")
# Only select counties in US
income = income[income['number'] != '—']
income = income[income['number'] != '']
income = income.dropna(subset = ['number'])

# For testing, select only Joe Biden Votes
election = election[election['candidate'] == 'Joe Biden']

count = {}
# pat = "(.)+[' '](County)"
# repl = lambda m: m.group('two').swapcase()
# pd.Series(['One Two Three', 'Foo Bar Baz']).str.replace(' State', '')

# Washington City -> District of Columbia
income['county'] = income['county'].replace({'Washington City': 'District of Columbia'}, regex=True)
election['county'] = election['county'].replace({'Larue': 'LaRue'}, regex=True)

election['county'] = election['county'].replace({' Suburbs': ''}, regex=True)
election['county'] = election['county'].replace({' Cty Townships': ''}, regex=True)
election['county'] = election['county'].replace({' Cty Townshps': ''}, regex=True)

# Remove 'Parish'
election['county'] = election['county'].replace({' Parish': ''}, regex=True)
income['county'] = income['county'].replace({' Parish': ''}, regex=True)

# Remove 'County'
election['county'] = election['county'].replace({' County': ''}, regex=True)
income['county'] = income['county'].replace({' County': ''}, regex=True)

# Remove 'City' and 'city'
election['county'] = election['county'].replace({' City': ''}, regex=True)
income['county'] = income['county'].replace({' City': ''}, regex=True)
election['county'] = election['county'].replace({' city': ''}, regex=True)
income['county'] = income['county'].replace({' city': ''}, regex=True)

# Remove Spaces NOTE: Do this last
election['county'] = election['county'].replace({' ': ''}, regex=True)
income['county'] = income['county'].replace({' ': ''}, regex=True)

# Merge dataframes
result = pd.merge(election[['state', 'county', 'party', 'total_votes']],
                  income[['number', 'county', 'state', 'per capita income', 'median household income',
                          'median family income']],
                  how='right', on=['state', 'county'])
print(result.head())
print(result['number'])
result.to_csv(r'./data/output/out.csv', index=False)

#
# for _, row in election.iterrows():
#     county = row['state'] + "," + row['county']
#     party = row['party']
#     if party == 'DEM' or party == 'REP':
#         count[county + '-total'] = count.get(county + '-total', 0) + row['total_votes']
#         count[county + '-' + party] = count.get(county + '-' + party, 0) + row['total_votes']
#
# print(count)
#
# income['DEM'] = -1
# income['REP'] = -1
# income['total'] = -1
#
# for i, row in income.iterrows():
#     county = row['State_Name'] + "," + row['County']
#     income.at[i, 'total'] = count.get(county + '-total', 0)
#     income.at[i, 'DEM'] = count.get(county + '-DEM', 0)
#     income.at[i, 'REP'] = count.get(county + '-REP', 0)
#
# print(income.head(1000))
