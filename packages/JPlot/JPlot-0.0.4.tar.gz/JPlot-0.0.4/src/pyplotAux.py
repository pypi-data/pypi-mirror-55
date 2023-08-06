
import os

from JPlot import GLOBAL_SETTING_DICT, BASE_PATH
from . import GLOBAL_SETTING_DICT
import subprocess
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def _default_process(fig, ax):
    fig.canvas.draw()
    ax.xaxis.set_major_locator(MaxNLocator(4))


    # ax.set_xticklabels(ax.get_xticks())
    #
    # # locs, labels = plt.xticks()
    # locs = ax.get_xticks()
    # labels = ax.get_xticklabels()
    # print(locs, " ".join([str(i) for i in labels]))
    # if len(locs) > 6:
    #     new_locs = [locs[i*2] for i in range((len(locs)-1)//2)]
    #     new_labels = [labels[i*2] for i in range((len(locs)-1)//2)]
    #     ax.set_xticks(new_locs)
    #     ax.set_xticklabels(new_labels)
    #     # print("{} {} set {} {}".format(locs, " ".join([str(i) for i in labels]), new_locs, new_labels))


def _extract_arg0(kwargs):
    figname = kwargs.pop("figname", None)
    xlabel  = kwargs.pop("xlabel", None)
    ylabel  = kwargs.pop("ylabel", None)
    xticks  = kwargs.pop("xticks", None)
    yticks  = kwargs.pop("yticks", None)
    xlim  = kwargs.pop("xlim", None)
    ylim  = kwargs.pop("ylim", None)
    xscale  = kwargs.pop("xscale", None)
    yscale  = kwargs.pop("yscale", None)
    grid = kwargs.pop("grid", None)
    add_hatch = kwargs.pop("add_hatch", None)
    rotate_xticks = kwargs.pop("rotate_xticks", None)

    auto_open = kwargs.pop("auto_open", GLOBAL_SETTING_DICT["auto_open"])
    has_legend = "labels" in kwargs

    return {"figname": figname, "xlabel": xlabel, "ylabel": ylabel, "xticks": xticks, "yticks": yticks, "xlim": xlim, "ylim": ylim,
            "grid": grid, "rotate_xticks": rotate_xticks, "add_hatch": add_hatch,
            "xscale": xscale, "yscale": yscale, "auto_open": auto_open, "has_legend": has_legend}
    # return figname, xlabel, ylabel, xticks, yticks, xlim, ylim, xscale, yscale, auto_open, has_legend

def _extract_arg(kwargs):
    new_kwargs = {}
    for key in ("figname", "xlabel", "ylabel", "xticks", "yticks", "xlim", "ylim",
                    "grid", "rotate_xticks", "add_hatch",
                    "xscale", "yscale", "auto_open", "has_legend"):
        if key in kwargs:
            new_kwargs[key] = kwargs.pop(key)
    return new_kwargs

def _postprocess_plot(figname=None, has_legend=False, **kwargs):
    for arg in ("xlabel", "ylabel", "xticks", "yticks", "xlim", "ylim", "xscale", "yscale", "title"):
        if kwargs.get(arg, None):
            getattr(plt, arg)(kwargs[arg])
    if kwargs.get("rotate_xticks", None):
        plt.xticks(rotation=kwargs.pop("rotate_xticks"), ha='right')

    if "grid" in kwargs and kwargs["grid"]:
        plt.grid(linestyle="--")
    if has_legend:
        plt.legend(loc="best")
    plt.tight_layout()

    if figname:
        if "." not in figname[:-5]:
            figname += "." + GLOBAL_SETTING_DICT["output_format"]
        if len(os.path.dirname(figname)) > 0 and not os.path.exists(os.path.dirname(figname)):
            os.mkdir(os.path.dirname(figname))
        plt.savefig(figname)
        plt.clf()
        plt.close("all")

        if GLOBAL_SETTING_DICT["auto_open"]:
            subprocess.run(["open", figname], shell=False)

def _process_plot(figname, **kwargs):
    if "xlim" in kwargs:
        plt.xlim(kwargs.pop("xlim"))
    if "ylim" in kwargs:
        plt.ylim(kwargs.pop("ylim"))
    if "xticks" in kwargs:
        plt.xticks(kwargs.pop("xticks"))
    if "yticks" in kwargs:
        plt.yticks(kwargs.pop("yticks"))
    if "xscale" in kwargs:
        plt.xscale(kwargs.pop("xscale"))
    if "yscale" in kwargs:
        plt.yscale(kwargs.pop("yscale"))
    if "xlabel" in kwargs:
        plt.xlabel(kwargs.pop("xlabel"))
    if "ylabel" in kwargs:
        plt.ylabel(kwargs.pop("ylabel"))
    if "title" in kwargs:
        plt.title(kwargs.pop("title"))

    if kwargs.pop("label", False):
        plt.legend(loc="best")

    assert len(kwargs) == 0, len(kwargs)

    plt.tight_layout()
    if not os.path.exists(os.path.dirname(figname)):
        os.mkdir(os.path.dirname(figname))
    plt.savefig(figname)
    plt.clf()
    plt.close("all")

    if GLOBAL_SETTING_DICT["auto_open"]:
        subprocess.run(["open", figname], shell=False)


def set_plot_style(kwargs):
    if not GLOBAL_SETTING_DICT["update_plot_style"]:
        return

    GLOBAL_SETTING_DICT["update_plot_style"] = False
    plot_style_list = [os.path.join(BASE_PATH, "styles/JStyle"), ]
    plot_styles = kwargs.pop("plot_style", GLOBAL_SETTING_DICT["plot_style"])
    for plot_style in plot_styles.split("-"):
        plot_style_path = os.path.join(BASE_PATH, "styles/" + plot_style)
        if not os.path.exists(plot_style_path):
            print("cannot find style {} at {}".format(plot_style, plot_style_path))
        else:
            plot_style_list.append(plot_style_path)

    plt.style.use(plot_style_list)

    if "pub" in plot_styles:
        GLOBAL_SETTING_DICT["output_format"] = "pdf"
    elif "presentation" in plot_styles:
        GLOBAL_SETTING_DICT["output_format"] = "png"