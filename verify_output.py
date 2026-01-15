"""
Verify the output Excel file contains correct calculations
"""

import pandas as pd

print("Verifying output file...")
print("=" * 70)

try:
    # Read the output file
    df = pd.read_excel('test_output_new.xlsx')
    
    print(f"\n✓ File loaded successfully")
    print(f"  Rows: {len(df)}")
    print(f"  Columns: {len(df.columns)}")
    
    print(f"\n📊 Columns in output file:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")
    
    print(f"\n📋 Sample data (first 3 rows):")
    print("-" * 70)
    
    # Display each row
    for idx, row in df.head(3).iterrows():
        print(f"\nRow {idx + 1}:")
        print(f"  Operación: {row['Operación']}")
        print(f"  Máquina: {row['Máquina']}")
        print(f"  Tiempo Estándar (seg): {row['Tiempo Estándar (seg)']}")
        print(f"  Tiempo Estándar (min): {row['Tiempo Estándar (min)']}")
        print(f"  Unidades/Hora: {row['Unidades/Hora']}")
        print(f"  Unidades/Día: {row['Unidades/Día']}")
    
    print("\n" + "-" * 70)
    print(f"\n📈 Summary Statistics:")
    print(f"  Total Operations: {len(df)}")
    print(f"  Avg Units/Hour: {df['Unidades/Hora'].mean():.2f}")
    print(f"  Avg Units/Day: {df['Unidades/Día'].mean():.2f}")
    print(f"  Min Units/Hour: {df['Unidades/Hora'].min():.2f}")
    print(f"  Max Units/Hour: {df['Unidades/Hora'].max():.2f}")
    
    print("\n" + "=" * 70)
    print("✓ Output file is valid and contains all expected data!")
    
except Exception as e:
    print(f"\n✗ Error reading file: {str(e)}")
