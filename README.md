# Ghana Housing Insights
This project is one where data was collected from meqasa (a popular ghanaian real estate website) to generate insights from properties, homes, apartments, office spaces listed for rent.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip install requirements.txt
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


## Test Coverage

Tests were implemented using **pytest** to ensure the reliability of the scraper.  
Each major function in the `MeqasaScraper` class was tested to validate expected behavior under various conditions.

### **Functions Tested**
- `fetch_page()` – verifies page fetching and HTTP status handling  
- `parse_listing_page()` – ensures correct parsing of property listings  
- `extract_listing_details()` – checks extraction of title, price, and URLs  
- `scrape_listing_details()` – validates detailed listing data extraction  
- `scrape_page()` – tests page-level scraping integration  
- `save_to_csv()` – confirms correct CSV file creation and saving  

### **Coverage Command**
```bash
pytest --cov=data --cov-report=term-missing
```

---------- coverage: platform win32, python 3.13 ----------
```
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
data/__init__.py          0      0   100%
data/datascraper.py      99     25    75%   48, 67, 73, 75, 78-84, 113, 121-123, 127-132, 137-146
---------------------------------------------------
TOTAL                    99     25    75%
```


## Interpretation
```
Overall Coverage: 75%
Core scraper logic (fetching, parsing, and saving) is fully tested.
The untested lines correspond mainly to:
    1.Console print statements
    2.time.sleep() delay logic
    3.Error-handling branches that require failed requests or missing data
```
## Conclusion

The test suite achieves 75% coverage, verifying that all critical scraper functions operate correctly.
Untested lines are non-critical, primarily involving print logs and timing delays.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
