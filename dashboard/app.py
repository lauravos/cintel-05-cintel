from shiny import reactive, render
from shiny.express import ui
import random
from datetime import datetime
from collections import deque
import pandas as pd
import plotly.express as px
from shinywidgets import render_plotly, render_widget
from scipy import stats
from faicons import icon_svg
from ipyleaflet import Map

# SET UP THE REACIVE CONTENT withupdate interval
UPDATE_INTERVAL_SECS: int = 5

#initialize a reactive value with a common data structure to store state (information)
DEQUE_SIZE: int = 10
reactive_value_wrapper = reactive.value(deque(maxlen=DEQUE_SIZE))

# Initialize a REACTIVE CALC that our display components can call
    # The calculation is invalidated every UPDATE_INTERVAL_SECS to trigger updates.
@reactive.calc()
def reactive_calc_combined():
    # Invalidate this calculation every UPDATE_INTERVAL_SECS to trigger updates
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)
    
    # Data generation logic. Get random temps, rounded to 1 decimal place
    temp = round(random.uniform(44, 51), 1)
    # Get a timestamp for "now" and use string format strftime() method to format it
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_dictionary_entry = {"temp": temp, "timestamp": timestamp}
    # get the deque and append the new entry
    reactive_value_wrapper.get().append(new_dictionary_entry)
    # Get a snapshot of the current deque for any further processing
    deque_snapshot = reactive_value_wrapper.get()
    # For Display: Convert deque to DataFrame for display
    df = pd.DataFrame(deque_snapshot)
    # For Display: Get the latest dictionary entry
    latest_dictionary_entry = new_dictionary_entry    
    # Return a tuple with everything we need
    # Every time we call this function, we'll get all these values
    return deque_snapshot, df, latest_dictionary_entry


# Define the Shiny UI Page layout - Page Options
    # Set title to a string in quotes that will appear at the top
    # Set fillable to True to use the whole page width for the UI
ui.page_opts(title="Laura's PyShiny Express: Live Data Example", fillable=True)

# Define the Shiny UI Page layout - Sidebar
with ui.sidebar(open="open", style="background-color:honeydew"):
    ui.h2("Milwaukee, Wisconsin Weather", class_="text-center")
    ui.p(
        "A demonstration of real-time temperature readings in Milwaukee, WI.",
        class_="text-center",
    )

    @render_widget
    def map(width="100%", height="100%"):
        return Map(center=(43.044040,-87.906498), zoom=11)

    ui.hr()
    ui.h6("Links:")
    ui.a(
        "GitHub Source",
        href="https://github.com/lauravos/cintel-05-cintel",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://denisecase.github.io/cintel-05-cintel-basic/",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "PyShiny Express",
        href="hhttps://shiny.posit.co/blog/posts/shiny-express/",
        target="_blank",
    )

    
    
# In Shiny Express, everything not in the sidebar is in the main panel
ui.h2("Current Conditions in Milwaukee")

with ui.layout_columns():
    with ui.value_box(
        showcase=icon_svg("cow"),
        theme="bg-gradient-blue-purple",
    ):

        "Current Temperature"

        @render.text
        def display_temp():
            """Get the latest reading and return a temperature string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['temp']} F"

        "windy conditons"


    with ui.card(full_screen=True, style="background-color: azure"):
        ui.card_header("Current Date and Time", style="background-color: lightsteelblue")

        @render.text
        def display_time():
            """Get the latest reading and return a timestamp string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['timestamp']}"

#with ui.card(full_screen=True, min_height="40%"):
with ui.card(full_screen=True, style="background-color: azure"):
    ui.card_header("Most Recent Readings", style="background-color: lightsteelblue")

    @render.data_frame
    def display_df():
        """Get the latest reading and return a dataframe with current readings"""
        deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
        pd.set_option('display.width', None)        # Use maximum width
        return render.DataGrid( df,width="100%")

with ui.card(style="background-color:honeydew"):
    ui.card_header("Chart with Current Trend", style="background-color: lightsteelblue")

    @render_plotly
    def display_plot():
        # Fetch from the reactive calc function
        deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()

        # Ensure the DataFrame is not empty before plotting
        if not df.empty:
            # Convert the 'timestamp' column to datetime for better plotting
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            # Create scatter plot for readings
            # pass in the df, the name of the x column, the name of the y column, and more
        
            fig = px.scatter(df,
            x="timestamp",
            y="temp",
            title="Temperature Readings with Regression Line",
            labels={"temp (F)": "Temperature (°F)", "timestamp": "Time"},
            color_discrete_sequence=["blue"] )
            
            # Linear regression - we need to get a list of the
            # Independent variable x values (time) and the
            # Dependent variable y values (temp)
            # then, it's pretty easy using scipy.stats.linregress()

            # For x let's generate a sequence of integers from 0 to len(df)
            sequence = range(len(df))
            x_vals = list(sequence)
            y_vals = df["temp"]

            slope, intercept, r_value, p_value, std_err = stats.linregress(x_vals, y_vals)
            df['best_fit_line'] = [slope * x + intercept for x in x_vals]

            # Add the regression line to the figure
            fig.add_scatter(x=df["timestamp"], y=df['best_fit_line'], mode='lines', name='Regression Line')

            # Update layout as needed to customize further
            fig.update_layout(xaxis_title="Time",yaxis_title="Temperature (°F)")

            return fig


