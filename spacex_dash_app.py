{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f93cd453",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import required libraries\n",
    "import pandas as pd\n",
    "import dash\n",
    "import dash_html_components as html\n",
    "import dash_core_components as dcc\n",
    "from dash.dependencies import Input, Output\n",
    "import plotly.express as px\n",
    "\n",
    "# Read the airline data into pandas dataframe\n",
    "spacex_df = pd.read_csv(\"spacex_launch_dash.csv\")\n",
    "max_payload = spacex_df['Payload Mass (kg)'].max()\n",
    "min_payload = spacex_df['Payload Mass (kg)'].min()\n",
    "\n",
    "# Create a dash application\n",
    "app = dash.Dash(__name__)\n",
    "\n",
    "# Create an app layout\n",
    "app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',\n",
    "                                        style={'textAlign': 'center', 'color': '#503D36',\n",
    "                                               'font-size': 40}),\n",
    "                                # TASK 1: Add a dropdown list to enable Launch Site selection\n",
    "                                # The default select value is for ALL sites\n",
    "                                dcc.Dropdown(id='site-dropdown',\n",
    "                                options=[\n",
    "                                    {'label': 'All Sites', 'value': 'All Sites'},\n",
    "                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},\n",
    "                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},\n",
    "                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},\n",
    "                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}\n",
    "                                ],\n",
    "                                placeholder='Select a Launch Site Here',\n",
    "                                value='All Sites',\n",
    "                                searchable=True\n",
    "                                ),\n",
    "                                html.Br(),\n",
    "\n",
    "                                # TASK 2: Add a pie chart to show the total successful launches count for all sites\n",
    "                                # If a specific launch site was selected, show the Success vs. Failed counts for the site\n",
    "                                html.Div(dcc.Graph(id='success-pie-chart')),\n",
    "                                html.Br(),\n",
    "\n",
    "                                html.P(\"Payload range (Kg):\"),\n",
    "                                # TASK 3: Add a slider to select payload range\n",
    "                                dcc.RangeSlider(id='payload-slider',\n",
    "                                min=0,\n",
    "                                max=10000,\n",
    "                                step=1000,\n",
    "                                marks={i: '{}'.format(i) for i in range(0, 10001, 1000)},\n",
    "                                value=[min_payload, max_payload]),\n",
    "\n",
    "                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success\n",
    "                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),\n",
    "                                ])\n",
    "\n",
    "# TASK 2:\n",
    "# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output\n",
    "@app.callback( Output(component_id='success-pie-chart', component_property='figure'),\n",
    "               Input(component_id='site-dropdown', component_property='value'))\n",
    "def get_pie_chart(launch_site):\n",
    "    if launch_site == 'All Sites':\n",
    "        fig = px.pie(values=spacex_df.groupby('Launch Site')['class'].mean(), \n",
    "                     names=spacex_df.groupby('Launch Site')['Launch Site'].first(),\n",
    "                     title='Total Success Launches by Site')\n",
    "    else:\n",
    "        fig = px.pie(values=spacex_df[spacex_df['Launch Site']==str(launch_site)]['class'].value_counts(normalize=True), \n",
    "                     names=spacex_df['class'].unique(), \n",
    "                     title='Total Success Launches for Site {}'.format(launch_site))\n",
    "    return(fig)\n",
    "\n",
    "# TASK 4:\n",
    "# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output\n",
    "@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),\n",
    "              [Input(component_id='site-dropdown', component_property='value'),\n",
    "               Input(component_id='payload-slider',component_property='value')])\n",
    "def get_payload_chart(launch_site, payload_mass):\n",
    "    if launch_site == 'All Sites':\n",
    "        fig = px.scatter(spacex_df[spacex_df['Payload Mass (kg)'].between(payload_mass[0], payload_mass[1])], \n",
    "                x=\"Payload Mass (kg)\",\n",
    "                y=\"class\",\n",
    "                color=\"Booster Version Category\",\n",
    "                hover_data=['Launch Site'],\n",
    "                title='Correlation Between Payload and Success for All Sites')\n",
    "    else:\n",
    "        df = spacex_df[spacex_df['Launch Site']==str(launch_site)]\n",
    "        fig = px.scatter(df[df['Payload Mass (kg)'].between(payload_mass[0], payload_mass[1])], \n",
    "                x=\"Payload Mass (kg)\",\n",
    "                y=\"class\",\n",
    "                color=\"Booster Version Category\",\n",
    "                hover_data=['Launch Site'],\n",
    "                title='Correlation Between Payload and Success for Site {}'.format(launch_site))\n",
    "    return(fig)\n",
    "\n",
    "\n",
    "# Run the app\n",
    "if __name__ == '__main__':\n",
    "    app.run_server()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
