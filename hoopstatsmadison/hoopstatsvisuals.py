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
        else:
            raise Exception('Must have at least one argument specified.')
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

    def shot_chart_dope(self, team='', home_team='', visiting_team='', player='', kind='kde'):
        self.team = team
        self.home_team = home_team
        self.visiting_team = visiting_team
        self.player = player
        dat = self.get_dat()
        cleaned_dat = self.clean_dat(dat)

        # Creating shot chart
        # Join Map
        cmap = plt.cm.viridis

        # n_levels sets the number of contour lines for the main kde plot
        joint_shot_chart = sns.jointplot(cleaned_dat['LOC_X'], cleaned_dat['LOC_Y'], stat_func=None,
                                         kind=kind, space=0.01, color=cmap(.1),
                                         cmap=cmap, n_levels=35)

        #joint_shot_chart.fig.set_size_inches(12, 11)

        # A joint plot has 3 Axes, the first one called ax_joint
        # is the one we want to draw our court onto and adjust some other settings
        ax = joint_shot_chart.ax_joint
        draw_court(ax)
        ax.set_xlim(-250, 250)
        ax.set_ylim(370, -47.50)
        ax.tick_params(labelbottom=False, labelleft=False)
        plt.xlabel('')
        plt.ylabel('')
        plt.legend().remove()
        plt.title('{} {} {} {}'.format(self.player, self.team,
                                       self.home_team, self.visiting_team), fontsize=30)
        plt.show()


