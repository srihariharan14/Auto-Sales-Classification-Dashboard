# Auto-Sales-Classification-Dashboard

# 🚗 Automobile Sales Classification Dashboard

## 🎯 Project Overview

This project implements an end-to-end data science and visualization pipeline for automobile sales data. It utilizes Python, Scikit-learn, and Plotly Dash to build an **interactive dashboard** that identifies sales patterns, analyzes regional performance trends, and showcases a Machine Learning model's classification of "Successful Sales" against key metrics.

The final dashboard allows for dynamic filtering across manufacturers, regions, and sales categories, providing real-time insights for strategic decision-making.

## ⚙️ Technologies Used

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Data Science** | Python, Pandas, NumPy | Data collection, cleaning, and complex analysis (identifying trends and patterns). |
| **Machine Learning** | Scikit-learn | Training a **Logistic Regression** model to classify sales success (our target variable). |
| **Visualization** | Plotly | Generates high-quality, interactive charts (Heatmaps, Trend Lines, Pie Charts). |
| **Web Application** | **Plotly Dash** | Built the interactive, web-based dashboard and handles all user input and callbacks. |

---

## 🚀 Key Features and Methodology

The project structure is built to showcase modularity and follows the steps below:

### 1. Data Collection, Cleaning, and Analysis

* **Action:** Collected, cleaned, and analyzed simulated automobile sales datasets using **Python, Pandas, and NumPy**.
* **Result:** Identified sales patterns, market distribution, and regional performance trends (e.g., peak sales quarters, highest-value regions).

### 2. Interactive Dashboard Construction

* **Action:** **Built an interactive dashboard with Dash and Plotly** to enable dynamic filtering and comparative analysis across regions, manufacturers, and time periods.
* **Result:** Users can dynamically slice the data to instantly see how sales trends, average prices, and success rates change.

### 3. Advanced Visualization

* **Action:** Applied data visualization techniques (heatmaps, bar charts, trend lines) to highlight seasonal trends, sales spikes, and category-wise performance.
* **Result:** Visual insights include a **Sales Volume Heatmap** (Region vs. Manufacturer) and a **Sales Classification Pie Chart** (ML Target Variable).

### 4. Modular and Reusable Components

* **Action:** **Designed modular and reusable components** using separate files (`app/components.py` and `app/callbacks.py`).
* **Result:** Ensures smooth user interaction, easy maintenance, and demonstration of proper Python package structure.

### 5. Deployment Readiness

* **Action:** The application is configured to run locally using the `python -m app.app` command and includes a **Procfile** for future **cloud deployment** (e.g., Heroku or Render), demonstrating an end-to-end data science + visualization pipeline.

---

## 📦 Repository Structure

The project is organized using a best-practice modular structure:

Auto-Sales-Classification-Dashboard/ ├── app/ # Main application package (Python Module) │ ├── app.py # Main server entry point and layout assembly. │ ├── components.py # Reusable functions for layout (KPIs, Filters, Charts). │ └── callbacks.py # Contains the interactive logic for dynamic filtering. ├── data/ │ ├── processed/ # cleaned_data.csv (Loaded by the app) │ └── model/ # classification_model.pkl (Loaded by the app) ├── notebooks/ # Documentation for data processing and ML training. ├── .gitignore # Excludes venv/, pycache/, and raw data. ├── requirements.txt # Lists all dependencies (Dash, Scikit-learn, etc.). └── Procfile # Configuration file for cloud deployment (e.g., gunicorn web server).


---

## 🚀 How to Run Locally

### Prerequisites

* Python 3.8+
* `venv` (Python Virtual Environment)

### Execution Steps

1.  **Activate Environment & Install Dependencies:**

    ```bash
    # 1. Activate the environment (if not already active)
    .\venv\Scripts\Activate.ps1
    
    # 2. Install all required packages
    pip install -r requirements.txt
    ```

2.  **Generate Data and Mock Model:**
    *(This step simulates the analysis and saves the necessary files the dashboard loads.)*

    ```bash
    python setup_pipeline_data.py
    ```

3.  **Launch the Dashboard:**
    *(Execute the package as a module using the -m flag for correct path resolution.)*

    ```bash
    python -m app.app
    ```

4.  **View:** Open your browser and navigate to the local address provided in the terminal (usually `http://127.0.0.1:8050/`).