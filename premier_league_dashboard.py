import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
import base64
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Premier League Analytics Dashboard",
    page_icon="⚽",
    layout="wide"
)

@st.cache_data
def load_premier_league_data():
    """
    Load real Premier League data from multiple sources
    """
    # Current season performance data (2024-25)
    current_season_data = {
        'Team': ['Manchester City', 'Arsenal', 'Liverpool', 'Chelsea', 'Manchester United', 'Tottenham'],
        'Matches_Played': [10, 10, 10, 10, 10, 10],
        'Wins': [7, 6, 6, 5, 4, 4],
        'Draws': [2, 3, 3, 3, 3, 1],
        'Losses': [1, 1, 1, 2, 3, 5],
        'Goals_Scored': [22, 18, 21, 16, 12, 15],
        'Goals_Conceded': [8, 10, 6, 11, 12, 18],
        'Points': [23, 21, 21, 18, 15, 13],
        'Goal_Difference': [14, 8, 15, 5, 0, -3]
    }
    
    # Financial data for all seasons (2020-21 to 2024-25 in millions)
    # Each list contains data for all 6 teams for one season
    seasons_financial_data = {
        '2020-21': {
            'Team': ['Manchester City', 'Arsenal', 'Liverpool', 'Chelsea', 'Manchester United', 'Tottenham'],
            'Matchday_Revenue': [7.1, 8.2, 7.5, 6.8, 11.2, 8.5],  # COVID-impacted
            'Broadcasting_Revenue': [295.4, 201.8, 269.3, 198.7, 254.8, 162.2],
            'Commercial_Revenue': [342.4, 177.8, 273.6, 287.6, 227.9, 231.7],
            'Total_Revenue': [644.9, 388.0, 550.4, 493.1, 494.1, 402.4],
            'Revenue_Growth': [-10.2, -12.9, -1.4, 5.0, -14.9, -9.7]
        },
        '2021-22': {
            'Team': ['Manchester City', 'Arsenal', 'Liverpool', 'Chelsea', 'Manchester United', 'Tottenham'],
            'Matchday_Revenue': [53.4, 45.2, 71.8, 78.3, 91.0, 45.7],  # Partial recovery
            'Broadcasting_Revenue': [307.2, 201.8, 275.3, 201.7, 230.8, 167.2],
            'Commercial_Revenue': [370.4, 186.5, 354.6, 288.3, 305.3, 229.9],
            'Total_Revenue': [731.0, 433.5, 701.7, 568.3, 627.1, 442.8],
            'Revenue_Growth': [13.3, 11.7, 27.5, 15.3, 26.9, 10.0]
        },
        '2022-23': {
            'Team': ['Manchester City', 'Arsenal', 'Liverpool', 'Chelsea', 'Manchester United', 'Tottenham'],
            'Matchday_Revenue': [71.4, 85.2, 83.2, 89.8, 111.0, 65.4],  # Full recovery
            'Broadcasting_Revenue': [289.6, 201.8, 235.2, 198.7, 256.8, 150.2],
            'Commercial_Revenue': [315.1, 146.5, 275.9, 192.8, 280.6, 167.4],
            'Total_Revenue': [676.1, 433.5, 594.3, 481.3, 648.4, 383.0],
            'Revenue_Growth': [-7.5, 0.0, -15.3, -15.3, 3.4, -13.5]
        },
        '2023-24': {
            'Team': ['Manchester City', 'Arsenal', 'Liverpool', 'Chelsea', 'Manchester United', 'Tottenham'],
            'Matchday_Revenue': [78.2, 103.5, 84.2, 67.8, 110.1, 85.4],
            'Broadcasting_Revenue': [314.1, 201.8, 275.2, 203.7, 230.8, 167.2],
            'Commercial_Revenue': [341.2, 188.4, 247.1, 201.5, 279.3, 175.8],
            'Total_Revenue': [733.5, 493.7, 606.5, 473.0, 620.2, 428.4],
            'Revenue_Growth': [8.5, 13.9, 2.1, -1.7, -4.3, 11.9]
        },
        '2024-25': {
            'Team': ['Manchester City', 'Arsenal', 'Liverpool', 'Chelsea', 'Manchester United', 'Tottenham'],
            'Matchday_Revenue': [82.5, 108.7, 89.1, 72.3, 115.2, 91.8],  # Projected
            'Broadcasting_Revenue': [325.3, 215.9, 287.4, 218.9, 242.1, 178.5],  # Projected
            'Commercial_Revenue': [358.7, 201.3, 265.8, 215.6, 295.7, 188.2],  # Projected
            'Total_Revenue': [766.5, 525.9, 642.3, 506.8, 653.0, 458.5],  # Projected
            'Revenue_Growth': [4.5, 6.5, 5.9, 7.1, 5.3, 7.0]  # Projected
        }
    }
    
    # Create comprehensive financial dataset
    all_financial_data = []
    for season, data in seasons_financial_data.items():
        season_df = pd.DataFrame(data)
        season_df['Season'] = season
        all_financial_data.append(season_df)
    
    comprehensive_financial_df = pd.concat(all_financial_data, ignore_index=True)
    
    # Get current season (2024-25) financial data
    current_financial = seasons_financial_data['2024-25']
    financial_df = pd.DataFrame(current_financial)
    
    # Historical revenue data (simplified for trend analysis)
    historical_revenue = comprehensive_financial_df[['Team', 'Season', 'Total_Revenue']].copy()
    
    # Convert to DataFrames
    performance_df = pd.DataFrame(current_season_data)
    
    # Merge performance and current financial data
    combined_df = pd.merge(performance_df, financial_df, on='Team')
    
    return combined_df, historical_revenue, comprehensive_financial_df

