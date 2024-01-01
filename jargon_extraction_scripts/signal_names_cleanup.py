'''
I made an SQL query to grab all the signal names from the forum
based on having text inbetween underscores, with 7 characters being the
longest string between underscores. This way PPDCIN_G3H, PP3V42_G3H, etc
all get through.

The problem is that it also grabs garbage from URLs since URLs
also have stuff with underscores in them! I found a regular expression
pattern that I think will get the signals without the junk, but I can't
be sure. This program will compare the CSVs made by each, and tell
me what the differences are in output, so that I can see if my new
mysql query is getting rid of valid signal names along with URL junk or
not.

EDIT - THE RESULT OF THIS IS THAT THERE'S STILL URL JUNK. THIS IS NOT
SOMETHING I SHOULD BE DOING IN MYSQL, NEED MORE ADVANCED STRING HANDLING 
OF PYTHON TO DO THIS PROPERLY!
'''

import pandas as pd

def compare_csv(file1, file2, output_file):
    try:
        # Reading the CSV files
        df1 = pd.read_csv(file1, header=None).iloc[:, 0].apply(lambda x: x.strip() if isinstance(x, str) else x)
        df2 = pd.read_csv(file2, header=None).iloc[:, 0].apply(lambda x: x.strip() if isinstance(x, str) else x)

        # Finding differences
        unique_in_file1 = pd.Series(list(set(df1) - set(df2)))
        unique_in_file2 = pd.Series(list(set(df2) - set(df1)))

        # Combine the unique entries into one DataFrame
        differences = pd.concat([unique_in_file1, unique_in_file2], axis=1)
        differences.columns = ['Unique_in_' + file1, 'Unique_in_' + file2]

        # Save to CSV
        differences.to_csv(output_file, index=False)
        print(f"Differences saved to {output_file}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except pd.errors.EmptyDataError:
        print("Error: One of the CSV files is empty.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Get file names and output file name from user input
fileone = input("Enter the name of the first CSV file: ")
filetwo = input("Enter the name of the second CSV file: ")
output_file = input("Enter the name of the output CSV file: ")

compare_csv(fileone, filetwo, output_file)
