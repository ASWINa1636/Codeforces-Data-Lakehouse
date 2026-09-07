# Codeforces Data Lakehouse

A production-style data engineering project that collects,
processes, stores, transforms, and analyzes Codeforces data.

## Architecture

Codeforces API
      ↓
Python Ingestion
      ↓
Raw Data
      ↓
DuckDB
      ↓
PostgreSQL
      ↓
dbt
      ↓
Analytics Marts
      ↓
Power BI

Airflow will orchestrate the complete pipeline.

## Tech Stack

- Python
- Codeforces REST API
- DuckDB
- PostgreSQL
- dbt
- Apache Airflow
- Docker
- Power BI

## Project Status

Phase 1 - Project Setup