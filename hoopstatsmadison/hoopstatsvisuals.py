# Importing modules
import matplotlib.pyplot as plt
from .hoopstatsdb import HoopStatsDB
from .drawcourt import draw_court
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns


class HoopStatsVisuals(HoopStatsDB):

    def __init__(self):
        super().__init__()

    def get_dat(self):
        if self.team != '':
            dat = self.team_df(team_name=self.team)
        elif self.home_team != '' or self.visiting_team != '' or self.player != '':
            dat = self.play_by_play(home_team=self.home_team, visiting_team=self.visiting_team, player=self.player)
        return dat

    def clean_dat(self, data):
        # Scaling data to fit the coordinates of the court.
        min_max_x = MinMaxScaler(feature_range=(-233, 233))
        data['LOC_X'] = min_max_x.fit_transform(data[['ZLOCATIONX']])
        min_max_y = MinMaxScaler(feature_range=(-47.5, 290))
        data['LOC_Y'] = min_max_y.fit_transform(data[['ZLOCATIONY']])
        return data

    def shot_chart(self, team='', home_team='', visiting_team='', player=''):
        self.team = team
        self.home_team = home_team
        self.visiting_team = visiting_team
        self.player = player
        dat = self.get_dat()
        cleaned_dat = self.clean_dat(dat)

        # Creating shot chart
        sns.set_style("dark")
        sns.set_color_codes()
        plt.figure(figsize=(12, 11))
        draw_court(outer_lines=True)
        sns.scatterplot(data=cleaned_dat, x='LOC_X', y='LOC_Y', hue='DESC', s=150, alpha=.5,
                        palette=dict(MISSED_2='red', MISSED_3='red', MADE_3='limegreen', MADE_2='limegreen'))
        plt.xlim(-250, 250)
        plt.ylim(422.5, -47.50)
        plt.tick_params(labelbottom=False, labelleft=False)
        plt.xlabel('')
        plt.ylabel('')
        plt.legend().remove()
        plt.title('{} {} {} {}'.format(self.player, self.team,
                                       self.home_team, self.visiting_team), fontsize=30)
        plt.show()

    def shot_chart_dope(self, player, team, home_team, visiting_team, kind='kde'):
        pass


