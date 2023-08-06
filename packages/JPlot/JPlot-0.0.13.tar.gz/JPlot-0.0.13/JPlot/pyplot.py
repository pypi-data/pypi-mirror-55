# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import subprocess
import matplotlib.pyplot as plt

from JPlot.pyplotAux import set_plot_style
from . import GLOBAL_SETTING_DICT
from . import get_default_color, get_default_hatch, get_default_linestyle, get_default_marker
from . import get_color, get_bw_color, get_single_color
from .pyplotAux import _extract_arg, _postprocess_plot
from .ax import AX

# this solves the missing functions in JPlot.pyplot 
from matplotlib.pyplot import *
MARKER, LINESTYLE, COLOR, HATCH = get_default_marker(), get_default_linestyle(), get_default_color(), get_default_hatch()


def general_processing(plotter, *args, **kwargs):
    global MARKER, LINESTYLE, COLOR, HATCH
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    caller = calframe[1][3]

    jargs = str(args)
    jkwargs = str(kwargs)
    GLOBAL_SETTING_DICT["plot_data"].append((caller, jargs, jkwargs))

    set_plot_style(kwargs)
    e_args = _extract_arg(kwargs)
    if "color" not in kwargs and "nocolor" not in kwargs and caller not in ("boxplot", ):
        kwargs["color"] = next(COLOR)
    elif "nocolor" in kwargs:
        kwargs.pop("nocolor")
    if caller == "plot" or caller == "semilogx" or caller == "semilogy":
        if "marker" not in kwargs and "nomarker" not in kwargs:
            kwargs["marker"] = next(MARKER)
        elif "nomarker" in kwargs:
            kwargs.pop("nomarker")
        if "linestyle" not in kwargs and "nolinestyle" not in kwargs:
            kwargs["linestyle"] = next(LINESTYLE)
        elif "nolinestyle" in kwargs:
            kwargs.pop("nolinestyle")

    getattr(plotter, caller)(*args, **kwargs)
    if len(e_args):
        _postprocess_plot(**e_args)


def plot(*args, **kwargs):
    general_processing(plt, *args, **kwargs)


def semilogx(*args, **kwargs):
    general_processing(plt, *args, **kwargs)


def bar(*args, **kwargs):
    if "hatch" not in kwargs:
        kwargs["hatch"] = next(HATCH)
    general_processing(plt, *args, **kwargs)


def box(*args, **kwargs):
    general_processing(plt, *args, **kwargs)


def boxplot(*args, **kwargs):
    # set_plot_style(kwargs)
    # e_args = _extract_arg(kwargs)
    # e_args["has_legend"] = False  # labels is different here
    # plt.boxplot(*args, **kwargs)
    general_processing(plt, *args, **kwargs)
    # _postprocess_plot(**e_args)


def scatter(*args, **kwargs):
    general_processing(plt, *args, **kwargs)


def hist(*args, **kwargs):
    general_processing(plt, *args, **kwargs)


def fill_between(*args, **kwargs): 
    general_processing(plt, *args, **kwargs)




def savefig(*args, **kwargs):
    if "fname" in kwargs:
        figname = kwargs["fname"]
    else:
        figname = args[0]
        args = args[1:]

    if "." not in figname[-5:]:
        figname += "." + GLOBAL_SETTING_DICT["output_format"]
    kwargs["fname"] = figname

    if "bbox_inches" not in kwargs:
        kwargs["bbox_inches"] = 'tight'

    if not kwargs.pop("no_save_plot_data", False):
        with open(f"{figname}"+".plotData.json", "w") as ofile:
            json.dump(GLOBAL_SETTING_DICT["plot_data"], ofile)
    GLOBAL_SETTING_DICT["plot_data"] = []

    if kwargs.pop("save_tex", False):
        try:
            import tikzplotlib
            filename = figname.replace(".png", ".tex").replace(".pdf", ".tex")
            tikzplotlib.save(filename)
        except Exception as e:
            print(e)

    plt.savefig(*args, **kwargs)
    if GLOBAL_SETTING_DICT["auto_open"]:
        subprocess.run(["open", figname], shell=False)
    GLOBAL_SETTING_DICT["update_plot_style"] = True


def cla():
    global MARKER, LINESTYLE, COLOR, HATCH
    MARKER, LINESTYLE, COLOR, HATCH = get_default_marker(), get_default_linestyle(), get_default_color(), get_default_hatch()
    GLOBAL_SETTING_DICT["update_plot_style"] = True
    plt.cla()


def clf():
    global MARKER, LINESTYLE, COLOR, HATCH
    MARKER, LINESTYLE, COLOR, HATCH = get_default_marker(), get_default_linestyle(), get_default_color(), get_default_hatch()
    GLOBAL_SETTING_DICT["update_plot_style"] = True
    plt.clf()

def close():
    global MARKER, LINESTYLE, COLOR, HATCH
    MARKER, LINESTYLE, COLOR, HATCH = get_default_marker(), get_default_linestyle(), get_default_color(), get_default_hatch()
    GLOBAL_SETTING_DICT["update_plot_style"] = True
    plt.close()


def replot(plot_data_file):
    replot_using_saved_data(plot_data_file)

def replot_using_saved_data(plot_data_file):
    with open(plot_data_file, "r") as ifile:
        plot_data = json.load(ifile)
    for p in plot_data:
        args = eval(p[1])
        kwargs = eval(p[2])
        # print(args, type(args))
        print(kwargs, type(kwargs))
        globals()[p[0]](*args, **kwargs)
    savefig(plot_data_file.replace(".plotData.json", ""))


def xticks(*args, **kwargs):
    plt.xticks(*args, **kwargs)


def yticks(*args, **kwargs):
    plt.yticks(*args, **kwargs)


def set_n_colors(n):
    global COLOR
    COLOR = get_color(n)
    return COLOR


def set_single_colors(n):
    global COLOR
    COLOR = get_single_color(n)
    return COLOR


def set_bw_colors(n):
    global COLOR
    COLOR = get_bw_color(n)
    return COLOR


def subplot(*args, **kwargs):
    set_plot_style(kwargs)
    return getattr(plt, "subplot")(*args, **kwargs)


def subplots(*args, **kwargs):
    set_plot_style(kwargs)
    fig, axes = getattr(plt, "subplots")(*args, **kwargs)
    new_axes = [AX(i) for i in axes]
    return fig, new_axes


