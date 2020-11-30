import pandas as pd
import json

# Aligning data
names = []
index = []
with open("./data/d3align/usstates.json") as json_file:
    data = json.load(json_file)
    for p in data:
        index.append(p['id'])
        names.append([p['properties']['name']])
stateData = pd.DataFrame(names, columns=['state'], index=index)

# Load county id, and split id in state and county id:
countyData = pd.read_csv("./data/d3align/county_id.csv")
countyData['county_id'] = [str(x)[len(str(x)) - 3:] for x in countyData['id']]
countyData['state_id'] = countyData['index'] = [
    str(x)[0:len(str(x)) - 3] if len(str(x)[0:len(str(x)) - 3]) > 1 else "0" + str(x)[0:len(str(x)) - 3] for x in
    countyData['id']]
countyData = countyData.set_index('index')

# Merge County and State Data
countyData = pd.merge(stateData, countyData, how='right', left_index=True, right_index=True).dropna()

electionData = pd.read_csv("./data/election/president_county_candidate.csv")

# Rename the election data to match the D3 linking data:
electionData['county'] = electionData['county'].replace({' County': ''}, regex=True)
electionData['county'] = electionData['county'].replace({' Parish': ''}, regex=True)
electionData['county'] = electionData['county'].replace({' Cty Townships': ''}, regex=True)
electionData['county'] = electionData['county'].replace({' City': ''}, regex=True)

m = electionData['state'] == 'Virginia'
electionData.loc[m, 'county'] = electionData.loc[m, 'county'].replace({' city': ''}, regex=True)

# print(electionData.loc[m]['county'].replace())
# Select DEM en REP votes only
electionDataCounty = electionData[electionData['party'].isin(['DEM', 'REP'])].drop(['won', 'candidate'], axis=1)
# Do this for state as well
# electionDataState = electionData[electionData['party'].isin(['DEM', 'REP'])].drop(['won', 'candidate'], axis=1)

# Flatten DataFrame
demVotes = electionDataCounty[electionDataCounty['party'] == 'DEM']
repVotes = electionDataCounty[electionDataCounty['party'] == 'REP']

electionDataCounty = repVotes.merge(demVotes, on=['state', 'county'], how='left', sort=False)
# Rename Columns:
electionDataCounty.rename(columns={"per capita income": "per_capita_income"}, inplace=True)
electionDataCounty.rename(columns={"total_votes_x": "DEM_votes"}, inplace=True)
electionDataCounty.rename(columns={"total_votes_y": "REP_votes"}, inplace=True)

# Merge D3 linking data with election data
countyData = pd.merge(countyData, electionDataCounty, how='left', left_on=['state', 'name'], right_on=['state', 'county'])

# Normalize election data:
normalized = []
for (a, b) in zip(countyData['DEM_votes'].astype("Float32"), countyData['REP_votes'].astype("Float32")):
    try:
        normalized.append(a / (a + b))
    except:
        normalized.append('')
countyData['normalized_election_outcome'] = normalized

# Output:
electionDataCounty.to_csv(r'./data/output/electionDataCounty.csv', index=False)

countyData.to_csv(r'./data/output/countyData.csv', index=False)
stateData.to_csv(r'./data/output/stateData.csv', index=False)