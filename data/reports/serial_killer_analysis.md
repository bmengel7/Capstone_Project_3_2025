# Serial Killer Data Analysis Report
Generated: 2025-03-25 20:26:31

## Dataset Overview
- Total records: 305
- Total columns: 14


## Temporal Analysis

### Activity Period Statistics
- Earliest recorded activity start: 1880
- Latest recorded activity start: 2016
- Earliest recorded activity end: 1906
- Latest recorded activity end: 2018
- Median activity start year: 1984
- Median activity end year: 1992

![Killers by Decade](charts/killers_by_decade.png)

### Activity Duration
- Average activity duration: 8.3 years
- Median activity duration: 5.0 years
- Maximum activity duration: 53.0 years
![Activity Duration](charts/activity_duration_distribution.png)


## Victim Analysis

### Victim Count Statistics
- Average victim count: 36.5
- Median victim count: 25.0
- Maximum victim count: 300

![Victim Count Distribution](charts/victim_count_distribution.png)

![Average Victims by Decade](charts/victims_by_decade.png)

### Cases with Potential Additional Victims
- 81 cases (26.6%) likely have additional undiscovered victims

![More Victims Possible](charts/more_victims_possible_pie.png)

![Victims by More Possible](charts/victims_by_more_possible.png)


## Efficiency Analysis

### Victims per Year Statistics
- Average victims per year: 8.22
- Median victims per year: 4.44
- Maximum victims per year: 50.00

![Victims per Year Distribution](charts/victims_per_year_distribution.png)

![Duration vs Victims](charts/duration_vs_victims_scatter.png)


## Categorical Analysis

### Identified 2 categorical variables for analysis

#### Analysis of 'source_file'
- Total unique values: 4
- Top values:
  - 5_to_14_victim_count.xlsx: 164 cases (53.8%)
  - 15_to_30_victim_count.xlsx: 78 cases (25.6%)
  - Highest_victim_count.xlsx: 34 cases (11.1%)
  - Lessthan_5_victim_count.xlsx: 29 cases (9.5%)
![source_file Distribution](charts/source_file_distribution.png)

![source_file Victims Boxplot](charts/source_file_victims_boxplot.png)

#### Analysis of 'more_victims_possible'
- Total unique values: 2
- Top values:
  - No: 224 cases (73.4%)
  - Yes: 81 cases (26.6%)
![more_victims_possible Distribution](charts/more_victims_possible_distribution.png)

![more_victims_possible Victims Boxplot](charts/more_victims_possible_victims_boxplot.png)


## Geographic Analysis

### Analysis by Country
- Total unique locations: 74
- Top locations:
  - United States: 92 cases (30.2%)
  - Russia: 21 cases (6.9%)
  - South Africa: 19 cases (6.2%)
  - Soviet Union: 13 cases (4.3%)
  - United Kingdom: 12 cases (3.9%)
  - India: 10 cases (3.3%)
  - China: 9 cases (3.0%)
  - Brazil: 8 cases (2.6%)
  - France: 6 cases (2.0%)
  - Italy: 6 cases (2.0%)
  - Canada: 5 cases (1.6%)
  - Australia: 5 cases (1.6%)
  - Soviet Union_x000D_
Russia: 4 cases (1.3%)
  - Colombia: 4 cases (1.3%)
  - South Korea: 4 cases (1.3%)
![Country Distribution](charts/country_distribution.png)

![Country Victims Boxplot](charts/country_victims_boxplot.png)


## Correlation Analysis

### Correlation Matrix
![Correlation Matrix](charts/correlation_matrix.png)

### Strongest Correlations
- from_year and decade: 0.994
- from_year and to_year: 0.949
- to_year and decade: 0.943
- active_duration and victims_per_year: -0.457
- number_possible_victims and victims_per_year: 0.363


## Summary Statistics Tables

### Numeric Variables

| Variable | Count | Mean | Std | Min | 25% | Median | 75% | Max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| from_year | 305 | 1978.13 | 26.49 | 1880.00 | 1972.00 | 1984.00 | 1996.00 | 2016.00 |
| to_year | 305 | 1985.42 | 25.45 | 1906.00 | 1979.00 | 1992.00 | 2003.00 | 2018.00 |
| active_duration | 305 | 8.28 | 8.37 | 1.00 | 2.00 | 5.00 | 12.00 | 53.00 |
| number_possible_victims | 81 | 36.54 | 41.39 | 3.00 | 15.00 | 25.00 | 40.00 | 300.00 |
| decade | 305 | 1973.80 | 26.47 | 1880.00 | 1970.00 | 1980.00 | 1990.00 | 2010.00 |
| victims_per_year | 81 | 8.22 | 10.04 | 0.24 | 2.08 | 4.44 | 10.00 | 50.00 |
