import streamlit as st
import pandas as pd
import altair as alt
import ast

dashboard_data = pd.read_csv('dashboard_data.csv')
dashboard_data['extracted_streets'] = dashboard_data['extracted_streets'].apply(ast.literal_eval)
dashboard_data['date_of_incident'] = pd.to_datetime(dashboard_data['date_of_incident'])

incident_selection = alt.selection_point(fields=['incident'], on='click', nearest=True)
location_selection = alt.selection_point(fields=['loi_standardized'], on='click', nearest=True)
month_wday_selection = alt.selection_point(encodings=['x', 'y'])
month_wday_highlight = alt.selection_point()
streets_selection = alt.selection_point(encodings=['x', 'y'])
streets_highlight = alt.selection_point()
doi_interval_selection = alt.selection_interval()

data = dashboard_data.copy(deep=True)
data2 = data.copy(deep=True)

# exploding the list of streets into rows, then split into columns
street_combos = data['extracted_streets'].apply(lambda x: [[x[0], x[-1]], [x[-1], x[0]]])
data_df = pd.DataFrame(street_combos.explode())
data_df[['street_x', 'street_y']] = data_df['extracted_streets'].apply(pd.Series)
data_df.drop('extracted_streets', axis=1, inplace=True)
data = data2.join(data_df)

incidents_by_month = alt.Chart(data).mark_line(point=True).encode(
    x=alt.X('yearmonth(date_of_incident):N', title='Date of Incident'),
    y=alt.Y('distinct(incident_url):Q', title='Reported Incidents'),
    text='distinct(incident_url):Q',
    tooltip=[
        alt.Tooltip('distinct(incident_url):Q', title='Reported Incidents'),
        alt.Tooltip('yearmonth(date_of_incident):N', title='Date of Incident'),
        alt.Tooltip('doi_semester:N', title='Semester of Incident'),
    ],
).add_params(
    doi_interval_selection
).transform_filter(
    incident_selection
).transform_filter(
    month_wday_selection
).transform_filter(
    location_selection
).transform_filter(
    streets_selection
).properties(
    title='Monthly Incidents',
    width=880,
    height=280,
)

month_wday_heatmap = alt.Chart(data).mark_rect().encode(
    x=alt.X('day(date_of_incident):O').title('Weekday of Incident'),
    y=alt.Y('month(date_of_incident):O').title('Month of Incident'),
    # color=alt.Color('distinct(incident_url):Q', title=''),
    color=alt.condition(month_wday_selection, 'distinct(incident_url):Q', alt.value('lightgrey'), title=''),
    tooltip=[
        alt.Tooltip('distinct(incident_url):Q', title='Reported Incidents'),
        alt.Tooltip('month(date_of_incident):N', title='Month of Incident'),
        alt.Tooltip('day(date_of_incident):N', title='Weekday of Incident'),
    ],
).add_params(
    month_wday_selection
).transform_filter(
    incident_selection
).transform_filter(
    doi_interval_selection
).transform_filter(
    location_selection
).transform_filter(
    streets_selection
).properties(
    title='Month & Weekday of Incident',
    width=400,
    height=280,
)

incident_type_bar = alt.Chart(data).mark_bar().encode(
    x=alt.X('distinct(incident_url):Q', title='Reported Incidents'),
    y=alt.Y('incident:N', title='', axis=alt.Axis(labelLimit=200)).sort('-x'),
    color=alt.condition(incident_selection, 'incident:N', alt.value('lightgrey')),
    text='distinct(incident_url):Q',
    tooltip=[
        alt.Tooltip('distinct(incident_url):Q', title='Reported Incidents'),
        alt.Tooltip('incident:N', title='Incident Type'),
    ],
).add_params(
    incident_selection
).transform_filter(
    doi_interval_selection
).transform_filter(
    location_selection
).transform_filter(
    month_wday_selection
).transform_filter(
    streets_selection
).properties(
    title='Type of Incident',
    width=200,
    height=490,
)

incident_type_by_hour = alt.Chart(data).mark_bar().encode(
    x=alt.X('distinct(incident_url):Q', title=''),
    y=alt.Y('hours(date_of_incident):N', title=''),
    color=alt.Color('distinct(incident_url):Q', title=''),
    text='distinct(incident_url):Q',
    tooltip=[
        alt.Tooltip('distinct(incident_url):Q', title='Reported Incidents'),
        alt.Tooltip('hours(date_of_incident):N', title='Hour of Incident'),
    ],
).transform_filter(
    incident_selection
).transform_filter(
    doi_interval_selection
).transform_filter(
    location_selection
).transform_filter(
    month_wday_selection
).transform_filter(
    streets_selection
).properties(
    title='Hour of Incident',
    width=150,
    height=490
)

