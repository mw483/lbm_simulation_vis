import pandas as pd
import plotly.express as px
import os
import numpy as np
from glob import glob

# Configuration for different plane types
PLANE_CONFIGS = {
    'xy': {
        'pattern': '**/xy_ins_u*.csv',
        'blocks': [
            {'name': "XY_ins_u_2", 'start_row': 2, 'nrows': 80, 'ncols': 96},
            {'name': "XY_ins_u_3", 'start_row': 83, 'nrows': 80, 'ncols': 96},  # 2 + 80 + 1
            {'name': "XY_ins_u_4", 'start_row': 164, 'nrows': 80, 'ncols': 96}  # 2 + 80 + 1 + 80 + 1
        ],
        'labels': dict(x="X", y="Y", color="U velocity"),
        'title_prefix': "XY Plane"
    },
    'xz': {
        'pattern': '**/xz_ins_u*.csv',
        'blocks': [
            {'name': "XZ_ins_u_2", 'start_row': 3, 'nrows': 19, 'ncols': 96}  # row 4 to 22 (0-indexed: 3 to 21)
        ],
        'labels': dict(x="X", y="Z", color="U velocity"),
        'title_prefix': "XZ Plane"
    },
    'yz': {
        'pattern': '**/yz_ins_u*.csv',
        'blocks': [
            {'name': "YZ_ins_u_2", 'start_row': 1, 'nrows': 19, 'ncols': 80}  # row 2 to 20 (0-indexed: 1 to 19)
        ],
        'labels': dict(x="Y", y="Z", color="U velocity"),
        'title_prefix': "YZ Plane"
    }
}

# Global settings
OUTPUT_BASE_DIR = "heatmaps"
OUTPUT_BASE_DIR = "heatmaps"

def find_files_by_pattern(base_directory, pattern):
    """Find all files matching the pattern in the base directory"""
    search_path = os.path.join(base_directory, pattern)
    files = glob(search_path, recursive=True)
    return sorted(files)  # Sort for consistent processing order

def process_file(file_path, plane_type, config):
    """Process a single file and generate all block heatmaps for a specific plane"""
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found")
        return
    
    # Extract timestep name from filename
    filename = os.path.basename(file_path)
    timestep_name = os.path.splitext(filename)[0]
    
    # Create output directory structure: heatmaps/plane_type/timestep/
    output_dir = os.path.join(OUTPUT_BASE_DIR, plane_type, timestep_name)
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each block defined in the configuration
    for block_config in config['blocks']:
        try:
            block_name = block_config['name']
            start_row = block_config['start_row']
            nrows = block_config['nrows']
            ncols = block_config['ncols']
            
            # Read data block with error handling
            df = pd.read_csv(
                file_path,
                header=None,
                skiprows=start_row,
                nrows=nrows,
                sep=',',
                engine='python',
                na_values=['', ' ', 'NaN', 'nan'],
                skipinitialspace=True
            )
            
            # Convert to numeric, replacing any remaining non-numeric values with NaN
            df = df.apply(pd.to_numeric, errors='coerce')
            
            # Validate data shape
            if df.shape[0] != nrows:
                print(f"Warning: Block {block_name} in {timestep_name} has {df.shape[0]} rows instead of {nrows}")
                continue
                
            if df.shape[1] != ncols:
                print(f"Warning: Block {block_name} in {timestep_name} has {df.shape[1]} columns instead of {ncols}")
                if df.shape[1] < ncols:
                    # Pad with NaN
                    for i in range(df.shape[1], ncols):
                        df[i] = np.nan
                else:
                    # Trim excess columns
                    df = df.iloc[:, :ncols]
            
            # Check for NaN values
            nan_count = df.isna().sum().sum()
            if nan_count > 0:
                print(f"Warning: Block {block_name} in {timestep_name} has {nan_count} NaN values")
            
            # Create heatmap with appropriate aspect ratio
            # For rectangular data, don't force square aspect
            aspect_ratio = 'auto' if nrows != ncols else 'equal'
            
            fig = px.imshow(
                df.values,
                color_continuous_scale='Viridis',
                labels=config['labels'],
                title=f"{config['title_prefix']} - {timestep_name} - {block_name}",
                aspect=aspect_ratio,
                origin='lower'
            )
            
            # Adjust layout based on data dimensions
            # For rectangular data, adjust width/height ratio
            if nrows != ncols:
                width = max(600, min(1200, ncols * 8))  # Scale width with columns
                height = max(400, min(800, nrows * 20))  # Scale height with rows
            else:
                width = height = 800
            
            # Optimize layout
            fig.update_layout(
                width=width,
                height=height,
                margin=dict(l=20, r=20, t=60, b=20),
                title_x=0.5,
                title_font_size=14
            )
            
            # Update axes
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
            
            # Generate filename and save as PNG
            filename = os.path.join(output_dir, f"heatmap_{block_name}.png")
            fig.write_image(filename, width=width, height=height, scale=2)
            
            print(f"Generated {filename} (shape: {nrows}x{ncols})")
            
        except Exception as e:
            print(f"Error processing {block_name} in {timestep_name} ({plane_type}): {str(e)}")
            import traceback
            print(f"Detailed error: {traceback.format_exc()}")

