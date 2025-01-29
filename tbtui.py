import polars as pl
from argparse import ArgumentParser
import os
from textual.app import App, ComposeResult
from textual.widgets import TabbedContent, TabPane, Footer, RadioSet, RadioButton
from textual_plotext import PlotextPlot
from textual.binding import Binding
from glob import glob


parser = ArgumentParser()
parser.add_argument(
    "--path",
    type=str,
    default=".",
    help="Path to CSV history files",
)
global df_names, df_paths


class MetricPlot(PlotextPlot):
    """
    MetricPlot This class represents a plot for a specific metric.

    Args:
        PlotextPlot (class): The textual_plotext.PlotextPlot class, from which
        our MetricPlot class inherits its functionality.
    """

    global df_names, df_paths

    def __init__(self, metric_name, values, id, *args, **kwargs):
        """
        Initialize a MetricPlot object.

        Args:
            metric_name (str): Name of the metric to be plotted.
            values (list): List of values to be plotted.
            id (int): Unique ID of the plot.

        Attributes:
            metric (str): Name of the metric to be plotted.
            x (list): List of x-coordinates of the plot.
            y (list): List of y-coordinates of the plot.
            id (int): Unique ID of the plot.
            show_min (bool): Whether to show the minimum value of the metric.
            show_max (bool): Whether to show the maximum value of the metric.
        """
        super().__init__(*args, **kwargs)
        self.metric = metric_name
        self.x = list(range(len(values)))
        self.y = values
        self.watch(self.app, "theme", lambda: self.call_after_refresh(self.replot))
        self.id = id

        self.show_min = False
        self.show_max = False

    def on_mount(self) -> None:
        """Plot the data using Plotext."""
        self.replot()

    def replot(self) -> None:
        """Redraw the plot."""
        self.plt.clear_data()
        self.plt.plot(self.x, self.y, color="red", marker="braille")
        self.plt.title(self.id)

        # Toggle min/max display
        if self.show_min:
            min_idx = self.y.index(min(self.y))
            self.plt.scatter(
                [self.x[min_idx]],
                [self.y[min_idx]],
                color="green",
                label=f"Min: {self.y[min_idx]:.3f} @ epoch: {self.x[min_idx]}",
                marker="+",
            )
            self.plt.vertical_line(self.x[min_idx], color="green")

        if self.show_max:
            max_idx = self.y.index(max(self.y))
            self.plt.scatter(
                [self.x[max_idx]],
                [self.y[max_idx]],
                color="green",
                label=f"Max: {self.y[max_idx]:.3f} @ epoch: {self.x[max_idx]}",
                marker="+",
            )
            self.plt.vertical_line(self.x[max_idx], color="green")

        self.plt.xticks(ticks=self.x[:: len(self.x) // 20])
        self.plt.grid(horizontal=True, vertical=True)
        self.refresh()

    def _watch_marker(self) -> None:
        """React to the marker being changed."""
        self.replot()

    def toggle_min(self):
        """Toggle the display of the minimum value."""
        self.show_min = not self.show_min
        self.replot()

    def toggle_max(self):
        """Toggle the display of the maximum value."""
        self.show_max = not self.show_max
        self.replot()


class ExperimentTracker(App):
    """
    ExperimentTracker This class represents the main application.

    Args:
        App (class): The textual.app.App class, from which our ExperimentTracker class inherits its functionality.

    """

    CSS_PATH = "vis_history.css"  # Optional CSS for styling

    BINDINGS = [
        Binding("m", "toggle_min", "Toggle Min Value", show=True),
        Binding("M", "toggle_max", "Toggle Max Value", show=True),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selected_df_idx = 0
        self.metrics = [i for i in dfs[self.selected_df_idx].columns if i != "epoch"]
        self.epochs = dfs[self.selected_df_idx]["epoch"].to_list()

    def compose(self) -> ComposeResult:
        """Create tabbed interface with plots for each metric"""
        with RadioSet(id="sidebar"):
            for idx, df_name in enumerate(df_names):
                yield RadioButton(
                    label=df_name,
                    id=f"{df_name}_rb",
                    value=df_name == df_names[self.selected_df_idx],
                )

        with TabbedContent():
            for metric in self.metrics:
                with TabPane(title=metric, id=f"{metric}_tab"):
                    yield MetricPlot(
                        metric_name=metric,
                        values=dfs[self.selected_df_idx][metric].to_list(),
                        id=f"{metric}_plot",
                    )
        yield Footer()

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        """
        When a radio button is changed, update the selected dataframe index, metrics,
        and epochs. Then, update the existing plots with the new data instead of recomposing.
        """

        self.selected_df_idx = df_names.index(str(event.pressed.label))
        self.metrics = [i for i in dfs[self.selected_df_idx].columns if i != "epoch"]
        self.epochs = dfs[self.selected_df_idx]["epoch"].to_list()

        # Update existing plots instead of recomposing
        for metric in self.metrics:
            # Find the existing plot
            plot = self.query_one(f"#{metric}_plot", MetricPlot)
            if plot:
                plot.y = dfs[self.selected_df_idx][metric].to_list()
                plot.x = list(range(len(plot.y)))
                plot.replot()

    def action_toggle_min(self) -> None:
        """Toggles minimum value display for all plots."""
        for metric in self.metrics:
            plot = self.query_one(f"#{metric}_plot", MetricPlot)
            if plot:
                plot.toggle_min()

    def action_toggle_max(self) -> None:
        """Toggles maximum value display for all plots."""
        for metric in self.metrics:
            plot = self.query_one(f"#{metric}_plot", MetricPlot)
            if plot:
                plot.toggle_max()


if __name__ == "__main__":
    args = parser.parse_args()

    df_paths = glob(
        os.path.join(args.path, "**", "*_history.csv"),
        recursive=True,
    )
    df_names = [i.split(os.sep)[-1].split("_history")[0] for i in df_paths]
    dfs = [pl.read_csv(i) for i in df_paths]

    app = ExperimentTracker()
    app.run()
