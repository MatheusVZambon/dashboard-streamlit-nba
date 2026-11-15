# Importação das bibliotecas necessárias
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import os
import numpy as np

# Atribuição dos csvs em dataframes
dfPlayers = pd.read_csv("datasets/playerStats.CSV")
dfTeams = pd.read_csv("datasets/teamStats.CSV")
dfShots = pd.read_csv("datasets/NBA_2025_Shots.csv")

# Ajustes nas tabelas
dfTeams = dfTeams.drop(columns=['Unnamed: 18','Unnamed: 23','Unnamed: 28'])

# Testes
#print("Arquivo iniciado")
#print(dfTeams.head())
#print(dfTeams.columns.tolist())
#print(dfTeams["TeamShort"].tolist())

percentColumns = ["FG%","3P%","2P%","eFG%","FT%"]
dfPlayers[percentColumns] = dfPlayers[percentColumns].fillna(0.0).astype(float)

# Testes para limpeza de dados

#print("JOGADORES")
#print(dfPlayers.shape)
#print(dfPlayers.columns.tolist())
#print(dfPlayers.info())

#print("TIMES")
#print(dfTeams.shape)
#print(dfTeams.columns.tolist())
#print(dfTeams.info())

#print("Valores ausentes")
#print(dfTeams.isnull().sum())
#print(dfPlayers.isnull().sum())

#print("Linhas duplicadas")
#print(dfTeams.duplicated().sum())
#print(dfPlayers.duplicated().sum())

# Streamlit

# Configuração de página inicial para carrossel
if "pageView" not in st.session_state:
      st.session_state.pageView = 0

