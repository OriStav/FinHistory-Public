# Stock Analysis Investment App

## Overview

A comprehensive stock analysis tool built with Streamlit that provides statistical comparisons of historical stock performance from Yahoo Finance. The application helps investors analyze stock performance over different time periods and provides ranking systems to identify optimal investment opportunities.


https://github.com/user-attachments/assets/186ae116-ae6d-4d2c-a790-f8d8a92caa34

## Features

### Core Functionality
- **Historical Performance Analysis**: Compare multiple stocks and indices over customizable time periods
- **Interactive Dashboard**: Built with Streamlit for easy web-based interaction
- **Investment Strategy Simulation**: Simulate investment scenarios with different parameters
- **Statistical Ranking**: Rank stocks based on historical and timing performance metrics
- **Visualization Suite**: Multiple chart types including histograms, line plots, and distribution charts
- **Data Export**: Generate analysis reports and data exports

### Key Metrics
- Historical Rank: Long-term performance comparison
- Timing Rank: Entry/exit timing analysis  
- Yearly Profit Percentage: Annual return calculations
- Risk Assessment: Statistical distribution analysis

*Dividends are not included in profit calculation

### Supported Assets
- US Stocks (NYSE, NASDAQ)
- Australian Stocks (ASX)
- Market Indices (S&P 500, etc.)
- ETFs and Index Funds
- Commodity ETFs (Gold, etc.)

## Installation

### Prerequisites
- Python 3.7+
- Conda or pip package manager

### Dependencies
Install the required packages using conda:

```bash
conda install -c conda-forge streamlit
conda install -c conda-forge yfinance
```

Or using pip:

```bash
pip install streamlit yfinance pandas numpy matplotlib seaborn plotly altair scikit-learn
```

### Additional Dependencies
For enhanced functionality:
```bash
pip install pytickersymbols
```

## Usage

### Running the Application

1. **Streamlit Web App** (Recommended):
   ```bash
   streamlit run app.py
   ```

2. **Command Line Interface**:
   ```bash
   python main.py
   ```

### Configuration

Before running, configure your analysis parameters in `classes/definition.py`:

```python
# Example configuration
symbols = ["^GSPC", "AAPL", "KO", "PEP", "NESN", "ADM"]
investment_duration = "1Y"  # Options: 1Y, 2Y, 5Y, etc.
last_withdrawal = "2024-01-01"
```

### Web Interface Usage

1. **Launch the App**: Run `streamlit run app.py`
2. **Configure Parameters**: Use the sidebar to select:
   - Stock symbols
   - Investment duration
   - Analysis time period
3. **View Results**: 
   - Top section shows key performance indicators
   - Distribution charts show risk analysis
   - Line charts display historical performance
4. **Interpret Rankings**:
   - Higher historical rank = better long-term performance
   - Higher timing rank = better entry/exit timing

## Project Structure

```
├── app.py                 # Main Streamlit application
├── main.py               # Core application logic
├── classes/              # Core business logic classes
│   ├── definition.py     # Configuration and parameters
│   ├── investor.py       # Investment strategy logic
│   ├── miner.py         # Data acquisition and processing
│   └── stocker.py       # Stock data management
├── methods/              # Utility and processing methods
│   ├── charts_design.py  # Visualization and chart generation
│   ├── explainer.py     # Data analysis and ranking
│   ├── read_excel.py    # Excel data import utilities
│   └── st_utils.py      # Streamlit UI utilities
├── proj_consts/         # Project constants and configuration
│   ├── consts.py        # Application constants
│   ├── paths.py         # File path configurations
│   └── paths_base.py    # Base path configurations
└── README.md            # This documentation file
```

## API Documentation

### Main Classes

#### `defs` (Definition Class)
Configuration management for analysis parameters.

**Key Attributes:**
- `symbols`: List of stock symbols to analyze
- `durations`: Investment duration periods
- `logger`: Logging configuration

#### `investor` Class
Manages investment strategy simulations.

