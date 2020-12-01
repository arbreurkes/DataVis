import pandas as pd
import json

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

# Rename
m = countyData['name'] == 'District of Columbia'
countyData.loc[m, 'id'] = 11000

countyData['county_id'] = [str(x)[len(str(x)) - 3:] for x in countyData['id']]
countyData['state_id'] = countyData['index'] = [
    str(x)[0:len(str(x)) - 3] if len(str(x)[0:len(str(x)) - 3]) > 1 else "0" + str(x)[0:len(str(x)) - 3] for x in
    countyData['id']]
countyData = countyData.set_index('index')

# Merge County and State Data
countyData = pd.merge(stateData, countyData, how='outer', left_index=True, right_index=True)

electionData = pd.read_csv("./data/election/president_county_candidate.csv")

# Rename the election data to match the D3 linking data:
electionData['county'] = electionData['county'].replace({' County': ''}, regex=True)
electionData['county'] = electionData['county'].replace({' Parish': ''}, regex=True)
electionData['county'] = electionData['county'].replace({' Cty Townships': ''}, regex=True)
electionData['county'] = electionData['county'].replace({' City': ''}, regex=True)

m = electionData['state'] == 'Virginia'
electionData.loc[m, 'county'] = electionData.loc[m, 'county'].replace({' city': ''}, regex=True)

m = countyData['name'] == 'District of Columbia'
countyData.loc[m, 'state'] = 'District of Columbia'

m = countyData['state'] == 'Alaska'
countyData.loc[m, 'name'] = 'Alaska'

# countyData.to_csv(r'./data/output/countyData-d3.csv', index=False)
combineElectionState('District of Columbia', electionData)
combineElectionState('Alaska', electionData)
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
countyData = pd.merge(countyData, electionDataCounty, how='outer', left_on=['state', 'name'], right_on=['state', 'county'])

# Normalize election data:
normalized = []
for (a, b) in zip(countyData['DEM_votes'].astype("Float32"), countyData['REP_votes'].astype("Float32")):
    try:
        normalized.append(a / (a + b))
    except:
        normalized.append('')
countyData['normalized_election_outcome'] = normalized

countyData = countyData.drop_duplicates()
statedf = countyData[['state', 'state_id', 'DEM_votes', 'REP_votes']].copy(deep=True)

groups = statedf.groupby('state')
for state, data in groups:
    if state != 'Alaska':
        sumDem = data['DEM_votes'].sum()
        sumRep = data['REP_votes'].sum()

        statedf.loc[(statedf['state'] == state), 'REP_votes'] = str(sumRep)
        statedf.loc[(statedf['state'] == state), 'DEM_votes'] = str(sumDem)
stateData = statedf.drop_duplicates()
normalized = []
for (a, b) in zip(stateData['DEM_votes'].astype("Float32"), stateData['REP_votes'].astype("Float32")):
    try:
        normalized.append(a / (a + b))
    except:
        normalized.append('')
stateData['normalized_election_outcome'] = normalized

# Output:
countyData[['state', 'county', 'state_id', 'county_id', 'DEM_votes', 'REP_votes', 'normalized_election_outcome']].to_csv(r'./data/output/countyData.csv', index=False)
stateData.to_csv(r'./data/output/stateData.csv', index=False)