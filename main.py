import requests
import time
import os
from colorama import init, Fore
from threading import Thread

init(autoreset=True)

banner = f"""
                           ┌─                                                                                                 ─┐
                                                                                                                                          
                               {Fore.RED}   _   _                              {Fore.GREEN}           _        _             
                               {Fore.RED}  | | | | __ ___   _____   ___        {Fore.GREEN} _ __ ___ | |_ __ _| |_ ___  _ __   
                               {Fore.RED}  | |_| |/ _` \ \ / / _ \ / __|       {Fore.GREEN}| '__/ _ \| __/ _` | __/ _ \| '__|
                               {Fore.RED}  |  _  | (_| |\ V / (_) | (__        {Fore.GREEN}| | | (_) | || (_| | || (_) | |   
                               {Fore.RED}  |_| |_|\__,_| \_/ \___/ \___|       {Fore.GREEN}|_|  \___/ \__\__,_|\__\___/|_|   
                                                 
                           └─                                                                                                 ─┘            
                                 {Fore.BLUE}Developers: | Death (tester zip){Fore.MAGENTA}
        
"""
token = "MTM0NTA1NTA0MTMwMzg3NTY4Ng.GEX8rp.peSrYEucYaK8H14hCho00l61ZfW99hPGMpYMM0"
print(banner)
TOKEN = input("Enter your Discord token: ").strip()
status_options = ["online", "idle", "dnd", "invisible"]
while True:
    DEFAULT_STATUS = input("Which status do you want? (online, idle, dnd, invisible): ").strip().lower()
    if DEFAULT_STATUS in status_options:
        break
    else:
        print("Invalid status. Please choose from (online, idle, dnd, invisible).")

URL = "https://discord.com/api/v10/users/@me/settings"
USER_URL = "https://discord.com/api/v10/users/@me"
headers = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

def fetch_username():
    response = requests.get(USER_URL, headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        return user_data['username']
    else:
        print(f"Failed to fetch username. Response code: {response.status_code}")
        return "UnknownUser"

def update_status(custom_text, presence):
    payload = {
        "status": presence,
        "custom_status": {"text": custom_text}
    }
    response = requests.patch(URL, headers=headers, json=payload)
    if response.status_code == 200:
        print_log(custom_text, presence)
    else:
        print(f"Failed to update status. Response code: {response.status_code}")

log_count = 0

def print_log(custom_text, presence):
    global log_count
    censored_token = TOKEN[:20] + '*****'
    username = fetch_username()
    current_time = time.strftime("%I:%M:%S %p")
    log_message = f"{Fore.MAGENTA}{current_time} | {Fore.MAGENTA}Status changed for: {Fore.GREEN}{censored_token} | {Fore.GREEN}{username}"
    if custom_text:
        log_message += f" | {Fore.MAGENTA}New Status: {Fore.MAGENTA}{custom_text}"
    if log_count == 0:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(banner)
    print(log_message)
    log_count += 1
    if log_count >= 12:
        log_count = 0

def setup():
    status_list = []
    while True:
        add_text = input("Do you want to add a status text? (yes/no): ").strip().lower()
        if add_text in ['yes', 'y']:
            text = input("Enter your status text: ").strip()
            status_list.append(text)
            print(f"Added: '{text}'")
        elif add_text in ['no', 'n']:
            break
        else:
            print("Please enter 'yes' or 'no'.")
    return status_list

def rotate_statuses(status_list):
    while True:
        for custom_text in status_list:
            update_status(custom_text, DEFAULT_STATUS)
            time.sleep(1.5)

def check_and_maintain_online_status():
    while True:
        response = requests.get(USER_URL, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            if user_data.get("status") != "online":
                update_status("", "online")
                print(f"{Fore.MAGENTA}{time.strftime('%I:%M:%S %p')} | Automatically reconnected to online status")
        else:
            print(f"Failed to check online status. Response code: {response.status_code}")
        time.sleep(600)

status_list = setup()
Thread(target=check_and_maintain_online_status, daemon=True).start()
Thread(target=rotate_statuses, args=(status_list,), daemon=True).start()

while True:
    time.sleep(1)
