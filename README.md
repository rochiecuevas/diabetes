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

Both datasets were downloaded as csv files and extracted using Python (version 3.6) [Pandas](https://pandas.pydata.org/pandas-docs/stable/) module. The [chronic diseases indicators](https://drive.google.com/open?id=1QLxhiRwirRHE_AO_6p53Yv1QJ0Ei1K2f) file contains the statistics for __diabetes__ prevalence in adults 18+ years old. On the other hand, the data for occurrence of __obesity__ in children 2–4 years old are found in the [nutrition, physical activity, and obesity](https://drive.google.com/open?id=1lzKsXYhbfvTQ_lWLI_8ejOAeVgkvMt59) file. 

```python
# Load CSV file as dataframe
    # The csv files are stored locally in a Resources folder. But because they exceed GitHub's file size requirement, links to the Google Drive copy of the files are provided.
diseasedata = pd.read_csv("Resources/U.S._Chronic_Disease_Indicators__CDI_.csv")

nutr_df = pd.read_csv("Resources/Nutrition__Physical_Activity__and_Obesity_-_Women__Infant__and_Child.csv")
```

### Transformation
#### Filtering the dataframe for the most relevant columns
The columns of interest in __diseasedata__ were those that provided information about the crude prevalence of adult diabetes. Hence, the dataframe was refined as follows:

```python
chronic_df = diseasedata[["YearEnd", "LocationDesc", "Topic", "Question", "DataValueUnit", "DataValueType", "DataValue", "Stratification1"]]
```


#### Obesity statistics in women, infants, and children (WIC)

### Loading
