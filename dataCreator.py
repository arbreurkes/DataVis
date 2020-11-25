import pandas as pd
import json

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

# Remove:
election = election.drop(election[(election['state'] == 'Maryland') & (election['county'] == 'Baltimore city')].index)
election = election.drop(election[(election['state'] == 'Maine') & (election['county'] == 'Franklin Cty Townships')].index)
election = election.drop(election[(election['state'] == 'Illinois') & (election['county'] == 'Cook')].index)
election = election.drop(election[(election['state'] == 'Maine') & (election['county'] == 'Hancock Cty Townships')].index)
election = election.drop(election[(election['state'] == 'Maine') & (election['county'] == 'Oxford Cty Townships')].index)
election = election.drop(election[(election['state'] == 'Maine') & (election['county'] == 'Penobscot Cty Townships')].index)
election = election.drop(election[(election['state'] == 'Maine') & (election['county'] == 'Washington Cty Townships')].index)
election = election.drop(election[(election['state'] == 'Maine') & (election['county'] == 'Somerset Cty Townships')].index)

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

# election['county'] = election['county'].replace({' Suburbs': ''}, regex=True)
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

# g = result.groupby(['state', 'county'])
# for name, group in g:
#     if len(group) > 1:
#         print(name)
# # print(result.head(10))

names = []
index = []
with open("./data/d3align/usstates.json") as json_file:
    data = json.load(json_file)
    for p in data:
        index.append(p['id'])
        names.append([p['properties']['name']])

stateId = (pd.DataFrame(names, columns=['state'], index=index))

# Load county id, and split id in state and county id:
countyId = pd.read_csv("./data/d3align/county_id.csv")
countyId['county_id'] = [str(x)[len(str(x)) - 3:] for x in countyId['id']]
countyId['state_id'] = [str(x)[0:len(str(x)) - 3] if len(str(x)[0:len(str(x)) - 3]) > 1 else "0" + str(x)[0:len(str(x)) - 3] for x in countyId['id']]
countyId = countyId.set_index('state_id')

# Merge County and State Data
linkingData = pd.merge(stateId, countyId, how='right', left_index=True, right_index=True)
linkingData['name'] = linkingData['name'].replace({' ': ''}, regex=True)

# Merge Linking data with result
out = pd.merge(result, linkingData, how='outer', left_on=['state', 'county'], right_on=['state', 'name'])

# Normalize election data:
normalized = []
for (a, b) in zip(out['total_votes_x'].astype("Float32"), out['total_votes_y'].astype("Float32")):
    try:
        normalized.append(a/(a+b))
    except:
        normalized.append(-1)
out['normalized_election_outcome'] = normalized

# Rename Columns:
out.rename(columns={"per capita income": "per_capita_income"}, inplace=True)
out.rename(columns={"total_votes_x": "DEM_votes"}, inplace=True)
out.rename(columns={"total_votes_y": "REP_votes"}, inplace=True)

out['id'] = out['id'].astype("Int32")

# Drop columns:
out.drop(['party_x', 'party_y'], axis=1, inplace=True)

# Data Output
linkingData.to_csv(r'./data/output/link.csv', index=False)
result.to_csv(r'./data/output/result.csv', index=False)
out.to_csv(r'./data/output/out.csv', index=False)