# Configuração inicial de página
st.set_page_config(
    page_title="Visualização - NBA",
    page_icon="⛹️‍♂️",
    layout="wide"
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100..900;1,100..900&family=Sansation:ital,wght@0,300;0,400;0,700;1,300;1,400;1,700&display=swap');
        .stMainBlockContainer{
            padding: 0,0,0,0;
        }
        div.stButton > button {
            background-color: transparent;
            border: none;
            box-shadow: none;
            padding: 0;
            min-height: 0;
        }
        div.stButton > button:hover{
            background-color: transparent;
            border: none;
        }
        *{
            font-family: 'Sansation', sans-serif;
        }
        .stMarkdown p{
            font-size: 20px;
            font-family: 'Sansation', sans-serif;
        }
        .nba-table {
            width: 100%;
            border-collapse: collapse;
            font-family: 'Sansation', sans-serif;
            font-size: 18px;
            text-align: justify;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Paletas de cores personalizadas
paletas = {
    "BOS": ["#007A33", "#F8DEAE"],
    "LAL": ["#552583", "#FDB927"],
    "GSW": ["#1D428A", "#FFC72C"],
    "CHI": ["#CE1141", "#FFFFFF"],
    "MIA": ["#98002E", "#F9A01B"],
    "NYK": ["#006BB6", "#F58426"],
    "BRK": ["#000000", "#FFFFFF"],
    "PHI": ["#006BB6", "#F1E3E7"],
    "MIL": ["#00471B", "#EEE1C6"],
    "DEN": ["#0E2240", "#FEC524"],
    "DAL": ["#00538C", "#B8C4CA"],
    "PHO": ["#1D1160", "#E56020"],
    "ATL": ["#E03A3E", "#FFFFFF"],
    "CLE": ["#860038", "#FDBB30"],
    "TOR": ["#CE1141", "#000000"],
    "SAC": ["#5A2D81", "#FAFAFA"],
    "HOU": ["#CE1141", "#000000"],
    "MEM": ["#5D76A9", "#12173F"],
    "NOP": ["#0C2340", "#C8102E"],
    "OKC": ["#007AC1", "#FFE600"],
    "MIN": ["#0C2340", "#78BE20"],
    "POR": ["#E03A3E", "#000000"],
    "UTA": ["#002B5C", "#F9A01B"],
    "WAS": ["#002B5C", "#E31837"],
    "ORL": ["#0077C0", "#C4CED4"],
    "CHO": ["#30C8E2", "#1D1160"],
    "DET": ["#F05670", "#0028AD"],
    "IND": ["#002D62", "#FDBB30"],
    "LAC": ["#EB5555", "#1D428A"],
    "SAS": ["#4C576D", "#FFFFFF"]
}

fixedCol, rotateCol = st.columns([1,2])

dfTeams = dfTeams.sort_values("Team")

selectedTeam = ""

with fixedCol:
    selectedTeam = st.selectbox(
        "Selecione o time",
        dfTeams["TeamShort"],
        # Transformar sigla
        format_func=lambda time: dfTeams.loc[
            dfTeams["TeamShort"] == time, "Team"
        ].iloc[0],
        index=0
    )

    primaryColor, secondaryColor = paletas[selectedTeam]
    hoverColor = primaryColor + "80"

    st.markdown(
        f"""
        <style>
            .nba-table th {{
                background-color: {primaryColor};
                color: {secondaryColor};
                padding: 12px;
                font-weight: bold;
                font-size:20px;
                border-bottom: 2px solid {secondaryColor};
                text-align: justify;
            }}
            .nba-table td {{
                background-color: {primaryColor};
                color: {secondaryColor};
                padding: 12px;
                border-bottom: 1px solid {secondaryColor};
            }}

            .nba-table tr:hover td {{
                background-color: {hoverColor};
            }}

            .st-key-fixedCol .stMarkdown p{{
                width: 100%;
                border: 2px solid {primaryColor};
                border-radius: 7px;
                background-color: {secondaryColor};
                color: {primaryColor};
                font-size: 32px;
                font-weight: bold;
                padding: 5px 10px;
            }}

            .stMarkdown p{{
                width: 100%;
                border: 2px solid {primaryColor};
                border-radius: 7px;
                background-color: {secondaryColor};
                color: {primaryColor};
                font-size: 20px;
                font-weight: bold;
                padding: 5px 10px;
            }}

            .st-key-fixedCol [data-testid="stVerticalBlock"] {{
                gap: 8px;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
            .st-key-fixedCol [data-testid="stMarkdownContainer"] {
                width: 100%;
            }
            .st-key-fixedCol {
                text-align: center;
                display: flex;
                justify-content: center;
                align-items: center; 
            }
            .legenda {
                text-align:center;
                border: none !important;
                color: {primaryColor} !important;
                font-size: 16px !important;
                font-weight: normal !important;
                padding: 0 !important;
                margin-bottom: -3px;
                background-color: transparent !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    logoPath = os.path.join("./media/logos/",f"{selectedTeam}.png")
    with st.container(key="fixedCol"):
        st.image(
            image=logoPath,
            width="content"
        )
        st.caption(
            body=dfTeams.loc[dfTeams["TeamShort"] == selectedTeam, "Team"].iloc[0],
            width="stretch",
            text_alignment="center"
        )
        st.caption(
            body=dfTeams.loc[dfTeams["TeamShort"] == selectedTeam, "City"].iloc[0] + "," + dfTeams.loc[dfTeams["TeamShort"] == selectedTeam, "ST"].iloc[0],
            width="stretch",
            text_alignment="center"
        )
    columnConf, columnDiv = st.columns(2)
    with columnConf:
        st.markdown("""<p class="legenda">Conferência</p>""", unsafe_allow_html=True)
        st.caption(
            dfTeams.loc[dfTeams["TeamShort"] == selectedTeam, "Conf"].iloc[0],
            width="stretch",
            text_alignment="center"
        )
    with columnDiv:
        st.markdown("""<p class="legenda">Divisão</p>""", unsafe_allow_html=True)
        st.caption(
            dfTeams.loc[dfTeams["TeamShort"] == selectedTeam, "Div"].iloc[0],
            width="stretch",
            text_alignment="center"
        )
    with st.container():
        st.markdown("""<p class="legenda">Arena</p>""", unsafe_allow_html=True)
        st.caption(
            dfTeams.loc[dfTeams["TeamShort"] == selectedTeam, "Arena"].iloc[0],
            width="stretch",
            text_alignment="center"
        )
    with st.container():
        st.markdown("""<p class="legenda">Vitórias/Derrotas</p>""", unsafe_allow_html=True)
        st.caption(
            body=str(dfTeams.loc[dfTeams["TeamShort"] == selectedTeam, "W"].iloc[0]) + "/" + str(dfTeams.loc[dfTeams["TeamShort"] == selectedTeam, "L"].iloc[0]),
            width="stretch",
            text_alignment="center"
        )
        st.markdown("""<p class="legenda">Títulos</p>""", unsafe_allow_html=True)
        st.caption(
            body=dfTeams.loc[dfTeams["TeamShort"] == selectedTeam, "Championships"].iloc[0],
            width="stretch",
            text_alignment="center"
        )


# Definição das estatísticas escolhidas
teamPlayers = dfPlayers[dfPlayers["Team"] == selectedTeam]

topPoints = teamPlayers.nlargest(5,"PTS")[["Player","PTS"]]
topRebounds = teamPlayers.nlargest(5,"TRB")[["Player","TRB"]]
topAssists = teamPlayers.nlargest(5,"AST")[["Player","AST"]]
topSteals = teamPlayers.nlargest(5,"STL")[["Player","STL"]]
topBlocks = teamPlayers.nlargest(5,"BLK")[["Player","BLK"]]
topMinutes = teamPlayers.nlargest(5,"MP")[["Player","MP"]]
topFG = teamPlayers.nlargest(5,"FG%")[["Player","FG%"]] 
top3FG = teamPlayers.nlargest(5,"3P%")[["Player","3P%"]] 

teamDRTG = dfTeams.loc[dfTeams["TeamShort"] == selectedTeam, "DRtg"].iloc[0]
teamORTG = dfTeams.loc[dfTeams["TeamShort"] == selectedTeam, "ORtg"].iloc[0]
teamNRTG = dfTeams.loc[dfTeams["TeamShort"] == selectedTeam, "NRtg"].iloc[0]
teamPace = dfTeams.loc[dfTeams["TeamShort"] == selectedTeam, "Pace"].iloc[0]
teamDRTGPos = int(dfTeams["DRtg"].rank(ascending=False,method="min").loc[dfTeams["TeamShort"] == selectedTeam].iloc[0])
teamORTGPos = int(dfTeams["ORtg"].rank(ascending=False,method="min").loc[dfTeams["TeamShort"] == selectedTeam].iloc[0])
teamNRTGPos = int(dfTeams["NRtg"].rank(ascending=False,method="min").loc[dfTeams["TeamShort"] == selectedTeam].iloc[0])
teamPacePos = int(dfTeams["Pace"].rank(ascending=False,method="min").loc[dfTeams["TeamShort"] == selectedTeam].iloc[0])
teamAge = dfTeams.loc[dfTeams["TeamShort"] == selectedTeam, "Age"].iloc[0]
teamWins = dfTeams.loc[dfTeams["TeamShort"] == selectedTeam, "W"].iloc[0]
teamLosses = dfTeams.loc[dfTeams["TeamShort"] == selectedTeam, "L"].iloc[0]
teamArena = dfTeams.loc[dfTeams["TeamShort"] == selectedTeam, "Arena"].iloc[0]
teamCity = dfTeams.loc[dfTeams["TeamShort"] == selectedTeam, "City"].iloc[0]
teamState = dfTeams.loc[dfTeams["TeamShort"] == selectedTeam, "ST"].iloc[0]
teamDiv = dfTeams.loc[dfTeams["TeamShort"] == selectedTeam, "Div"].iloc[0]
teamConf = dfTeams.loc[dfTeams["TeamShort"] == selectedTeam, "Conf"].iloc[0]
teamTitles = dfTeams.loc[dfTeams["TeamShort"] == selectedTeam, "Championships"].iloc[0]

# Função para mostrar as tabelas de estatísticas
def showStatsTable(data):
    st.markdown(
        data.to_html(index=False, classes="nba-table", border=0),
        unsafe_allow_html = True
    )

with rotateCol:
    if st.session_state.pageView == 0:
        col1,col2 = st.columns(2)
        col3,col4 = st.columns(2)

        with col1:
            st.subheader("Pontos por jogo")
            topPoints = topPoints.rename(columns={"Player":"Jogador"})
            showStatsTable(topPoints)
        with col2:
            st.subheader("Rebotes por jogo")
            topRebounds = topRebounds.rename(columns={"Player":"Jogador"})
            showStatsTable(topRebounds)
        with col3:
            st.subheader("Assistências por jogo")
            topAssists = topAssists.rename(columns={"Player":"Jogador"})
            showStatsTable(topAssists)
        with col4:
            st.subheader("Minutos por jogo")
            topMinutes = topMinutes.rename(columns={"Player":"Jogador"})
            showStatsTable(topMinutes)

    elif st.session_state.pageView == 1:
        col5,col6 = st.columns(2)
        col7,col8 = st.columns(2)

        with col5:
            st.subheader("Roubadas de bola por jogo")
            topSteals = topSteals.rename(columns={"Player":"Jogador"})
            showStatsTable(topSteals)
        with col6:
            st.subheader("Tocos por jogo")
            topBlocks = topBlocks.rename(columns={"Player":"Jogador"})
            showStatsTable(topBlocks)
        with col7:
            st.subheader("Melhores aproveitamentos de arremesso")
            topFG = topFG.rename(columns={"Player":"Jogador"})
            topFG["FG%"] = (topFG["FG%"] * 100).map(lambda x: f"{x:.1f}%")
            showStatsTable(topFG)
        with col8:
            st.subheader("Melhores arremessadores para 3pt")
            top3FG = top3FG.rename(columns={"Player":"Jogador"})
            top3FG["3P%"] = (top3FG["3P%"] * 100).map(lambda x: f"{x:.1f}%")
            showStatsTable(top3FG)

    elif st.session_state.pageView == 2:
            col9,col10 = st.columns(2)
            col11,col12 = st.columns(2)
    
            with col9:
                with st.container(key="ORTG"):
                    st.subheader("Rating Ofensivo")
                    st.caption(teamORTG)
                    st.caption(f"{teamORTGPos}º na liga")
            with col10:
                with st.container(key="DRTG"):
                    st.subheader("Rating Defensivo")
                    st.caption(teamDRTG)
                    st.caption(f"{teamDRTGPos}º na liga")
            with col11:
                with st.container(key="NRTG"):
                    st.subheader("Net Rating")
                    st.caption(teamNRTG)
                    st.caption(f"{teamNRTGPos}º na liga")
            with col12:
                with st.container(key="Pace"):
                    st.subheader("Pace")
                    st.caption(teamPace)
                    st.caption(f"{teamPacePos}º na liga")

                st.markdown("""
                    <style>
                    .st-key-ORTG .stMarkdown p, .st-key-DRTG .stMarkdown p, .st-key-NRTG .stMarkdown p, .st-key-Pace .stMarkdown p{
                        text-align: center;
                        font-size: 28px;
                        font-weight: bold;
                    }
                    </style>
                    """, unsafe_allow_html=True
                )

    elif st.session_state.pageView == 3:
            #col13 = st.columns(1)

            with st.container():
                # Seleções de time e jogador pro shotchart
                #teams = sorted(dfShots["TEAM_NAME"].unique())
                fullSelectedTeam = dfTeams.loc[dfTeams["TeamShort"] == selectedTeam,"Team"].iloc[0]
                #selectedTeam = st.selectbox("Selecione o time", teams)
                players = sorted(dfShots[dfShots["TEAM_NAME"] == fullSelectedTeam]["PLAYER_NAME"].unique())

                selectedPlayer = st.selectbox("Selecione o jogador", players)

                playerShots = dfShots[(dfShots["TEAM_NAME"] == fullSelectedTeam) & (dfShots["PLAYER_NAME"] == selectedPlayer)]

                playerShots = playerShots.copy()
                playerShots["RES"] = playerShots["SHOT_MADE"].map({True:"Convertido",False:"Errado"})

                # Esquematização dos dados
                fig = px.scatter(
                        playerShots,
                        x="LOC_X",
                        y="LOC_Y",
                        color="RES",
                        color_discrete_map={
                            "Convertido": "green",
                            "Errado": "red"
                        },
                        hover_data=["SHOT_DISTANCE"],
                        title=f"Arremessos de {selectedPlayer}"
                )

                # Linha de 3 pts
                x = np.linspace(-22, 22, 200)
                y = 5.25 + np.sqrt(23.75**2 - x**2)

                fig.add_trace(go.Scatter(
                    x=x,
                    y=y,
                    mode="lines",
                    line=dict(color="black", width=2),
                    showlegend=False
                ))
                # Inversão para design de meia-quadra
                fig.update_layout(
                    height=700,
                    showlegend=False,
                    xaxis=dict(
                        range=[-26, 26],
                        showgrid=False,
                        title="",
                        showticklabels=False,
                        zeroline=False
                    ),
                    yaxis=dict(
                        range=[-0.25, 43],
                        showgrid=False,
                        zeroline=False,
                        title="",
                        showticklabels=False,
                        scaleanchor="x",
                        scaleratio=1
                    )
                )
                # Desenho da meia-quadra
                fig.add_shape(
                    type="rect",
                    x0=-25, y0=-0.25,
                    x1=25, y1=42.75,
                    line=dict(color="black", width=2)
                )

                fig.add_shape(
                    type="rect",
                    x0=-8, y0=-5.25,
                    x1=8, y1=14,
                    line=dict(color="black", width=2)
                )

                fig.add_shape(
                    type="circle",
                    x0=-6, y0=8,
                    x1=6, y1=20,
                    line=dict(color="black", width=2)
                )

                fig.add_shape(
                    type="circle",
                    x0=-2, y0=0.25,
                    x1=2, y1=4.25,
                    line=dict(color="black", width=2)
                )

                fig.add_shape(
                    type="line",
                    x0=-3, y0=-4,
                    x1=3, y1=-4,
                    line=dict(color="black", width=2)
                )
                fig.add_shape(
                    type="line",
                    x0=-22, y0=0,
                    x1=-22, y1=14.17,
                    line=dict(color="black", width=2)
                )

                fig.add_shape(
                    type="line",
                    x0=22, y0=0,
                    x1=22, y1=14.17,
                    line=dict(color="black", width=2)
                )

                st.plotly_chart(fig, use_container_width=True)

    rotatePages = ["Main Stats","Hustle Stats","Team Stats","Shot Chart"]
    columns = st.columns([1,1,1,1,1])
    
    with columns[1]:
        if st.button("●" if st.session_state.pageView == 0 else "o", key="page0", width=45):
            st.session_state.pageView = 0
            st.rerun()

    with columns[2]:
        if st.button("●" if st.session_state.pageView == 1 else "o", key="page1", width=45):
            st.session_state.pageView = 1
            st.rerun()

    with columns[3]:
        if st.button("●" if st.session_state.pageView == 2 else "o", key="page2", width=45):
            st.session_state.pageView = 2
            st.rerun()

    with columns[4]:
        if st.button("●" if st.session_state.pageView == 3 else "o", key="page3", width=45):
            st.session_state.pageView = 3
            st.rerun()

