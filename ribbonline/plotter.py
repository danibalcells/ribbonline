import logging
import datetime
import os
from functools import partial

import matplotlib.pyplot as plt
import numpy as np
from bokeh import events
from bokeh.plotting import figure, output_file, show
from bokeh.models import tools, Range1d, Legend, CustomJS, ColumnDataSource
from bokeh.models.glyphs import Patch
from bokeh.models.annotations import Title
from bokeh.resources import CDN
from bokeh.embed import file_html

from . import constants, event


TITLE = 'Exploring the Emoji Divide in Catalonia'
COLOR_RIBBON_IN_TEXT = '#f2ce1a'
COLOR_RIBBON_IN_USERNAME = '#ffe251'
COLOR_FLAG_IN_USERNAME = '#f96d6d'
COLOR_FLAG_IN_TEXT = '#db0d0d'
COLOR_BACKGROUND = '#242424'
COLOR_EVENTS = '#bababa'
PLOT_WIDTH = 655
PLOT_HEIGHT = 600
LINE_WIDTH = 2
LEGEND_RIBBON_IN_TEXT = f'{constants.EMOJI_RIBBON} in tweet text'
LEGEND_RIBBON_IN_USERNAME = f'{constants.EMOJI_RIBBON} in username'
LEGEND_FLAG_IN_USERNAME = f'{constants.EMOJI_FLAG} in username'
LEGEND_FLAG_IN_TEXT = f'{constants.EMOJI_FLAG} in tweet text'
NAME_RIBBON_IN_TEXT = 'ribbon_in_text'
NAME_RIBBON_IN_USERNAME = 'ribbon_in_username'
NAME_FLAG_IN_USERNAME = 'flag_in_username'
NAME_FLAG_IN_TEXT = 'flag_in_text'
NAME_EVENTS = 'events'
NAME_EVENTS_RIGHT = 'events_right'
NAME_EVENTS_LEFT = 'events_left'
INITIAL_START_DATE = datetime.datetime(2017, 9, 1)
INITIAL_END_DATE = datetime.datetime(2017, 11, 1)


FIGURE = None


