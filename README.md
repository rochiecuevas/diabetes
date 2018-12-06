# ETL of 2012 and 2014 data on adult diabetes and childhood obesity from the Centres for Disease Control and Prevention

## Introduction

## Methodology
Three Jupyter notebooks were used for extracting, transforming, and loading the diabetes and obesity data:

1. [Clean_Chronic_Disease_indicators.ipynb](https://github.com/rochiecuevas/diabetes/blob/master/Clean_Chronic_Disease_indicators.ipynb)
2. [Clean_Nutrition_Data.ipynb](https://github.com/rochiecuevas/diabetes/blob/master/Clean_Nutrition_Data.ipynb)
3. [Join_obesity_diabetes_tables.ipynb](https://github.com/rochiecuevas/diabetes/blob/master/Join_obesity_diabetes_tables.ipynb)

In addition, the MySQL database __diabetes_db__ was created using the [Diabetes.sql](https://github.com/rochiecuevas/diabetes/blob/master/Diabetes.sql) script. On the other hand, a Flask app ([diabetes_app.py](https://github.com/rochiecuevas/diabetes/blob/master/diabetes_app.py)) was developed to display the table and plots generated from the data onto html. This app is not yet online and currently lives on the localhost upon download. The code for these plots are found in  [Join_obesity_diabetes_tables.ipynb](https://github.com/rochiecuevas/diabetes/blob/master/Join_obesity_diabetes_tables.ipynb). 

### Extraction
Data was extracted from two datasets provided by the CDC: (1) on [chronic disease indicators](https://catalog.data.gov/dataset/u-s-chronic-disease-indicators-cdi) in the U.S.A. and (2) on [nutrition, physical activity, and obesity in women, infants, and children](https://catalog.data.gov/dataset/nutrition-physical-activity-and-obesity-women-infant-and-child-dfe5d/resource/415dca15-b90a-46c3-8d13-70322ee4628e).

Both datasets were downloaded as csv files and extracted using Python (version 3.6) [Pandas](https://pandas.pydata.org/pandas-docs/stable/) module in separate Jupyter Notebooks. 

```python
# Dependencies
import pandas as pd
```

The [chronic diseases indicators](https://drive.google.com/open?id=1QLxhiRwirRHE_AO_6p53Yv1QJ0Ei1K2f) file contains the statistics for __diabetes__ prevalence in adults 18+ years old. On the other hand, the data for occurrence of __obesity__ in children 2–4 years old are found in the [nutrition, physical activity, and obesity](https://drive.google.com/open?id=1lzKsXYhbfvTQ_lWLI_8ejOAeVgkvMt59) file. 

```python
# Load CSV file as dataframe
    # The csv files are stored locally in a Resources folder. But because they exceed GitHub's file size requirement, 
    # links to the Google Drive copy of the files are provided.
diseasedata = pd.read_csv("Resources/U.S._Chronic_Disease_Indicators__CDI_.csv")

nutr_df = pd.read_csv("Resources/Nutrition__Physical_Activity__and_Obesity_-_Women__Infant__and_Child.csv")
```

### Transformation
#### Filtering the dataframe for the most relevant columns
The columns of interest in __diseasedata__ were those that provided information about the crude prevalence of adult diabetes in 2012 and in 2014. Hence, the dataframe __chronic_df__ was generated as follows:

```python
chronic_df = diseasedata[["YearEnd", "LocationDesc", "Topic", "Question", "DataValueUnit", "DataValueType", 
"DataValue", "Stratification1"]]
```

The columns of interest in __nutr_df__ provided information about obesity in children 2–4 years old in 2012 and in 2014. Therefore, the next iteration of the dataframe was generated with the following code.

```python
nutr_df2 = nutr_df[["YearEnd", "LocationDesc", "Question", "Data_Value", "StratificationID1"]]
```

#### Select the values for 2010, 2012, and 2014
Originally, this project intended to extract data for three years (2010, 2012, and 2014). Hence, the codes used to subset the dataframes for the identified years were:

```python
Years = [2010, 2012, 2014]
chronic_df2 = chronic_df[chronic_df["YearEnd"].isin(Years)]
nutr_df3 = nutr_df2[nutr_df2["YearEnd"].isin(Years)]
```

#### Select diabetes as the chronic disease of interest
There were numerous chronic diseases in the __chronic_df__ dataframe. Because diabetes in adults was of interest, rows pertaining for this disease were selected:

```python
chronic_df3 = chronic_df2[chronic_df2["Topic"] == "Diabetes"]
```

Obesity was not selected in the __nutr_df__ dataframe because all rows were associated with obesity and weight status.

#### Select rows on US states and territories
The chronic diseases dataframe featured data for each U.S. state and territory and country-wide data. The country-wide data was removed from the dataframe since this project was focused only on data from the different states and territories.

```python
chronic_df4 = chronic_df3[chronic_df3["LocationDesc"]!="United States"]
```

This step was not performed in the nutrition dataframe because it did not contain country-wide data; just for each state and territory.

#### Select rows with no stratification (value = "Overall")
The values to be presented were for overall prevalence. Hence, the other stratification (e.g., age, gender, ethnicity) were filtered out. For the latest iteration of __nutr_df__, the dataframe was also filtered for the target question (obesity in 2–4 year-old children). For the latest iteration of __chronic_df__, rows pertaining to crude prevalence were retained.

```python
nutr_df4 = nutr_df3.query("StratificationID1 == 'OVERALL'& \
                          Question == 'Percent of WIC children aged 2 to 4 years who have obesity'")

chronic_df5 = chronic_df4.query("DataValueType == 'Crude Prevalence' & Stratification1 == 'Overall'")
```

The filtering of __chronic_df__ was refined by selecting the prevalence of diabetes in adults 18+ years.

```python
chronic_df6 = chronic_df5[chronic_df5["Question"] == "Prevalence of diagnosed diabetes \
among adults aged >= 18 years"]
```

#### Removal of columns that showed the same information
After all the filtering, the latest iteration of the dataframes, __nutr_df4__ and __chronic_df6__, contained category columns that contained the same values in their rows. Hence, these columns had to be removed and their values were used as names of the data columns.

```python
# Rename columns for clarity
chronic_df6 = chronic_df6.rename(columns = {"YearEnd": "Year",
                                            "LocationDesc": "US_State",
                                            "DataValue": "Adult_Diabetics_Percent"})

nutr_df4 = nutr_df4.rename(columns = {"YearEnd": "Year",
                                      "LocationDesc": "US_State",
                                      "Data_Value": "Obese_Children_Percent"})

# Further clean the dataset
chronic_df7 = chronic_df6[["Year", "US_State", "Adult_Diabetics_Percent"]]
nutr_df4 = nutr_df4[["YearEnd", "LocationDesc", "Data_Value"]]
```

### Creating a database
The nutrition and the chronic dataframes could now loaded into the __diabetes_db__ which has been written in [MySQL](https://dev.mysql.com/doc/refman/8.0/en/). Two tables were created in this database: (1) obesity; and (2) diabetes.

### Loading into the database
The obesity data (from __nutr_df4__) was loaded into the __obesity__ table while the diabetes data (from __chronic_df__) was loaded into the __diabetes__ table through SQLAlchemy.

```python
# Dependencies
from sqlalchemy import create_engine
from config import password
```

The __config.py__ file containing the password to MySQL was not included in the GitHub repository for security purposes.

A connection to __diabetes_db__ was created as follows:

```python
conn = "root:{0}@localhost:3306/diabetes_db".format(password) # Password is in a separate file
engine = create_engine(f"mysql://{conn}")
```

The presence of the two tables in __diabetes_db__ was first confirmed before loading data.

```python
engine.table_names()
```

The data was then loaded using the following script. if_exists is set to "replace" so that if the code were to be run again, the data wouldn't be appended as duplicates. index was set to "False" so that the index assigned to the data in the dataframes would not be saved in the database.

```python
chronic_df7.to_sql(name = "diabetes", con = engine, if_exists = "replace", index = False)
nutr_df4.to_sql(name = "obesity", con = engine, if_exists = "replace", index = False)
```

### Joining tables and a second ETL 
A third table was created in __diabetes_db__, called 'merged'. This would contain the resulting data from joining the data from the 'obesity' and the 'diabetes' tables. SQLAlchemy was used to create a connection to the updated database and the presence of the three tables was confirmed using the code above.

To extract the data from the 'obesity' and the 'diabetes' table, Pandas was used:

```python
# Read the table contents (for diabetes)
diabetes = pd.read_sql("select * from diabetes", con = engine)
diabetes = diabetes.sort_values(by = "US_State")

# Read the table contents (for obesity)
obesity = pd.read_sql("select * from obesity", con = engine)
obesity = obesity.sort_values(by = "US_State")
```

The data was sorted in alphabetical order of the U.S. state or territory. Then, the data was transformed by merging the two dataframes, __diabetes__ and __obesity__ based on year and U.S. state.

```python
# Merge diabetes and obesity dataframes
merged = pd.merge(diabetes, obesity, on=['Year','US_State'], how='inner')
```

Using "inner" to merge the two dataframes caused rows pertaining to 2010 data to be removed. Hence, only data for two years, 2012 and 2014, were retained. The resulting dataframe was loaded into the 'merged' table of __diabetes_db__:

```python
merged.to_sql(name = "merged", con = engine, if_exists = "replace", index = False)
```

The newly loaded data could be read either using MySQL or pandas.

```python
In Jupyter notebook:
pd.read_sql_query("select * from merged", con = engine).head()

OR 

In MySQL Workbench:
SELECT * FROM merged;
```

## Extras: Creating a Flask app that renders static HTML files
### Visualising diabetes and obesity trends per statefor 2012 and 2014
In the third Jupyter notebook, the __merged__ dataframe was further cleaned to replace 'None' with NaN and to convert numerical values from string to float.

```python
# Convert None values to NAN
merged.fillna(value = pd.np.nan, inplace = True)

merged["Adult_Diabetics_Percent"] = merged["Adult_Diabetics_Percent"].astype(float)
```

The dataframe was then split into two based on the year:

```python
merged_2012 = merged[merged["Year"] == 2012]
merged_2014 = merged[merged["Year"] == 2014]
```

To create a bar chart for diabetes for 2012, the following code was used:

```python
x_pos = np.arange(len(merged_2012["US_State"]))
diabetics_2012 = list(merged_2012["Adult_Diabetics_Percent"])

plt.figure(figsize = (16,8))
plt.bar(x_pos, diabetics_2012)
plt.xticks(x_pos, merged_2012["US_State"], rotation = 90, fontsize = 12)
plt.yticks(fontsize = 12)
plt.xlabel("U.S. State or Territory", fontsize = 16)
plt.ylabel("Prevalence of Adult Diabetics (%)", fontsize = 16)
plt.tight_layout()
```

This code was used to pattern other code to generate data for diabetes in 2014, and obesity for 2012 and for 2014.

To create plots that compared data between years per disease, __merged__ was spliced to create new dataframe based on diseases:

```python
merged_diabetics = merged[["Year", "US_State", "Adult_Diabetics_Percent"]]
merged_obesity = merged[["Year", "US_State", "Obese_Children_Percent"]]
```

To create a grouped bar chart, the dataframes had to be pivoted such that the datapoints were placed into two columns based on the year.

```python
merged_diabetics = merged_diabetics.pivot(index = "US_State", columns = "Year")
merged_obesity = merged_obesity.pivot(index = "US_State", columns = "Year")
```

The grouped bar plot for diabetes prevalence, comparing 2012 and 2014, was generated with the following script:

```python
ax = merged_diabetics.plot(kind = "bar", figsize = (16,8))
ax.set_xlabel("U.S. State or Territory", fontsize = 16)
ax.set_ylabel("Prevalence of Adult Diabetes (%)", fontsize = 16)
ax.legend(["2012","2014"], fontsize = 12)
plt.tight_layout()
```

A similar bar plot for obesity prevalence was also generated, adopting the code above.

All plots were saved into the Images folder. For example:

```python
plt.savefig("Images/diabetics_2012_2014.png")
```

### Flask app development
The __diabetes_app.py__ needed [PyMySQL](https://pymysql.readthedocs.io/en/latest/) to connect to the __diabetes_db__ database and several Flask features:

```python
from flask import Flask, request, render_template, jsonify
import pymysql
from config import password
```

The connection to the database was created.

```python
db = pymysql.connect("localhost", "root", f"{password}", "diabetes_db")
```

Several static html pages were rendered by some of the routes. For example:

```python
@app.route('/')
def intro():
    return render_template("index.html")
```

These static pages have been pre-loaded with the plots saved in the Images folder. One html page, however, contains the data extracted from the connected database:

```python
@app.route('/data')
def index():
    cursor = db.cursor()
    sql = "SELECT * FROM merged"
    cursor.execute(sql)
    columns = [col[0] for col in cursor.description] # gets the column headers in the merged table
    results = [dict(zip(columns, row)) for row in cursor.fetchall()] # output is a list of dictionaries
    return render_template("data.html", results = results)
```

Using __cursor.fetchall()__ would lead to a list of tuples containing values. 

```python
#Output example (tuple) in HTML
(2012, "Alabama", "12.2", 15.6)
```

To be able to render the data onto a HTML table, the output needed to be a list of dictionaries. Hence, the column names were extracted from the 'merged' table as well (the first element in a list outputted by __[cursor.description](https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-description.html)__). For each row (effectively, each tuple in the list), the column names and the rows were zipped and converted to a dictionary. 

```python
# Output example (dictionary) in HTML
{"Year": 2012, "US_State": "Alabama", "Adult_Diabetics_Percent": "12.2", "Obese_Children_Percent": 15.6}
```

The dictionary was rendered onto the table in __data.html__.

```html
...
<table>
    ...
    <!-- Loop through rows in results -->
    <!-- Each row contains year, state, diabetics, obese values -->
    {% for row in results %}
    <tr>
        <td>{{ row.Year }}</td>
        <td>{{ row.US_State }}</td>
        <td>{{ row.Adult_Diabetics_Percent }}</td>
        <td>{{ row.Obese_Children_Percent }}</td>
    </tr>
    {% endfor %}
    ...
</table>    
...
```