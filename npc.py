import requests
import plotly.graph_objs as go
from datetime import datetime
import pytz

# Function to get historical prices for a specific date range
def get_historical_prices(coin_id, start_date):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/range"
    end_date = datetime.now(pytz.timezone('Europe/Budapest')).timestamp()  # Current timestamp
    start_date_timestamp = start_date.timestamp()
    
    response = requests.get(url, params={"vs_currency": "usd", "from": start_date_timestamp, "to": end_date})
    
    if response.status_code == 200:
        return response.json()['prices']
    else:
        print(f"Failed to fetch data for {coin_id}: {response.status_code} {response.text}")
        return []

# Define liquidity post dates and hardcoded prices for each coin
liquidity_dates = {
    'simon-s-cat': (datetime(2024, 9, 11, 12, 26, tzinfo=pytz.timezone('Europe/Budapest')), 900000, "427K Views", 0.00002483),
    'why': (datetime(2024, 7, 16, 13, 0, tzinfo=pytz.timezone('Europe/Budapest')), 200000, "300.5K Views", 0.0000001724),
    'coco-coin': (datetime(2024, 10, 8, 14, 1, tzinfo=pytz.timezone('Europe/Budapest')), 50000, "136.5K Views", 0.001141),
}

# Define start dates for the price chart
start_dates = {
    'simon-s-cat': datetime(2024, 9, 7, tzinfo=pytz.timezone('Europe/Budapest')),
    'why': datetime(2024, 7, 12, tzinfo=pytz.timezone('Europe/Budapest')),
    'coco-coin': datetime(2024, 10, 8, tzinfo=pytz.timezone('Europe/Budapest')),
}

# Fetch and plot prices for each coin in separate charts
def plot_prices():
    for coin_id, (liquidity_date, liquidity, views, hardcoded_price) in liquidity_dates.items():
        # Fetch historical prices
        start_date = start_dates[coin_id]
        prices = get_historical_prices(coin_id, start_date)
        
        if not prices:
            continue
        
        # Extract timestamps and prices
        timestamps = [datetime.fromtimestamp(price[0] / 1000, tz=pytz.timezone('Europe/Budapest')) for price in prices]
        price_values = [price[1] for price in prices]

        # Plotly graph setup
        fig = go.Figure()

        # Add price line
        fig.add_trace(go.Scatter(
            x=timestamps, 
            y=price_values, 
            mode='lines', 
            name=coin_id.replace('-', ' ').title(),
            line=dict(color='blue')
        ))

        # Add liquidity line
        fig.add_vline(x=liquidity_date, line_dash="dash", line_color="grey")
        liquidity_price = hardcoded_price if hardcoded_price else price_values[-1]
        
        # Add liquidity price text
        fig.add_annotation(
            x=liquidity_date,
            y=max(price_values) * 0.9,
            text=f'Liquidity: ${liquidity:,}<br>Price: ${liquidity_price:.9f}',
            showarrow=False,
            xanchor='right',
            bgcolor='yellow',
            font=dict(color='black', size=10)
        )

        # Add current price
        current_price = price_values[-1]
        current_date = timestamps[-1]
        
        fig.add_annotation(
            x=current_date,
            y=max(price_values) * 0.95,
            text=f'Current Price: ${current_price:.9f}',
            showarrow=False,
            xanchor='left',
            bgcolor='black',
            font=dict(color='white', size=10)
        )

        # Calculate and display PnL in %
        pnl_percent = ((current_price - liquidity_price) / liquidity_price) * 100
        pnl_color = 'green' if pnl_percent >= 0 else 'red'

        fig.add_annotation(
            x=current_date,
            y=max(price_values) * 0.85,
            text=f'PnL: {pnl_percent:.2f}%',
            showarrow=False,
            xanchor='left',
            bgcolor='white',
            font=dict(color=pnl_color, size=10)
        )

        # Calculate and display Max PnL in %
        max_price = max(price_values)
        max_pnl_percent = ((max_price - liquidity_price) / liquidity_price) * 100
        max_pnl_color = 'green' if max_pnl_percent >= 0 else 'red'

        fig.add_annotation(
            x=current_date,
            y=max(price_values) * 0.75,
            text=f'Max PnL: {max_pnl_percent:.2f}%',
            showarrow=False,
            xanchor='left',
            bgcolor='white',
            font=dict(color=max_pnl_color, size=10)
        )

        # Insert max price annotation
        max_price_timestamp = timestamps[price_values.index(max_price)]  # Find the timestamp of max price
        fig.add_annotation(
            x=max_price_timestamp,
            y=max_price * 1.05,  # Position above the max price
            text=f'Max Price: ${max_price:.9f}',
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-40,
            bgcolor='green',
            font=dict(color='white', size=10)
        )

        # Set title and labels
        fig.update_layout(
            title=f'Historical Prices of {coin_id.replace("-", " ").title()}',
            xaxis_title='Date',
            yaxis_title='Price (USD)',
            legend_title='Coins',
            plot_bgcolor='white',
            font=dict(family='Arial', size=12, color='black'),
            xaxis=dict(
                tickformat='%Y-%m-%d',
                showgrid=True,
                gridcolor='lightgrey'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='lightgrey'
            )
        )
        
        # Show the plot for each coin
        fig.show()

# Main execution
plot_prices()
