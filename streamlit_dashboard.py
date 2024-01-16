import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import altair as alt
import ast

dashboard_data = pd.read_csv('dashboard_data.csv')
dashboard_data['extracted_streets'] = dashboard_data['extracted_streets'].apply(ast.literal_eval)
dashboard_data['date_of_incident'] = pd.to_datetime(dashboard_data['date_of_incident'])

domain_types = list(dashboard_data['incident'].value_counts().reset_index()['incident'])
tableau_16 = """
#4c78a8ff
#ff9d98ff
#79706eff
#f2cf5bff
#d67195ff
#f58519ff
#439895ff
#fcbfd2ff
#ffbf78ff
#bab0acff
#54a24aff
#b79a20ff
#9ecae9ff
#83bcb6ff
#88d27aff
#e45756ff
""".strip().split('\n')

incident_selection = alt.selection_point(fields=['incident'], on='click', nearest=True)
hour_selection = alt.selection_point(encodings=['y'])
month_selection = alt.selection_point(encodings=['y'])
year_selection = alt.selection_point(encodings=['y'])
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
    x=alt.X('yearmonth(date_of_incident):N', title='Month of Incident'),
    y=alt.Y('distinct(incident_url):Q', title='Reported Incidents'),
    text='distinct(incident_url):Q',
    tooltip=[
        alt.Tooltip('distinct(incident_url):Q', title='Reported Incidents'),
        alt.Tooltip('yearmonth(date_of_incident):N', title='Date of Incident'),
        alt.Tooltip('doi_semester:N', title='Semester of Incident'),
    ],
).properties(
    title='Monthly Incidents',
    width=950,
    height=280,
).add_params(
    doi_interval_selection
)

totals = alt.Chart(data).mark_text(
    fontSize=23,
).encode(
    text='distinct(incident_url):Q',
).properties(
    title='Total Incidents',
    width=50,
).transform_filter(
    incident_selection
).transform_filter(
    doi_interval_selection
).transform_filter(
    location_selection
).transform_filter(
    streets_selection
).transform_filter(
    month_wday_selection
).transform_filter(
    hour_selection
).transform_filter(
    month_selection
).transform_filter(
    year_selection
)

total_types = alt.Chart(data).mark_text(
    fontSize=23,
).encode(
    text='distinct(incident):Q',
).properties(
    title='Incident Types',
    width=50,
).transform_filter(
    incident_selection
).transform_filter(
    doi_interval_selection
).transform_filter(
    location_selection
).transform_filter(
    streets_selection
).transform_filter(
    month_wday_selection
).transform_filter(
    hour_selection
).transform_filter(
    month_selection
).transform_filter(
    year_selection
)

earliest = alt.Chart(data).mark_text(
    fontSize=20,
    align='center',
).encode(
    text='min(date_of_incident):T',
).properties(
    title='Earliest Incident',
    width=70,
).transform_filter(
    incident_selection
).transform_filter(
    doi_interval_selection
).transform_filter(
    location_selection
).transform_filter(
    streets_selection
).transform_filter(
    month_wday_selection
).transform_filter(
    hour_selection
).transform_filter(
    month_selection
).transform_filter(
    year_selection
)

latest = alt.Chart(data).mark_text(
    fontSize=20,
    align='center',
).encode(
    text='max(date_of_incident):T',
).properties(
    title='Latest Incident',
    width=70,
).transform_filter(
    incident_selection
).transform_filter(
    doi_interval_selection
).transform_filter(
    location_selection
).transform_filter(
    streets_selection
).transform_filter(
    month_wday_selection
).transform_filter(
    hour_selection
).transform_filter(
    month_selection
).transform_filter(
    year_selection
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
).properties(
    title='Month & Weekday of Incident',
    width=300,
    height=280,
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
).transform_filter(
    hour_selection
).transform_filter(
    month_selection
).transform_filter(
    year_selection
)

incident_type_bar = alt.Chart(data).mark_bar().encode(
    x=alt.X('distinct(incident_url):Q', title='Reported Incidents'),
    y=alt.Y('incident:N', title='', axis=alt.Axis(labelLimit=200)).sort('-x'),
    color=alt.condition(
        incident_selection,
        alt.Color('incident:N').scale(
            domain=domain_types, range=tableau_16
        ), alt.value('lightgrey')
    ),
    text='distinct(incident_url):Q',
    tooltip=[
        alt.Tooltip('distinct(incident_url):Q', title='Reported Incidents'),
        alt.Tooltip('incident:N', title='Incident Type'),
    ],
).properties(
    title='Type of Incident',
    width=200,
    height=490,
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
).transform_filter(
    hour_selection
).transform_filter(
    month_selection
).transform_filter(
    year_selection
)

