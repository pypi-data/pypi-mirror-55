
from matplotlib.axes import Axes
from matplotlib.axis import Axis
import JPlot.pyplot as plt

class AX():
    def __init__(self, matplotlib_ax, *args, **kwargs):
        # super(AX, self).__init__(matplotlib_ax.axes, *args, **kwargs)
        self.matplotlib_ax = matplotlib_ax
        self.xaxis = matplotlib_ax.xaxis
        self.yaxis = matplotlib_ax.yaxis

    def plot(self, *args, **kwargs):
        plt.general_processing(self.matplotlib_ax, *args, **kwargs)

    def box(self, *args, **kwargs):
        plt.general_processing(self.matplotlib_ax, *args, **kwargs)

    def bar(self, *args, **kwargs):
        plt.general_processing(self.matplotlib_ax, *args, **kwargs)

    def scatter(self, *args, **kwargs):
        plt.general_processing(self.matplotlib_ax, *args, **kwargs)

    def fill_between(self, *args, **kwargs):
        plt.general_processing(self.matplotlib_ax, *args, **kwargs)

    def boxplot(self, *args, **kwargs):
        plt.general_processing(self.matplotlib_ax, *args, **kwargs)


    def set_xlabel(self, *args, **kwargs):
        self.matplotlib_ax.set_xlabel(*args, **kwargs)

    def set_ylabel(self, *args, **kwargs):
        self.matplotlib_ax.set_ylabel(*args, **kwargs)

    def set_xlim(self, *args, **kwargs):
        self.matplotlib_ax.set_xlim(*args, **kwargs)

    def set_ylim(self, *args, **kwargs):
        self.matplotlib_ax.set_ylim(*args, **kwargs)

    def set_title(self, *args, **kwargs):
        self.matplotlib_ax.set_title(*args, **kwargs)

    def set_xscale(self, *args, **kwargs):
        self.matplotlib_ax.set_xscale(*args, **kwargs)

    def set_yscale(self, *args, **kwargs):
        self.matplotlib_ax.set_yscale(*args, **kwargs)

    def set_xticks(self, *args, **kwargs):
        self.matplotlib_ax.set_xticks(*args, **kwargs)

    def set_yticks(self, *args, **kwargs):
        self.matplotlib_ax.set_yticks(*args, **kwargs)

    def set_xticklabels(self, *args, **kwargs):
        self.matplotlib_ax.set_xticklabels(*args, **kwargs)

    def set_yticklabels(self, *args, **kwargs):
        self.matplotlib_ax.set_yticklabels(*args, **kwargs)


    # def _get_label(self):
    #     raise NotImplementedError('Derived must override')
    #
    # def _get_offset_text(self):
    #     raise NotImplementedError('Derived must override')

