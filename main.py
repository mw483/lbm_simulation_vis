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

for path in file_paths:
    df = pd.read_csv(path, skiprows=1, header=None)
    df.columns = columns
    step = path.split("prof")[1].split("_")[0]
    steps.append(step)
    

    for key in ["U", "V", "W", "UU", "VV", "WW"]:
        profiles[key].append(df[key])
        # print(f"Step {step} - {key} profile")
        # print(pd.DataFrame({'z': df['z'], key: df[key]}).head(10))  # Show first 10 rows
    profiles["z"].append(df["z"])

# Plot each variable separately across steps
for key in ["U", "V", "W"]:
    plt.figure(figsize=(6, 4))
    for i, step in enumerate(steps):
        plt.plot(profiles["z"][i], profiles[key][i], label=f"Step {step}")
    plt.xlabel("z (Height)")
    plt.ylabel(f"{key} (Velocity)")
    plt.title(f"z vs {key} Profile")
    plt.legend()
    plt.grid(True)
    ax = plt.gca()
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.3f'))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=10))  # More z-axis ticks
    ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))   # Fewer y-axis ticks
    plt.tight_layout()
    plt.show()
    # plt.savefig(os.path.join(output_dir, f"z_vs_{key}_profile.png"), dpi=300)
    # plt.close()

for key in ["UU", "VV", "WW"]:
    plt.figure(figsize=(6, 4))
    for i, step in enumerate(steps):
        plt.plot(profiles["z"][i], profiles[key][i], label=f"Step {step}")
    plt.xlabel("z (Height)")
    plt.ylabel(f"{key} (Velocity Variance)")
    plt.title(f"z vs {key} Profile")
    plt.legend()
    plt.grid(True)
    ax = plt.gca()
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.3f'))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=10))  # More z-axis ticks
    ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))   # Fewer y-axis ticks
    plt.tight_layout()
    plt.show()
    # plt.savefig(os.path.join(output_dir, f"{key}_profile_vs_z.png"), dpi=300)
    # plt.close()