incident_type_by_hour = alt.Chart(data).mark_bar().encode(
    x=alt.X('distinct(incident_url):Q', title=''),
    y=alt.Y('hours(date_of_incident):N', title=''),
    color=alt.condition(hour_selection, 'distinct(incident_url):Q', alt.value('lightgrey'), title=''),
    text='distinct(incident_url):Q',
    tooltip=[
        alt.Tooltip('distinct(incident_url):Q', title='Reported Incidents'),
        alt.Tooltip('hours(date_of_incident):N', title='Hour of Incident'),
    ],
).properties(
    title='Hour of Incident',
    width=150,
    height=490
).add_params(
    hour_selection
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
).transform_filter(
    month_selection
).transform_filter(
    year_selection
)

incident_type_by_month = alt.Chart(data).mark_bar().encode(
    x=alt.X('distinct(incident_url):Q', title=''),
    y=alt.Y('month(date_of_incident):N', title=''),
    color=alt.condition(month_selection, 'distinct(incident_url):Q', alt.value('lightgrey'), title=''),
    text='distinct(incident_url):Q',
    tooltip=[
        alt.Tooltip('distinct(incident_url):Q', title='Reported Incidents'),
        alt.Tooltip('month(date_of_incident):N', title='Month of Incident'),
        alt.Tooltip('doi_semester:N', title='Semester of Incident'),
    ],
).properties(
    title='Month of Incident',
    width=150,
    height=490
).add_params(
    month_selection
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
).transform_filter(
    hour_selection
).transform_filter(
    year_selection
)

incident_type_by_year = alt.Chart(data).mark_bar().encode(
    x=alt.X('distinct(incident_url):Q', title=''),
    y=alt.Y('year(date_of_incident):N', title=''),
    color=alt.condition(year_selection, 'distinct(incident_url):Q', alt.value('lightgrey'), title=''),
    text='distinct(incident_url):Q',
    tooltip=[
        alt.Tooltip('distinct(incident_url):Q', title='Reported Incidents'),
        alt.Tooltip('year(date_of_incident):N', title='Year of Incident'),
    ],
).properties(
    title='Year of Incident',
    width=150,
    height=490
).add_params(
    year_selection
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
).transform_filter(
    hour_selection
).transform_filter(
    month_selection
)


incidents_by_loc_base = alt.Chart(data).mark_bar().encode(
    y=alt.Y('distinct(incident_url):Q', title='Reported Incidents'),
    x=alt.X('loi_standardized:N', title='', axis=alt.Axis(labelLimit=200)).sort('-y'),
).properties(
    title='Location of Incident',
    width=1100,
    height=300,
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
).transform_filter(
    hour_selection
).transform_filter(
    month_selection
).transform_filter(
    year_selection
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
).transform_filter(
    hour_selection
).transform_filter(
    month_selection
).transform_filter(
    year_selection
)

data[['latitude', 'longitude']] = data['coordinates'].apply(lambda x: pd.Series(str(x).split(', ')) if x else pd.Series([0, 0]))

map_select = alt.selection_interval()

map_chart = alt.Chart(data).mark_circle().encode(
    longitude='longitude:Q',
    latitude='latitude:Q',
    tooltip=[
        alt.Tooltip('distinct(incident_url)', title='incidents'),
        alt.Tooltip('loi_standardized', title='location'),
    ]
).properties(
    width=700,
    height=700
).transform_filter(
    (alt.datum.coordinates)
).project(
    "albers"
)

vis_layer = map_chart.mark_circle(size=450).encode(
    color=alt.Color('distinct(incident_url)', title='incidents'),
)

gy_label = map_chart.mark_text(align='center', dy=-7, dx=-44, lineBreak=r'and').encode(
    text='loi_standardized',
).transform_filter(
    (alt.datum.loi_standardized == 'gould street and yonge street')
)

dy_label = map_chart.mark_text(align='center', dy=-10, dx=-45, lineBreak=r'and').encode(
    text='loi_standardized',
).transform_filter(
    (alt.datum.loi_standardized == 'dundas street and yonge street')
)

