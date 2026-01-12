import csv
from collections import defaultdict

# Analyze BoaviztAPI.csv
print("=" * 60)
print("FICHIER: EfficiencyAnalysis - BoaviztAPI.csv")
print("=" * 60)

used_cols = ['name', 'manufacturer', 'tdp', 'cores', 'frequency', 'total_die_size']
null_counts = defaultdict(int)
total_rows = 0
rows_with_nulls = 0

with open('data/terminals/EfficiencyAnalysis - BoaviztAPI.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    
    for row in reader:
        total_rows += 1
        has_null = False
        
        for col in used_cols:
            if not row.get(col) or row.get(col).strip() == '':
                null_counts[col] += 1
                has_null = True
        
        if has_null:
            rows_with_nulls += 1

print(f"\nTotal rows: {total_rows}")
print(f"\nNull values in USED columns:")
for col in used_cols:
    percentage = (null_counts[col] / total_rows * 100) if total_rows > 0 else 0
    print(f"  {col:20} : {null_counts[col]:5} nulls ({percentage:5.1f}%)")

print(f"\nRows with ANY null in used columns: {rows_with_nulls} ({rows_with_nulls/total_rows*100:.1f}%)")
print(f"Clean rows (no nulls): {total_rows - rows_with_nulls} ({(total_rows-rows_with_nulls)/total_rows*100:.1f}%)")

# Analyze The CHIP Dataset
print("\n" + "=" * 60)
print("FICHIER: EfficiencyAnalysis - The CHIP Dataset.csv")
print("=" * 60)

used_cols2 = ['Product', 'Type', 'Release Date', 'TDP (W)', 'Vendor']
null_counts2 = defaultdict(int)
total_rows2 = 0
rows_with_nulls2 = 0

with open('data/terminals/EfficiencyAnalysis - The CHIP Dataset.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        total_rows2 += 1
        has_null = False
        
        for col in used_cols2:
            if not row.get(col) or row.get(col).strip() == '':
                null_counts2[col] += 1
                has_null = True
        
        if has_null:
            rows_with_nulls2 += 1

print(f"\nTotal rows: {total_rows2}")
print(f"\nNull values in USED columns:")
for col in used_cols2:
    percentage = (null_counts2[col] / total_rows2 * 100) if total_rows2 > 0 else 0
    print(f"  {col:20} : {null_counts2[col]:5} nulls ({percentage:5.1f}%)")

print(f"\nRows with ANY null in used columns: {rows_with_nulls2} ({rows_with_nulls2/total_rows2*100:.1f}%)")
print(f"Clean rows (no nulls): {total_rows2 - rows_with_nulls2} ({(total_rows2-rows_with_nulls2)/total_rows2*100:.1f}%)")
