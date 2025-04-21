import pandas as pd

df = pd.read_csv("classified_by_sector.csv")

df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
df.rename(columns={'india/states': 'state'}, inplace=True)

df['nic_name'] = df['nic_name'].astype(str).str.lower().str.strip()

def classify_sector(nic_text):
    if any(keyword in nic_text for keyword in [
        'agriculture', 'farming', 'crop', 'poultry', 'growing',
        'planting', 'harvesting', 'cultivation', 'vegetables', 'rice',
        'cereals', 'animal', 'propagation', 'raising', 'livestock', 'buffalo', 'cattle', 'sheep', 'goats', 'swine', 'pigs']):
        return 'Agriculture'
    elif any(keyword in nic_text for keyword in ['manufacture', 'factory', 'production']):
        return 'Manufacturing'
    elif any(keyword in nic_text for keyword in ['retail', 'shop', 'store', 'sale']):
        return 'Retail'
    elif any(keyword in nic_text for keyword in ['construction', 'building']):
        return 'Construction'
    elif any(keyword in nic_text for keyword in ['software', 'it', 'computer', 'data']):
        return 'IT / Services'
    elif any(keyword in nic_text for keyword in ['education', 'school', 'college', 'teaching']):
        return 'Education'
    elif any(keyword in nic_text for keyword in ['transport', 'logistics', 'delivery']):
        return 'Transport & Logistics'
    elif any(keyword in nic_text for keyword in ['health', 'hospital', 'clinic', 'medical']):
        return 'Healthcare'
    else:
        return 'Other'

df['sector'] = df['nic_name'].apply(classify_sector)

print(df[['nic_name', 'sector']].head(20))

print("\nSector Distribution:")
print(df['sector'].value_counts())

df.to_csv(r"C:\Task\classified_by_sector.csv", index=False)
