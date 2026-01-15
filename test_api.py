"""
Test script to verify the API works correctly
"""

import requests
import os

# Check if sample file exists
if not os.path.exists('sample_time_study.xlsx'):
    print("Error: sample_time_study.xlsx not found")
    print("Run: python generate_sample.py first")
    exit(1)

print("Testing API endpoint...")
print("-" * 50)

url = 'http://127.0.0.1:8000/api/process-time-study/'

try:
    with open('sample_time_study.xlsx', 'rb') as f:
        files = {'file': ('sample_time_study.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
        
        print(f"Sending POST request to {url}")
        response = requests.post(url, files=files, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        
        if response.status_code == 200:
            # Save the output file
            output_file = 'test_output_new.xlsx'
            with open(output_file, 'wb') as output:
                output.write(response.content)
            
            print(f"\n✓ SUCCESS!")
            print(f"Output file saved as: {output_file}")
            print(f"File size: {len(response.content)} bytes")
            
            if 'X-Summary' in response.headers:
                print(f"Summary: {response.headers['X-Summary']}")
        else:
            print(f"\n✗ ERROR!")
            try:
                error_data = response.json()
                print(f"Error: {error_data}")
            except:
                print(f"Response: {response.text[:500]}")
                
except requests.exceptions.ConnectionError:
    print("✗ Connection Error: Make sure the Django server is running")
    print("Run: python manage.py runserver")
except Exception as e:
    print(f"✗ Unexpected error: {str(e)}")

print("-" * 50)
