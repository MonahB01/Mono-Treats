import os
repo = os.path.expanduser("~/Documents/GitHub/MonoSolutions/")

import matplotlib.pyplot as plt
import seaborn as sns
import math
import numpy as np

from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections import register_projection
from matplotlib.projections.polar import PolarAxes
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D


# %%-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Graphing Utilities
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def graph_maker(quant=2, columns=2, style="plots", skew="Bot", y_size=5, x_size=7, example=False):
    axes=[]
    sfig=[]
    if (quant % columns) == 0:
        if style.lower() in ["plots", "plts", "plot", "plt"]:
            main_figure, axis_start = plt.subplots(nrows=int(quant/columns), ncols=columns, tight_layout=True, figsize=[int(columns)*x_size, int(quant/columns)*y_size])
            for axis_row in axis_start:
                try:
                    for ax in axis_row:
                        axes.append(ax)
                except:
                    axes.append(axis_row)
            
            if example == True:
                numbered_charts = axes #These are here because I would like to use a deepcopy but it makes the original unusable
                for i, ax in enumerate(numbered_charts):
                    ax.text(s=str(i), x=0.5, y=0.5, fontsize=22, fontweight='bold', ha='center')
                plt.show()
                

        if style.lower() in ["figs", "figures", "fig", "figure"]:
            main_figure = plt.figure(layout='constrained', figsize=[int(columns)*x_size, int(quant/columns)*y_size])
            subfigs = main_figure.subfigures(int(quant/columns), columns, wspace=0.07)
            for figs in subfigs:
                try:
                    for fig in figs:
                        sfig.append(fig)
                except:
                    sfig.append(figs)

            if example == True:
                numbered_charts = sfig
                for i, fig in enumerate(numbered_charts):
                    ax = fig.subplots(1,1)
                    ax.text(s=str(i), x=0.5, y=0.5, fontsize=22, fontweight='bold', ha='center')
                plt.show()
            
    else:
        print("not an even grid!")
        if skew.lower() in ["right", "left", "top", "bottom", "bot"]:
            skew = skew.lower()
        else:
            raise ValueError("Skew must be one of the following: right, left, top, bottom")

        remainder = quant % columns

        main_figure = plt.figure(layout='constrained', figsize=[int(columns)*x_size, int(math.ceil(quant/columns))*y_size])

        if skew.lower() in ["right", "left"]:
            subfigs = main_figure.subfigures(ncols=int(math.ceil(quant/columns)), wspace=0.07)
        
            if style.lower() in ["plots"]:
                for i, figs in enumerate(subfigs):
                    if skew in ["right"]:
                        if i <= math.floor(quant/columns)-1:
                            ax = figs.subplots(nrows=columns, ncols=1)
                            try:
                                for axis in ax:
                                    axes.append(axis)
                            except:
                                axes.append(ax)
                        else:
                            ax = figs.subplots(nrows=remainder + 2, ncols=1, gridspec_kw={"height_ratios": [0.5] + [1]*remainder + [0.5]})
                            try:
                                for n, axis in enumerate(ax):
                                    if n == 0 or n == len(ax)-1:
                                        axis.axis('off')
                                    else:
                                        axes.append(axis)
                            except:
                                axes.append(ax)
                    
                    if skew in ["left"]:    
                        if i == 0:
                            ax = figs.subplots(nrows=remainder + 2, ncols=1, gridspec_kw={"height_ratios": [0.5] + [1]*remainder + [0.5]})
                            try:
                                for n, axis in enumerate(ax):
                                    if n == 0 or n == len(ax)-1:
                                        axis.axis('off')
                                    else:
                                        axes.append(axis)
                            except:
                                axes.append(ax)
                        else:
                            ax = figs.subplots(nrows=columns, ncols=1)
                            try:
                                for axis in ax:
                                    axes.append(axis)
                            except:
                                axes.append(ax)

                if example == True:
                    numbered_charts = axes #These are here because I would like to use a deepcopy but it makes the original unusable
                    for i, ax in enumerate(numbered_charts):
                        ax.text(s=str(i), x=0.5, y=0.5, fontsize=22, fontweight='bold', ha='center')
                    plt.show()

            if style.lower() in ["figs", "figures"]:
                for i, row_fig in enumerate(subfigs):
                    if skew in ["right"]:
                        if i <= math.floor(quant/columns)-1:
                            column_fig = row_fig.subfigures(nrows=columns,ncols=1)
                            for figs in column_fig:
                                sfig.append(figs)
                        else:
                            column_fig = row_fig.subfigures(nrows=remainder,ncols=1)
                            try:
                                for figs in column_fig:
                                    sfig.append(figs)
                            except:
                                sfig.append(column_fig)
                    
                    if skew in ["left"]:
                        if i == 0:
                            column_fig = row_fig.subfigures(nrows=remainder,ncols=1)
                            try:
                                for figs in column_fig:
                                    sfig.append(figs)
                            except:
                                sfig.append(column_fig)
                        else:
                            column_fig = row_fig.subfigures(nrows=columns,ncols=1)
                            for figs in column_fig:
                                sfig.append(figs)

                if example == True:
                    numbered_charts = sfig #These are here because I would like to use a deepcopy but it makes the original unusable
                    for i, figs in enumerate(sfig):
                        ax = figs.subplots(1,1)
                        ax.text(s=str(i), x=0.5, y=0.5, fontsize=22, fontweight='bold', ha='center')
                    plt.show()


        elif skew.lower() in ["top", "bottom", "bot"]:
            subfigs = main_figure.subfigures(nrows=int(math.ceil(quant/columns)), wspace=0.07)
        
            if style.lower() in ["plots"]:
                for i, figs in enumerate(subfigs):
                    if skew in ["bot", "bottom"]:
                        if i <= math.floor(quant/columns)-1:
                            ax = figs.subplots(nrows=1, ncols=columns)
                            for axis in ax:
                                axes.append(axis)
                        else:
                            ax = figs.subplots(nrows=1, ncols=remainder + 2, gridspec_kw={"width_ratios": [0.5] + [1]*remainder + [0.5]})
                            try:
                                for n, axis in enumerate(ax):
                                    if n == 0 or n == len(ax)-1:
                                        axis.axis('off')
                                    else:
                                        axes.append(axis)
                            except:
                                axes.append(ax)
                    
                    if skew in ["top"]:
                        if i == 0:
                            ax = figs.subplots(nrows=1, ncols=remainder + 2, gridspec_kw={"width_ratios": [0.5] + [1]*remainder + [0.5]})
                            try:
                                for n, axis in enumerate(ax):
                                    if n == 0 or n == len(ax)-1:
                                        axis.axis('off')
                                    else:
                                        axes.append(axis)
                            except:
                                axes.append(ax)
                        else:
                            ax = figs.subplots(nrows=1, ncols=columns)
                            for axis in ax:
                                axes.append(axis)

                if example == True:
                    numbered_charts = axes #These are here because I would like to use a deepcopy but it makes the original unusable
                    for i, ax in enumerate(numbered_charts):
                        ax.text(s=str(i), x=0.5, y=0.5, fontsize=22, fontweight='bold', ha='center')
                    plt.show()


            if style.lower() in ["figs", "figures"]:
                for i, row_fig in enumerate(subfigs):
                    if skew in ["bot", "bottom"]:
                        if i <= (math.floor(quant/columns)-1):
                            column_fig = row_fig.subfigures(nrows=1,ncols=columns)
                            for figs in column_fig:
                                sfig.append(figs)
                        else:
                            column_fig = row_fig.subfigures(nrows=1,ncols=remainder)
                            try:
                                for figs in column_fig:
                                    sfig.append(figs)
                            except:
                                sfig.append(column_fig)
                    
                    elif skew in ["top"]:
                        if i == 0:
                            column_fig = row_fig.subfigures(nrows=1,ncols=remainder)
                            try:
                                for figs in column_fig:
                                    sfig.append(figs)
                            except:
                                sfig.append(column_fig)
                        else:
                            column_fig = row_fig.subfigures(nrows=1,ncols=columns)
                            for figs in column_fig:
                                sfig.append(figs)

                if example == True:
                    numbered_charts = sfig #These are here because I would like to use a deepcopy but it makes the original unusable
                    for i, figs in enumerate(sfig):
                        ax = figs.subplots(1,1)
                        ax.text(s=str(i), x=0.5, y=0.5, fontsize=22, fontweight='bold', ha='center')
                    plt.show()

    if example == True:
        main_figure, sfig = graph_maker(quant=quant, columns=columns, style=style, skew=skew, example=False, y_size=y_size,x_size=x_size)
        axes = sfig

    if style.lower() in ["figs", "figures"]:
        return(main_figure, sfig)
    
    if style.lower() in ["plots"]:
        return(main_figure, axes)