class TimelinePlotter(object):

    def __init__(self, timeline):
        self.timeline = timeline
        self.dates = np.array(timeline.dates)
        self.opinions = np.array([
            opinion.list for opinion in self.timeline.opinions])
        self._set_height()
        self._set_values()
        self._set_positions()
        self._set_labels()
        self._set_daily_totals()
        self.vis_generated = False

    @property
    def opinions_array(self):
        return

    def _set_height(self):
        daily_sums = self.opinions.sum(axis=1)
        N = len(daily_sums)
        max_sum = np.max(daily_sums)
        self.height = int(np.round(max_sum*1.1))

    def _set_values(self):
        self.ribbon_in_text_val = self.opinions[:,0]
        self.ribbon_in_username_val = self.opinions[:,1]
        self.flag_in_username_val = self.opinions[:,2]
        self.flag_in_text_val = self.opinions[:,3]
        self.neutral_val = (self.height -
                            self.ribbon_in_text_val -
                            self.ribbon_in_username_val -
                            self.flag_in_username_val -
                            self.flag_in_text_val)

    def _set_positions(self):
        self.ribbon_in_text_pos = self.ribbon_in_text_val
        self.ribbon_in_username_pos = (self.ribbon_in_text_pos +
                                       self.ribbon_in_username_val)
        self.neutral_pos = self.ribbon_in_username_pos + self.neutral_val
        self.flag_in_username_pos = (self.neutral_pos +
                                     self.flag_in_username_val)
        self.flag_in_text_pos = (self.flag_in_username_pos +
                                 self.flag_in_text_val)
        self._set_events_pos()

    def _set_labels(self):
        tweet_samples = self.timeline.sample_tweets()
        self.date_labels = [d.strftime('%b %d, %Y') for d in self.dates]
        self.ribbon_in_text_texts = []
        self.ribbon_in_text_usernames = []
        self.ribbon_in_username_texts = []
        self.ribbon_in_username_usernames = []
        self.flag_in_text_texts = []
        self.flag_in_text_usernames = []
        self.flag_in_username_texts = []
        self.flag_in_username_usernames = []
        for s in tweet_samples:
            self.ribbon_in_text_texts.append(
                s[0].text if s[0] else 'None')
            self.ribbon_in_text_usernames.append(
                s[0].username if s[0] else 'None')
            self.ribbon_in_username_texts.append(
                s[1].text if s[1] else 'None')
            self.ribbon_in_username_usernames.append(
                s[1].username if s[1] else 'None')
            self.flag_in_username_texts.append(
                s[2].text if s[2] else 'None')
            self.flag_in_username_usernames.append(
                s[2].username if s[2] else 'None')
            self.flag_in_text_texts.append(
                s[3].text if s[3] else 'None')
            self.flag_in_text_usernames.append(
                s[3].username if s[3] else 'None')

    def _set_daily_totals(self):
        self.ribbon_in_text_totals = []
        self.ribbon_in_username_totals = []
        self.flag_in_username_totals = []
        self.flag_in_text_totals = []
        for opinion in self.timeline.opinions:
            daily_tweets = opinion.tweets
            self.ribbon_in_text_totals.append(
                daily_tweets.text_has_ribbon.length)
            self.ribbon_in_username_totals.append(
                daily_tweets.username_has_ribbon.length)
            self.flag_in_username_totals.append(
                daily_tweets.username_has_flag.length)
            self.flag_in_text_totals.append(
                daily_tweets.text_has_flag.length)


    def _init_figure(self):
        hover_ribbon_lines = tools.HoverTool(
            tooltips=[
                ('Date', '@date_label'),
                ('Daily total', '@daily_total'),
                ('User', '@username'),
                ('Tweet', '@text')],
            names=[
                NAME_RIBBON_IN_TEXT,
                NAME_RIBBON_IN_USERNAME,
            ],
            attachment='below',
        )
        hover_flag_lines = tools.HoverTool(
            tooltips=[
                ('Date', '@date_label'),
                ('Daily total', '@daily_total'),
                ('User', '@username'),
                ('Tweet', '@text')],
            names=[
                NAME_FLAG_IN_USERNAME,
                NAME_FLAG_IN_TEXT,
            ],
            attachment='below',
        )
        hover_events_left = tools.HoverTool(
            tooltips=[
                ('Date', '@date_label'),
                ('Event', '@description')
            ],
            names=[NAME_EVENTS_LEFT],
            attachment='above',
        )
        hover_events_right = tools.HoverTool(
            tooltips=[
                ('Date', '@date_label'),
                ('Event', '@description')
            ],
            names=[NAME_EVENTS_RIGHT],
            attachment='above',
        )
        wheel_zoom = tools.WheelZoomTool(maintain_focus=False,
                                         dimensions='height')
        p = figure(
            title="",
            plot_width=PLOT_WIDTH, 
            plot_height=PLOT_HEIGHT,
            sizing_mode='stretch_both',
            y_axis_type='datetime',
            x_range=Range1d(
                self.height,
                0,
                bounds='auto'),
            y_range=Range1d(
                INITIAL_END_DATE,
                INITIAL_START_DATE,
                bounds=(
                    self.timeline.start_date,
                    self.timeline.end_date, 
                )),
            tools=[
                hover_ribbon_lines, hover_flag_lines,
                hover_events_left, hover_events_right,
                'box_zoom', wheel_zoom, 'pan', 'reset'],
            active_drag='pan',
            active_scroll=wheel_zoom,
        )
        p.title = Title(
            text=('Explore by scrolling and dragging. '
                  'Hover to see tweets and events. '
                  'Double-tap to toggle legend.'),
            text_font_style='italic',
            align='right',
            text_font_size='8pt',
        )
        p.background_fill_color = COLOR_BACKGROUND
        #  p.min_border = 75
        p.toolbar.autohide = True
        p.toolbar_location = None
        p.xaxis.ticker = []
        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None
        self.p = p

    def _add_lines(self):
        ribbon_in_text_source = ColumnDataSource(data=dict(
            y=self.dates,
            x=self.ribbon_in_text_pos,
            text=self.ribbon_in_text_texts,
            username=self.ribbon_in_text_usernames,
            date_label=self.date_labels,
            daily_total=self.ribbon_in_text_totals,
        ))

        ribbon_in_username_source = ColumnDataSource(data=dict(
            y=self.dates,
            x=self.ribbon_in_username_pos,
            text=self.ribbon_in_username_texts,
            username=self.ribbon_in_username_usernames,
            date_label=self.date_labels,
            daily_total=self.ribbon_in_username_totals,
        ))

        flag_in_username_source = ColumnDataSource(data=dict(
            y=self.dates,
            x=self.neutral_pos,
            text=self.flag_in_username_texts,
            username=self.flag_in_username_usernames,
            date_label=self.date_labels,
            daily_total=self.flag_in_username_totals,
        ))

        flag_in_text_source = ColumnDataSource(data=dict(
            y=self.dates,
            x=self.flag_in_username_pos,
            text=self.flag_in_text_texts,
            username=self.flag_in_text_usernames,
            date_label=self.date_labels,
            daily_total=self.flag_in_text_totals,
        ))
        flag_in_text_line = self.p.line(
            'x', 'y', source=flag_in_text_source,
            line_color=COLOR_FLAG_IN_TEXT,
            line_width=LINE_WIDTH,
            name=NAME_FLAG_IN_TEXT,
            legend=LEGEND_FLAG_IN_TEXT)
        flag_in_username_line = self.p.line(
            'x', 'y', source=flag_in_username_source,
            line_color=COLOR_FLAG_IN_USERNAME,
            line_width=LINE_WIDTH,
            name=NAME_FLAG_IN_USERNAME,
            legend=LEGEND_FLAG_IN_USERNAME)
        ribbon_in_username_line = self.p.line(
            'x', 'y', source=ribbon_in_username_source,
            line_color=COLOR_RIBBON_IN_USERNAME,
            line_width=LINE_WIDTH,
            name=NAME_RIBBON_IN_USERNAME,
            legend=LEGEND_RIBBON_IN_USERNAME)
        ribbon_in_text_line = self.p.line(
            'x', 'y', source=ribbon_in_text_source,
            line_color=COLOR_RIBBON_IN_TEXT,
            line_width=LINE_WIDTH,
            name=NAME_RIBBON_IN_TEXT,
            legend=LEGEND_RIBBON_IN_TEXT)
        def show_hide_legend(legend=self.p.legend[0]):
            legend.visible = not legend.visible
        self.p.js_on_event(events.DoubleTap,
                        CustomJS.from_py_func(show_hide_legend))
        self.p.legend.visible = False
        self.p.legend.background_fill_alpha = 0.95

    def _fill_between(self, bottom, top, color):
        data_source = ColumnDataSource(data=dict(
            y=np.hstack((self.dates, np.flip(self.dates))),
            x=np.hstack((bottom, np.flip(top)))
        ))

        glyph = Patch(x='x', y='y', fill_color=color, line_alpha=0.0)
        self.p.add_glyph(data_source, glyph)

    def _add_fills(self):
        bottom = np.zeros_like(self.dates)
        self._fill_between(bottom,
                           self.ribbon_in_text_pos,
                           COLOR_RIBBON_IN_TEXT)
        self._fill_between(self.ribbon_in_text_pos,
                           self.ribbon_in_username_pos,
                           COLOR_RIBBON_IN_USERNAME)
        self._fill_between(self.neutral_pos,
                           self.flag_in_username_pos,
                           COLOR_FLAG_IN_USERNAME)
        self._fill_between(self.flag_in_username_pos,
                           self.flag_in_text_pos,
                           COLOR_FLAG_IN_TEXT)

    def _get_event_pos(self, event):
        for (date, pos0, pos1) in zip(
                self.dates,
                self.ribbon_in_username_pos,
                self.neutral_pos):
            if date == event.date:
                return pos0, pos1

    def _set_events_pos(self):
        self.events_pos0_pos = []
        self.events_pos1_pos = []
        self.events_midpoints = []
        for e in event.EVENTS:
            pos0, pos1 = self._get_event_pos(e)
            self.events_pos0_pos.append(pos0)
            self.events_pos1_pos.append(pos1)
            self.events_midpoints.append((pos0 + pos1) / 2.0)

    def _add_events(self):
        events_source = ColumnDataSource(data=dict(
            y0=event.EVENTS.dates,
            y1=event.EVENTS.dates,
            x0=self.events_pos0_pos,
            #  y0=np.zeros_like(event.EVENTS.dates),
            x1=self.events_pos1_pos,
            #  y1=self.height*np.ones_like(event.EVENTS.dates),
            midpoints=self.events_midpoints,
            date_label=event.EVENTS.date_labels,
            description=event.EVENTS.descriptions,
        ))
        self.p.segment(x0='x0', x1='x1', y0='y0', y1='y1',
                       source=events_source,
                       line_width=2, line_alpha=0.5,
                       color=COLOR_EVENTS,
                       name=NAME_EVENTS)
        self.p.scatter(x='x0', y='y0',
                       source=events_source,
                       fill_color=COLOR_EVENTS,
                       fill_alpha=0,
                       line_alpha=0,
                       size=3,
                       name=NAME_EVENTS_LEFT)
        self.p.scatter(x='x1', y='y0',
                       source=events_source,
                       fill_color=COLOR_EVENTS,
                       fill_alpha=0,
                       line_alpha=0,
                       size=3,
                       name=NAME_EVENTS_RIGHT)


    def generate_visualization(self):
        self._init_figure()
        self._add_events()
        self._add_lines()
        self._add_fills()
        self.vis_generated = True

    def plot(self):
        if not self.vis_generated:
            self.generate_visualization()
        show(self.p)

    def get_filename(self):
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        return f'plots/ribbonline_plot_{timestamp}.html'

    def export_html(self, filename=None):
        if not filename:
            filename = self.get_filename()
        html = file_html(self.p, CDN, filename)
        if not os.path.exists('plots'):
            os.mkdir('plots')
        with open(filename, 'wt') as f:
            f.write(html)
