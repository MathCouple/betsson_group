<h1 align="center">
  <b>Data Engineering Assessment - Matheus Alves</b>
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Pydantic-Data%20Validation-forestgreen?logo=pydantic&logoColor=white" alt="Pydantic">
  <img src="https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter&logoColor=white" alt="Jupyter Notebook">
  <img src="https://img.shields.io/badge/Alembic-Database%20Migration-lightgrey?logo=alembic&logoColor=white" alt="Alembic">
  <img src="https://img.shields.io/badge/MSSQL-Server-red?logo=microsoft-sql-server&logoColor=white" alt="MSSQL">
  <img src="https://img.shields.io/badge/SQLAlchemy-ORM-red?logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
</p>


## The Challenge

1. **By making use of the `invoices.xls` data file as your source, create a Data Warehouse model with best practices in place, using the Kimball methodology.**
2. **Populate the model created in step 1 with the data provided in the Excel sheet.**
3. **Analyze any abnormalities (if any) in the data provided and take any action needed (where possible).**
4. **List any assumptions taken into consideration.**
5. **Provide 3 different aggregations one might use for reporting purposes.**  

<br>
<br>

<p align="center">
  <img src="./assets/betsson_logo.png" alt="Betsson Logo" style="max-width: 100%; width: 600px;">
</p>

<br>



## Table of Contents