kh_label = map_chart.mark_text(align='center', dx=-32, dy=0).encode(
    text='loi_standardized',
).transform_filter(
    (alt.datum.loi_standardized == 'kerr hall')
)

dv_label = map_chart.mark_text(align='center', dx=-45, dy=-16, lineBreak=r'and').encode(
    text='loi_standardized',
).transform_filter(
    (alt.datum.loi_standardized == 'dundas street east and victoria street')
)

bg_label = map_chart.mark_text(align='center', dx=-41, dy=-12, lineBreak=r'and').encode(
    text='loi_standardized',
).transform_filter(
    (alt.datum.loi_standardized == 'bond street and gould street')
)

incident_map = vis_layer + gy_label + dy_label + dv_label + bg_label + kh_label

incident_type_bar = incident_type_bar + incident_type_bar.mark_text(align='left', dx=3)
incidents_by_loc = incidents_by_loc + incidents_by_loc_text.mark_text(align='center', dy=-6)

cards = totals | total_types | earliest | latest

row_1 = incidents_by_month | month_wday_heatmap
row_2 = incident_type_bar | incidents_by_loc
row_3 = incident_type_by_hour | incident_type_by_month | incident_type_by_year | streets_chart
#
dashboard_visuals = cards & row_1.resolve_scale(
    color='independent'
) & row_2 & row_3.resolve_scale(
    color='independent'
)


def dashboard():
    st.set_page_config(layout="wide")
    st.title('Security Incidents @ TMU')
    col1, col2 = st.columns([6, 5])

    with col1:
        st.write('')
        st.write('')
        st.markdown('''
        :orange[Github:] https://github.com/timothycho01/TMU_Security_Incidents

        :orange[Data Last Updated:] 2023-12-31
        
        :orange[Data Source:] https://www.torontomu.ca/community-safety-security/security-incidents/list-of-security-incidents/
        ''')

    with col2:
        tab1, tab2 = st.tabs(["User Interaction", "Visual Demo"])

        with tab1:
            st.markdown('''
            - :orange[multi-select:] hold shift + click
            - :orange[time interval:] click and drag, scroll to widen/narrow
            - :orange[clear selections:] double-click
            ''')
        with tab2:
            st.image('readme_visuals/dashboard_demo.gif')

    st.subheader('Dashboard', anchor='dashboard')
    with st.expander('Show/Hide:', expanded=True):

        st.altair_chart(dashboard_visuals, theme=None)

    st.subheader('Incident Maps', anchor='incident-maps')
    with st.expander('Show/Hide:', expanded=True):
        st.markdown('Note: Map does not have any cross-filtering.')

        tab1, tab2, tab3 = st.tabs(["Folium Map", "Altair Map", "Unmapped Records"])
        with tab1:
            st.markdown('''
            - :orange[pan:] click + drag
            - :orange[zoom:] scroll
            ''')

            with open('dashboard_heatmap.html', 'r') as f:
                html_data = f.read()

            components.html(html_data, height=1200)
        with tab2:
            st.markdown('''
            - :orange[more details:] hover over points.
            ''')
            st.altair_chart(incident_map, theme=None)

        with tab3:
            st.markdown('''
            Following records excluded because:
            - not a physical location.
            - not an intersection (i.e., two parallel streets).
            - ambiguous (ex: parking garage, tmu campus).
            ''')
            unmapped = dashboard_data[dashboard_data['coordinates'].isna()]
            cols = ['date_of_incident', 'incident', 'loi_standardized', 'incident_details', 'incident_url']
            st.data_editor(
                unmapped[cols],
                column_config={
                    "incident_url": st.column_config.LinkColumn("incident_url")
                },
                hide_index=True,
                use_container_width=True,
                disabled=True,
            )

    st.subheader('Data Table', anchor='data-table')
    with st.expander('Show/Hide', expanded=False):
        st.markdown('Note: Table does not have any cross-filtering.')
        cols = ['date_of_incident', 'incident', 'loi_standardized', 'incident_details', 'incident_url']
        st.data_editor(
            dashboard_data[cols],
            column_config={
                "incident_url": st.column_config.LinkColumn("incident_url")
            },
            hide_index=True,
            use_container_width=True,
            disabled=True,
        )


if __name__ == "__main__":
    dashboard()
