import streamlit as st
from statsbombpy import sb
import pandas as pd
from mplsoccer import Pitch,VerticalPitch
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches 

#Page Setup
st.set_page_config(
    page_title="Plotball",
    page_icon="🧩",
)
st.title("PLOTBALL")
st.subheader("Check various visualisatons of your favorite stars✨")

#Selecting Competition

c = sb.competitions()

comps = c['competition_name'].unique().tolist()
comp_id = c['competition_id'].unique().tolist()

comp_to_id = dict(zip(comp_id,comps))


Comp = st.selectbox(
    "Select the competition to display stats of",
    (comps),
   placeholder="Select Competition")


for key, value in comp_to_id.items():
        if Comp == value:
            comp_id = key

comp_ = c[c['competition_name'] == Comp]

#Selecting Season
season_id = comp_['season_id'].unique().tolist()
season = comp_['season_name'].unique().tolist()
sidtos = dict(zip(season_id,season))
seas = []

        

season = st.selectbox(
    "Select the season to display stats of",
    (season))

for key, value in sidtos.items():
        if season == value:
               season_id = key

#Selecting Match

Match = sb.matches(competition_id=comp_id,season_id=season_id)
Match['Match'] = Match['home_team'] + ' V/S '+ Match['away_team']
Match_ = Match['Match'].unique().tolist()
Match_id = Match['match_id'].unique().tolist()
mid_to_m =dict(zip(Match_id,Match_))

Match = st.selectbox(
    "Select the Match to display stats of",
    (Match_))

for key, value in mid_to_m.items():
        if Match == value:
               Match_id = key



df = sb.events(match_id = Match_id)

c.columns = c.columns.str.replace(' ', '_')



#Making Lists

players = df['player'].unique().tolist()
players = players[1:]

players_id = df['player_id'].unique().tolist()
players_id = players_id[1:]

team_id = df['team_id'].unique().tolist()
team = df['team'].unique().tolist()




player_to_id = dict(zip(players_id,players))
team_to_id = dict(zip(team_id,team))

#Getting Score
@st.cache_data
def Game_Score(Match_ID):
    match_df = sb.events(match_id = Match_ID)
    match_df = match_df[match_df['minute'] < 120 ]
    team1 = match_df.team_id.unique().tolist()[0]
    team2 = match_df.team_id.unique().tolist()[1]
    team1_score = match_df[(match_df['shot_outcome'] == 'Goal') & (match_df['team_id'] == team1)]
    team2_score = match_df[(match_df['shot_outcome'] == 'Goal') & (match_df['team_id'] == team2)]
    score = f"( {team1_score.shape[0]} - {team2_score.shape[0]} )" 
    return score



#Displaying Selection Bars
a = st.subheader(f"{Match} {Game_Score(Match_id)}")



player = st.selectbox(
    "Select the player you want to see stats of",
    (players))
stat = st.selectbox(
    "Select the stat you want to see",
    (['Pass Map','Shot Map']))

for key, value in player_to_id.items():
        if player == value:
            player_id = key
for key, value in team_to_id.items():
        if team == value:
            team_id = key
        else:
             opp = value


def Download_image(img):
    st.download_button(label = "Download Plot",data = img,mime="image/png")


@st.cache_data(experimental_allow_widgets=True)
def pass_map(Match_ID,P_ID):
    match_df1 = sb.events(match_id = Match_ID)
    match_df1 = match_df1[(match_df1['type'] == 'Pass') & (match_df1['player_id']>0)]

    l = match_df1['player'].unique().tolist()
    k = match_df1['player_id'].unique().tolist()
    m= dict(zip(l,k))
    z = pd.DataFrame(list(m.items()), columns=['Player', 'Player_ID'])
    
    edf = match_df1[(match_df1['player_id'] == P_ID )& (match_df1['type'] == 'Pass')]
    edf[['x_start','y_start']] = pd.DataFrame(edf.location.tolist(),index = edf.index)
    edf[['x_end','y_end']] = pd.DataFrame(edf.pass_end_location.tolist(),index = edf.index)

    edff = edf[edf['x_start'] - edf['x_end'] >= 0]
    edfb = edf[edf['x_start'] - edf['x_end'] < 0]
    assists = edf[edf['pass_goal_assist'] == True]
    




    P = Pitch(pitch_type = 'statsbomb')
    fig,ax = P.draw(figsize = (8,8))



    P.scatter(x = edfb['x_start'],y = edfb['y_start'],ax = ax,c = 'b')
    P.lines(xstart = edfb['x_start'],ystart = edfb['y_start'],xend = edfb['x_end'],yend = edfb['y_end'],ax = ax,comet = True,color = 'g')
   
    P.scatter(x = edff['x_start'],y = edff['y_start'],ax = ax,c = 'b')
    P.lines(xstart = edff['x_start'],ystart = edff['y_start'],xend = edff['x_end'],yend = edff['y_end'],ax = ax,comet = True,color = 'r')

    P.scatter(x = assists['x_start'],y = assists['y_start'],ax = ax,c = 'b',marker = 'D')
    P.lines(xstart = assists['x_start'],ystart = assists['y_start'],xend = assists['x_end'],yend = assists['y_end'],ax = ax,comet = True,color = 'y')

    patch1 = mpatches.Patch(color='green', label='Forward Passes')
    patch2 = mpatches.Patch(color='red', label='Backward Passes')
    patch3 = mpatches.Patch(color='yellow', label='Assist') 
    plt.legend(handles=([patch1,patch2,patch3])) 

    ax_title = ax.set_title(f"Pass Map of {player} ({edf.shape[0]} passes)\n Forward Passes --> {edfb.shape[0]} \n Backward Passes --> {edff.shape[0]}\n Assists --> {assists.shape[0]}",fontsize=15)



    fig.savefig("Pass_Plots")
    img = st.image('Pass_Plots.png')
    Download_image(img)

@st.cache_data
def ShotMap(Match_ID,P_ID):
    match_df2 = sb.events(match_id = Match_ID)
    sdf = match_df2[match_df2['type'] == 'Shot']
    sdf = sdf[sdf['player_id'] == P_ID]
    sdf = sdf[sdf['minute'] < 120]
    edf_g = sdf[sdf['shot_outcome'] == 'Goal']
    edf_ng = sdf[sdf['shot_outcome'] != 'Goal']

    p = VerticalPitch(half=True)
    
    fig,ax = p.draw()

    if sdf.shape[0] > 0:
        sdf[['x_start','y_start']] = pd.DataFrame(sdf.location.tolist(),index = sdf.index)
        edf_g = sdf[sdf['shot_outcome'] == 'Goal']
        edf_ng = sdf[sdf['shot_outcome'] != 'Goal']
        
        p.scatter(edf_ng['x_start'],edf_ng['y_start'],hatch = '//',marker = 'o',ax = ax,color = 'red')
        p.scatter(edf_g['x_start'],edf_g['y_start'],marker = 'football',ax = ax,c = 'white')
         

    ax.text(x=40, y=80, s=f'Shots --> {sdf.shape[0]} \n Goals --> {edf_g.shape[0]} \n xGoals --> {sdf.shot_statsbomb_xg.sum()}',
            size=10,
            color='Red',
            va='center', ha='center')
    fig.savefig("Shot_Map")
    img = st.image('Shot_Map.png')
    Download_image(img)
     
def main():
     if stat == 'Pass Map':
        pass_map(Match_id,player_id)

     if stat == 'Shot Map':
        ShotMap(Match_id,player_id)


main()
