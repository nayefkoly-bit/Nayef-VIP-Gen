import asyncio, aiohttp, re, os, time, json, sys, socket
from colorama import Fore, Style, init

init(autoreset=True)

# Sources & DB
SOURCE_URL = "https://sieuthidora.io.vn/br1/hma.php?step=1"
DB_FILE = "system_data.json"

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f: json.dump({"NAYEF_OWNER": {"expiry": 4102444800, "used": False}}, f)
    with open(DB_FILE, "r") as f: return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f: json.dump(data, f, indent=4)

def get_ip():
    try: return socket.gethostbyname(socket.gethostname())
    except: return "127.0.0.1"

def animation(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)
    print()

def banner():
    os.system('clear')
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════╗")
    print(f"{Fore.GREEN}║          亗 NAYEF VIP LEGENDARY SYSTEM 亗            ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════╝")

async def fetch_key(session):
    try:
        async with session.get(f"{SOURCE_URL}&cache={time.time()}", timeout=10) as response:
            text = await response.text()
            match = re.search(r'KEY_FREE_BR_[A-Z0-9]+', text)
            return match.group(0) if match else None
    except: return None

async def main_gen():
    banner()
    animation(f"{Fore.YELLOW}>>> INITIALIZING TURBO GENERATOR ENGINE...")
    try:
        amount = int(input(f"{Fore.WHITE}[?] ENTER QUANTITY: {Fore.GREEN}"))
    except: return

    print(f"\n{Fore.MAGENTA}🚀 INJECTING REQUESTS...")
    
    keys = []
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=100)) as session:
        tasks = [fetch_key(session) for _ in range(amount)]
        results = await asyncio.gather(*tasks)
        keys = [k for k in results if k]

    print(f"\n{Fore.GREEN}--- [ DATABASE OUTPUT ] ---")
    for k in keys: print(f"{Fore.WHITE}{k}")
    
    while True:
        print(f"\n{Fore.YELLOW}[1] COPY ALL (10K LIMIT) | [2] DOWNLOAD | [3] EXIT")
        opt = input(f"\n{Fore.CYAN}ACTION >> {Fore.WHITE}")
        if opt == '1':
            os.system(f"echo '{chr(10).join(keys)}' | termux-clipboard-set")
            print(f"{Fore.GREEN}✔ SUCCESS: CLIPPED TO BOARD!")
        elif opt == '2':
            fn = f"nayef_{int(time.time())}.txt"
            with open(fn, "w") as f: f.write("\n".join(keys))
            print(f"{Fore.BLUE}✔ SAVED AS: {fn}")
        elif opt == '3': sys.exit()

def admin_panel():
    banner()
    print(f"{Fore.RED}--- [ SECRET ADMIN CONTROL ] ---")
    days = int(input(f"{Fore.WHITE}SET VALIDITY (DAYS): "))
    new_key = "NAYEF_VIP_" + os.urandom(3).hex().upper()
    db = load_db()
    db[new_key] = {"expiry": time.time() + (days * 86400), "used": False}
    save_db(db)
    print(f"\n{Fore.GREEN}ACCESS KEY CREATED: {Fore.WHITE}{new_key}")
    input("\nPRESS ENTER TO RETURN...")

def login():
    banner()
    animation(f"{Fore.WHITE}Checking System Integrity...")
    print(f"\n{Fore.WHITE}[1] ACCESS SYSTEM")
    print(f"{Fore.BLACK}[.] HIDDEN PORTAL") # সাধারণ চোখে দেখা যাবে না
    
    choice = input(f"\n{Fore.CYAN}SELECT >> {Fore.WHITE}")

    if choice == '99': # সিক্রেট কোড (৯৯ চাপলে এডমিন প্যানেল আসবে)
        admin_panel()
        login()

    elif choice == '1':
        user_key = input(f"{Fore.YELLOW}ENTER LICENSE KEY: {Fore.WHITE}")
        db = load_db()
        if user_key in db:
            data = db[user_key]
            if time.time() > data['expiry']:
                print(f"{Fore.RED}LICENSE EXPIRED!"); sys.exit()
            
            # Advanced User Info
            rem = data['expiry'] - time.time()
            banner()
            animation(f"{Fore.GREEN}>>> ACCESS GRANTED!")
            print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"{Fore.WHITE}USER IP    : {Fore.YELLOW}{get_ip()}")
            print(f"{Fore.WHITE}STATUS     : {Fore.GREEN}ACTIVE")
            print(f"{Fore.WHITE}VALIDITY   : {Fore.YELLOW}{int(rem//86400)} Days {int((rem%86400)//3600)} Hours")
            print(f"{Fore.WHITE}SERVER     : {Fore.GREEN}CONNECTED")
            print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            time.sleep(2)
            asyncio.run(main_gen())
        else:
            print(f"{Fore.RED}INVALID LICENSE!"); time.sleep(1); login()

if __name__ == "__main__":
    login()
    