import json


raised_amount_map = dict()
f = open("main_urls.txt", "r")
for line in f:
    line = line.strip()
    index = line.find(",")
    url = line[:index]
    raised_amount = int(line[index+1:])
    raised_amount_map[url] = raised_amount
f.close()

file_path = 'dataset/analysis_campaign_ML_cleaned.json'
with open(file_path, 'r') as file:
    data = json.load(file)


for campaign in data:
    url = campaign["URL"]
    if url in raised_amount_map:
        campaign["RaisedAmount"] = raised_amount_map[url]
        if campaign["RaisedAmount"] > campaign["GoalAmount"]:
            campaign["success"] = 1
        else:
            campaign["success"] = 0


try:
    with open("final_gfmdata_for_analysis", 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data successfully saved")
except Exception as e:
    print(f"An error occurred: {e}")
    
