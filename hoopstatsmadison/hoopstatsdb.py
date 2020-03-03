# Loading modules
import pandas as pd
import sqlite3

# Event type reference data frame
ZTYPE = [x for x in range(26)]
ZTYPE.append(100)
DESC = ["MADE_2","MADE_3","MADE_FT","MISSED_2","MISSED_3","MISSED_FT","ASSIST","OFF_REBOUND",
"DEF_REBOUND","BLOCK","TURNOVER","STEAL","TIMEOUT","OFF_FOUL","DEF_FOUL","TEC_FOUL","SUB_IN","SUB_OUT",
"REC_OFF_FOUL","REC_DEF_FOUL","DEFLECT","TECH_1","TECH_2","CUST_1","CUST_2","POSSESSION","TIMEOUT30"]
GROUP = ["shot", "shot", "shot", "shot", "shot", "shot", "assist", "rebound", "rebound", "block", "turnover",
 "steal", "timeout", "foul", "foul", "foul", "sub", "sub", "rec_foul", "rec_foul",
 "deflection", "tech", "tech", "cust", "cust", "possession", "timeout"]
type_df = pd.DataFrame({'ZTYPE':ZTYPE, "DESC": DESC, "GROUP": GROUP})

# Creating class


class HoopStatsDB:

    def __init__(self):
        self.conn = ''
        self.player = ''
        self.team = ""
        self.home_team = ''
        self.visiting_team = ''
        self.teams = []
        self.players = []
        self.full_ref = []
        self.game = ''
        self.date = ""
        self.play_type_ref = type_df
        self.query_df = (
            "SELECT ZTEAM.ZNAME AS TEAM, ZHOME, ZVISITORS, ZGAME, ZPLAYER.ZNAME AS PLAYERNAME, \n"
            "ZEVENT.ZTYPE, ZLOCATIONX, ZLOCATIONY, ZEVENT.ZPERIOD, ZTIMESTRING\n"
            "FROM ZTEAM\n"
            "LEFT JOIN ZEVENT ON ZTEAM.Z_PK = ZEVENT.ZTEAM\n"
            "LEFT JOIN ZPLAYER ON ZPLAYER.Z_PK = ZEVENT.ZPLAYER\n"
            "LEFT JOIN ZGAME ON ZGAME.Z_PK = ZEVENT.ZGAME")
        self.query_ref = (
            "SELECT DISTINCT ZTEAM.Z_PK, ZTEAM.ZNAME AS TEAM, ZPLAYER.ZNAME AS PLAYERNAME \n"
            "FROM ZTEAM\n"
            "LEFT JOIN ZEVENT ON ZTEAM.Z_PK = ZEVENT.ZTEAM\n"
            "LEFT JOIN ZPLAYER ON ZPLAYER.Z_PK = ZEVENT.ZPLAYER")

    def connect(self, sqlite_db):
        self.conn = sqlite3.connect(sqlite_db)
        self.teams = self.team_ref()
        self.players = self.player_ref('all').iloc[:,2]
        self.full_ref = self.player_ref('all')

    def join_play_type(self, df, play_type):
        df2 = pd.merge(df, self.play_type_ref, how='left', on='ZTYPE')
        if play_type == 'shots':
            return df2[df2['ZTYPE'].isin([0,1,3,4])]
        elif play_type == 'all':
            return df2

    def player_ref(self, team_name='Madison Varsity 19-20'):
        self.team = team_name
        if team_name == 'all':
            return pd.read_sql_query(self.query_ref, self.conn)
        else:
            player_ref_query = self.query_ref + "\nWHERE ZTEAM.ZNAME = \"{}\"".format(self.team)
            player_name_ref = pd.read_sql_query(player_ref_query, self.conn).iloc[:,1:]
            return player_name_ref

    def team_ref(self):
        team_name_query = "SELECT DISTINCT ZNAME FROM ZTEAM ORDER BY ZNAME"
        team_name_df = pd.read_sql_query(team_name_query, self.conn)
        return team_name_df

    def team_df(self, team_name, play_type='shots'):
        self.team = team_name
        team_query = self.query_df + "\nWHERE ZTEAM.ZNAME = \"{}\";".format(self.team)
        team_df = pd.read_sql_query(team_query, self.conn)
        team_df_merged = self.join_play_type(team_df, play_type=play_type)
        return team_df_merged

    def play_by_play(self, home_team='Madison Varsity 19-20', visiting_team='', player='', play_type='shots'):
        self.player = player
        self.home_team = home_team
        self.visiting_team = visiting_team
        if self.home_team != '':
            home_team = self.full_ref[self.full_ref['TEAM'] == home_team].iloc[0,0]
        if self.visiting_team != '':
            visiting_team = self.full_ref[self.full_ref['TEAM'] == visiting_team].iloc[0,0]
        play_query = self.query_df + "\nWHERE ZHOME LIKE \"%{}%\" AND ZVISITORS LIKE \"%{}%\" AND " \
                                     "ZPLAYER.ZNAME LIKE \"%{}%\"".format(home_team, visiting_team, self.player) + \
                     "\nORDER BY ZGAME, ZEVENT.ZPERIOD, ZTIMESTRING DESC;"
        play_df = pd.read_sql_query(play_query, self.conn)
        play_df_merged = self.join_play_type(play_df, play_type=play_type)
        return play_df_merged



