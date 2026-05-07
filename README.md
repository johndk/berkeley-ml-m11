**ATTENTION: Note to reviewer. This submission is in-progress. I am requesting a six-hour extension. 
Estimated completion time 3:30 PM PDT Thursday, May 7, 2026.**

## Overview

This project analyzes a cleaned dataset of used vehicle listings originally sourced from Kaggle. The goal is to 
identify which vehicle characteristics are most associated with higher or lower used car prices.

## Business Problem

Used car dealers need to decide which vehicles to acquire, promote, and price competitively. This analysis 
investigates the relationship between vehicle price and features such as age, mileage, make, model, condition, 
fuel type, drive type, transmission, size, and vehicle type.

The primary business question is:

**What factors make a used car more or less expensive?**

## Data Source

The original dataset comes from Kaggle:

[Craigslist Cars and Trucks Data](https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data)

The Craigslist dataset contains 426,880 used vehicle listings. The cleaned dataset used for modeling 
and analysis was prepared from this source and contains 326,408 listings.

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

## Data Cleaning Summary

Extensive data cleaning was performed on the [vehicles.csv](./data/vehicles.csv) dataset. The cleaned dataset 
is in [cars.csv](./data/cars.csv) and the cleaning steps were implemented in the notebook [clean.ipynb](./clean.ipynb).

Major cleaning steps included:

### Removed unrealistic price values

Listings below \$1,000 were treated as likely placeholders, salvage vehicles, parts-only vehicles, or 
non-standard transactions. Listings above \$250,000 were treated as outliers outside the typical dealership 
inventory range.

Rows removed by price filter: 46,410<br>
Percentage removed: 10.9%

### Removed older vehicles

The year boundaries were chosen to keep the analysis focused on ordinary used-car inventory. Vehicles older 
than 1995 were excluded because they are more likely to be classic, collector, salvage, or project vehicles 
with pricing behavior that differs from the broader used-car market.

Rows removed by year filter: 16,128<br>
Percentage removed: 3.8%

### Removed unrealistic odometer values

The odometer boundaries were chosen to focus the analysis on ordinary used-car inventory. Vehicles below 1,000 miles 
were treated as likely new vehicles, placeholders, or data-entry issues. Vehicles above 250,000 miles were treated 
as extreme high-mileage listings whose pricing may depend heavily on mechanical condition and maintenance history.

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
as motorcycles, RVs, trailers, boats, commercial equipment, or parts-only vehicles follow different pricing patterns 
and are not directly comparable to ordinary passenger vehicles. SUVs and pickup trucks were not removed.

Rows removed by non-car filter: 2,073<br>
Percentage removed: 0.5%

### Removed cars for salvage.

Salvage vehicles follow different pricing rules than ordinary used cars. Their 
prices are strongly affected by damage history, repair quality, insurance risk, and resale concerns. Cars
without clean title were also removed with this cohort.

Rows removed by condition and title filter: 17,111
Percentage removed: 4.0%

### Renamed manufacture and make columns

The car manufacturer and model columns were replaced respectively with the make and model columns as explained next in 
the report.

### Discovered missing manufacturers; normalize model strings

The car model strings in the original dataset were not standardized. Many entries used inconsistent naming 
conventions, contained ambiguous descriptions, or included unnecessary extra information, making the original 
model column difficult to interpret reliably.

Generative AI tools were used to map the original model strings to consistent car model labels. In some 
cases, the model strings also contained manufacturer names, which were used to fill in missing manufacturer 
values when possible. The standardized vehicle manufacturer and model names were stored in the new make 
and model columns. This process also removed unusable model strings.

The AI generated "model strings to canonical labels mapping" implementation is in 
[normalized_models.py](normalize_models.py).

Rows removed by make and model discovery filters: 2,003<br>
Percentage removed: 0.5%

### Consolidated sparse (make,model) groups

Consistently naming conventions, for the car model in particular, allowed for reliable grouping and the identification
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

The `age` feature was introduced to make car depreciation easier to analyze and interpret. Since used-car prices 
generally decline as cars get older, age provides a direct measure of this effect. It is also more intuitive 
for a dealership audience than the raw model year because inventory decisions are often discussed in terms of 
how many years old a car is.