**Key Methods:**
- `invest(dfn)`: Execute investment simulation
- `invested(dfn)`: Analyze existing investment positions

#### `stocker` Class
Handles stock data acquisition and processing.

**Key Methods:**
- `trade(dfn, source)`: Execute stock data trading logic
- `stocks_loop(stocks_df)`: Process multiple stock datasets

### Key Functions

#### `main(ui_choices=None)`
Primary application entry point.

**Parameters:**
- `ui_choices` (dict): User interface configuration options

**Returns:**
- `sym_dur_rnk`: Symbol duration rankings
- `latest`: Latest performance data
- `tot_transactions`: Complete transaction history

#### Visualization Functions
- `tables_presenter()`: Display performance tables
- `dist_presenter()`: Show distribution charts
- `lines_presenter()`: Generate line plots

## Configuration Examples

### Basic Stock Analysis
```python
symbols = ["AAPL", "GOOGL", "MSFT", "TSLA"]
durations = ["1Y", "2Y", "5Y"]
```

### Sector Comparison
```python
# Technology sector
tech_symbols = ["AAPL", "GOOGL", "MSFT", "NVDA", "META"]

# Financial sector  
finance_symbols = ["JPM", "BAC", "WFC", "GS", "MS"]
```

### International Markets
```python
# Australian stocks
aus_symbols = ["BHP.AX", "CBA.AX", "CSL.AX", "WBC.AX"]

# ETFs and Indices
etf_symbols = ["^GSPC", "QQQ", "GLD", "VTI"]
```

## Features in Development

### Planned Improvements
1. **Enhanced Comparisons**: Stocks vs. indices vs. retirement funds
2. **Duration Analysis**: Multi-period investment comparison
3. **Dividend Integration**: Include dividend calculations in profit analysis
4. **Risk Metrics**: Enhanced risk assessment tools
5. **Portfolio Optimization**: Multi-asset portfolio analysis

### Technical Improvements
- Database integration for historical data caching
- Enhanced error handling and validation
- Performance optimization for large datasets
- Mobile-responsive interface improvements

## Contributing

### Development Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up development environment
4. Run tests: `python -m pytest tests/`

### Code Style
- Follow PEP 8 Python style guidelines
- Use type hints where applicable
- Maintain comprehensive docstrings
- Write unit tests for new features

### Reporting Issues
Please report bugs and feature requests through the issue tracker with:
- Detailed description of the problem
- Steps to reproduce
- Expected vs. actual behavior
- Environment details (OS, Python version, etc.)

## Important Notes

### Data Limitations
- **Dividends**: Currently not included in profit calculations
- **Real-time Data**: Uses Yahoo Finance with potential delays
- **Market Hours**: Some data may be unavailable outside trading hours

### Platform Compatibility
- **Path Separators**: Modify "/" to "\\" for Windows compatibility in Path class
- **Dependencies**: Ensure all required packages are installed
- **Memory Usage**: Large datasets may require adequate system memory

## Deployment

### Streamlit Community Cloud
For public deployment:
1. Push code to GitHub repository
2. Connect to Streamlit Community Cloud
3. Configure deployment settings
4. Deploy application

Reference: [Streamlit Deployment Guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app)

## Useful Resources

### Documentation
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Yahoo Finance API](https://pypi.org/project/yfinance/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

### Chart Libraries
- [Altair Visualization](https://altair-viz.github.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [Matplotlib Tutorials](https://matplotlib.org/stable/tutorials/index.html)

### Financial Analysis Tools
- [Stock Analysis Resources](https://money.usnews.com/investing/articles/best-free-stock-analysis-tools-research)
- [TipRanks Analysis](https://www.tipranks.com/)

## License

This project is developed for educational and research purposes. Please ensure compliance with data provider terms of service when using financial data.

## Author

**OS made**, 2024

---

*"Data Doesn't Lie... But it Doesn't Tell the Whole Story"*

## Support

For questions, issues, or contributions, please refer to the project repository or contact the development team.