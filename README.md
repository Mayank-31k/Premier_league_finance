# 🏆 Premier League Performance & Financial Analytics Dashboard

| | |
|---|---|
| | **Made with ❤️ by Mayank Kumar** |

A comprehensive business intelligence dashboard for analyzing the performance and financial metrics of the top 6 Premier League teams across multiple seasons (2020-21 to 2024-25).

![Dashboard Preview](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)

## 🚀 Features

### 📊 **Multi-Season Analysis**
- **5 Complete Seasons**: 2020-21, 2021-22, 2022-23, 2023-24, 2024-25
- **Dynamic Season Selection**: Switch between seasons with real-time data updates
- **Historical Trends**: 5-year revenue progression analysis
- **COVID Impact Analysis**: Includes pandemic effects on 2020-21 revenues

### 💰 **Financial Analytics**
- **Revenue Streams Analysis**: Matchday, Broadcasting, and Commercial revenue breakdown
- **Growth Tracking**: Year-over-year revenue growth percentages
- **Revenue Diversification**: Portfolio analysis across multiple income sources
- **Financial Efficiency Index (FEI)**: Proprietary metric for financial performance evaluation

### ⚽ **Performance Integration** (2024-25 Season)
- **League Table Data**: Points, wins, draws, losses, goals
- **Performance Metrics**: Goal difference, matches played
- **Performance-Financial Correlation**: Analysis of on-field success vs. revenue

### 🎯 **Key Performance Indicators**
- **Season-Specific Targets**: Contextual benchmarks for each time period
- **Real-time Metrics**: Total revenue, commercial share, growth rates
- **Comparative Analysis**: Performance vs. industry benchmarks

### 📈 **Advanced Visualizations**
- **Interactive Charts**: Plotly-powered responsive visualizations
- **Revenue Comparison**: Bar charts comparing team revenues
- **Trend Analysis**: Line charts showing 5-year revenue evolution
- **Portfolio Breakdown**: Pie charts for revenue stream analysis
- **Correlation Plots**: Scatter plots showing performance-revenue relationships
- **Efficiency Metrics**: Color-coded FEI performance indicators

### 🎯 **Business Intelligence**
- **Risk Assessment**: Financial efficiency and diversification analysis
- **Strategic Recommendations**: Data-driven business insights
- **Performance Alerts**: Below-average efficiency warnings
- **Growth Opportunities**: Commercial and matchday revenue optimization

### 📱 **Data Export & Sharing**
- **CSV Export**: Download filtered datasets for external analysis
- **Interactive Filtering**: Multi-select team and season filters
- **Real-time Updates**: Live data integration capabilities

## 🛠️ Tech Stack

### **Backend & Data**
- **Python 3.12+**: Core programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations

### **Frontend & Visualization**
- **Streamlit**: Web application framework
- **Plotly Express**: Interactive plotting library
- **Plotly Graph Objects**: Advanced chart customization

### **Data Sources**
- **Real APIs**: OpenFootball.json for live Premier League data
- **Deloitte Reports**: Financial data from Football Money League
- **Historical Datasets**: 5-year revenue and performance trends

### **Development Tools**
- **Git**: Version control
- **Python Virtual Environment**: Dependency management
- **Streamlit Cloud**: Deployment platform

## 📊 Financial Efficiency Index (FEI)

### **Formula**
```
FEI = (Revenue Growth Factor × Commercial Diversification × Revenue Stability) ÷ Revenue Risk Factor
```

### **Components**
- **Revenue Growth Factor**: `(Revenue Growth% + 10) ÷ 10` (minimum 0.5)
- **Commercial Diversification**: `Commercial Revenue ÷ Total Revenue`
- **Revenue Stability**: `1 + (Matchday Revenue ÷ Total Revenue)`
- **Revenue Risk Factor**: `Total Revenue ÷ £500M` (normalization)

### **Interpretation**
- **FEI > 0.600**: Excellent financial efficiency
- **FEI 0.400-0.600**: Good financial performance
- **FEI < 0.400**: Needs improvement

## 🏃‍♂️ Quick Start

### **Prerequisites**
```bash
Python 3.12+
pip (Python package manager)
```

### **Installation**
```bash
# Clone the repository
git clone <repository-url>
cd Premeir0league

# Install dependencies
pip install streamlit plotly pandas requests

# Run the dashboard
streamlit run premier_league_dashboard.py
```

### **Access**
- **Local**: http://localhost:8501
- **Network**: Use the network URL provided by Streamlit

## 📋 Usage Guide

### **1. Season Selection**
- Use the sidebar dropdown to select any season from 2020-21 to 2024-25
- Data and visualizations update automatically

### **2. Team Filtering**
- Multi-select teams from the top 6 Premier League clubs
- All charts and metrics adjust to selected teams

### **3. Data Analysis**
- **KPIs**: View season-specific financial metrics at the top
- **Visualizations**: Analyze trends through interactive charts
- **FEI Analysis**: Review financial efficiency scores and rankings
- **Risk Assessment**: Identify potential financial risks and opportunities

### **4. Export Data**
- Click "Download CSV Report" to export current filtered data
- Use exported data for external analysis or reporting

## 🏆 Supported Teams

- **Manchester City** 🔵
- **Arsenal** 🔴
- **Liverpool** 🔴
- **Chelsea** 🔵
- **Manchester United** 🔴
- **Tottenham Hotspur** ⚪

## 📊 Data Coverage

### **Performance Data** (2024-25 Season)
- League points and standings
- Goals scored and conceded
- Wins, draws, losses
- Goal difference

### **Financial Data** (All Seasons)
- Total revenue (£M)
- Matchday revenue
- Broadcasting revenue  
- Commercial revenue
- Year-over-year growth rates

### **Historical Analysis**
- 5-year revenue trends
- Season-over-season comparisons
- COVID-19 impact analysis
- Recovery and growth patterns

## 🎯 Business Insights

### **Key Metrics**
- **Revenue Diversification**: Optimal 45% Broadcasting, 35% Commercial, 20% Matchday
- **Growth Targets**: 5-8% annual revenue growth
- **Efficiency Benchmark**: FEI > 0.600 for sustainable performance

### **Risk Indicators**
- Revenue decline warnings
- Over-reliance on single revenue streams
- Below-average financial efficiency alerts
- Growth stagnation identification

## 🚀 Deployment

### **Streamlit Cloud**
1. Push code to GitHub repository
2. Connect to Streamlit Cloud
3. Deploy with automatic updates

### **Local Deployment**
```bash
streamlit run premier_league_dashboard.py --server.port 8501
```

### **Docker Deployment**
```dockerfile
FROM python:3.12-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "premier_league_dashboard.py"]
```

## 📈 Future Enhancements

- [ ] **Additional Leagues**: Expand to other European leagues
- [ ] **Player Analytics**: Individual player performance metrics  
- [ ] **Predictive Modeling**: Revenue forecasting algorithms
- [ ] **Real-time APIs**: Live match and financial data integration
- [ ] **Mobile Optimization**: Enhanced mobile user experience
- [ ] **PDF Reports**: Automated report generation
- [ ] **Database Integration**: PostgreSQL/MongoDB backend
- [ ] **User Authentication**: Multi-user dashboard access

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support, questions, or feature requests:
- Create an issue on GitHub
- Contact the development team
- Check the documentation

## 🙏 Acknowledgments

- **Deloitte**: Football Money League financial data
- **OpenFootball**: Open-source football data
- **Premier League**: Official performance statistics
- **Streamlit Community**: Dashboard framework and support

---

**Built with ❤️ for football analytics enthusiasts**

*Last Updated: August 2025*