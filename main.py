import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

file_paths = [
    r"Simulation 20250619\Output\prof00060000_0000.csv",
    r"Simulation 20250619\Output\prof00120000_0000.csv",
    r"Simulation 20250619\Output\prof00180000_0000.csv",
]

columns = [
    "z", "RHO", "U", "V", "W", "UU", "VV", "WW", "UV", "UW", "VW",
    "UUU", "VVV", "WWW", "UUW", "VVW", "T", "TT", "UT", "VT", "WT", "TTT"
]

# Output directory relative to the script location
output_dir = os.path.join(os.path.dirname(__file__), "Fig_Prof_Sim20250619")
os.makedirs(output_dir, exist_ok=True)

# Initialize dictionaries to store profiles
profiles = {"U": [], "V": [], "W": [], "UU": [], "VV": [], "WW": [], "z": []}
steps = []

# Debug: Check data loading
for path in file_paths:
    print(f"\nProcessing file: {path}")
    
    # Read CSV with proper handling - skip first row, use second row as headers
    try:
        df = pd.read_csv(path, skiprows=1, header=0)  # Skip first row, use second row as header
        
        # Convert columns to numeric, handling any string values
        numeric_columns = ["z", "U", "V", "W", "UU", "VV", "WW"]
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove any rows with NaN values (from conversion errors)
        df = df.dropna(subset=[col for col in numeric_columns if col in df.columns])
        # Debug: Print basic info about the dataframe (after conversion)
        print(f"DataFrame shape after cleaning: {df.shape}")
        print(f"First few rows of z: {df['z'].head().values}")
        print(f"First few rows of U: {df['U'].head().values}")
        print(f"U range: {df['U'].min():.3f} to {df['U'].max():.3f}")
        print(f"z range: {df['z'].min():.3f} to {df['z'].max():.3f}")
        
        # Check for any NaN or infinite values
        print(f"NaN values in U: {df['U'].isna().sum()}")
        print(f"Infinite values in U: {df['U'].isin([float('inf'), float('-inf')]).sum()}")
        
    except Exception as e:
        print(f"Error reading {path}: {e}")
        continue
    
    step = path.split("prof")[1].split("_")[0]
    steps.append(step)
    
    # Store the data
    for key in ["U", "V", "W", "UU", "VV", "WW"]:
        profiles[key].append(df[key])
    profiles["z"].append(df["z"])

# Plot each velocity component separately
for key in ["U", "V", "W"]:
    plt.figure(figsize=(8, 6))
    
    for i, step in enumerate(steps):
        z_data = profiles["z"][i]
        vel_data = profiles[key][i]
        
        # Debug: Print data ranges for this step
        print(f"\nStep {step}, Variable {key}:")
        print(f"  z range: {z_data.min():.3f} to {z_data.max():.3f}")
        print(f"  {key} range: {vel_data.min():.3f} to {vel_data.max():.3f}")
        
        # Plot with height on x-axis and velocity on y-axis
        plt.plot(z_data, vel_data, label=f"Step {step}", marker='o', markersize=3, linewidth=1.5)
    
    plt.xlabel("Height z")
    plt.ylabel(f"{key} Velocity Component")
    plt.title(f"Height vs {key} Velocity Profile")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Format axes
    ax = plt.gca()
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.3f'))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=10))
    ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=8))
    
    # Ensure proper axis limits
    ax.set_xlim(left=0)  # Start z from 0 if appropriate
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"height_vs_{key}_velocity.png"), dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

# Plot turbulent kinetic energy components
for key in ["UU", "VV", "WW"]:
    plt.figure(figsize=(8, 6))
    
    for i, step in enumerate(steps):
        z_data = profiles["z"][i]
        tke_data = profiles[key][i]
        
        # Debug: Print data ranges for this step
        print(f"\nStep {step}, Variable {key}:")
        print(f"  z range: {z_data.min():.3f} to {z_data.max():.3f}")
        print(f"  {key} range: {tke_data.min():.6f} to {tke_data.max():.6f}")
        
        # Plot with height on x-axis and TKE on y-axis
        plt.plot(z_data, tke_data, label=f"Step {step}", marker='s', markersize=3, linewidth=1.5)
    
    plt.xlabel("Height z")
    plt.ylabel(f"{key} Turbulent Kinetic Energy")
    plt.title(f"Height vs {key} TKE Profile")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Format axes
    ax = plt.gca()
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=10))
    ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=8))
    
    # Ensure proper axis limits
    ax.set_xlim(left=0)  # Start z from 0 if appropriate
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"height_vs_{key}_TKE.png"), dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

# Additional debugging: Create a summary plot showing all velocity components for one time step
if len(steps) > 0:
    plt.figure(figsize=(10, 6))
    step_idx = 0  # Use first time step
    z_data = profiles["z"][step_idx]
    
    for key in ["U", "V", "W"]:
        vel_data = profiles[key][step_idx]
        plt.plot(z_data, vel_data, label=f"{key} velocity", marker='o', markersize=4, linewidth=2)
    
    plt.xlabel("Height z")
    plt.ylabel("Velocity Components")
    plt.title(f"All Velocity Components vs Height (Step {steps[step_idx]})")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    ax = plt.gca()
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.3f'))
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"all_velocity_components_step_{steps[step_idx]}.png"), dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()