# Option Strategy Analyzer - Desktop Application

A standalone desktop GUI application for analyzing option strategies, specifically Bullish and Bearish Risk Reversals. This application has been refactored from a Flask web application into a native Windows desktop application using Python's Tkinter.

## Features

- **Desktop GUI**: Native Windows application with intuitive interface
- **Real-time Analysis**: Analyzes option chains using Yahoo Finance data
- **Strategy Types**: Supports both Bullish and Bearish Risk Reversal strategies
- **Customizable Parameters**: Set ticker symbol, minimum/maximum days to expiration (DTE)
- **Threaded Processing**: Analysis runs in background to prevent GUI freezing
- **Detailed Reports**: Comprehensive text-based analysis reports
- **Single Executable**: Can be distributed as a single .exe file

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Windows 10/11

### Development Setup
1. Clone or download the project files
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
1. **Development Mode**: Run the Python script directly
   ```bash
   python main_app.py
   ```

2. **Build Executable**: Create a standalone .exe file
   ```bash
   build.bat
   ```
   The executable will be created in the `dist/` folder as `OptionAnalyzer.exe`

## Usage

### GUI Interface
1. **Ticker Symbol**: Enter the stock ticker (e.g., AAPL, TSLA, SPY)
2. **DTE Range**: Set minimum and maximum days to expiration
3. **Strategy Selection**: Choose between Bullish or Bearish
4. **Run Analysis**: Click the "Run Analysis" button or press Enter
5. **View Results**: Analysis results appear in the scrollable text area

### Input Parameters
- **Ticker Symbol**: Any valid stock symbol available on Yahoo Finance
- **Minimum DTE**: Minimum days to expiration (recommended: 30+ days)
- **Maximum DTE**: Maximum days to expiration (recommended: 90-180 days)
- **Strategy**: 
  - **Bullish**: Long OTM Call + Short OTM Put
  - **Bearish**: Long OTM Put + Short OTM Call

### Analysis Output
The application generates detailed reports including:
- Top recommended trade with key metrics
- Strategy overview and risk warnings
- Analysis summary by expiration date
- Top 5 combinations ranked by score
- Key metrics: Net Cost, Net Vega, Efficiency, Breakeven

## Strategy Details

### Bullish Risk Reversal
- **Structure**: Long OTM Call + Short OTM Put
- **Objective**: Synthetic long stock position with low/zero cost
- **Primary Risk**: Short put assignment if stock falls below strike
- **Best For**: Bullish outlook with limited capital

### Bearish Risk Reversal
- **Structure**: Long OTM Put + Short OTM Call
- **Objective**: Synthetic short stock position with low/zero cost
- **Primary Risk**: Short call assignment if stock rises above strike
- **Best For**: Bearish outlook with limited capital

## Technical Details

### Architecture
- **Frontend**: Tkinter GUI framework
- **Backend**: Custom analysis engine with Black-Scholes calculations
- **Data Source**: Yahoo Finance API (yfinance)
- **Threading**: Background processing to maintain GUI responsiveness

### Key Components
- `main_app.py`: Main GUI application and entry point
- `analysis_engine.py`: Core analysis logic and calculations
- `build.bat`: PyInstaller build script for creating executable

### Dependencies
- `yfinance`: Yahoo Finance data access
- `pandas`: Data manipulation and analysis
- `numpy`: Numerical computations
- `scipy`: Statistical functions (normal distribution)
- `pyinstaller`: Executable packaging

## Building the Executable

### Automatic Build
Run the provided build script:
```bash
build.bat
```

### Manual Build
If you need to customize the build:
```bash
pyinstaller --onefile --windowed --name="OptionAnalyzer" main_app.py
```

### Build Options
- `--onefile`: Creates a single executable file
- `--windowed`: Runs without console window
- `--name`: Sets the output filename

## Troubleshooting

### Common Issues
1. **"No expirations found"**: Try different DTE ranges or ticker symbols
2. **"No valid strategies"**: The ticker may not have suitable options data
3. **Slow analysis**: Network delays when fetching data from Yahoo Finance
4. **GUI freezing**: Analysis runs in background - wait for completion

### Data Limitations
- Requires active internet connection
- Depends on Yahoo Finance data availability
- Some tickers may have limited options data
- Market hours may affect data freshness

## Testing

Run the test script to verify functionality:
```bash
python test_analysis.py
```

This will test both bullish and bearish analysis with sample data.

## Distribution

The built executable (`OptionAnalyzer.exe`) can be distributed to any Windows computer without requiring Python installation. Users simply need to:
1. Download the .exe file
2. Double-click to run
3. No installation required

## License

This application is for educational and research purposes. Always verify analysis results and consult with financial professionals before making investment decisions.

## Disclaimer

This software is provided "as is" without warranty. Option trading involves substantial risk and is not suitable for all investors. Past performance does not guarantee future results. Always conduct your own research and consider consulting with a financial advisor. 