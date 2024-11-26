# **Data Engineering Assessment - Matheus Alves**

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Pydantic-Data%20Validation-forestgreen?logo=pydantic&logoColor=white" alt="Pydantic">
  <img src="https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter&logoColor=white" alt="Jupyter Notebook">
  <img src="https://img.shields.io/badge/Alembic-Database%20Migration-lightgrey?logo=alembic&logoColor=white" alt="Alembic">
  <img src="https://img.shields.io/badge/MSSQL-Server-red?logo=microsoft-sql-server&logoColor=white" alt="MSSQL">
  <img src="https://img.shields.io/badge/SQLAlchemy-ORM-red?logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
</p>

---

## The Challenge

1. **Using the `invoices.xls` data file as the source, create a Data Warehouse model with best practices, adhering to the Kimball methodology.**
2. **Populate the model created in step 1 with the data provided.**
3. **Analyze abnormalities in the data and take corrective actions where possible.**
4. **List all assumptions made.**
5. **Provide three aggregations for reporting purposes.**

<p align="center">
  <img src="./assets/betsson_logo.png" alt="Betsson Logo" style="max-width: 100%; width: 600px;">
</p>

---

## Table of Contents

1. [Base Constraints](#0-base-constraints)
2. [Scope Matrix](#01-scope-matrix---documentation-and-code)
3. [Assumptions & Abnormalities](#1-assumptions--abnormalities)
4. [Pipeline Architecture Diagram](#2-pipeline-architecture-diagram)
5. [Packages and Modules Overview](#3-packages-and-modules-overview)
6. [General Code Structure](#4-general-code-structure)
7. [Additional Notes](#additional-notes)

---

## 0. Base Constraints

- Task to be done using MSSQL, Python, or C#.
- Code should include comments and structured logic.
- Deliverables can be `.py` or `.ipynb` files.
- Assumptions and abnormalities should be documented separately.

---

## 0.1 Scope Matrix - Documentation and Code

### Base General Process

| Feature                              | In Scope (MVP) | Out of Scope |
|--------------------------------------|----------------|--------------|
| README.md-based documentation        | ✅             |              |
| PDF documentation                    | ✅             |              |
| Package/module details               | ✅             |              |
| Real-world assumptions               | ✅             |              |
| Reusable packages/modules            | ✅             |              |
| Data quality checks                  | ✅             |              |
| Cloud environments                   |                | ✅           |
| Full production-ready pipeline       |                | ✅           |

### Base ETL Considerations

| Feature                              | In Scope (MVP) | Out of Scope |
|--------------------------------------|----------------|--------------|
| Process diagrams                     | ✅             |              |
| Virtual environment (`.venv`)        | ✅             |              |
| `pip` requirements                   | ✅             |              |
| APIs                                 |                | ✅           |
| Scheduler-ready                      |                | ✅           |

### Base Warehouse Considerations

| Feature                              | In Scope (MVP) | Out of Scope |
|--------------------------------------|----------------|--------------|
| Full metadata for data               | ✅             |              |
| Basic tuning example (MSSQL)         | ✅             |              |
| Decision explanation                 | ✅             |              |
| Database server setup                |                | ✅           |

### Bonus

| Feature                              | In Scope (MVP) | Out of Scope |
|--------------------------------------|----------------|--------------|
| Data lineage tracking                | ✅             |              |
| Personalized logger                  | ✅             |              |

---

## 1. Assumptions & Abnormalities

### 1.1 Base Considerations

Two main approaches:
- **Straightforward (Jupyter Notebook):** A logical, straightforward solution.
- **Reusable (Script):** Focuses on structured, reusable long-term practices.

Collaborative discussions in real scenarios would refine solutions.

### 1.2 Overall Data Assumptions

- Data snapshot only; no updates required.
- Dimensions use Slowly Changing Dimensions (SCD) Type 2.
- Column names use snake case.
- Location data inferred from metadata and adjusted as needed.
- "Online sales" identified via descriptions.

### 1.3 Overall Data Abnormalities

#### General
- Missing values handled with placeholders ("Unspecified") or left null.
- Test values removed.
- Customer ID and descriptions missing with negative values flagged as errors.

#### Specific Columns

- **Location Column:**
  - Renamed to "Location" for broader categorization.
  - Includes abbreviations and regions like "Channel Islands."

- **Price Column:**
  - Negative prices indicate returns, discounts, or losses.

- **Quantity Column:**
  - Negative or zero values flagged for business rule evaluation.

- **Description Column:**
  - Normalized; non-informative entries flagged.
  - Adjustments and financial details properly categorized.

- **StockCode Column:**
  - Special patterns (e.g., "M", "D") identified as discounts.
  - Samples and gifts flagged separately.

---

## 2. Pipeline Architecture Diagram

<p align="center">
  <img src="./assets/pipeline_architecture_diagram.png" alt="Pipeline Architecture Diagram" style="max-width: 100%; width: 900px;">
</p>

---

## 3. Packages and Modules Overview

### 3.0 Running the Project

1. **Requirements:** Python 3.9+, Jupyter Notebook.
2. **Setup:** Create a virtual environment (`python -m venv .venv`).
3. **Installation:** `pip install -r requirements_xxx.txt`.
4. **Environment Variables:** Fill `.env-template` and save as `.env`.
5. **Run the script:** `python main_one_time_analysis.py`.

### 3.1 Main Script

- **`solution.ipynb`:** End-to-end Jupyter Notebook solution.
- **`main_adjusted_retail_analysis.py`:** Script-based reusable pipeline.

### 3.2 Infra

- **Models:** Dimensional and fact models for the data warehouse.
- **Pipeline:**
  - Metadata handling.
  - Lineage tracking.

### 3.3 Ingestion

- Compressed data in `.7z`.
- Extracted data as `.csv` or `.xls`.

### 3.4 Utils

- General utilities for logging, time handling, and file operations.

---

## 4. General Code Structure

### 4.1 Data Understanding and Adjustments

- Load data from `Invoices_Year_2009-2010.csv`.
- Quick checks for nulls, data types, and memory usage.
- Normalize column names and types.
- Lineage tracking with stage consistency checks.
- Format columns for data governance.

---

## Additional Notes

- **Revenue Formula:** `revenue = quantity * price`.
- **Discount Efficiency:** Tracks return rates after discounts.
- **Data Quality:** Columns like "Country" renamed to "Locations" for consistency.
