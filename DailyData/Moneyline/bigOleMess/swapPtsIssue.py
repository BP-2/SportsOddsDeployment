import csv

input_file = 'allPtsIncorrect.csv'
output_file = 'allPtsCorrected.csv'

with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
     open(output_file, mode='w', newline='', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames  
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    writer.writeheader()

    for row in reader:
        row['PTS'], row['PTS2'] = row['PTS2'], row['PTS']
        row['AwayOdds'], row['HomeOdds'] =  row['HomeOdds'], row['AwayOdds']
        writer.writerow(row)

print(f"Swapped PTS and PTS2 successfully. Output saved to {output_file}.")
