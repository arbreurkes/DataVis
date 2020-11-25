import pandas as pd

income = pd.read_csv(
    "./data/Farmers Markets in the United States/wiki_county_info.csv")
election = pd.read_csv("./data/election/president_county_candidate.csv")

# Only select counties in US
income = income[income['number'] != '—']
income = income[income['number'] != '']
income = income.dropna()

# Format
income['per capita income'] = income['per capita income'].str.replace('$', '')
income['per capita income'] = income['per capita income'].replace({',': ''}, regex=True)
income['per capita income'] = income['per capita income'].replace({' ': ''}, regex=True)

income['population'] = income['population'].replace({',': ''}, regex=True)


# Select DEM en REP votes only
election = election[election['party'].isin(['DEM', 'REP'])]


# Method to combine election data of all counties within a state:
def combineElectionState(state, df):
    # Select all data of state:
    counties = df[df['state'] == state]
    # Group per party
    groups = counties.groupby('party')
    for party, data in groups:
        # Sum all votes
        sum = data['total_votes'].sum()
        # Adjust the votes to the total
        df.loc[(df['state'] == state) & (df['party'] == party), 'total_votes'] = str(sum)
        df.loc[(df['state'] == state) & (df['party'] == party), 'county'] = state


def combineIncomeData(state, df):
    # print(df['per capita income'])
    counties = df[df['state'] == state]
    newIncome = 0
    sum = 0
    for s in counties['population']:
        sum += int(s)
    for income, weight in zip(counties['per capita income'], counties['population']):
        newIncome += int(income) * int(weight) / int(sum)
    df.loc[df['state'] == state, 'per capita income'] = str(newIncome)
    df.loc[df['state'] == state, 'county'] = state
    df.loc[df['state'] == state, 'number'] = -1


# Collapse Columbia
combineElectionState('District of Columbia', election)
combineElectionState('Alaska', election)

combineIncomeData('Alaska', income)

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
                  income[['number', 'county', 'state', 'per capita income']],
                  how='right', on=['state', 'county'])
result = result.drop_duplicates()

demVotes = result[result['party'] == 'DEM']
repVotes = result[result['party'] == 'REP']

result = demVotes.merge(repVotes, on=['state', 'county','number','per capita income'], how='left', sort=False)
print(result.head(10))
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
