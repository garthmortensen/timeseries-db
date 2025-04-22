#!/usr/bin/env python3
# example_db_connect.py

"""Example of connecting to the TimeSeries DB and storing pipeline results."""

import os
import json
import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Database connection parameters from environment variables
DB_USER = os.getenv("DB_USER", "timeseriesuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "timeseriespass")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "timeseriesdb")

# Database connection string
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def get_db_session():
    """Create and return a database session."""
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return Session()

def store_pipeline_run():
    """Store example pipeline run and results."""
    try:
        session = get_db_session()
        
        # Create a pipeline run
        pipeline_run_query = """
        INSERT INTO pipeline_runs 
        (name, status, source_type, start_date, end_date, start_time, symbols)
        VALUES (:name, :status, :source_type, :start_date, :end_date, NOW(), ARRAY[:symbols])
        RETURNING id
        """
        
        result = session.execute(
            text(pipeline_run_query),
            {
                'name': 'Example Pipeline Run',
                'status': 'running',
                'source_type': 'synthetic',
                'start_date': '2023-01-01',
                'end_date': '2023-01-31',
                'symbols': ['GME', 'BYND', 'BYD']
            }
        )
        
        pipeline_run_id = result.fetchone()[0]
        print(f"Created pipeline run with ID: {pipeline_run_id}")
        
        # Store stationarity results
        stationarity_query = """
        INSERT INTO pipeline_results
        (pipeline_run_id, symbol, result_type, is_stationary, adf_statistic, p_value, interpretation)
        VALUES (:pipeline_run_id, :symbol, :result_type, :is_stationary, :adf_statistic, :p_value, :interpretation)
        """
        
        session.execute(
            text(stationarity_query),
            {
                'pipeline_run_id': pipeline_run_id,
                'symbol': 'GME',
                'result_type': 'stationarity',
                'is_stationary': True,
                'adf_statistic': -3.5,
                'p_value': 0.01,
                'interpretation': 'The series is stationary'
            }
        )
        
        # Store ARIMA results
        arima_query = """
        INSERT INTO pipeline_results
        (pipeline_run_id, symbol, result_type, model_summary, forecast, interpretation)
        VALUES (:pipeline_run_id, :symbol, :result_type, :model_summary, :forecast, :interpretation)
        """
        
        session.execute(
            text(arima_query),
            {
                'pipeline_run_id': pipeline_run_id,
                'symbol': 'GME',
                'result_type': 'arima',
                'model_summary': 'ARIMA(1,1,1) model summary...',
                'forecast': json.dumps([101.2, 102.3, 103.5]),
                'interpretation': 'The forecast shows an increasing trend'
            }
        )
        
        # Store GARCH results
        garch_query = """
        INSERT INTO pipeline_results
        (pipeline_run_id, symbol, result_type, model_summary, forecast, interpretation)
        VALUES (:pipeline_run_id, :symbol, :result_type, :model_summary, :forecast, :interpretation)
        """
        
        session.execute(
            text(garch_query),
            {
                'pipeline_run_id': pipeline_run_id,
                'symbol': 'GME',
                'result_type': 'garch',
                'model_summary': 'GARCH(1,1) model summary...',
                'forecast': json.dumps([0.01, 0.015, 0.02]),
                'interpretation': 'Volatility is expected to increase'
            }
        )
        
        # Update pipeline run to completed
        update_query = """
        UPDATE pipeline_runs
        SET status = :status, end_time = NOW(), execution_time_seconds = :execution_time
        WHERE id = :pipeline_run_id
        """
        
        session.execute(
            text(update_query),
            {
                'status': 'completed',
                'execution_time': 1.5,
                'pipeline_run_id': pipeline_run_id
            }
        )
        
        session.commit()
        print("Pipeline results stored successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    store_pipeline_run()
