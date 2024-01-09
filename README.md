# TMU_Security_Incidents
## Overview
By collecting security incident data reported by [TMU's Community Safety and Security Website](https://www.torontomu.ca/community-safety-security/security-incidents/list-of-security-incidents/), this project aims to:
- Develop a machine learning model which will forecast incidents.
- Provide insights which can help TMU Security plan and allocate rescources to enhance safety.
- Dashboard all reported incidents into a interactive and customizable view.
- Serve as the basis for future machine learning and NLP projects.

### Packages Used
- Pandas, Selenium, BeautifulSoup4, Seaborn, Vega-Altair, Scikit-Learn, Streamlit

## Data Cleaning & Exploration
A subset of 32 reports are only titled 'Toronto Police Service News Release':
- Incident type had to be extracted from the text found in incident_details.

![alt text](https://github.com/timothycho01/TMU_Security_Incidents/blob/main/readme_visuals/incidents_from_news_releases.png?raw=true)

Location Inconsistencies:
- Ordering:
  - Yonge Street and Gould Street vs Gould Street and Yonge Street

- Renaming:
  - TMU Image Centre vs Ryerson Image Centre

- Level of Precision:
  - Tim Hortons at the Yonge- Dundas Square vs Yonge- Dundas Square
    
- Locations were standardized:
  - Streets of intersections ordered alphabetically
  - Ryerson replaced with TMU
  - Precision reduced to general building or area

### Visuals
![alt text](https://github.com/timothycho01/TMU_Security_Incidents/blob/main/readme_visuals/incidents_by_location.png?raw=true)
![alt text](https://github.com/timothycho01/TMU_Security_Incidents/blob/main/readme_visuals/incidents_by_type.png?raw=true)
![alt text](https://github.com/timothycho01/TMU_Security_Incidents/blob/main/readme_visuals/incidents_by_hour.png?raw=true)
![alt text](https://github.com/timothycho01/TMU_Security_Incidents/blob/main/readme_visuals/incidents_by_weekday.png?raw=true)
![alt text](https://github.com/timothycho01/TMU_Security_Incidents/blob/main/readme_visuals/incidents_by_month.png?raw=true)
![alt text](https://github.com/timothycho01/TMU_Security_Incidents/blob/main/readme_visuals/incidents_by_year.png?raw=true)

## Time Series
### Decomposition
![alt text](https://github.com/timothycho01/TMU_Security_Incidents/blob/main/readme_visuals/decomposition.png?raw=true)

### Monthly Incidents + 12 Month Forecast
![alt text](https://github.com/timothycho01/TMU_Security_Incidents/blob/main/readme_visuals/monthly_history_and_forecast.png?raw=true)

## Streamlit Dashboard
![alt text](https://)

## Future Steps
Content
