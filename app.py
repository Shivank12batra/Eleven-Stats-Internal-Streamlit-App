import pandas as pd
import streamlit as st

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

players = players_df['player'].tolist()
players.insert(0, 'None')

select_player = st.sidebar.selectbox(
     'See Scores For One Specific Player:',
     players
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
        result_df = df[['player', attribute]].sort_values(attribute, ascending=False)
        result_df.reset_index(inplace=True, drop=True)
        result_df = result_df.head(50)
    return result_df

output_df = output_data(select_league, select_attribute, att_poss_adj, def_poss_adj)

if select_player != 'None':
    st.write(f"Showing all the attribute scores for <mark>{select_player}</mark>", unsafe_allow_html=True)
else:
    st.write(f"Showing the top 50 players who score the highest on <mark>{select_attribute}</mark> in {select_league}",
             unsafe_allow_html=True)
st.table(output_df)