def process_plane_type(base_directory, plane_type):
    """Process all files for a specific plane type"""
    
    if plane_type not in PLANE_CONFIGS:
        print(f"Error: Unknown plane type '{plane_type}'. Available types: {list(PLANE_CONFIGS.keys())}")
        return
    
    config = PLANE_CONFIGS[plane_type]
    
    # Find all files matching the pattern
    files = find_files_by_pattern(base_directory, config['pattern'])
    
    if not files:
        print(f"No files found for plane type '{plane_type}' with pattern '{config['pattern']}'")
        return
    
    print(f"\nProcessing {len(files)} files for {plane_type.upper()} plane:")
    for file_path in files:
        print(f"  Processing: {os.path.basename(file_path)}")
        process_file(file_path, plane_type, config)

def process_all_planes(base_directory):
    """Process all plane types found in the base directory"""
    
    print("=== Multi-Plane Heatmap Generator ===")
    print(f"Base directory: {base_directory}")
    
    for plane_type in PLANE_CONFIGS.keys():
        print(f"\n{'='*50}")
        print(f"Processing {plane_type.upper()} plane files...")
        print(f"{'='*50}")
        
        process_plane_type(base_directory, plane_type)

def process_specific_files(file_list, plane_type):
    """Process a specific list of files for a given plane type"""
    
    if plane_type not in PLANE_CONFIGS:
        print(f"Error: Unknown plane type '{plane_type}'. Available types: {list(PLANE_CONFIGS.keys())}")
        return
    
    config = PLANE_CONFIGS[plane_type]
    
    print(f"\nProcessing {len(file_list)} specific files for {plane_type.upper()} plane:")
    for file_path in file_list:
        print(f"  Processing: {os.path.basename(file_path)}")
        process_file(file_path, plane_type, config)

def main():
    """Main function with different usage modes"""
    
    # Mode 1: Process all planes automatically from a base directory
    # Uncomment and modify the path below to use this mode
    # process_all_planes("20250623_1900_Output")
    
    # Mode 2: Process specific files (original approach)
    # Example for XY plane
    xy_files = [
        "20250623_1900_Output/xy_ins_u00000000_0000.csv",
        "20250623_1900_Output/xy_ins_u00060000_0000.csv",
        "20250623_1900_Output/xy_ins_u00120000_0000.csv",
        "20250623_1900_Output/xy_ins_u00180000_0000.csv",
        "20250623_1900_Output/xy_ins_u00240000_0000.csv"
    ]
    process_specific_files(xy_files, 'xy')

    # Add XZ and YZ files as needed
    # xz_files = ["path/to/xz_file1.csv", "path/to/xz_file2.csv", ...]
    # process_specific_files(xz_files, 'xz')
    
    xz_files = [
        "20250623_1900_Output/xz_ins_u00000000_0000_00002.csv",
        "20250623_1900_Output/xz_ins_u00060000_0000_00002.csv",
        "20250623_1900_Output/xz_ins_u00120000_0000_00002.csv",
        "20250623_1900_Output/xz_ins_u00180000_0000_00002.csv",
        "20250623_1900_Output/xz_ins_u00240000_0000_00002.csv"
    ]
    process_specific_files(xz_files, 'xz')

    # yz_files = ["path/to/yz_file1.csv", "path/to/yz_file2.csv", ...]
    # process_specific_files(yz_files, 'yz')

    yz_files = [
        "20250623_1900_Output/yz_ins_u00000000_0000_00002.csv",
        "20250623_1900_Output/yz_ins_u00060000_0000_00002.csv",
        "20250623_1900_Output/yz_ins_u00120000_0000_00002.csv",
        "20250623_1900_Output/yz_ins_u00180000_0000_00002.csv",
        "20250623_1900_Output/yz_ins_u00240000_0000_00002.csv"
    ]
    process_specific_files(yz_files, 'yz')
    
    print("\nHeatmap generation completed!")

if __name__ == "__main__":
    main()