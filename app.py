import pandas as pd
import streamlit as st
import numpy as np
from sklearn.preprocessing import MinMaxScaler

st.markdown("<h1 style='text-align: center'>Eleven Stats Player Attribute System</h1>", unsafe_allow_html=True)
st.markdown('An internal Streamlit app for the usecase of showing and sharing the results of the Player Attribute System.')
st.markdown('The data is available for the top five leagues for the recent season i.e. 2021-2022' \
' with options to possession adjust attacking and defensive metrics.')
st.markdown('Final attribute scores are in the range of 0-100.')

leagues = ['Premier_League', 'LaLiga', 'Bundesliga', 'Serie_A', 'Ligue_1']
league_countries = ['EN', 'ES', 'DE', 'IT', 'FR']
league_dict = dict(zip(leagues, league_countries))
season = '2021-2022'

sample_df = pd.read_csv('data/LaLiga_ES_2021-2022_final_attribute_scores_attPossAdj=True_defPossAdj=True')

attribute_scores = list(sample_df.columns)[8:]

select_league = st.sidebar.selectbox(
      'Select League',
      leagues
)

select_attribute = st.sidebar.selectbox(
       'Select Attribute',
       attribute_scores
)

poss_adj_dict = {'Yes' : True, 'No' : False}
att_poss_adj = st.sidebar.radio(
    'Possession Adjust Attacking Attributes?',
    ('Yes', 'No')
)

def_poss_adj = st.sidebar.radio(
    'Possession Adjust Defensive Attributes?',
    ('Yes', 'No')
)

players_df = pd.read_csv(f'data/{select_league}_{league_dict[select_league]}_{season}_final_attribute_scores_'\
f'attPossAdj={poss_adj_dict[att_poss_adj]}_defPossAdj={poss_adj_dict[def_poss_adj]}')

players = players_df['player'].unique().tolist()
position_dict = {
    'Goalkeeper': ['Goalkeeper'],
    'Defenders' : ['Left Back', 'Right Back', 'Left Centre Back(3 at the back)',
                    'Left Centre Back', 'Right Centre Back', 'Centre Back', 'Left Back(5 at the back)',
                    'Left Wingback', 'Right Wingback'],
    'Midfielders': ['Left Centre Midfielder', 'Left Defensive Midfielder', 'Right Defensive Midfielder',
                     'Right Attacking Midfielder', 'Defensive Midfielder', 'Left Attacking Midfielder',
                      'Attacking Midfielder', 'Right Centre Midfielder'],
    'Forwards' : ['Striker', 'Right Attacking Midfielder', 'Left Attacking Midfielder', 'Attacking Midfielder',
                   'Attacking Midfielder', 'Left Winger', 'Right Winger', 'Left Wing Forward', 'Right Wing Forward']
}
players.insert(0, 'None')
positions = list(position_dict.keys())
positions.insert(0, 'None')
print(positions)

select_player = st.sidebar.selectbox(
     'See Scores For One Specific Player:',
     players
)

select_position = st.sidebar.selectbox(
      'Compare By Position Only:',
      positions
)


def output_data(league, attribute, att_poss_adj, def_poss_adj):
    # read data
    df = pd.read_csv(f'data/{league}_{league_dict[league]}_{season}_final_attribute_scores_'\
    f'attPossAdj={poss_adj_dict[att_poss_adj]}_defPossAdj={poss_adj_dict[def_poss_adj]}')
    # sort dataframe according to the attribute chosen
    if select_player != 'None':
        result_df = df[df['player'] == select_player][attribute_scores]
        result_df = result_df.T
        result_df.rename(columns={result_df.columns[0]: f'{select_player}'}, inplace = True)
    else:
        result_df = df[['player', 'position_1', attribute]].sort_values(attribute, ascending=False)
        result_df.reset_index(inplace=True, drop=True)

    if select_position != 'None':
        try:
            result_df = result_df[result_df['position_1'].isin(position_dict[select_position])]
        except:
            pass
        scaler = MinMaxScaler()
        try:
            result_df[attribute] = scaler.fit_transform(np.array(result_df[attribute]).reshape(-1, 1))
            result_df[attribute] = result_df[attribute].apply(lambda x: x*100)
        except:
            pass

    return result_df.head(50)

output_df = output_data(select_league, select_attribute, att_poss_adj, def_poss_adj)

if select_player != 'None':
    st.write(f"Showing all the attribute scores for <mark>{select_player}</mark>", unsafe_allow_html=True)
else:
    st.write(f"Showing the top 50 players who score the highest on <mark>{select_attribute}</mark> in {select_league}",
             unsafe_allow_html=True)
st.table(output_df)