incident_type_by_month = alt.Chart(data).mark_bar().encode(
    x=alt.X('distinct(incident_url):Q', title=''),
    y=alt.Y('month(date_of_incident):N', title=''),
    color=alt.Color('distinct(incident_url):Q', title=''),
    text='distinct(incident_url):Q',
    tooltip=[
        alt.Tooltip('distinct(incident_url):Q', title='Reported Incidents'),
        alt.Tooltip('month(date_of_incident):N', title='Month of Incident'),
        alt.Tooltip('doi_semester:N', title='Semester of Incident'),
    ],
).transform_filter(
    incident_selection
).transform_filter(
    doi_interval_selection
).transform_filter(
    location_selection
).transform_filter(
    month_wday_selection
).transform_filter(
    streets_selection
).properties(
    title='Month of Incident',
    width=150,
    height=490
)

incident_type_by_year = alt.Chart(data).mark_bar().encode(
    x=alt.X('distinct(incident_url):Q', title=''),
    y=alt.Y('year(date_of_incident):N', title=''),
    color=alt.Color('distinct(incident_url):Q', title=''),
    text='distinct(incident_url):Q',
    tooltip=[
        alt.Tooltip('distinct(incident_url):Q', title='Reported Incidents'),
        alt.Tooltip('year(date_of_incident):N', title='Year of Incident'),
    ],
).transform_filter(
    incident_selection
).transform_filter(
    doi_interval_selection
).transform_filter(
    location_selection
).transform_filter(
    month_wday_selection
).transform_filter(
    streets_selection
).properties(
    title='Year of Incident',
    width=150,
    height=490
)


incidents_by_loc_base = alt.Chart(data).mark_bar().encode(
    y=alt.Y('distinct(incident_url):Q', title='Reported Incidents'),
    x=alt.X('loi_standardized:N', title='', axis=alt.Axis(labelLimit=200)).sort('-y'),
).add_params(
    location_selection
).transform_filter(
    incident_selection
).transform_filter(
    doi_interval_selection
).transform_filter(
    month_wday_selection
).transform_filter(
    streets_selection
).properties(
    title='Location of Incident',
    width=1100,
    height=300,
)

incidents_by_loc = incidents_by_loc_base.encode(
    color=alt.condition(location_selection, 'incident:N', alt.value('lightgrey'), legend=None),
    tooltip=[
        alt.Tooltip('distinct(incident_url):Q', title='Reported Incidents'),
        alt.Tooltip('loi_standardized:N', title='Location of Incident'),
        alt.Tooltip('incident:N', title='Incident Type'),
    ],
)

incidents_by_loc_text = incidents_by_loc_base.encode(
    text='distinct(incident_url):Q',
)

streets_chart = alt.Chart(data).mark_rect().encode(
    x=alt.X('street_x:O', title=''),
    y=alt.Y('street_y:O', title=''),
    color=alt.condition(streets_selection, 'distinct(incident_url):Q', alt.value('lightgrey'), title=''),
    tooltip=[
        alt.Tooltip('distinct(incident_url):Q', title='Reported Incidents'),
        alt.Tooltip('loi_standardized:N', title='Location of Incident'),
    ],
).properties(
    title='Street Intersections Reported As Location of Incident',
    width=490,
    height=490,
).add_params(
    streets_selection
).transform_filter(
    (alt.datum.street_x != 'building') & (alt.datum.street_y != 'building')
).transform_filter(
    incident_selection
).transform_filter(
    location_selection
).transform_filter(
    doi_interval_selection
).transform_filter(
    month_wday_selection
)


incident_type_bar = incident_type_bar + incident_type_bar.mark_text(align='left', dx=3)
incidents_by_loc = incidents_by_loc + incidents_by_loc_text.mark_text(align='center', dy=-6)

row_1 = incidents_by_month | month_wday_heatmap
row_2 = incident_type_bar | incidents_by_loc
row_3 = incident_type_by_hour | incident_type_by_month | incident_type_by_year | streets_chart
#
dashboard_visuals = row_1 & row_2 & row_3.resolve_scale(
    color='independent'
)


def dashboard():
    st.set_page_config(layout="wide")
    st.title('Security Incidents @ TMU')
    with st.expander('About this dashboard:'):
        st.markdown('''
        :orange[Github:] https://github.com/timothycho01/TMU_Security_Incidents

        :orange[Data Last Updated:] 2023-12-31
        
        :orange[Data Source:] https://www.torontomu.ca/community-safety-security/security-incidents/list-of-security-incidents/
        ''')
    with st.expander('User Interaction:', expanded=True):
        st.markdown('''
        - :orange[multi-select:] hold shift + click
        - :orange[time interval:] click and drag, scroll to widen/narrow
        - :orange[clear selections:] double-click
        ''')
    dashboard_visuals

if __name__ == "__main__":
    dashboard()
