# Define grid dimensions
rows, cols = 80, 80

# Define block pattern parameters
block_sections = [
    (4, 11),   # First block section (rows 4-11)
    (20, 27),  # Second block section (rows 20-27)
    (36, 43),  # Third block section (rows 36-43)
    (52, 59),  # Fourth block section (rows 52-59)
    (68, 75)   # Fifth block section (rows 68-75)
]

# Create the grid content
grid = []
for i in range(rows):
    if any(start <= i <= end for start, end in block_sections):
        # Create a row with the correct block pattern
        row = []
        # Initial 20 zeros
        row.extend([0] * 20)
        # Add 4 blocks of eight 8s with proper spacing
        for block in range(4):
            # Add eight 8s
            row.extend([8] * 8)
            # Add spacing: 8 zeros after blocks 1-3, 4 zeros after last block
            if block < 3:
                row.extend([0] * 8)
            else:
                row.extend([0] * 4)
        grid.append(row)
    else:
        # Create a full row of zeros
        grid.append([0] * cols)

# Write directly to .dat file with proper formatting
filename = "c_shibuya_topo.dat"
with open(filename, 'w') as f:
    # Write header without any extra spaces
    f.write(f"{rows}\t{cols}\n")
    
    # Write grid content without leading spaces
    for i, row in enumerate(grid):
        # Use strip() to ensure no leading/trailing whitespace
        f.write("\t".join(map(str, row)).rstrip() + "\n")

print(f"File '{filename}' successfully created with {rows}x{cols} grid.")
print("Pattern details:")
print("- Block sections at rows: 4-11, 20-27, 36-43, 52-59, 68-75")
print("- Each block row: 20 zeros, then 4 blocks of eight 8s")
print("- Blocks separated by 8 zeros, with 4 zeros after last block")
print()
print("To copy to server, run in PowerShell:")
print(f'scp "{filename}" mikael@172.20.25.11:/data/mikael/LBM_particle_test/map/')