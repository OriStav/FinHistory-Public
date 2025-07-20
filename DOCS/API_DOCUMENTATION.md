# API Documentation

This document provides detailed technical documentation for the Stock Analysis Investment App's core classes, methods, and functions.

## Table of Contents

- [Core Classes](#core-classes)
- [Main Functions](#main-functions)
- [Utility Methods](#utility-methods)
- [Visualization Functions](#visualization-functions)
- [Configuration Classes](#configuration-classes)
- [Data Models](#data-models)
- [Error Handling](#error-handling)

## Core Classes

### `defs` Class (classes/definition.py)

Configuration management class that handles application parameters and settings.

```python
class defs:
    def __init__(self, ui_choices: dict) -> None
```

**Attributes:**
- `durations`: List of investment duration periods
- `symbols`: List of stock symbols to analyze
- `logger`: Logging configuration object

**Methods:**

#### `stock_symbols_tabler()`
Returns a structured table of predefined stock symbols organized by category.

**Returns:** `pandas.DataFrame` - Categorized stock symbols

#### `from_definition()`
Loads configuration from definition file.

**Returns:** Configuration parameters

#### `set_logger()`
Configures logging for the application.

**Returns:** `logging.Logger` - Configured logger instance

---

### `investor` Class (classes/investor.py)

Handles investment strategy simulation and portfolio management.

```python
def invest(dfn) -> Tuple[pd.DataFrame, pd.DataFrame]
def invested(dfn) -> Tuple[pd.DataFrame, pd.DataFrame]
```

**Parameters:**
- `dfn`: Definition object containing configuration parameters

**Returns:**
- `stocks_df`: DataFrame containing stock price data
- `tot_transactions`: DataFrame containing transaction history

**Functionality:**
- Simulates investment strategies over specified time periods
- Calculates profit/loss for different scenarios
- Manages portfolio allocation and rebalancing

---

### `stocker` Class (classes/stocker.py)

Manages stock data acquisition, processing, and transaction calculations.

```python
def trade(dfn_import, source: Optional[str] = "yfinance") -> Tuple[pd.DataFrame, pd.DataFrame]
```

**Parameters:**
- `dfn_import`: Definition object with configuration
- `source`: Data source provider (default: "yfinance")

**Returns:**
- `stocks_df`: Raw stock data
- `transactions`: Processed transaction data

#### Key Methods:

##### `stocks_loop(stocks_df: pd.DataFrame) -> pd.DataFrame`
Processes multiple stocks through the analysis pipeline.

##### `post_calcs(dif_table: pd.DataFrame) -> pd.DataFrame`
Performs post-processing calculations on transaction data.

##### `calc_deltas(stock: pd.DataFrame) -> pd.DataFrame`
Calculates price differences and percentage changes.

**Parameters:**
- `stock`: DataFrame containing single stock's price data

**Returns:** DataFrame with calculated deltas and metrics

---

### `miner` Class (classes/miner.py)

Handles data acquisition from external APIs and data sources.

```python
def mine(dfn, source: str) -> pd.DataFrame
```

**Parameters:**
- `dfn`: Definition object with symbols and parameters
- `source`: Data source identifier

**Returns:** `pd.DataFrame` - Raw stock price data

**Functionality:**
- Connects to Yahoo Finance API
- Handles API rate limiting and errors
- Formats and validates retrieved data

## Main Functions

### `main(ui_choices: dict = None)`

Primary application entry point that orchestrates the analysis workflow.

**Parameters:**
- `ui_choices`: Dictionary containing user interface selections
  - `symbols`: List of stock symbols
  - `durations`: Investment time periods
  - `start_date`: Analysis start date
  - `end_date`: Analysis end date

**Returns:**
- `sym_dur_rnk`: Symbol duration rankings DataFrame
- `latest`: Latest performance metrics DataFrame
- `tot_transactions`: Complete transaction history DataFrame

**Example Usage:**
```python
ui_choices = {
    "symbols": ["AAPL", "GOOGL", "MSFT"],
    "durations": ["1Y", "2Y", "5Y"],
    "start_date": "2020-01-01",
    "end_date": "2024-01-01"
}
rankings, latest, transactions = main(ui_choices)
```

### `main_util(ui_choices: dict = None, invested_bool: bool = False)`

Utility function that handles the core analysis logic.

**Parameters:**
- `ui_choices`: User configuration dictionary
- `invested_bool`: Whether to analyze existing investments

**Returns:**
- `tot_transactions`: All transaction data
- `stocks_df`: Raw stock price data
- `sym_dur_grp`: Grouped symbol duration data
- `sym_dur_rnk`: Ranked analysis results

## Utility Methods

### Explainer Module (methods/explainer.py)

#### `agg_sym_dur(tot_transactions: pd.DataFrame) -> pd.DataFrame`

Aggregates transaction data by symbol and duration.

**Parameters:**
- `tot_transactions`: Complete transaction DataFrame

**Returns:** Aggregated data grouped by symbol and duration

#### `rnk(sym_dur_grp: pd.DataFrame) -> pd.DataFrame`

Ranks stocks based on performance metrics.

**Parameters:**
- `sym_dur_grp`: Grouped symbol duration data

**Returns:** DataFrame with ranking columns added

#### `latest_rnk(tot_transactions: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]`

Calculates latest performance rankings.

**Returns:**
- Latest performance data
- Summary statistics

### Streamlit Utils (methods/st_utils.py)

#### `choices_section() -> dict`

Creates Streamlit sidebar for user input selection.

**Returns:** Dictionary containing user selections

#### `selections() -> dict`

Handles advanced selection options in the UI.

#### `table_filter(df: pd.DataFrame, column: str, value: any) -> pd.DataFrame`

Filters DataFrame based on column values for display.

## Visualization Functions

### Charts Design Module (methods/charts_design.py)

#### `tables_presenter(sym_dur_rnk: pd.DataFrame, latest: pd.DataFrame)`

Displays performance tables in Streamlit interface.

**Parameters:**
- `sym_dur_rnk`: Ranked symbol duration data
- `latest`: Latest performance metrics

#### `dist_presenter(tot_transactions: pd.DataFrame)`

Creates and displays distribution charts.

**Parameters:**
- `tot_transactions`: Transaction data for visualization

#### `lines_presenter(tot_transactions: pd.DataFrame)`

Generates line plots for historical performance.

#### `alt_violin(tot_transactions: pd.DataFrame, para: str = "yearly_profit_percentage", by: str = "Symdur")`

Creates violin plots using Altair.

**Parameters:**
- `tot_transactions`: Data to plot
- `para`: Parameter to visualize
- `by`: Grouping variable

#### `alt_line_plot(plt_table: pd.DataFrame, header: str, x_col: str, y_col: str, color_col: str)`

Generates interactive line plots.

**Parameters:**
- `plt_table`: Data for plotting
- `header`: Chart title
- `x_col`: X-axis column name
- `y_col`: Y-axis column name
- `color_col`: Color grouping column

#### Chart Styling Functions:

##### `make_pretty(styler) -> pd.io.formats.style.Styler`
Applies visual styling to pandas DataFrames.

##### `normalizer(df: pd.DataFrame, val: str, cat: str) -> pd.DataFrame`
Normalizes data for comparative visualization.

## Configuration Classes

### Constants (proj_consts/consts.py)

Application-wide constants and configuration values.

### Paths (proj_consts/paths.py)

File path management and configuration.

```python
class Paths:
    def __init__(self):
        self.base_path = os.path.dirname(__file__)
        self.data_path = os.path.join(self.base_path, "data")
        self.output_path = os.path.join(self.base_path, "output")
```

## Data Models

### Transaction DataFrame Structure

Standard structure for transaction data:

```python
columns = [
    'Symbol',                    # Stock symbol
    'investment_date',           # Purchase date
    'withdrawal_date',          # Sale date
    'investment_duration',      # Holding period
    'investment_close',         # Purchase price
    'withdrawal_close',         # Sale price
    'profit_loss',              # Absolute profit/loss
    'yearly_profit_percentage', # Annualized return %
    'Symdur'                   # Symbol-Duration combination
]
```

### Ranking DataFrame Structure

Structure for performance rankings:

```python
columns = [
    'Symbol',                   # Stock symbol
    'investment_duration',      # Time period
    'avg_profit_percentage',    # Average return
    'std_profit_percentage',    # Return standard deviation
    'rank_historical',          # Historical performance rank
    'rank_timing',             # Timing-based rank
    'rank_overall'             # Combined ranking score
]
```

## Error Handling

### Common Exceptions

#### `DataAcquisitionError`
Raised when stock data cannot be retrieved from external APIs.

#### `InvalidSymbolError`
Raised when provided stock symbols are invalid or not found.

#### `ConfigurationError`
Raised when configuration parameters are invalid or missing.

### Error Handling Patterns

```python
try:
    stocks_df = mine(dfn, source)
    if len(stocks_df) == 0:
        raise DataAcquisitionError("No data retrieved")
except Exception as e:
    logger.error(f"Data acquisition failed: {str(e)}")
    return pd.DataFrame(), pd.DataFrame()
```

## Performance Considerations

### Memory Optimization
- Use chunked data processing for large datasets
- Implement data caching for frequently accessed symbols
- Clear intermediate DataFrames when not needed

### API Rate Limiting
- Implement exponential backoff for API requests
- Cache historical data to reduce API calls
- Handle API timeouts gracefully

### Computational Efficiency
- Vectorize operations using pandas/numpy
- Use appropriate data types for memory efficiency
- Implement parallel processing for independent calculations

## Extension Points

### Adding New Data Sources
1. Implement new miner class following the `mine()` interface
2. Update `trade()` function to handle new source parameter
3. Add appropriate error handling for new API

### Custom Metrics
1. Add metric calculation in `post_calcs()` function
2. Update visualization functions to display new metrics
3. Modify ranking algorithms to include new metrics

### New Visualization Types
1. Create new chart functions in `charts_design.py`
2. Add corresponding presenter function
3. Integrate with Streamlit interface in `app.py`

## Testing

### Unit Test Structure
```python
def test_main_functionality():
    """Test main analysis workflow"""
    ui_choices = {"symbols": ["AAPL"], "durations": ["1Y"]}
    result = main(ui_choices)
    assert len(result) == 3
    assert all(isinstance(df, pd.DataFrame) for df in result)
```

### Integration Test Examples
```python
def test_end_to_end_analysis():
    """Test complete analysis pipeline"""
    # Setup test data
    # Run analysis
    # Verify results
```

## Version Compatibility

### Python Version Requirements
- Minimum: Python 3.7
- Recommended: Python 3.9+
- Tested: Python 3.8, 3.9, 3.10, 3.11

### Dependency Version Matrix
See `requirements.txt` for specific version requirements and compatibility information.

---

For additional technical support or clarification on API usage, please refer to the source code comments and docstrings within each module.