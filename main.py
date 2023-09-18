import requests
import json
import tkinter as tk

# Set up API endpoint
url = "https://groups.roblox.com/v1/groups/{}/assets?assetType=1&sortOrder=Desc&limit=100&createdAfter=0"

# Set up authentication
def authenticate():
    cookies = cookie_entry.get()
    headers = {"Cookie": cookies}
    response = requests.get("https://www.roblox.com/home", headers=headers)
    if response.status_code == 200:
        return headers
    else:
        return None

# Get group assets
def get_assets():
    group_id = group_entry.get()
    headers = authenticate()
    if headers is None:
        status_label.config(text="Invalid cookies")
        return
    response = requests.get(url.format(group_id), headers=headers)
    if response.status_code == 200:
        data = json.loads(response.text)
        for asset in sorted(data["data"], key=lambda x: x["created"]):
            if asset["assetType"]["name"] == "Shirt" or asset["assetType"]["name"] == "Pants":
                asset_listbox.insert(tk.END, f"{asset['name']} ({asset['id']})")
    else:
        status_label.config(text="Invalid group ID")

# Update asset descriptions
def update_assets():
    headers = authenticate()
    if headers is None:
        status_label.config(text="Invalid cookies")
        return
    for index in asset_listbox.curselection():
        asset_id = asset_listbox.get(index).split("(")[1].split(")")[0]
        asset_url = f"https://api.roblox.com/marketplace/productinfo?assetId={asset_id}"
        asset_response = requests.get(asset_url)
        asset_data = json.loads(asset_response.text)
        if asset_data["AssetTypeId"] == 11:
            payload = {"description": "shirt"}
        elif asset_data["AssetTypeId"] == 12:
            payload = {"description": "pants"}
        else:
            continue
        edit_url = f"https://www.roblox.com/catalog/{asset_id}/update"
        edit_response = requests.post(edit_url, headers=headers, data=payload)
        status_label.config(text=f"Updated {asset_data['Name']} ({asset_id}) with description {payload['description']}")

# Set up GUI
root = tk.Tk()
root.title("Group Clothing Description Updater")

cookie_label = tk.Label(root, text="Roblox authentication cookies:")
cookie_label.pack()
cookie_entry = tk.Entry(root)
cookie_entry.pack()

group_label = tk.Label(root, text="Group ID:")
group_label.pack()
group_entry = tk.Entry(root)
group_entry.pack()

get_assets_button = tk.Button(root, text="Get Assets", command=get_assets)
get_assets_button.pack()

asset_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
asset_listbox.pack()

description_label = tk.Label(root, text="New Description:")
description_label.pack()
description_entry = tk.Entry(root)
description_entry.pack()

update_button = tk.Button(root, text="Update Descriptions", command=update_assets)
update_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
