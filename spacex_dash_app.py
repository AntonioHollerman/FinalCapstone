# Import required libraries
import pandas as pd
from dash import callback, Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                         {'label': 'All Sites', 'value': 'ALL'},
                                                     ] + [{'label': name, 'value': name} for name in spacex_df['Launch Site'].unique()],
                                             value='ALL',
                                             placeholder="Select a Launch Site here",
                                             searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart', figure=px.pie(
                                    spacex_df.groupby('Launch Site')['class'].sum().reset_index(),
                                    values='class',
                                    names='Launch Site'))),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={i: str(i) for i in range(0, 10001, 1000)},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart',
                                                   figure=px.scatter(spacex_df, color="Booster Version Category",
                                                                     x='Payload Mass (kg)', y='class',
                                                                     title='Correlation between Payload and '
                                                                           'Success for all Sites'))),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output


@callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_chart(site_selected: str):
    if site_selected == 'ALL':
        fig = px.pie(spacex_df.groupby('Launch Site')['class'].sum().reset_index(),
                     values='class',
                     names='Launch Site')
    else:
        data = spacex_df[spacex_df['Launch Site'] == site_selected]
        data = data['class'].value_counts().reset_index()
        fig = px.pie(data,
                     values='count',
                     names='class')
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


@callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
          [Input(component_id='site-dropdown', component_property='value'),
           Input(component_id='payload-slider', component_property='value')])
def update_plot(site, min_max):
    min_, max_ = min_max
    if site == "ALL":
        data = spacex_df[(spacex_df['Payload Mass (kg)'] <= max_) &
                         (spacex_df['Payload Mass (kg)'] >= min_)]
        title = 'Correlation between Payload and Success for all Sites'
    else:
        data = spacex_df[(spacex_df['Launch Site'] == site) &
                         (spacex_df['Payload Mass (kg)'] <= max_) &
                         (spacex_df['Payload Mass (kg)'] >= min_)]
        title = f'Correlation between Payload and Success for {site}'
    fig = px.scatter(data, color="Booster Version Category", x='Payload Mass (kg)', y='class', title=title)
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