- [0. Base Constraints](#0-base-constraints)
- [0.1. Scope Matrix - Documentation and Code](#01-scope-matrix---documentation-and-code)
  - [0.1.1 Base General Process](#base-general-process)
  - [0.1.2 Base ETL Considerations](#base-etl-considerations)
  - [0.1.3 Base Warehouse Considerations](#base-warehouse-considerations)
  - [0.1.4 Bonus](#bonus) 
- [1. Assumptions & Abnormalities](#1-assumptions--abnormalities)
  - [1.1 Base Considerations](#11-base-considerations)
  - [1.1 Overall Data Assumptions](#12-overall-data-assumptions)
  - [1.2 Overall Data Abnormalities](#13-overall-data-abnormalities)
- [2. Pipeline Architecture Diagram](#2-pipeline-architecture-diagram)
- [3. 2. Packages and modules overview](#2-packages-and-modules-overview)
  - [3.0. Running the project](#30-running-the-project) 
  - [3.1. Main Script](#31-main-script)
  - [3.2. infra](#32-infra)
  - [3.3. ingestion](#33-ingestion)
  - [3.4. utils](#34-utils)
  - [3.5. assets](#35-assets)
- [4. Jupyter Notebook Structure](#3-jupyter-notebook-structure)
  - [4.1. Base Data Process](#31-base-data-process)
    - [4.1.1. Importing Base Dataframe](#311-importing-base-dataframe)
    - [4.1.2. Briefly Checking the Data](#312-briefly-checking-the-data)
    - [4.1.3. Dataset Base Info](#313-dataset-base-info)
    - [4.1.4. Data Variations](#314-data-variations)
    - [3.1.5. Base Memory Usage](#315-base-memory-usage)
    - [3.1.6. Overview of Top and Bottom Data](#316-overview-of-top-and-bottom-data)
- [Aditional Notes](#additional-notes)

---

## 0. Base Constraints

- This task may be done either with MSSQL, Python or C#.

- It is highly recommended that comments are included, and code is structured well.

- If making use of python, you can make use of Jupyter notebooks, thus you can either

- provide a .PY file or .IPYNB file.

- Assumptions & Abnormalities are to be provided in a separate document.

<br>
<br>

## 0.1 Scope Matrix - Documentation and Code


### Base General Process
| Feature                                          | In Scope (MVP) | Out of Scope |
|--------------------------------------------------|----------------|--------------|
| README.md-based documentation (iterative view)  | ✅             |              |
| PDF documentation (static)                      | ✅             |              |
| Module and package details                      | ✅             |              |
| Base real case assumptions                      | ✅             |              |
| Packages and modules partially/fully reusable   | ✅             |            |
| Base data quality check                         | ✅             |            |
| Cloud-related environments                      |                | ✅           |
| Full production-ready                           |                | ✅           |
| Non-Python frameworks for ETL                   |                | ✅           |
| Specific metrics logging (to be used in Prometheus, for instance)           |                | ✅           |
| Deeply statistic approaches in warehouse/data cleaning           |                | ✅           |
| Specific Architecture Consumption/Tunning Scenario|| ✅           |

### Base ETL Considerations
| Feature                                          | In Scope (MVP) | Out of Scope |
|--------------------------------------------------|----------------|--------------|
| Process diagrams                                | ✅             |              |
| Isolated environment (.venv, optional)          | ✅             |              |
| `pip` requirements (`pip install -r requirements_xx.txt`) | ✅  |              |
| APIs                                            |                | ✅           |
| Scheduler-ready                                 |                | ✅           |

### Base Warehouse Considerations
| Feature                                          | In Scope (MVP) | Out of Scope |
|--------------------------------------------------|----------------|--------------|
| Data full metadata                              | ✅             |              |
| Client basic tuning example (MSSQL Query Plan)  | ✅             |              |
| Decision explained                              | ✅             |              |
| Physical computing/database architecture and setup |              | ✅           |
| Server basic tuning (on possible queries)       |                | ✅           |

## Bonus
| Feature                                          | In Scope (MVP) | Out of Scope |
|--------------------------------------------------|----------------|--------------|
| Base data lineage (physical .parquet storing)   | ✅             |              |
| Personalized logger                             | ✅             |              |

<br>
<br>

## 1. Assumptions & Abnormalities

### 1.1 Base Considerations

There are two main logic on this assesment answers
  - One that demonstrates deeply understanding of the purpose of the seletive process, with a logical/straightforward solution approach. It's the solution.ipynb. ipynb solutions starts General Code Structure. But their functions can be 
  - The other one is more structured and reusable, thinking on best long-term practices and reusability. Still addressing the same problem.
- In a real-world scenario, every point would be discussed with the appropriate team or area. This collaborative approach ensures that the problem is addressed and resolved in the most effective way possible.

As a professional data engineer, I have some knowledge in managing the chaotic nature of real-world data, a common challenge faced by most organizations. My goal is to address the challenges posed by this selective while showcasing the delivery of reliable and efficient solutions tailored to specific business needs.

- Additionally, I aim to demonstrate how data and code can be democratized and standardized across organizations, fostering scalability, collaboration, and long-term value.
<br>

***I hope you enjoy the read.***

<br>

---

#### 1.2 Overall Data Assumptions
- I'm assuming that we are working with the data in an API, and we need to decompress it and save it locally. Also, it is assumed that the data is a snapshot and we don't need to update it in the database.
  - Even with that in mind, we have dimensions, for instance, that take into consideration Slowly Changing Dimensions (SCD) Type 2, to keep track of the changes in the data.

- Lowercase will be used for column names, in addition to snake case.
  - This is a common practice to avoid any possible issues with the database.
    - For instance, Postgres is not case-sensitive, so we would need to use quotes to refer to column names in queries if uppercase or mixed case were used.

#### 1.3 Overall Data Abnormalities
- Columns contain missing values that can represent various scenarios, ranging from errors/bugs to information that was not shared.
  - Additionally, if I set them to "Unspecified," for instance, I could end up:
    - Masking the root cause of why the data is missing.
    - Complicating future analysis, as "Unspecified" might be treated as a valid category rather than missing data.
    - Introducing ambiguities (like interpreting it as a category in the wrong scenario).

- There are curious values in the quantity and price columns.
  - It could be some loss product category. It could be a return. It could be an error, among other possibilities.
  - I would need to check the data with the business team to understand the context and take the proper action.
    - For example, I could try to figure out the context by checking the invoice number.
    - Or, if I had access to all available sales data, I could verify whether it is a 'loss' product.
    - Supposing that it is an unkwown error, I could try to compare unitary priceses (price/quantity) to understand better the context.
  - To keep it simple, I'll assume it is a product return and flag it in the Warehouse.
- There were test values that have been addressed and removed from all columns.
##### 1.3.Last-2 Customer ID columns

##### 1.3.Last-1 country columns
- There are native "Unspecified" values in the data. I'm generally applying this approach across all string columns:
- Unspecified: Represents cases where clients/stores explicitly chose not to declare their information (e.g., location, category).
  - Null (e.g., `None`, `NaN`): Indicates cases where clients/stores did not settle or provide the information at all, potentially due to:
    - Errors in data entry or processing.
    - Omissions in data collection.
    - Incomplete or unavailable information.
  
- Some entries in the Country column might not represent valid country names (e.g., typos, placeholders, or regions like "Channel Islands").
  - The simplest approach would rename Country to Locations, avoiding the necessity of creating different columns indicating category types and adjusting Country Column information.
  - Further, this column will be a dimension of location_name, location_type
- Some entries in the Country column are abbreviated, such as "United Kingdom" and "UK". In this case, a simple solution is to use a dictionary to map and standardize the values. However, for more complex cases involving large datasets, approaches can range from using a Cartesian mapping stored in a .txt file to developing a classification model to identify and standardize variations in location names automatically.

<br>
<br>

---
## 2. Pipeline Architecture Diagram

<p align="center">
  <img src="./assets/pipeline_architecture_diagram.png" alt="Pipeline Architeture Diagram" style="max-width: 100%; width: 900px;">
</p>

<br>
<br>

---
## 3. Packages and modules overview

### 3.0. Running the project

- **Requirements**: Python 3.9+ and Jupyter Notebook.
- **Use a virtual environment**: `python -m venv .venv`
- **Installation**: Run `pip install -r requirements_xxx.txt`. The requirements file includes two sets of dependencies: one specifically for the Jupyter Notebook (.ipynb) and another for the Python-based script. This separation ensures that the notebook's additional dependencies are only installed if you plan to use it, keeping the main script lightweight and efficient.
- **Fill .env-template**: Copy the `.env-template` to `.env` and fill the variables.
- **Attention**: The flag `_MIGRATE_DATABASE` at the beginning of the main scripts is a boolean that controls the database migration behavior.
  - When set to `True`, it will overwrite or create the database and tables.
  - When set to `False`, it will append data to the existing database and tables, validating constraints only on natural keys.
- **Run the main script**: `python main_one_time_analysis.py` on the root project diretory.

### 3.1. Main Script
- **`solution.ipynb`**: Straightforward End-to-End Approach to Address the Challenge
- **`main_adjusted_retail_analysis.py`**: Example of a dedicated pipeline, including all modules. Lineage tracker ready, with space to implement a run back from stopped stage.

### 3.2. infra
- models
  - Dimensional and fact models.
    - `dim.py` - all dimensional to our DW models.
    - `fact.py` - all fact to our DW models.

- pipeline
  - Pipeline specif codes
    - `pipeline_metadata.py` - References to metadata process. Like Mapping, etc.
        - NORMATIZE_LOCATION_MAP - a dict containing the mapping of normalized location names.
    - `pipeline_lineage.py` - It stores stages related to the pipeline.
      - get_csv_df - Reads CSV files into pandas DataFrame format.
      - PipelineTransformer - BR Contains every stage and their transformations, as well as a saving method.
    - `pipeline_transformers.py` - Business rules (BR) and general transformations (GR) to be used on the pipeline.
      - sanitize_column_data - BR related to fill null data and format types.
      - sanitize_text - BR related to sanitize text data. It will remove special characters, and replace accented characters with their unaccented counterparts.
  
- handlers
  - General handlers for database related and data processing.
    - `db_migration_handler.py` - Alembic migration handler. It is supposed to run once, and it will create the database and tables. As well with the possible indexes, based on the warehouse models.
    - `msql_handler.py` - MSSQL connection handler. It will be used to return the connection engine to be orchestrated by sqlalchemy/alembic/direct-queries.


### 3.3. ingestion
- Ingested data as 7z.
- Extracted data as csv/xls.

### 3.4. utils
- `_references.py` - base code references, like logging, etc.
  - get_current_utc_time - datetime now in UTC time.
  - create_logger - created supposed to use as unique logger for the application.
- `file_handlers.py` - utilities to write/read/process/format files.
  - extract_7z - It will extract the 7z file to a folder. This one is our "imaginary API".

### 3.5. assets
- Images and other assets used on README.md and other documentation.
It doesn't make part of the codebase.

<br>
<br>

---

## 4. General Code Structure

### 4.1. Data Understainding and base adjustments

#### 4.1.1. Importing Base Dataframe
- Load the data from the `_ingestion.Invoices_Year_2009-2010.csv` file.

#### 4.1.1. Importing Base Dataframe
- Load the data from the `_ingestion.Invoices_Year_2009-2010.csv` file.

#### 4.1.2. Briefly Checking the Data
  - Quick overview of the dataset.
  - Display dataset information and types.
  - Quick overview of minimum and maximum values in the data.
  - Quick overview of nulls and base critical values in the data.
  - Understanding raw memory consumption.
  - Understanding unique values in the data.

#### 4.1.3. Digging into the Data Types and Suggesting Base Corrections
- Formatting column dtypes
- Formatting column names
- Removing "test" data.


#### 4.1.4. Lineage Checkup
- Stage-final consistency checkup.
- Write changes into a parquet file to keep track of lineage and all modifications made to the data from the previous stage.

#### 4.1.5. Deeply addresing columns dtypes and content
- Governance and basic data quality layer:
  - Columns are normalized and sanitized.
  - Columns are formatted to the correct data type.

---

## Additional Notes

- **Revenue Formula**: `revenue = quantity * price`
- **Data Issues**: Country column contains mixed data categories and has been renamed to Locations, for consistency.
- **Data Issues**: Country column contains mixed data categories and has been renamed to Locations, for consistency.

