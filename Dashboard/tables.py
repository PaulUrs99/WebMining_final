#create a csv file with the column header 'user_key', 'user_name', 'steam_id', 'epic_id' in the directory C:\Users\paulu\OneDrive\Dokumente\GitHub\WebMining\Datenbank
import csv
import os

# Define the file path
file_path = r'C:\Users\paulu\OneDrive\Dokumente\GitHub\WebMining\Datenbank\USER.csv'

# Define the column headers
headers = ['user_id', 'user_name','steam_id', 'epic_id']

# Create the directory if it doesn't exist
os.makedirs(os.path.dirname(file_path), exist_ok=True)

# Write the headers to the CSV file
with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

print(f"CSV file created at {file_path} with headers {headers}")