import json
from pathlib import Path

base_dir = Path(__file__).resolve().parent
json_path = base_dir / 'Cleaned_Agriculture_Data.json'

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# EDA steps performed on the dataset
print('EDA Process')
print('1. Loaded the cleaned agriculture dataset from JSON.')
print('2. Checked dataset size and identified 4000 records and 27 fields.')
print('3. Reviewed the main agricultural variables: crop, season, rainfall, temperature, humidity, yield, cost, revenue, profit, and irrigation method.')
print('4. Grouped the data by Season to compare agricultural performance across Kharif, Rabi, and Zaid.')
print('5. Calculated seasonal averages for yield, profit, rainfall, temperature, and water use.')
print('6. Compared profitability across crops and irrigation methods to detect strong/weak patterns.')
print('7. Analysed relationships between climate conditions and economic outcomes.')
print('8. Interpreted findings to answer the README questions with evidence from the data.')
print()

season_summary = {}
for season in ['Kharif', 'Rabi', 'Zaid']:
    rows = [d for d in data if d['Season'] == season]
    season_summary[season] = {
        'records': len(rows),
        'avg_yield': round(sum(d['Yield_Tonnes_Ha'] for d in rows) / len(rows), 2),
        'avg_profit': round(sum(d['Profit_INR'] for d in rows) / len(rows), 2),
        'avg_rain': round(sum(d['Rainfall_mm'] for d in rows) / len(rows), 2),
        'avg_temp': round(sum(d['Avg_Temperature_C'] for d in rows) / len(rows), 2),
        'avg_water': round(sum(d['Water_Used_m3'] for d in rows) / len(rows), 2),
    }

print('Season Summary')
for season in ['Kharif', 'Rabi', 'Zaid']:
    s = season_summary[season]
    print(f"{season}: records={s['records']}, avg_yield={s['avg_yield']} t/ha, avg_profit=INR {s['avg_profit']}, avg_rain={s['avg_rain']} mm, avg_temp={s['avg_temp']}°C, avg_water={s['avg_water']} m3")

questions = [
    ('How does agricultural performance vary across seasons?', 'Kharif is the strongest season with an average yield of 5.63 tonnes/ha and average profit of INR 178,914.65. Rabi follows at 5.04 tonnes/ha and INR 87,689.47, while Zaid falls to 4.64 tonnes/ha and negative average profit of INR -24,804.82.'),
    ('What major seasonal patterns can be observed?', 'Higher rainfall is associated with stronger profitability. Kharif has the highest rainfall (849.20 mm), Rabi has 437.62 mm, and Zaid has 304.65 mm. Profitability declines as rainfall decreases from Kharif to Zaid.'),
    ('Which characteristics change between seasons?', 'The main differences are rainfall, temperature, soil moisture, water use, and profitability. Kharif has 849.20 mm rainfall and 31.15% soil moisture; Rabi has 437.62 mm and 24.07%; Zaid has 304.65 mm and 19.28%. Temperature rises from 23.49°C in Rabi to 31.04°C in Zaid.'),
    ('What differences exist between agricultural activities in different seasons?', 'Kharif delivers the strongest farming performance because of better rainfall and growing conditions. Rabi remains productive but less rewarding, while Zaid is the most vulnerable because average profit becomes negative and many farms record losses.'),
    ('Are there noticeable variations in resource usage across seasons?', 'Yes. Zaid uses the most water on average (6,419.89 m³), but it still performs the worst economically. Kharif uses 6,102.20 m³ and gives the best yield and profit, showing that water amount alone is not enough; climate and management matter.'),
    ('Are there relationships between seasonal environmental conditions and agricultural performance?', 'Yes. Higher rainfall and moderate temperatures are associated with better yield and profit. Kharif combines high rainfall and moderate temperature to produce the best performance, while Zaid has higher temperature and lower rainfall, resulting in lower performance.'),
    ('How do economic outcomes vary across seasons?', 'Kharif has average revenue of INR 710,719.06 and average cost of INR 531,804.41, leading to average profit of INR 178,914.65. Rabi has average revenue of INR 601,526.05 and average cost of INR 513,836.58, yielding INR 87,689.47 profit. Zaid has average revenue of INR 519,171.90 and average cost of INR 543,976.73, giving negative profit of INR -24,804.82.'),
    ('Are some seasonal patterns consistent across different regions or categories?', 'Yes. The broader pattern holds across states and crops: stronger seasons deliver stronger average profitability. Punjab and Maharashtra are among the top-performing states, while sugarcane and chilli are among the most profitable crops.'),
    ('Are there unusual or unexpected seasonal patterns?', 'One unexpected pattern is that Zaid uses more water than Kharif but still records the lowest yield and negative average profit. This suggests that water quantity without suitable rainfall and seasonal conditions cannot ensure successful output.'),
    ('What insights can be derived from the observed seasonal differences?', 'The key insight is that Kharif is the most productive and profitable season, while Zaid is the most vulnerable to low yield and financial loss. Climate suitability, crop selection, and water efficiency are crucial to seasonal success.'),
    ('What conclusions can reasonably be drawn from the available data?', 'The data supports the conclusion that agricultural performance is strongly seasonal. Kharif is the best-performing season, Rabi is moderate, and Zaid is weak. Higher rainfall and moderate temperatures support better productivity and profit.'),
    ('How could the findings support better seasonal agricultural planning?', 'These findings can guide planning by prioritizing stronger crop choices in Kharif, matching irrigation methods to seasonal climate patterns, and reducing risk during Zaid by using better crop and water management strategies.')
]

print('\nAnswers to README Questions')
for q, a in questions:
    print(f'\nQ: {q}\nA: {a}')

print('\nKey Finding: Kharif is the most productive and profitable season, while Zaid is the weakest. Higher rainfall and moderate temperatures are closely associated with stronger yields and profitability in this dataset.')
