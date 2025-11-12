# Solar Energy Insights Dashboard

Interactive Streamlit dashboard for analyzing global solar irradiance data with beautiful visualizations.

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org)

## Quick Start

```bash
# Clone repository
git clone https://github.com/Kalid-moh/solar-challenge-week0.git
cd solar-challenge-week0

# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run app/main.py
```

## Features

- **Modern UI** - Beautiful gradient design with smooth animations
- **Interactive Filters** - Multi-select countries and metrics
- **Visualizations** - Boxplots, top performers table, statistics
- **Data Explorer** - Search and export filtered data
- **Responsive** - Works on all devices

## Requirements

```txt
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
numpy>=1.24.0
```

## Project Structure

```
solar-challenge-week0/
├── app/
│   ├── main.py          # Main dashboard application
│   └── utils.py         # Helper functions
├── data/                # Local data (gitignored)
│   └── solar_data.csv
└── requirements.txt     # Dependencies
```

## Usage

1. **Load Data**: Place CSV in `data/` folder or upload via UI
2. **Select Countries**: Use sidebar multi-select
3. **Choose Metric**: Select from available metrics (GHI, DNI, DHI, etc.)
4. **Explore**: View distribution, top performers, and data table
5. **Export**: Download filtered data as CSV

## Deployment

Deploy to Streamlit Cloud:

1. Push code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Deploy from `main` branch, file: `app/main.py`

## Data Format

CSV should include:

- Geographic column (country, location, region)
- Numeric metric columns (GHI, DNI, DHI, Tamb, etc.)

## Contributing

```bash
git checkout -b feature/new-feature
git commit -m "feat: add new feature"
git push origin feature/new-feature
```

## Author

**Kalid Mohamed** - [@Kalid-moh](https://github.com/Kalid-moh)

---

Built with using Streamlit | [Live Demo](#) | [Report Bug](https://github.com/Kalid-moh/solar-challenge-week0/issues)
