import pandas as pd
import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, 'safety-nonsafety/')

# NORMALIZATION
def normalize_label(label):
    label = label.lower()
    if any(word in label for word in ['pit', 'forklift', 'vehicle', 'speeding', 'proximity']):
        return 'Vehicle & PIT Operations'
    if any(word in label for word in ['ergonomic', 'overreach', 'bending', 'lifting', 'posture']):
        return 'Ergonomics & Manual Handling'
    if any(word in label for word in ['pedestrian', 'no-ped', 'prohibited zone', 'walkway']):
        return 'Pedestrian Safety & Area Control'
    if any(word in label for word in ['obstruction', 'blocked', 'egress', 'fire exit', 'hazard']):
        return 'Facility Hazards & Egress'
    if any(word in label for word in ['reporting', 'dashboard', 'api', 'action', 'workflow', 'assign']):
        return 'Platform & Admin Features'
    return 'Other / Specialized'

# DATA LOADING
def load_all_data(directory):
    all_records = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as f:
                data = json.load(f)
                meeting = data.get('meeting_title')
                for cat in ['safety_use_cases', 'nonsafety_use_cases']:
                    cases = data.get('extraction', {}).get(cat, [])
                    for case in cases:
                        label = case.get('label')
                        for ev in case.get('evidence', []):
                            all_records.append({
                                'file': filename,
                                'meeting': meeting,
                                'category': cat,
                                'raw_label': label,
                                'normalized': normalize_label(label),
                                'quote': ev.get('quote', '').lower(),
                                'speaker': ev.get('speaker')
                            })
    return pd.DataFrame(all_records)

#EXECUTION
df = load_all_data(DATA_DIR)

#AUTOMATED AUDIT 
print("1: NORMALIZED VIEW ")
print(df['normalized'].value_counts())

print("\n 2: QUALITY ISSUES (Hallucinations & Noise)")
# Audit for Roadmap Hallucinations (Benchmarking, Future Talk)
roadmap_keys = ['working toward', 'planned', 'future', 'roadmap', 'next release']
hals = df[df['quote'].str.contains('|'.join(roadmap_keys))]
print(f"Roadmap Hallucinations detected: {len(hals)}")

# Audit for Environmental Noise (The 'Rug' Problem)
noise_keys = ['randomly', 'rug', 'false positive', 'misidentifying', 'disabled']
noise = df[df['quote'].str.contains('|'.join(noise_keys))]
print(f"Data Noise/False Positives detected: {len(noise)}")

print("\n 3: TOP OPPORTUNITIES (Non-Safety/Logistics)")
opp_keys = ['trailer', 'turnaround', 'detention', 'security', 'after hours', 'efficiency']
opps = df[df['quote'].str.contains('|'.join(opp_keys))]
print(f"Non-safety opportunity signals: {len(opps)}")

if not opps.empty:
    print("\nSample Opportunity Quote:")
    print(opps[['meeting', 'quote']].iloc[0].values)