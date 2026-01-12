import requests
import json
import csv

# Load a sample CPU from our data
print("=" * 70)
print("BOAVIZTA API TEST - CPU Environmental Impact")
print("=" * 70)

# Read one CPU from our CSV
with open('data/terminals/EfficiencyAnalysis - BoaviztAPI.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    # Find first CPU with complete data (tdp and cores)
    cpu = None
    for row in reader:
        if row['tdp'] and row['cores'] and row['tdp'].strip() and row['cores'].strip():
            cpu = row
            break

if not cpu:
    print("❌ No CPU found with complete data!")
    exit(1)

print(f"\n📊 Selected CPU:")
print(f"   Name: {cpu['name']}")
print(f"   Manufacturer: {cpu['manufacturer']}")
print(f"   TDP: {cpu['tdp']} W")
print(f"   Cores: {cpu['cores']}")
print(f"   Frequency: {cpu['frequency']}")

# Prepare API request
api_url = "https://api.boavizta.org/v1/component/cpu"

payload = {
    "core_units": int(cpu['cores']),
    "tdp": int(float(cpu['tdp'])),
    "usage": {
        "hours_life_time": 35040,  # 4 years × 365 days × 24h
        "time_workload": 50        # 50% active usage
    }
}

print(f"\n🔌 API Request:")
print(f"   URL: {api_url}")
print(f"   Payload:")
print(json.dumps(payload, indent=6))

# Make API call
print(f"\n⏳ Calling Boavizta API...")

try:
    response = requests.post(api_url, json=payload, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"\n✅ API Response (Status: {response.status_code})")
        print("=" * 70)
        
        # Pretty print the full response
        print("\n📄 FULL JSON RESPONSE:")
        print(json.dumps(data, indent=2))
        
        # Extract key metrics
        print("\n" + "=" * 70)
        print("🌍 KEY ENVIRONMENTAL IMPACTS")
        print("=" * 70)
        
        if 'impacts' in data:
            impacts = data['impacts']
            
            # Global Warming Potential (GWP) - CO2 equivalent
            if 'gwp' in impacts:
                gwp = impacts['gwp']
                unit = gwp.get('unit', 'kgCO2eq')
                print(f"\n🔥 Global Warming Potential (GWP) - CO2 Emissions:")
                if 'embedded' in gwp:
                    print(f"   Manufacturing: {gwp['embedded']['value']:.2f} {unit}")
                if 'use' in gwp:
                    print(f"   Usage (4 years): {gwp['use']['value']:.2f} {unit}")
                
                total_gwp = gwp['embedded']['value'] + gwp['use']['value']
                print(f"   TOTAL: {total_gwp:.2f} {unit}")
            
            # Primary Energy (PE)
            if 'pe' in impacts:
                pe = impacts['pe']
                unit = pe.get('unit', 'MJ')
                print(f"\n⚡ Primary Energy (PE):")
                if 'embedded' in pe:
                    print(f"   Manufacturing: {pe['embedded']['value']:.2f} {unit}")
                if 'use' in pe:
                    print(f"   Usage (4 years): {pe['use']['value']:.2f} {unit}")
                
                total_pe = pe['embedded']['value'] + pe['use']['value']
                print(f"   TOTAL: {total_pe:.2f} {unit}")
            
            # Abiotic Depletion Potential (ADP)
            if 'adp' in impacts:
                adp = impacts['adp']
                unit = adp.get('unit', 'kgSbeq')
                print(f"\n🪨 Abiotic Depletion Potential (ADP) - Minerals:")
                if 'embedded' in adp:
                    print(f"   Manufacturing: {adp['embedded']['value']:.2e} {unit}")
                if 'use' in adp:
                    print(f"   Usage (4 years): {adp['use']['value']:.2e} {unit}")
                
                total_adp = adp['embedded']['value'] + adp['use']['value']
                print(f"   TOTAL: {total_adp:.2e} {unit}")
        
        # Visual summary
        print("\n" + "=" * 70)
        print("📊 VISUAL SUMMARY")
        print("=" * 70)
        
        if 'impacts' in data and 'gwp' in data['impacts']:
            gwp = data['impacts']['gwp']
            total_co2 = gwp['embedded']['value'] + gwp['use']['value']
            manufacturing_co2 = gwp['embedded']['value']
            usage_co2 = gwp['use']['value']
            
            manufacturing_pct = (manufacturing_co2 / total_co2 * 100) if total_co2 > 0 else 0
            usage_pct = (usage_co2 / total_co2 * 100) if total_co2 > 0 else 0
            
            print(f"\n🌳 Total CO2 Emissions: {total_co2:.1f} kgCO2eq")
            print(f"\n   Manufacturing: {'█' * int(manufacturing_pct/2)} {manufacturing_pct:.1f}%")
            print(f"   Usage:         {'█' * int(usage_pct/2)} {usage_pct:.1f}%")
            
            # Equivalences
            trees_needed = total_co2 / 20  # 1 tree absorbs ~20kg CO2/year
            km_driven = total_co2 / 0.12   # avg car emits ~120g CO2/km
            
            print(f"\n🌍 Equivalents:")
            print(f"   • {trees_needed:.1f} trees needed to absorb this CO2 (1 year)")
            print(f"   • {km_driven:.0f} km driven in average car")
            print(f"   • {total_co2/21.3:.1f}% of average person's annual CO2 budget")
        
    else:
        print(f"\n❌ API Error (Status: {response.status_code})")
        print(f"   Response: {response.text}")

except requests.exceptions.Timeout:
    print("\n❌ API call timed out. Please check your internet connection.")
except requests.exceptions.RequestException as e:
    print(f"\n❌ API call failed: {e}")
except Exception as e:
    print(f"\n❌ Unexpected error: {e}")

print("\n" + "=" * 70)
