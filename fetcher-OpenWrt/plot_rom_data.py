import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_rom_data():
    # List all files in the current directory starting with "ROM_" and ending with ".txt"
    files = [f for f in os.listdir() if f.startswith("ROM_") and f.endswith(".txt")]

    if not files:
        print("No ROM_*.txt files found in the current directory.")
        return

    for file in files:
        try:
            # Read the file into a DataFrame (tab-delimited)
            data = pd.read_csv(file, sep="\t", names=["DAT", "SAMPLE", "RAW"], header=None)
            
            # Parse the DAT column into datetime objects
            data['DAT'] = pd.to_datetime(data['DAT'], format="%Y-%m-%d %H:%M:%S")
            
            # Convert RAW to float
            data['RAW'] = data['RAW'].astype(float)
            
            # Extract ROM ID from the filename
            rom_id = file.split("_")[1].split(".")[0]
            
            # Plot the data
            plt.figure(figsize=(10, 6))
            plt.plot(data['DAT'], data['RAW'], label=f"ROM {rom_id}")
            plt.title(f"Temperature Readings for ROM {rom_id}")
            plt.xlabel("Time")
            plt.ylabel("Temperature (RAW)")
            plt.grid(True)
            plt.legend()
            
            # Save the plot as a PNG file
            output_file = f"ROM_{rom_id}.png"
            plt.savefig(output_file)
            plt.close()
            
            print(f"Plot saved: {output_file}")
        except Exception as e:
            print(f"Error processing {file}: {e}")

if __name__ == "__main__":
    plot_rom_data()
