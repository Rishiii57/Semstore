# Indian Housing Rent Price Dataset

This dataset contains housing rental data across major Indian cities (Mumbai, Delhi, Pune & Hisar). The data has been preprocessed, cleaned, and split into training and testing sets.

## Dataset Splits

The original data was aggregated from three separate city datasets and combined into a single corpus before splitting to ensure a proportional stratified representation of all cities in both the train and test subsets.

- **`train.csv`**: Contains 11,128 records (80% of the data).
- **`test.csv`**: Contains 2,782 records (20% of the data).

## Feature Dictionary

The datasets contain 16 columns resulting from preprocessing. The target variable for predictive modeling is usually `price`.

| Feature Name | Data Type | Description |
| :--- | :--- | :--- |
| `location` | String / Categorical | Specific area or neighborhood where the property is located. |
| `city` | String / Categorical | The city where the property is situated (Mumbai, Delhi, Pune & Hisar). |
| `latitude` | Float | Geographic latitude coordinates of the property location. |
| `longitude` | Float | Geographic longitude coordinates of the property location. |
| `price` | Float | Rental price of the house per month in **INR**. *(Target Variable)* |
| `numBathrooms` | Integer | Total number of bathrooms in the house. |
| `numBalconies` | Integer | Total number of balconies in the house. |
| `isNegotiable` | Integer (Binary) | Indicates whether the rental price is negotiable (`1` = Negotiable, `0` = Not Negotiable). |
| `SecurityDeposit` | Integer | Amount of security deposit required for renting the property in **INR**. |
| `Status` | String / Categorical | Furnishing status of the property (e.g., Furnished, Unfurnished, Semi-Furnished). |
| `Size_ft²` | Integer | Size of the house isolated into pure numerical square feet. |
| `BHK` | Integer (Binary) | Identifies the fundamental dwelling type category (`1` = BHK [Bedroom Hall Kitchen], `0` = RK [Room Kitchen]). |
| `rooms_num` | Integer | Total count of rooms parsed from the original property type structure. |
| `property_type` | String / Categorical | The classification of the property (e.g., Apartment, Independent House, Studio Apartment). |
| `verification_days` | Float | The numerical representation (in days) derived from the original posting/verification date string indicating how long ago the property was posted. |