def cat_plot_explorer(df, xval, yval, y_size=5, x_size=7):
    fig, ax_list = graph_maker(quant=8, columns=4, style="plots", skew="Bot", y_size=y_size, x_size=x_size, example=False)

    for ax, type in zip(ax_list, ["count", "bar", "box", "violin", "strip", "swarm", "point", "bar"]):
        if type == "count":
            sns.countplot(data=df, x=xval, ax=ax)
            ax.set_title("Count Plot")
        elif type == "bar":
            sns.barplot(data=df, x=xval, y=yval, ax=ax)
            ax.set_title("Bar Plot")
        elif type == "box":
            sns.boxplot(data=df, x=xval, y=yval, ax=ax)
            ax.set_title("Box Plot")
        elif type == "violin":
            sns.violinplot(data=df, x=xval, y=yval, ax=ax)
            ax.set_title("Violin Plot")
        elif type == "strip":
            sns.stripplot(data=df, x=xval, y=yval, ax=ax)
            ax.set_title("Strip Plot")
        elif type == "swarm":
            sns.swarmplot(data=df, x=xval, y=yval, ax=ax)
            ax.set_title("Swarm Plot")
        elif type == "point":
            sns.pointplot(data=df, x=xval, y=yval, ax=ax)
            ax.set_title("Point Plot")
        
    plt.show()

