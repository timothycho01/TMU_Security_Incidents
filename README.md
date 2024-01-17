# TMU_Security_Incidents
## Overview
By collecting security incident data reported by [TMU's Community Safety and Security Site](https://www.torontomu.ca/community-safety-security/security-incidents/list-of-security-incidents/), this project aims to:
- Forecast monthly incidents using SARIMAX for the upcoming year.
- Dashboard all reported incident data into an interactive view.
- Provide insights which can help TMU Security plan and allocate rescources to enhance safety.
- Serve as the basis for future machine learning and NLP projects.

### Packages Used
- Pandas, Selenium, BeautifulSoup4, Seaborn, statsmodels, Streamlit, Vega-Altair

## Results

### Streamlit Dashboard
https://tmu-security-incidents-dashboard.streamlit.app/

  <details>
  <summary>Preview</summary>
    
  ![alt text](https://github.com/timothycho01/TMU_Security_Incidents/blob/main/readme_visuals/dashboard.png?raw=true)
  
  </details>

![alt text](https://github.com/timothycho01/TMU_Security_Incidents/blob/main/readme_visuals/dashboard_demo.gif?raw=true)

### Monthly Forecast
![alt text](https://github.com/timothycho01/TMU_Security_Incidents/blob/main/readme_visuals/monthly_history_and_forecast.png?raw=true)

# Process Walkthrough
## Data Cleaning & Exploration
A subset of 32 reports are only titled 'Toronto Police Service News Release':
- Incident type had to be extracted from the text found in incident_details by keyword/phrase mapping.

![alt text](https://github.com/timothycho01/TMU_Security_Incidents/blob/main/readme_visuals/incidents_from_news_releases.png?raw=true)

Location Inconsistencies:
- Ordering:
  - Yonge Street and Gould Street vs Gould Street and Yonge Street.

- Renaming:
  - TMU Image Centre vs Ryerson Image Centre.

- Level of Precision:
  - Tim Hortons at the Yonge- Dundas Square vs Yonge- Dundas Square.
    
- Locations were standardized by the following:
  - Streets of intersections ordered alphabetically.
  - Ryerson replaced with TMU.
  - Precision reduced to general building or area.
  - Spelling errors corrected.

### Visuals
![alt text](https://github.com/timothycho01/TMU_Security_Incidents/blob/main/readme_visuals/incidents_by_location.png?raw=true)
![alt text](https://github.com/timothycho01/TMU_Security_Incidents/blob/main/readme_visuals/incidents_by_type.png?raw=true)
![alt text](https://github.com/timothycho01/TMU_Security_Incidents/blob/main/readme_visuals/incidents_by_hour.png?raw=true)
![alt text](https://github.com/timothycho01/TMU_Security_Incidents/blob/main/readme_visuals/incidents_by_weekday.png?raw=true)
![alt text](https://github.com/timothycho01/TMU_Security_Incidents/blob/main/readme_visuals/incidents_by_month.png?raw=true)
![alt text](https://github.com/timothycho01/TMU_Security_Incidents/blob/main/readme_visuals/incidents_by_year.png?raw=true)

## Time Series Analysis
### Decomposition
![alt text](https://github.com/timothycho01/TMU_Security_Incidents/blob/main/readme_visuals/decomposition.png?raw=true)

### Monthly Incidents + 12 Month Forecast
![alt text](https://github.com/timothycho01/TMU_Security_Incidents/blob/main/readme_visuals/monthly_history_and_forecast.png?raw=true)

## Work in Progress - NLP + K-means clustering 
- Endcoding entities in incident_details
  <details open>
  <summary>Example</summary>

  ```
  'tmu community members': 'TMU_MEMBER',
  'tmu community member': 'TMU_MEMBER',
  'ryerson community members': 'TMU_MEMBER',
  'ryerson community member': 'TMU_MEMBER',
  'community members': 'TMU_MEMBER',
  'community member': 'TMU_MEMBER',

  'tmu community guests': 'TMU_GUEST',
  'tmu community guest': 'TMU_GUEST',
  'ryerson community guests': 'TMU_GUEST',
  'ryerson community guest': 'TMU_GUEST',
  'community guests': 'TMU_GUEST',
  'community guest': 'TMU_GUEST',

  'tmu security': 'TMU_SECURITY',
  'ryerson security': 'TMU_SECURITY',
  'security': 'TMU_SECURITY',

  'members of the public': 'MEMBER_OF_THE_PUBLIC',
  'member of the public': 'MEMBER_OF_THE_PUBLIC',
  'members of public': 'MEMBER_OF_THE_PUBLIC',
  'member of public': 'MEMBER_OF_THE_PUBLIC',

  'individual' : 'INDIVIDUAL',
  'individuals' : 'INDIVIDUAL',

  'toronto police services': 'TORONTO_POLICE_SERVICES',
  'toronto police service': 'TORONTO_POLICE_SERVICES',
  'toronto police': 'TORONTO_POLICE_SERVICES',
  ' tps ': ' TORONTO_POLICE_SERVICES ',
  'police officers': 'TORONTO_POLICE_SERVICES',
  'police officer': 'TORONTO_POLICE_SERVICES',
  'police': 'TORONTO_POLICE_SERVICES',
  'officers': 'TORONTO_POLICE_SERVICES',
  'officer': 'TORONTO_POLICE_SERVICES',

  'toronto paramedic services': 'TORONTO_PARAMEDIC_SERVICES',
  'toronto paramedic service': 'TORONTO_PARAMEDIC_SERVICES',
  'paramedics': 'TORONTO_PARAMEDIC_SERVICES',
  'paramedic': 'TORONTO_PARAMEDIC_SERVICES',
  ```
  </details>
- Extract features from sentences based on Part-of-speech tagging in relation to entity
- TF-IDF
- K-means clustering
