# -*- coding: utf-8 -*-
#
# Copyright © 2009 Pierre Raybaut
# Licensed under the terms of the MIT License
# see the mpl licenses directory for a copy of the license


"""Module that provides a GUI-based editor for matplotlib's figure options"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import six

import os.path as osp

import matplotlib.backends.qt4_editor.formlayout as formlayout
from matplotlib.backends.qt4_compat import QtGui
from matplotlib import markers

def get_icon(name):
    import matplotlib
    basedir = osp.join(matplotlib.rcParams['datapath'], 'images')
    return QtGui.QIcon(osp.join(basedir, name))

LINESTYLES = {
              '-': 'Solid',
              '--': 'Dashed',
              '-.': 'DashDot',
              ':': 'Dotted',
              'steps': 'Steps',
              'none': 'None',
              }

MARKERS = markers.MarkerStyle.markers

def figure_edit(axes, parent=None):
    """Edit matplotlib figure options"""
    sep = (None, None) # separator

    has_curve = len(axes.get_lines()) > 0

    # Get / General
    xmin, xmax = axes.get_xlim()
    ymin, ymax = axes.get_ylim()
    general = [('Title', axes.get_title()),
               sep,
               (None, "<b>X-Axis</b>"),
               ('Min', xmin), ('Max', xmax),
               ('Label', axes.get_xlabel()),
               ('Scale', [axes.get_xscale(), 'linear', 'log']),
               sep,
               (None, "<b>Y-Axis</b>"),
               ('Min', ymin), ('Max', ymax),
               ('Label', axes.get_ylabel()),
               ('Scale', [axes.get_yscale(), 'linear', 'log'])
               sep,
               #re-generate auto legend defaults to False, as it clobbers carefully hand crafted legends /2014-04-22
               ('(Re-)Generate automatic legend', False)
               ]

    if has_curve:
        # Get / Curves
        linedict = {}
        for line in axes.get_lines():
            label = line.get_label()
            if label == '_nolegend_':
                continue
            linedict[label] = line
        curves = []
        linestyles = list(six.iteritems(LINESTYLES))
        markers = list(six.iteritems(MARKERS))
        curvelabels = sorted(linedict.keys())
        for label in curvelabels:
            line = linedict[label]
            curvedata = [
                         ('Label', label),
                         sep,
                         (None, '<b>Line</b>'),
                         ('Style', [line.get_linestyle()] + linestyles),
                         ('Width', line.get_linewidth()),
                         ('Color', line.get_color()),
                         sep,
                         (None, '<b>Marker</b>'),
                         ('Style', [line.get_marker()] + markers),
                         ('Size', line.get_markersize()),
                         ('Facecolor', line.get_markerfacecolor()),
                         ('Edgecolor', line.get_markeredgecolor()),
                         ]
            curves.append([curvedata, label, ""])

    datalist = [(general, "Axes", "")]
    if has_curve:
        datalist.append((curves, "Curves", ""))

    def apply_callback(data):
        """This function will be called to apply changes"""
        if has_curve:
            general, curves = data
        else:
            general, = data

        # Set / General
        title, xmin, xmax, xlabel, xscale, ymin, ymax, ylabel, yscale, generate_legend = general #/2014-04-22
        axes.set_xscale(xscale)
        axes.set_yscale(yscale)
        axes.set_title(title)
        axes.set_xlim(xmin, xmax)
        axes.set_xlabel(xlabel)
        axes.set_ylim(ymin, ymax)
        axes.set_ylabel(ylabel)

        if has_curve:
            # Set / Curves
            for index, curve in enumerate(curves):
                line = linedict[curvelabels[index]]
                label, linestyle, linewidth, color, \
                    marker, markersize, markerfacecolor, markeredgecolor = curve
                line.set_label(label)
                line.set_linestyle(linestyle)
                line.set_linewidth(linewidth)
                line.set_color(color)
                if marker is not 'none':
                    line.set_marker(marker)
                    line.set_markersize(markersize)
                    line.set_markerfacecolor(markerfacecolor)
                    line.set_markeredgecolor(markeredgecolor)
        
        # re-generate legend, if checkbox is checked. Stefan Kraus/tacaswell 2014-04-22
        if generate_legend:
            if axes.legend_ is not None:
                old_legend = axes.get_legend()
                """try to set everything mentioned in http://matplotlib.org/api/legend_api.html:
                class matplotlib.legend.Legend(parent, handles, labels, loc=None, numpoints=None,
                markerscale=None, scatterpoints=None, scatteryoffsets=None, prop=None, fontsize=None,
                borderpad=None, labelspacing=None, handlelength=None, handleheight=None,
                handletextpad=None, borderaxespad=None, columnspacing=None, ncol=1,
                mode=None, fancybox=None, shadow=None, title=None, framealpha=None,
                bbox_to_anchor=None, bbox_transform=None, frameon=None, handler_map=None)
                
                fancybox needs special treatment
                
                framealpha needs still special treatment
                
                title needs special treatment as 'None' often is the title "text" of the old legend
                """
                h, l = axes.get_legend_handles_labels()
                new_legend = axes.legend(h, l, loc=old_legend._loc,
                                         numpoints=old_legend.numpoints,
                                         markerscale=old_legend.markerscale,
                                         scatterpoints=old_legend.scatterpoints,
                                         scatteryoffsets=old_legend._scatteryoffsets,
                                         prop=old_legend.prop,
                                         fontsize=old_legend._fontsize,
                                         borderpad=old_legend.borderpad,
                                         labelspacing=old_legend.labelspacing,
                                         handlelength=old_legend.handlelength,
                                         handleheight=old_legend.handleheight,
                                         handletextpad=old_legend.handletextpad,
                                         borderaxespad=old_legend.borderaxespad,
                                         columnspacing=old_legend.columnspacing,
                                         ncol=old_legend._ncol,
                                         mode=old_legend._mode,
##                                       fancybox=old_legend._fancybox,
##                """old_legend.legendPatch.set_boxstyle("round", pad=0, rounding_size=0.2)"""
                                         shadow=old_legend.shadow,
                                     
#                                        title=str(old_legend.get_title().get_text()),
##                                       framealpha=old_legend._framealpha,
##               """old_legend.get_frame().set_alpha(framealpha)"""
##                                       bbox_to_anchor=old_legend._bbox_to_anchor,
##                  """bbox_to_anchor=old_legend._bbox_to_anchor, lets the legend
##                  disappear"""
##                                       bbox_transform=old_legend.bbox_transform,
##                """see below"""
                                         frameon=old_legend._drawFrame,
                                         handler_map=old_legend._handler_map
                                         )
                #deal with fancybox:
                new_legend.legendPatch = old_legend.legendPatch
                new_legend.draggable(old_legend._draggable is not None)
                # I don't like to test for strings! That's bad! why is it not
                # None, but "None" as a string at all?!
                # /Stefan Kraus 2014-04-22
                if old_legend.get_title().get_text() != 'None':
                    new_legend.set_title(old_legend.get_title().get_text())
                    print('"None" is not the old title') #debug
                    new_legend.get_title().set_color(old_legend.get_title().get_color())
                    new_legend.get_title().set_horizontalalignment(old_legend.get_title().get_horizontalalignment())
                    new_legend.get_title().set_verticalalignment(old_legend.get_title().get_verticalalignment())
                    new_legend.get_title().set_position(old_legend.get_title().get_position())
                    new_legend.get_title().set_rotation_mode(old_legend.get_title().get_rotation_mode())
    #               new_legend.get_title().set_window_extent(old_legend.get_title().get_window_extent()) # there is no set_window_extent
    #               new_legend.get_title().set_backgroundcolor(old_legend.get_title().get_backgroundcolor()) # there is no get_backgroundcolor
    #               new_legend.get_title().set_bbox(old_legend.get_title().get_bbox()) # there is no get_bbox
                    new_legend.get_title().set_x(old_legend.get_title().get_position()[0])
                    new_legend.get_title().set_y(old_legend.get_title().get_position()[1])
                    new_legend.get_title().set_fontproperties(old_legend.get_title().get_fontproperties())
            else:
                new_legend = axes.legend()
                new_legend.draggable(True)
                
        # Redraw
        figure = axes.get_figure()
        figure.canvas.draw()

    data = formlayout.fedit(datalist, title="Figure options", parent=parent,
                            icon=get_icon('qt4_editor_options.svg'), apply=apply_callback)
    if data is not None:
        apply_callback(data)
