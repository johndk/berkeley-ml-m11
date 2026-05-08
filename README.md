# What Drives the Price of a Car?

## Overview

This assignment analyzes a cleaned dataset of used vehicle listings originally sourced from Kaggle. The goal is to 
identify which vehicle characteristics are most associated with higher or lower used car prices.

## Business Understanding

Used car dealers need to decide which vehicles to acquire, promote, and price competitively. This analysis 
investigates the relationship between vehicle price and features such as age, mileage, make, model, 
fuel, transmission.

The primary business question is:

**What factors make a used car more or less expensive?**

## Data Source

The original dataset comes from Kaggle:
[Craigslist Cars and Trucks Data](https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data). This dataset contains 426,880 used vehicle listings. The cleaned 
dataset used for modeling and analysis was prepared from this source and contains 326,408 listings.

## Methodology

This project is informed by the CRISP-DM framework.

The major stages include:

1. Business understanding
2. Data understanding
3. Data cleaning and preparation
4. Exploratory data analysis
5. Visualization
6. Modeling
7. Evaluation
8. Business recommendations

## Data Cleaning and Preparation

Extensive data cleaning was performed on the Kaggle [vehicles.csv](./data/vehicles.csv) dataset. The cleaned dataset 
is [cars.csv](./data/cars.csv). The cleaning steps were implemented in the notebook [clean.ipynb](./clean.ipynb).

Major cleaning steps included:

### Removed unrealistic price values

Listings below \$1,000 were treated as likely salvage vehicles, placeholders, parts-only vehicles, or 
non-standard transactions. Listings above \$250,000 were treated as outside the typical dealership 
inventory range.

Rows removed by price filter: 46,410<br>
Percentage removed: 10.9%

### Removed older vehicles

The year boundaries were chosen to keep the analysis focused on ordinary used-car inventory. Vehicles older 
than 1995 were excluded.

Rows removed by year filter: 16,128<br>
Percentage removed: 3.8%

### Removed unrealistic odometer values

The odometer boundaries were chosen to focus the analysis on ordinary used-car inventory. Vehicles below 1,000 miles 
were treated as likely new vehicles, placeholders, or data-entry issues. Vehicles above 250,000 miles were treated 
as extreme high-mileage listings.

Rows removed by odometer filter: 13,799<br>
Percentage removed: 3.2%

### Removed missing model strings

Missing car model strings were removed because the `model` column is only useful when 
it identifies a real vehicle model. Additional processing was performed on the manufacturer and model columns as 
explained later in the report.

Rows removed by missing model filter: 2,948<br>
Percentage removed: 0.7%

### Removed non-car model strings

Non-car models were removed because the project focuses on used cars, not all vehicle types. Listings such 
as motorcycles, RVs, trailers, boats, commercial equipment, or parts-only vehicles were removed. 
SUVs and pickup trucks were not removed.

Rows removed by non-car filter: 2,073<br>
Percentage removed: 0.5%

### Removed cars for salvage.

Salvage vehicles follow different pricing rules than ordinary used cars. Cars
without clean title were also removed with this cohort.

Rows removed by condition and title filter: 17,111
Percentage removed: 4.0%

### Renamed manufacture and make columns

The car manufacturer and model columns were replaced respectively with the make and model columns as explained next in 
the report.

### Discovered missing manufacturers; normalized model strings

The car model strings in the Kaggle dataset were not standardized. Many entries used inconsistent naming 
conventions, contained ambiguous descriptions, or included unnecessary extra information, making the original 
model column difficult to interpret reliably.

Generative AI tools were used to map the original model strings to consistent car model labels, see [normalized_models.py](normalize_models.py). In some 
cases, the model strings also contained manufacturer names, which were used to fill in missing manufacturer 
values when possible. The standardized vehicle manufacturer and model names were stored in the new make 
and model columns. This process also removed unusable model strings.


Rows removed by make and model discovery filters: 2,003<br>
Percentage removed: 0.5%

### Consolidated sparse (make,model) groups

Consistent category labels allowed for reliable identification
of low count (make,model) groups. The "other" category was introduced to avoid sparse (make,model) groups.

For example

| make   | model | count |
|--------|-------|-------|
| accura | ilx   | 488   |
| accura | mdx   | 1974  |
| accura | other | 138   |
| ...    | ...   | ...   |
| other  | other | 350   |
| ...    | ...   | ...   |

### Imputed missing features

The mode for each (make,model) group was used to fill missing values for the following feature columns:

- condition
- cylinders
- fuel
- transmission
- drive
- size
- type

### Introduced the age feature

The `age` feature was introduced to make car depreciation easier to analyze and interpret. Since car prices 
generally decline as cars get older, age provides a direct measure of this effect. It is also more intuitive 
than the raw model year because inventory decisions are often discussed in terms of 
how many years old a car is.

## EDA and Visualization

Visualization are in the EDA notebooks. The plots were well documented in those notebooks and will not be
summarized here. Intuitively the plots indicate age, milage, make, and model are strong predictors of price. 
The relationships between age and price, and milage and price, are somewhat linear but not quite, suggesting 
polynomial features which was confirmed by the machine learning experiments. Price distribution plots indicate
that log transformed price mitigates skewing. 

[eda.ipynb](eda.ipynb)<br>
[eda_chevrolet.ipynb](eda_chevrolet.ipynb)<br>
[eda_ford.ipynb](eda_ford.ipynb)<br>
[eda_honda.ipynb](eda_honda.ipynb)<br>
[eda_nissan.ipynb](eda_nissan.ipynb)<br>
[eda_toyota.ipynb](eda_toyota.ipynb)<br>

## Modeling

Simple linear regression experiments in [linereg.ipynb](linereg.ipynb) did not produce very good results but 
did indicate that polynomial feature modeling of the age and odometer features improved results.

Ridge regression models in [ridge.ipynp](ridge.ipynb) cover

- Polynomial numeric features with one-hot encoded categorical features and cross validation
  - Both price and log transformed price were modeled
- Polynomial numeric features with one-hot categorical features and grid search
  - Log transformed price only

Cross validation with polynomial numeric feature selection on [age,odometer], and one-hot encoded categorical 
features [make,model], with log transformed price, was representative of the best results which are shown below

```
cv_mae     3467.217503
cv_rmse    5501.244025
cv_r2         0.821704
dtype: float64
test_mae     3458.711440
test_rmse    5501.787543
test_r2         0.821980
dtype: float64
              y_test    ridge_preds
mean    19318.045232   18783.557334
std     13039.824946   12827.083717
median  16591.000000   15515.574322
min      1000.000000    1039.250963
max     65500.000000  100224.962135
```

Variant experients with additional categorical features and grid search did not produce significantly 
better results. The car model feature had a significant impact; the extensive data cleaning steps had an
impact.

## Business recommendations

Based on the dataset used for this assignment, car age, milage, make, and model are very good predictors of car price.





