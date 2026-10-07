# Entry point for development: draws the three charts and runs the tests.
import time_series_visualizer
from unittest import main

# Draw and save the charts
time_series_visualizer.draw_line_plot()
time_series_visualizer.draw_bar_plot()
time_series_visualizer.draw_box_plot()

# Run unit tests automatically
main(module='test_module', exit=False)
