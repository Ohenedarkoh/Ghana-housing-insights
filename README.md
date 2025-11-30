# Ghana Housing Insights: Predicting Rental Prices with Machine Learning

This project delivers an end-to-end data science solution for analyzing and predicting rental housing prices in Ghana. It covers automated web scraping, data processing, machine learning model development, and API deployment to provide data-driven insights for the real estate market.

## Key Features

*   **Data Acquisition**: Python web scraper for Meqasa property listings.
*   **ETL Pipeline**: Data cleaning, feature engineering (including advanced amenity grouping), and loading into a **PostgreSQL** database.
*   **Price Prediction Model**: Optimized **XGBoost Regressor** for housing price prediction.
*   **Real-time API**: **FastAPI** for serving model predictions with interactive Swagger UI.
*   **Business Intelligence**: **Power BI dashboards** for market insights.

## Technologies Used

Python (Pandas, NumPy, BeautifulSoup4, Requests, Scikit-Learn, XGBoost, FastAPI, Pydantic, Uvicorn, SQLAlchemy), PostgreSQL, Microsoft Power BI, Jupyter Notebook, Render.com.

## Setup & Local Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Ohenedarkoh/Ghana-housing-insights.git
    cd Ghana-housing-insights
    ```
2.  **Create & activate virtual environment.**
3.  **Install dependencies:** `pip install -r requirements.txt`
4.  **PostgreSQL & Environment Variables**: Set up a PostgreSQL database and configure credentials in a `.env` file (added to `.gitignore`).

## Usage

*   **Run ETL**: Execute `notebooks/cleaning.ipynb` to clean data and load into PostgreSQL.
*   **Train Model**: Run `notebooks/xgboost.ipynb` to train, tune, and save the XGBoost model.
*   **Run API Locally**: From project root, use `uvicorn model.api.app:app --reload`. Access docs at `https://ghana-housing-insights-1.onrender.com`.

## Deployment

The FastAPI application is deployed as a Web Service on **Render.com**.
*   **Deployed API Base URL**: https://ghana-housing-insights-1.onrender.com
*   **Deployed API Docs**: https://ghana-housing-insights-1.onrender.com/docs

## Model Performance

The optimized XGBoost Regressor shows strong predictive power:
*   **Initial R² ,RMSE and MAE Score**:  0.4116, 0.7992, 0.6058
*   **Optimized R² Score**: 0.45089

## Contact

[Frank Ohene-Darkoh] - [ohenedarkohfrank@gmail.com] - [[Your LinkedIn Profile URL](https://www.linkedin.com/in/frankohene-darkoh-44412222b)]

## License

MIT License.