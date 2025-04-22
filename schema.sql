-- schema.sql
-- initialize the timeseries database schema

-- pipeline run tracking
create table if not exists pipeline_runs (
    id serial primary key,
    name varchar(255) not null,
    status varchar(50) not null,
    source_type varchar(50),
    start_date varchar(50),
    end_date varchar(50), 
    start_time timestamp default current_timestamp,
    end_time timestamp,
    execution_time_seconds float,
    symbols text[]
);

-- pipeline results for each symbol/operation
create table if not exists pipeline_results (
    id serial primary key,
    pipeline_run_id integer references pipeline_runs(id) on delete cascade,
    symbol varchar(50) not null,
    result_type varchar(50) not null,  -- 'arima', 'garch', 'stationarity'
    is_stationary boolean,
    adf_statistic float,
    p_value float,
    model_summary text,
    forecast jsonb,  -- store forecast values as json
    interpretation text
);
