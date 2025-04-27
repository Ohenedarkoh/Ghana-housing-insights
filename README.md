# Ghana Housing Insights
This project is one where data was collected from meqasa (a popular ghanaian real estate website) to generate insights from properties, homes, apartments, office spaces listed for rent.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pandas.

```bash
pip install pandas
```

## Usage

```python
import pandas as pd

# read a csv file'
housing = pd.read_csv()

# check for duplicates
housing_duplicates = housing.duplicated() 
print("Duplicated in the housing file is ",housing_duplicated)

# print number of null values
null_counts= housing.isnull().sum()
print(null_counts)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)