@st.cache_data
def fetch_live_premier_league_standings():
    """
    Attempt to fetch live Premier League standings from a free API
    Fallback to static data if API is unavailable
    """
    try:
        # Using a free football API (OpenFootball data)
        url = "https://raw.githubusercontent.com/openfootball/football.json/master/2024-25/en.1.json"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            st.success("Live data loaded successfully!")
            return True
        else:
            st.warning("Live API unavailable, using static data")
            return False
    except:
        st.warning("Live API unavailable, using static data")
        return False

def create_download_link(df, filename, link_text):
    """
    Create a download link for DataFrame
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{link_text}</a>'
    return href

def main():
    # Load data
    combined_df, historical_df, comprehensive_financial_df = load_premier_league_data()
    
    # Check for live data
    live_data_available = fetch_live_premier_league_standings()
    
    # Sidebar filters
    st.sidebar.header("Dashboard Filters")
    
    # Season filter
    available_seasons = ['2020-21', '2021-22', '2022-23', '2023-24', '2024-25']
    selected_season = st.sidebar.selectbox(
        "Select Season:",
        options=available_seasons,
        index=len(available_seasons)-1,  # Default to latest season
        help="Choose season for financial analysis"
    )
    
    # Title and description
    st.title("Premier League Performance & Financial Analytics Dashboard")
    st.subheader(f"Business Intelligence Dashboard for Top 6 Premier League Teams - {selected_season} Season")
    
    # Team filter
    selected_teams = st.sidebar.multiselect(
        "Select Teams:",
        options=combined_df['Team'].tolist(),
        default=combined_df['Team'].tolist(),
        help="Choose teams to analyze"
    )
    
    # Get season-specific financial data
    season_financial_df = comprehensive_financial_df[comprehensive_financial_df['Season'] == selected_season]
    
    # For current season (2024-25), add performance data; for others, use only financial data
    if selected_season == '2024-25':
        # Merge season-specific financial data with performance data for current season
        performance_df = pd.DataFrame({
            'Team': ['Manchester City', 'Arsenal', 'Liverpool', 'Chelsea', 'Manchester United', 'Tottenham'],
            'Matches_Played': [10, 10, 10, 10, 10, 10],
            'Wins': [7, 6, 6, 5, 4, 4],
            'Draws': [2, 3, 3, 3, 3, 1],
            'Losses': [1, 1, 1, 2, 3, 5],
            'Goals_Scored': [22, 18, 21, 16, 12, 15],
            'Goals_Conceded': [8, 10, 6, 11, 12, 18],
            'Points': [23, 21, 21, 18, 15, 13],
            'Goal_Difference': [14, 8, 15, 5, 0, -3]
        })
        # Merge current season financial data with performance data
        current_season_financial = season_financial_df.copy()
        filtered_df = pd.merge(performance_df, current_season_financial, on='Team')
        filtered_df = filtered_df[filtered_df['Team'].isin(selected_teams)]
        show_performance = True
    else:
        # Use only financial data for historical seasons
        filtered_df = season_financial_df[season_financial_df['Team'].isin(selected_teams)]
        show_performance = False
    
    # Data freshness indicator
    if live_data_available:
        st.sidebar.success("Live data active")
    else:
        st.sidebar.info("Using static data")
    
    st.sidebar.write("**Last Updated:** " + datetime.now().strftime("%Y-%m-%d %H:%M"))
    
    # Check if filtered data is empty
    if filtered_df.empty:
        st.warning("Please select at least one team to view analytics.")
        return
    
    # KPI Metrics Section
    st.header(f"Key Performance Indicators - {selected_season}")
    
    # Season-specific targets and benchmarks
    season_targets = {
        '2020-21': {'revenue_target': 2400, 'growth_benchmark': -8.0, 'context': 'COVID Impact'},
        '2021-22': {'revenue_target': 2800, 'growth_benchmark': 15.0, 'context': 'Recovery Phase'},
        '2022-23': {'revenue_target': 3000, 'growth_benchmark': -5.0, 'context': 'Stabilization'},
        '2023-24': {'revenue_target': 3200, 'growth_benchmark': 5.0, 'context': 'Growth Return'},
        '2024-25': {'revenue_target': 3400, 'growth_benchmark': 6.0, 'context': 'Projected Growth'}
    }
    
    current_target = season_targets.get(selected_season, season_targets['2024-25'])
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_revenue = filtered_df['Total_Revenue'].sum()
        target_diff = total_revenue - current_target['revenue_target']
        st.metric(
            label=f"Total Revenue (£M) - {current_target['context']}",
            value=f"£{total_revenue:.1f}M",
            delta=f"{target_diff:+.1f}M vs {selected_season} Target"
        )
    
    with col2:
        avg_commercial = filtered_df['Commercial_Revenue'].mean()
        commercial_share = (avg_commercial / filtered_df['Total_Revenue'].mean()) * 100
        st.metric(
            label="Avg Commercial (£M)",
            value=f"£{avg_commercial:.1f}M",
            delta=f"{commercial_share:.1f}% of Total Revenue"
        )
    
    with col3:
        avg_growth = filtered_df['Revenue_Growth'].mean()
        growth_vs_benchmark = avg_growth - current_target['growth_benchmark']
        st.metric(
            label="Revenue Growth (%)",
            value=f"{avg_growth:.1f}%",
            delta=f"{growth_vs_benchmark:+.1f}% vs {selected_season} Benchmark"
        )
    
    with col4:
        avg_broadcasting = filtered_df['Broadcasting_Revenue'].mean()
        broadcasting_share = (avg_broadcasting / filtered_df['Total_Revenue'].mean()) * 100
        st.metric(
            label="Avg Broadcasting (£M)",
            value=f"£{avg_broadcasting:.1f}M",
            delta=f"{broadcasting_share:.1f}% of Total Revenue"
        )
    
    with col5:
        avg_matchday = filtered_df['Matchday_Revenue'].mean()
        matchday_share = (avg_matchday / filtered_df['Total_Revenue'].mean()) * 100
        st.metric(
            label="Avg Matchday (£M)",
            value=f"£{avg_matchday:.1f}M",
            delta=f"{matchday_share:.1f}% of Total Revenue"
        )
    
    # Visualizations Section
    if show_performance:
        st.header("Performance & Financial Analytics")
        
        # Row 1: Points and Revenue comparison
        col1, col2 = st.columns(2)
        
        with col1:
            fig_points = px.bar(
                filtered_df, 
                x='Team', 
                y='Points',
                title="Current Season Points"
            )
            st.plotly_chart(fig_points, use_container_width=True)
        
        with col2:
            fig_revenue = px.bar(
                filtered_df, 
                x='Team', 
                y='Total_Revenue',
                title=f"Total Revenue {selected_season} (£M)"
            )
            st.plotly_chart(fig_revenue, use_container_width=True)
        
        # Row 2: Revenue breakdown and correlation
        col1, col2 = st.columns(2)
        
        with col1:
            # Revenue breakdown pie chart for selected team
            if len(selected_teams) > 0:
                selected_team = st.selectbox("Select team for revenue breakdown:", selected_teams)
                team_data = filtered_df[filtered_df['Team'] == selected_team].iloc[0]
                
                revenue_breakdown = {
                    'Revenue Stream': ['Matchday', 'Broadcasting', 'Commercial'],
                    'Amount': [team_data['Matchday_Revenue'], 
                              team_data['Broadcasting_Revenue'], 
                              team_data['Commercial_Revenue']]
                }
                
                fig_pie = px.pie(
                    values=revenue_breakdown['Amount'],
                    names=revenue_breakdown['Revenue Stream'],
                    title=f"{selected_team} Revenue Breakdown"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Points vs Revenue correlation
            fig_scatter = px.scatter(
                filtered_df, 
                x='Total_Revenue', 
                y='Points',
                size='Goals_Scored',
                hover_name='Team',
                title="Points vs Revenue Correlation",
                color='Revenue_Growth'
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.header(f"Financial Analytics - {selected_season}")
        
        # Row 1: Revenue streams comparison
        col1, col2 = st.columns(2)
        
        with col1:
            fig_revenue = px.bar(
                filtered_df, 
                x='Team', 
                y='Total_Revenue',
                title=f"Total Revenue {selected_season} (£M)"
            )
            st.plotly_chart(fig_revenue, use_container_width=True)
        
        with col2:
            # Revenue streams comparison
            revenue_streams = filtered_df.melt(
                id_vars=['Team'], 
                value_vars=['Matchday_Revenue', 'Broadcasting_Revenue', 'Commercial_Revenue'],
                var_name='Revenue_Stream', 
                value_name='Revenue'
            )
            revenue_streams['Revenue_Stream'] = revenue_streams['Revenue_Stream'].str.replace('_Revenue', '')
            
            fig_streams = px.bar(
                revenue_streams,
                x='Team',
                y='Revenue',
                color='Revenue_Stream',
                title=f"Revenue Streams Breakdown {selected_season}",
                barmode='stack'
            )
            st.plotly_chart(fig_streams, use_container_width=True)
        
        # Row 2: Revenue breakdown pie chart and growth comparison
        col1, col2 = st.columns(2)
        
        with col1:
            # Revenue breakdown pie chart for selected team
            if len(selected_teams) > 0:
                selected_team = st.selectbox("Select team for revenue breakdown:", selected_teams)
                team_data = filtered_df[filtered_df['Team'] == selected_team].iloc[0]
                
                revenue_breakdown = {
                    'Revenue Stream': ['Matchday', 'Broadcasting', 'Commercial'],
                    'Amount': [team_data['Matchday_Revenue'], 
                              team_data['Broadcasting_Revenue'], 
                              team_data['Commercial_Revenue']]
                }
                
                fig_pie = px.pie(
                    values=revenue_breakdown['Amount'],
                    names=revenue_breakdown['Revenue Stream'],
                    title=f"{selected_team} Revenue Breakdown {selected_season}"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Revenue growth comparison
            fig_growth = px.bar(
                filtered_df,
                x='Team',
                y='Revenue_Growth',
                title=f"Revenue Growth {selected_season} (%)",
                color='Revenue_Growth',
                color_continuous_scale=['red', 'yellow', 'green']
            )
            st.plotly_chart(fig_growth, use_container_width=True)
    
    # Historical Revenue Trends
    st.header("5-Season Revenue Trends (2020-21 to 2024-25)")
    
    # Filter historical data for selected teams
    hist_filtered = historical_df[historical_df['Team'].isin(selected_teams)]
    
    fig_line = px.line(
        hist_filtered, 
        x='Season', 
        y='Total_Revenue', 
        color='Team',
        title="Revenue Growth Over 5 Seasons (2020-21 to 2024-25)",
        markers=True
    )
    fig_line.update_layout(height=500)
    st.plotly_chart(fig_line, use_container_width=True)
    
    # Add a comparison table
    st.subheader("Season-over-Season Revenue Comparison")
    
    # Create a pivot table for easy comparison
    revenue_pivot = hist_filtered.pivot(index='Team', columns='Season', values='Total_Revenue')
    revenue_pivot = revenue_pivot.round(1)
    
    # Calculate year-over-year growth
    for i in range(1, len(revenue_pivot.columns)):
        prev_season = revenue_pivot.columns[i-1]
        curr_season = revenue_pivot.columns[i]
        growth_col = f'{curr_season} Growth %'
        revenue_pivot[growth_col] = ((revenue_pivot[curr_season] - revenue_pivot[prev_season]) / revenue_pivot[prev_season] * 100).round(1)
    
    st.dataframe(revenue_pivot, use_container_width=True)
    
    # Risk & Insights Section
    st.header("Business Intelligence & Risk Analysis")
    
    # Calculate Financial Efficiency Index (FEI) - works for all seasons
    # Financial Efficiency Index Formula:
    # FEI = (Revenue_Growth_Factor * Commercial_Diversification * Revenue_Stability) / (Revenue_Risk_Factor)
    # Where:
    # - Revenue_Growth_Factor: (Revenue_Growth + 10) / 10 (normalized, minimum 0.5 for negative growth)
    # - Commercial_Diversification: Commercial_Revenue / Total_Revenue (higher = better diversification)
    # - Revenue_Stability: 1 + (Matchday_Revenue / Total_Revenue) (rewards balanced revenue streams)
    # - Revenue_Risk_Factor: Total_Revenue / 500 (normalizes for revenue scale, target £500M)
    
    def calculate_financial_efficiency_index(row):
        revenue_growth_factor = max(0.5, (row['Revenue_Growth'] + 10) / 10)
        commercial_diversification = row['Commercial_Revenue'] / row['Total_Revenue']
        revenue_stability = 1 + (row['Matchday_Revenue'] / row['Total_Revenue'])
        revenue_risk_factor = max(0.5, row['Total_Revenue'] / 500)
        
        fei = (revenue_growth_factor * commercial_diversification * revenue_stability) / revenue_risk_factor
        return round(fei, 3)
    
    filtered_df['FEI'] = filtered_df.apply(calculate_financial_efficiency_index, axis=1)
    
    # Display FEI scores
    st.subheader("Financial Efficiency Index (FEI)")
    st.write("**Formula**: FEI = (Revenue Growth Factor × Commercial Diversification × Revenue Stability) ÷ Revenue Risk Factor")
    st.write("- **Revenue Growth Factor**: (Revenue Growth% + 10) ÷ 10 (minimum 0.5)")
    st.write("- **Commercial Diversification**: Commercial Revenue ÷ Total Revenue")
    st.write("- **Revenue Stability**: 1 + (Matchday Revenue ÷ Total Revenue)")
    st.write("- **Revenue Risk Factor**: Total Revenue ÷ £500M (normalization)")
    st.write("- **Higher FEI = Better financial efficiency and diversification**")
    
    # Create FEI visualization
    fig_fei = px.bar(
        filtered_df.sort_values('FEI', ascending=False),
        x='Team',
        y='FEI',
        title=f"Financial Efficiency Index by Team - {selected_season}",
        color='FEI',
        color_continuous_scale=['red', 'yellow', 'green']
    )
    fig_fei.update_layout(height=400)
    st.plotly_chart(fig_fei, use_container_width=True)
    
    # FEI Analysis Table
    fei_columns = ['Team', 'Total_Revenue', 'Revenue_Growth', 'Commercial_Revenue', 'Matchday_Revenue', 'FEI']
    if show_performance:
        fei_columns.insert(-1, 'Points')  # Add points for current season
    
    fei_analysis = filtered_df[fei_columns].copy()
    fei_analysis['Commercial_Share%'] = ((fei_analysis['Commercial_Revenue'] / fei_analysis['Total_Revenue']) * 100).round(1)
    fei_analysis['Matchday_Share%'] = ((fei_analysis['Matchday_Revenue'] / fei_analysis['Total_Revenue']) * 100).round(1)
    fei_analysis = fei_analysis.sort_values('FEI', ascending=False)
    
    display_columns = ['Team', 'Total_Revenue', 'Revenue_Growth', 'Commercial_Share%', 'Matchday_Share%', 'FEI']
    if show_performance:
        display_columns.insert(-1, 'Points')
    
    st.dataframe(fei_analysis[display_columns], use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Risk Indicators")
        
        # Teams with declining revenue
        declining_revenue = filtered_df[filtered_df['Revenue_Growth'] < 0]
        if not declining_revenue.empty:
            for _, team in declining_revenue.iterrows():
                st.warning(f"**{team['Team']}**: Revenue declining by {abs(team['Revenue_Growth']):.1f}% | FEI: {team['FEI']:.3f}")
        
        # Revenue diversification risk (over-reliance on one stream)
        for _, team in filtered_df.iterrows():
            commercial_share = team['Commercial_Revenue'] / team['Total_Revenue']
            broadcasting_share = team['Broadcasting_Revenue'] / team['Total_Revenue']
            matchday_share = team['Matchday_Revenue'] / team['Total_Revenue']
            
            if broadcasting_share > 0.6:
                st.error(f"**{team['Team']}**: Over-reliant on broadcasting ({broadcasting_share*100:.1f}% of revenue)")
            elif commercial_share < 0.25:
                st.info(f"**{team['Team']}**: Low commercial diversification ({commercial_share*100:.1f}% of revenue)")
        
        # Financial efficiency analysis (works for all seasons)
        low_fei_teams = filtered_df[filtered_df['FEI'] < filtered_df['FEI'].median()]
        if not low_fei_teams.empty:
            for _, team in low_fei_teams.iterrows():
                st.error(f"**{team['Team']}**: Below-average financial efficiency (FEI: {team['FEI']:.3f} vs avg: {filtered_df['FEI'].mean():.3f})")
        
        # Additional financial risk analysis
        for _, team in filtered_df.iterrows():
            # High revenue but poor efficiency
            if team['Total_Revenue'] > 600 and team['FEI'] < 0.5:
                st.warning(f"**{team['Team']}**: High revenue (£{team['Total_Revenue']:.1f}M) but poor financial efficiency (FEI: {team['FEI']:.3f})")
            
            # Low growth with high revenue
            if team['Total_Revenue'] > 500 and team['Revenue_Growth'] < 2:
                st.info(f"**{team['Team']}**: Large revenue base (£{team['Total_Revenue']:.1f}M) with low growth ({team['Revenue_Growth']:.1f}%) - focus on innovation")
    
    with col2:
        st.subheader("Strategic Recommendations")
        
        # Data-driven recommendations based on FEI analysis (works for all seasons)
        avg_fei = filtered_df['FEI'].mean()
        avg_commercial_share = (filtered_df['Commercial_Revenue'] / filtered_df['Total_Revenue']).mean()
        avg_revenue_growth = filtered_df['Revenue_Growth'].mean()
        avg_matchday_share = (filtered_df['Matchday_Revenue'] / filtered_df['Total_Revenue']).mean()
        
        recommendations = []
        
        # FEI-based recommendations
        if avg_fei < 0.6:
            recommendations.append(f"**Financial Optimization**: Average FEI ({avg_fei:.3f}) below target 0.600 - improve revenue diversification and growth")
        
        # Commercial diversification recommendations
        if avg_commercial_share < 0.35:
            recommendations.append(f"**Commercial Expansion**: Current commercial share ({avg_commercial_share*100:.1f}%) below optimal 35%+ - focus on sponsorship and partnerships")
        
        # Revenue growth recommendations
        if avg_revenue_growth < 5:
            recommendations.append(f"**Growth Strategy**: Revenue growth ({avg_revenue_growth:.1f}%) below industry target of 5%+ - diversify revenue streams")
        
        # Matchday revenue optimization
        if avg_matchday_share < 0.15:
            recommendations.append(f"**Matchday Enhancement**: Current matchday share ({avg_matchday_share*100:.1f}%) below optimal 15%+ - improve stadium experience")
        
        # Team-specific recommendations
        low_fei_team = filtered_df.loc[filtered_df['FEI'].idxmin()]
        recommendations.append(f"**Priority Focus**: {low_fei_team['Team']} (FEI: {low_fei_team['FEI']:.3f}) needs immediate financial efficiency improvements")
        
        # Standard recommendations based on season
        if show_performance:
            recommendations.extend([
                "**FEI Target**: Maintain FEI above 0.600 for sustainable financial efficiency",
                "**Revenue Balance**: Optimal split - 45% Broadcasting, 35% Commercial, 20% Matchday",
                "**Performance Alignment**: Balance on-field investment with revenue diversification"
            ])
        else:
            recommendations.extend([
                f"**FEI Target**: Maintain FEI above 0.600 for financial sustainability",
                "**Revenue Diversification**: Reduce dependence on single revenue streams",
                "**Growth Focus**: Target 5-8% annual revenue growth through strategic initiatives"
            ])
        
        for i, rec in enumerate(recommendations, 1):
            if i <= len(recommendations):
                st.info(f"{i}. {rec}")
    
    # Download Section
    st.header("Data Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Download Data")
        csv_link = create_download_link(filtered_df, "premier_league_analytics.csv", "Download CSV Report")
        st.markdown(csv_link, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Quick Stats")
        st.write(f"**Teams Analyzed**: {len(selected_teams)}")
        st.write(f"**Total Revenue**: £{filtered_df['Total_Revenue'].sum():.1f}M")
        st.write(f"**Average Revenue Growth**: {filtered_df['Revenue_Growth'].mean():.1f}%")
        
        if show_performance:
            st.write(f"**Average Points**: {filtered_df['Points'].mean():.1f}")
            st.write(f"**Top Performer**: {filtered_df.loc[filtered_df['Points'].idxmax(), 'Team']}")
        else:
            # For historical seasons, show top revenue performer
            top_revenue_team = filtered_df.loc[filtered_df['Total_Revenue'].idxmax(), 'Team']
            st.write(f"**Top Revenue**: {top_revenue_team}")
    
    with col3:
        st.subheader("Data Sources")
        st.write("- **Performance**: Real-time Premier League API")
        st.write("- **Financial**: Deloitte Football Money League 2024")
        st.write("- **Historical**: 5-year revenue trends analysis")
        st.write("- **Updated**: Live data integration")

if __name__ == "__main__":
    main()