def cat_plot_maker(df, xval, yval, plot_type="box", hue_val=None, y_size=5, x_size=7):
    
    if type(xval) == str:
        xval = [xval]
    if type(yval) == str:
        yval = [yval]
    
    fig, ax_list = graph_maker(quant=len(xval)*len(yval), columns=len(xval), style="plots", skew="Bot", y_size=y_size, x_size=x_size, example=False)
    
    for j, yplot in enumerate(yval):
        if yplot not in df.columns:
            raise ValueError(f"{yplot} is not a column in the dataframe.")    
        for i, xplot in enumerate(xval):
            if hue_val is None:
                hue_val = xplot
            if xplot not in df.columns:
                raise ValueError(f"{xplot} is not a column in the dataframe.")
            ax = ax_list[i + j*(len(xval))]
        
            if plot_type.lower() == "count":
                sns.countplot(data=df, x=xplot, hue=hue_val, ax=ax)
                ax.set_title(f"Count Plot of {xplot}")
            else:
                sns.catplot(data=df, x=xplot, y=yplot, kind=plot_type.lower(), hue=hue_val, ax=ax)
                ax.set_title(f"{plot_type.capitalize()} Plot of {yplot} by {xplot}")
    
    plt.show()

#functions for charts? CODE FROM MATPLOTLIB EXAMPLE!
def radar_factory(num_vars, frame='circle'):
    """
    Create a radar chart with `num_vars` Axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle', 'polygon'}
        Shape of frame surrounding Axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarTransform(PolarAxes.PolarTransform):

        def transform_path_non_affine(self, path):
            # Paths with non-unit interpolation steps correspond to gridlines,
            # in which case we force interpolation (to defeat PolarTransform's
            # autoconversion to circular arcs).
            if path._interpolation_steps > 1:
                path = path.interpolated(num_vars)
            return Path(self.transform(path.vertices), path.codes)

    class RadarAxes(PolarAxes):

        name = 'radar'
        PolarTransform = RadarTransform

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta
