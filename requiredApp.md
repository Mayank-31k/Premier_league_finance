Build a complete Streamlit application called premier_league_dashboard.py that serves as a Performance & Financial Analytics Dashboard for the top 6 Premier League teams. The app should be styled in a clean, business-consulting layout (Mastercard feel) and contain the following features:
Data
Use a sample static dataset (CSV or Python dict) with the following columns:
Team, Matches Played, Wins, Draws, Losses, Goals Scored, Goals Conceded, Points, Matchday Revenue (M$), Broadcasting Revenue (M$), Commercial Revenue (M$), Total Revenue (M$), Revenue Growth (%).
Include at least one season's data for the top 6 teams, and a second dataset with the last 5 seasons' total revenue per team for trend analysis.
UI Layout
Top section: App title, description, and a season/team filter sidebar.
Metrics section: Use st.metric() to show KPIs for performance (Points, Wins, Goal Difference) and finance (Total Revenue, Revenue Growth %).
Visualizations (use Plotly)
Bar chart comparing Points for top 6 teams.
Bar chart comparing Total Revenue for top 6 teams.
Pie chart of revenue breakdown (Matchday vs Broadcasting vs Commercial) for the selected team.
Line chart showing revenue growth over last 5 seasons.
Scatter plot showing correlation between Points and Total Revenue.
Risk & Insight Section
Highlight any teams with declining revenue despite high points.
Highlight any teams with strong revenue but poor on-field performance.
Generate 3–4 business-style recommendations as text output (e.g., strategies to boost sponsorship, improve performance efficiency).
Download Options
Allow CSV download of current filtered dataset.
Allow PDF export of the dashboard charts + insights.
Styling
Use Streamlit’s layout features and markdown for section dividers.
Use a professional theme with Mastercard-like black, white, and gold color palette.
Ensure charts are responsive and interactive.
Ensure the final code is complete, runnable with streamlit run premier_league_dashboard.py, includes sample datasets, and deployable on Streamlit Cloud without extra setup.