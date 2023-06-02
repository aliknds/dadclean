import tkinter as tk
from tkinter import filedialog 
import pandas as pd

# Function to clean the CSV file
def clean_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        # Read the first line of the file to determine the delimiter
        first_line = file.readline()
        # List of potential delimiters
        delimiters = [',', ';', '\t']

        # Iterate over the delimiters and check which one is present in the first line
        for delimiter in delimiters:
            if delimiter in first_line:
                # Read the CSV file using pandas with the identified delimiter
                df = pd.read_csv(file_path, skiprows=1, delimiter=delimiter, encoding='utf-8')
                # Exclude the summary rows at the bottom
                df = df.iloc[:-2]
                # Adjust column names and translate to English
                df = adjust_columns(df)
                # Drop rows with missing 'Огноо' (Date) value
                df = df.dropna(subset=['Огноо'])
                return df
    # If no delimiter is found, display an error message
    print("Error: Unable to determine the delimiter of the CSV file.")
    return None 

# Function to adjust column names and translate them to English
def adjust_columns(df):
    # Get the number of columns in the DataFrame
    num_columns = df.shape[1]
    expected_columns = ['Падаан', 'Огноо', 'Харилцагч', 'Бараа', 'Буцаалт', 'төлөх дүн', 'Төлсөн']
    translation_mapping = {
        'Падаан': 'Number',
        'Огноо': 'Date',
        'Харилцагч': 'Customer',
        'Бараа': 'Product',
        'Буцаалт': 'Return',
        'төлөх дүн': 'Payment',
        'Төлсөн': 'Paid'
    }

    # Check if the number of columns in the CSV file matches the expected number
    if num_columns != len(expected_columns):
        # Adjust the column names based on the expected number of columns
        if num_columns > len(expected_columns):
            # Truncate extra columns
            df = df.iloc[:, :len(expected_columns)]
            df.columns = expected_columns
        else:
            # Add missing columns with empty values
            for i in range(num_columns, len(expected_columns)):
                df.insert(i, expected_columns[i], '')
    
    # Translate column names to English
    df = df.rename(columns=translation_mapping)

    return df

# Function to handle file drop event 
def handle_drop(event):
    file_path = event.widget.selection_get()
    if file_path: 
        cleaned_df = clean_csv(file_path)
        if cleaned_df is not None:
            # Save the cleaned DataFrame
            save_file(cleaned_df)

# Select a file using file dialog 
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
    if file_path:
        cleaned_df = clean_csv(file_path)
        if cleaned_df is not None:
            # Save the cleaned DataFrame
            save_file(cleaned_df)

# Function to save the cleaned DataFrame to a CSV file
def save_file(dataframe):
    save_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV Files', '*.csv')])

    if save_path:
        dataframe.to_csv(save_path, index=False)
        print("File  saved successfully.")
        # Close the window after finishing the work
        window.destroy()

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

window.mainloop()