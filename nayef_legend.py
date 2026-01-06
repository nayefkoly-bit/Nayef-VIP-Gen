import asyncio, aiohttp, re, os, time, json, sys, subprocess
from colorama import Fore, init

init(autoreset=True)

SOURCE_URL = "https://sieuthidora.io.vn/br1/hma.php?step=1"
DB_FILE = "system_data.json"

# ১. ইউনিক ডিভাইস আইডি বের করার ফাংশন
def get_hwid():
    # টার্মাক্সে ডিভাইসের ইউনিক সিরিয়াল বা আইডি নেওয়ার চেষ্টা
    try:
        # termux-telephony-deviceinfo বা প্রোসেসর আইডি ব্যবহার করা যায়
        hwid = subprocess.check_output('getprop ro.serialno', shell=True).decode().strip()
        if not hwid:
            hwid = subprocess.check_output('getprop ro.product.model', shell=True).decode().strip()
        return hwid
    except:
        return "UNKNOWN_DEVICE"

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f: json.dump({}, f)
    with open(DB_FILE, "r") as f: return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f: json.dump(data, f, indent=4)

# ২. মডিফাইড লগইন সিস্টেম (Device Lock সহ)
def login():
    os.system('clear')
    print(f"{Fore.CYAN}亗 NAYEF VIP DEVICE LOCK SYSTEM 亗")
    
    db = load_db()
    user_key = input(f"\n{Fore.YELLOW}ENTER LICENSE KEY: {Fore.WHITE}")
    current_hwid = get_hwid() # বর্তমান ফোনের আইডি

    if user_key in db:
        user_data = db[user_key]
        
        # ডিভাইস চেক লজিক
        if "hwid" not in user_data or user_data["hwid"] == "":
            # প্রথমবার লগইন করলে আইডি সেভ হবে
            user_data["hwid"] = current_hwid
            save_db(db)
            print(f"{Fore.GREEN}SUCCESS: DEVICE REGISTERED!")
        elif user_data["hwid"] != current_hwid:
            # অন্য ডিভাইসে লগইন করতে চাইলে বাধা দিবে
            print(f"{Fore.RED}ERROR: DEVICE NOT ALLOWED!")
            print(f"{Fore.WHITE}THIS KEY IS LOCKED TO ANOTHER DEVICE.")
            sys.exit()
        
        # ভ্যালিডিটি চেক
        if time.time() > user_data['expiry']:
            print(f"{Fore.RED}ERROR: KEY EXPIRED!"); sys.exit()
            
        print(f"{Fore.GREEN}LOGIN SUCCESSFUL! WELCOME NAYEF VIP USER.")
        time.sleep(2)
        asyncio.run(main_gen()) # জেনারেটর চালু হবে
    else:
        print(f"{Fore.RED}INVALID KEY!"); time.sleep(1); login()

# বাকি জেনারেটর কোড আগের মতোই থাকবে...
