import pandas as pd
import plotly.express as px
from plotly.offline import plot as offline_plot

file_path = "xy_gs00060000_0000_withHeatmap.csv"
block_size = 240  # Number of data rows per block
header_gap = 1    # Header rows between blocks
block_names = ["XY_GS_2", "XY_GS_3", "XY_GS_4"]  # Your block names

# Calculate starting rows for each block
block_starts = [2 + i*(block_size + header_gap) for i in range(len(block_names))]

for start_row, name in zip(block_starts, block_names):
    # Read data block
    df = pd.read_csv(
        file_path,
        header=None,
        skiprows=start_row,
        nrows=block_size
    )
    
    # Create heatmap
    fig = px.imshow(
        df.values,
        color_continuous_scale='Viridis',
        labels=dict(x="Column Index", y="Row Index", color="Value"),
        title=f"Heatmap: {name}"
    )
    
    # Optimize layout
    fig.update_layout(
        xaxis_title="Columns (0-255)",
        yaxis_title="Data Rows",
        width=900,
        height=700
    )
    
    # Hide axis labels
    fig.update_xaxes(showticklabels=False, ticks="")
    fig.update_yaxes(showticklabels=False, ticks="")
    
    # Generate filename and save
    filename = f"heatmap_{name.lower()}.html"
    offline_plot(fig, filename=filename, auto_open=True)
    
    print(f"Generated heatmap for {name} starting at row {start_row}")