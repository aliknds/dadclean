import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES

# Function to clean the CSV file
def clean_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        # Use csv.Sniffer to automatically detect the delimiter
        sniffer = csv.Sniffer()
        sample_data = file.read(1024)  # Read a sample of the file
        delimiter = sniffer.sniff(sample_data).delimiter

        # Read the CSV file using pandas with the identified delimiter and proper encoding
        df = pd.read_csv(file_path, delimiter=delimiter, encoding='utf-8')

        # Exclude the summary rows at the bottom (assuming they have NaN values in 'Date' column)
        df = df.dropna(subset=['Date'])

        # Fill missing values in 'Date' column with the previous non-null value
        df['Date'] = df['Date'].fillna(method='ffill')

        # Adjust column names and translate them to English
        df = adjust_columns(df)

        return df

    # If no delimiter is found, display an error message
    print("Error: Unable to determine the delimiter of the CSV file.")
    return None

# Function to adjust column names and translate them to English
def adjust_columns(df):
    num_columns = df.shape[1]  # Get the number of columns in the DataFrame
    expected_columns = ['Number', 'Date', 'Customer', 'Product', 'Return', 'Payment', 'Paid']

    # Check if the number of columns matches the expected number
    if num_columns != len(expected_columns):
        # Adjust column names based on the number of columns
        if num_columns > len(expected_columns):
            df = df.iloc[:, :len(expected_columns)]  # Truncate extra columns
            df.columns = expected_columns
        else:
            # Add missing columns with empty values
            for i in range(num_columns, len(expected_columns)):
                df.insert(i, expected_columns[i], '')

    # Rename columns to English names
    df = df.rename(columns=dict(zip(df.columns, expected_columns)))

    return df

# Function to handle file drop event
def handle_drop(event):
    file_path = event.widget.tk.splitlist(event.widget.tk.call('::tk::DND::Drop', 'data'))[0]
    if file_path:
        cleaned_df = clean_csv(file_path)
        if cleaned_df is not None:
            save_file(cleaned_df)  # Save the cleaned DataFrame

# Function to select a file using file dialog
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
    if file_path:
        cleaned_df = clean_csv(file_path)
        if cleaned_df is not None:
            save_file(cleaned_df)  # Save the cleaned DataFrame

# Function to save the cleaned DataFrame to a CSV file
def save_file(dataframe):
    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[('CSV Files', '*.csv')])

    if save_path:
        dataframe.to_csv(save_path, index=False)
        print("File saved successfully.")
        window.destroy()  # Close the window after finishing the work

# Create the main window
window = tk.Tk()
window.title("CSV File Selection")
window.geometry("400x200")

# Create a label
label = tk.Label(window, text="Select a CSV file or drag and drop here:")
label.pack(pady=20)

# Create a button to browse and select a file
button = tk.Button(window, text="Browse", command=select_file)
button.pack(pady=10)

# Enable file drop on the window
window.bind("<B1-Motion>", handle_drop)

# Run the main event loop
window.mainloop()
