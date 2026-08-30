import discord
from discord import app_commands
import json
import os
import io
import aiohttp
import asyncio
from datetime import datetime, timedelta, timezone
import random
import re
import string
from typing import Dict, List, Optional, Tuple
import hashlib
import base64
import mimetypes
from urllib.parse import quote_plus
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from fairness import (
    deterministic_boolean,
    deterministic_choice,
    deterministic_sample,
    deterministic_shuffle,
    deterministic_weighted_choice,
    generate_server_seed,
    get_server_seed_hash,
)

import time
import threading
import sys
import ctypes
from ctypes import wintypes

ACTIVE_RACE_PANEL_VIEWS: List[discord.ui.View] = []
ACTIVE_MINIGAME_TASKS: Dict[str, asyncio.Task] = {}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

                                                            
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import pyautogui
except Exception:
    webdriver = None
    Service = None
    Options = None
    By = None
    WebDriverWait = None
    EC = None
    pyautogui = None

                                                                                         
_LAUNCHER_DRIVER = None
_LAUNCHER_LOCK = threading.Lock()


BOT_TOKEN = "DM @kem.dev for help!"  


VALUE_EMOJI = "DM @kem.dev for help!"
WILD_MODE_EMOJI = "DM @kem.dev for help!"
MINES_SAFE_EMOJI = "DM @kem.dev for help!"  
MINES_HIT_EMOJI = "DM @kem.dev for help!"
HEADS_EMOJI = "DM @kem.dev for help!" 
TAILS_EMOJI = "DM @kem.dev for help!" 
ADMIN_USER_IDS = [DM @kem.dev for help!, 2ND USER ID GOES HERE]  

TAX_PROFILES = {
    "1290983964236054542": {"emoji": "<:Lach679:1528632991973249134>", "tax_rate": 0.5},
    "1512843503703691295": {"emoji": "<:callz2smart:1528632983152496690>", "tax_rate": 0.5},
}

STAFF_PROFILES = {
    "1460355839188668607": {"emoji": "<:Zy:1528633915445612634>", "uses": 0, "limit": 10},
    "807160521353854986": {"emoji": "<:Spicy:1528633906075537449>", "uses": 0, "limit": 10}
}

EVENT_HOST_PROFILES = {
    "1460355839188668607": {"emoji": "<:Zy:1528633915445612634>", "uses": 0, "limit": 3},
    "807160521353854986": {"emoji": "<:Spicy:1510963986819055806>", "uses": 0, "limit": 3}
}

                        
MINIGAME_NAMES = [
    {"name": "Guess the Crypto", "emoji": ""},
    {"name": "Guess the Pet", "emoji": ""},
    {"name": "Guess the Set", "emoji": ""},
    {"name": "VC Roullete", "emoji": ""},
]

                      
GUESS_CRYPTO_CHANNEL_ID = DM @kem.dev for help!                                            
GUESS_PET_CHANNEL_ID = DM @kem.dev for help!                                         
GUESS_SET_CHANNEL_ID = DM @kem.dev for help!                                         
VC_ROULETTE_TEXT_CHANNEL_ID = DM @kem.dev for help!                                                
VC_ROULETTE_CATEGORY_ID = DM @kem.dev for help!                                                         

                                              
CRYPTO_SYMBOLS_CONFIG = {
    "BTC": {"emoji": "<:Bitcoin:1528625118904057897>", "image": ""},
    "ETH": {"emoji": "<:Etherium:1528625127510638714>", "image": ""},
    "DOGE": {"emoji": "<:DOGE:1528634074540019884>", "image": ""},
    "LTC": {"emoji": "<:Litecoin:1528625110242820178>", "image": ""},
    "SOL": {"emoji": "<:Solana:1528625144409362572>", "image": ""},
    "TETHER": {"emoji": "<:Tether:1528625135852978248>", "image": ""},
    "USDC": {"emoji": "<:USDC:1528634083901706350>", "image": ""},
    "XRP": {"emoji": "<:XRP:1528634093091295405>", "image": ""},
    "BNB": {"emoji": "<:BNB:1528634102494924940>", "image": ""},
    "POL": {"emoji": "<:POLY:1528634111294574632>", "image": ""},
    "TON": {"emoji": "<:TON:1528634120152944702>", "image": ""},
    "TRUMP": {"emoji": "<:TRUMP:1528634138532384838>", "image": ""},
    "PEPE": {"emoji": "<:PEPE:1528634128944205965>", "image": ""},
}

                                                    
PET_NAMES_CONFIG = {
    "Neon Fury": {"emoji": "", "image": ""},
    "Star": {"emoji": "", "image": ""},
    "Neon Ruby": {"emoji": "", "image": ""},
    "Ominous Glow": {"emoji": "", "image": ""},
    "Relic": {"emoji": "", "image": ""},
    "Glow Essence": {"emoji": "", "image": ""},
    "Infernal Glow": {"emoji": "", "image": ""},
    "Prismatic Star": {"emoji": "", "image": ""},
    "Starlight Essence": {"emoji": "", "image": ""},
}

                                         
SET_NAMES_CONFIG = {
    "Flowerwood Set": {"emoji": "<:FlowerwoodSet:1528634312168050818>", "image": "https://cdn.nookazon.com/128x128/mm2/Sets/fff0f88c3c3a5e101642327d68c5b0c1.jpeg", "items": ["Flowerwood","Flowerwood Gun",]},
    "Bringer Set": {"emoji": "<:BringerSet:1528634303448088617>", "image": "", "items": []},
    "Hallow Set": {"emoji": "<:HallowSet:1528634294455767070>", "image": "", "items": []},
    "Soul Set": {"emoji": "<:SoulSet:1528634285802913895>", "image": "", "items": []},
    "Travelers Set": {"emoji": "<:TravelersSet:1528634276906668142>", "image": "", "items": []},
    "Ocean Set": {"emoji": "<:OceanSet:1528634268190773328>", "image": "", "items": []},
    "Rainbow Set": {"emoji": "<:RainbowSet:1528634259043254453>", "image": "", "items": []},
    "Xeno Set": {"emoji": "<:XenoSet:1528634249878573078>", "image": "", "items": []},
    "Blizzard Set": {"emoji": "<:BlizzardSet:1528634241624314016>", "image": "", "items": []},
    "Sun Set": {"emoji": "<:SunSet:1528634232837111948>", "image": "", "items": []},
    "Ever Set": {"emoji": "<:EverSet:1528634224272347146>", "image": "", "items": []},
    "Bloom Set": {"emoji": "<:BloomSet:1528634215128764539>", "image": "", "items": []},
    "Dark Set": {"emoji": "<:DarkSet:1528634206819979274>", "image": "", "items": []},
    "Vampires Set": {"emoji": "<:VampiresSet:1528634198250750123>", "image": "", "items": []},
    "Celestial Set": {"emoji": "<:CelestialSet:1528634189618876466>", "image": "", "items": []},
    "Bauble Set": {"emoji": "<:BaubleSet:1528634181121343529>", "image": "", "items": []},
    "Snow Set": {"emoji": "<:SnowSet:1528634172661563412>", "image": "", "items": []},
    "Sakura Set": {"emoji": "<:SakuraSet:1528634164293668935>", "image": "", "items": []},
    "Alien Set": {"emoji": "<:AlienSet:1528634155125047317>", "image": "", "items": []},
    "Sweet Set": {"emoji": "<:SweetSet:1528634146858078228>", "image": "", "items": []},
}

ACTIVE_CRYPTO_GAMES = {}
ACTIVE_PET_GAMES = {}
ACTIVE_SET_GAMES = {}
ACTIVE_ROULETTE_GAMES = {}
                                                      
                                                                         
                                                                        
RACE_PRIZE_CONFIG = {
    "daily": {
        1: ["Chroma Evergun"],
        2: ["Bauble"],
        3: ["Candy"],
        4: ["Candy"],
        5: ["Sugar"],
    },
    "weekly": {
        1: ["Evergun"],
        2: ["Bauble"],
        3: ["Candy"],
        4: ["Candy"],
        5: ["Sugar"],
    },
    "monthly": {
        1: ["Chroma Evergun"],
        2: ["Evergun"],
        3: ["Bauble"],
        4: ["Candy"],
        5: ["Candy"],
    },
    "adm_daily": {
        1: ["Harvester"],
        2: ["Ice Breaker"],
        3: ["Sugar"],
        4: ["Sugar"],
        5: ["Sugar"],
    },
    "adm_weekly": {
        1: ["Candy"],
        2: ["Sugar"],
        3: ["Sugar"],
        4: ["Sugar"],
        5: ["Sugar"],
    },
    "adm_monthly": {
        1: ["Candy"],
        2: ["Sugar"],
        3: ["Sugar"],
        4: ["Sugar"],
        5: ["Sugar"],
    },
}

RACE_BANNER_CONFIG = {
    "daily": "https://cdn.discordapp.com/attachments/1512846833012052058/1529664830859120670/Your_paragraph_text_9.png?ex=6a62c2e3&is=6a617163&hm=a74592da15da9bac740b9fe1883a9d1fca22f26358e90ce30b0d2d084a77d346&",
    "weekly": "https://cdn.discordapp.com/attachments/1512846833012052058/1529684319747182592/Your_paragraph_text_11.png?ex=6a62d509&is=6a618389&hm=e935a5d03dbe05f01188d3d54d11718ec891680a7e6c8ae9b87379fd6e1b717a&",
    "monthly": "https://cdn.discordapp.com/attachments/1512846833012052058/1529699217516400701/Your_paragraph_text_12.png?ex=6a62e2e9&is=6a619169&hm=4f642422f38a733acfba9d19acc3a62c7bb5d500acf8d37727baf72f58d5417b&",
    "adm_daily": "https://cdn.discordapp.com/attachments/1512846833012052058/1529664830859120670/Your_paragraph_text_9.png?ex=6a62c2e3&is=6a617163&hm=a74592da15da9bac740b9fe1883a9d1fca22f26358e90ce30b0d2d084a77d346&",
    "adm_weekly": "https://cdn.discordapp.com/attachments/1512846833012052058/1529684319747182592/Your_paragraph_text_11.png?ex=6a62d509&is=6a618389&hm=e935a5d03dbe05f01188d3d54d11718ec891680a7e6c8ae9b87379fd6e1b717a&",
    "adm_monthly": "https://cdn.discordapp.com/attachments/1512846833012052058/1529699217516400701/Your_paragraph_text_12.png?ex=6a62e2e9&is=6a619169&hm=4f642422f38a733acfba9d19acc3a62c7bb5d500acf8d37727baf72f58d5417b&",
}

RACE_BANNER_PLACEHOLDER_COORDS = {
    3: (1640, 430),
    2: (790, 430),
    1: (1210, 340),
}

RACE_BANNER_PLACEHOLDER_SIZE = 360
RACE_BANNER_AVATAR_URL = "https://tr.rbxcdn.com/30DAY-Avatar-D156CF11461372A56EC0F4400BE65CB8-Png/720/720/Avatar/Webp/noFilter"

ADMIN_PANEL_CHANNEL_ID = DM @kem.dev for help!
TAX_PANEL_CHANNEL_ID = DM @kem.dev for help!  
TAX_LOG_CHANNEL_ID = DM @kem.dev for help!  
EVENT_PANEL_CHANNEL_ID = DM @kem.dev for help!                                           
RACE_CHANNEL_CATEGORY_ID = DM @kem.dev for help!
RACE_CHANNEL_CATEGORY_BEFORE_ID = DM @kem.dev for help!
WITHDRAWAL_CATEGORY_ID = DM @kem.dev for help! 
SUPPORT_TEAM_ROLE_ID = DM @kem.dev for help!  
RULES_CHANNEL_ID = DM @kem.dev for help!                                    
RULES_IMAGE_URL = "https://cdn.discordapp.com/attachments/1513819693910196285/1529099741126725792/Your_paragraph_text.png?ex=6a60b49b&is=6a5f631b&hm=b7e431ba1b37e2432670910e8e4f39cf701a33a183c3088ed5de113c0b0bb10b&"                                     
TAG_ADOPTION_CHANNEL_ID = DM @kem.dev for help!                                                           
TAG_EVENT_CHANNEL_ID = DM @kem.dev for help!                                           
TAG_REWARD_STATE_FILE = "tag_reward_state.json"

                                 
INVITE_LOGS_CHANNEL_ID = DM @kem.dev for help!                                          
INVITE_EVENT_CHANNEL_ID = DM @kem.dev for help!                                        
INVITE_REWARD_STATE_FILE = "invite_reward_state.json"

                       
LISTING_CHANNEL_ID = DM @kem.dev for help! 

                                     
VERIFICATION_CHANNEL_ID = DM @kem.dev for help!                                                
VERIFICATION_PANEL_FILE = "verification_panel.json"                                      
REFERRALS_URL = "https://discord.com/channels/1497891147664588870/1513526142236229813"                                      

            
ITEMS_FILE = "mm2.json"
INVENTORY_FILE = "inventory.json"
REGISTRATIONS_FILE = "registrations.json"
MINES_GAMES_FILE = "active_mines_games.json"
THUMBNAIL_PATH = "Bloxloot.jpg"  
BLACKJACK_GAMES_FILE = "active_blackjack_games.json"
LISTINGS_FILE = "active_listings.json"
WITHDRAWALS_FILE = "active_withdrawals.json"
TAX_ITEMS_FILE = "taxed_items.json"
ADMIN_PANEL_FILE = "admin_panel.json"
TAX_PANEL_FILE = "tax_panel.json"
DEPOSIT_PANEL_FILE = "deposit_panel.json"
WITHDRAW_PANEL_FILE = "withdraw_panel.json"
EVENT_PANEL_FILE = "event_panel.json"
EVENT_HOST_PROFILES_FILE = "event_host_profiles.json"
STAFF_PROFILES_FILE = "staff_profiles.json"
DEVELOPER_PROFILES_FILE = "developer_profiles.json"
UPDATE_LOG_CHANNEL_ID = 1507263112464826440
UPDATES_FILE = "update_logs.json"
STOCK_FILE = "stock.json"
TOWERS_GAMES_FILE = "active_towers_games.json"
CRYPTO_DEPOSITS_FILE = "crypto_deposits.json"
CRYPTO_WITHDRAWALS_FILE = "crypto_withdrawals.json"
BALANCES_FILE = "balances.json"
COMPLETED_GAMES_FILE = "completed_games.json"
PROCESSED_TRADES_FILE = "processed_trades.json"
RULES_PANEL_FILE = "rules_panel.json"
RPS_GAMES_FILE = "active_rps_games.json"

DEPOSIT_CHANNEL_ID = DM @kem.dev for help!  
WITHDRAW_CHANNEL_ID = DM @kem.dev for help!  
OXA_MERCHANT_API_KEY = "DM @kem.dev for help!"  
OXA_PAYOUT_API_KEY = "DM @kem.dev for help!"  
OXA_MERCHANT_ID = "DM @kem.dev for help!" 

MM2_DEPOSIT_SERVERS = [
    {
        "name": "Notnnkasbrother",
        "roblox_username": "Notnnkasbrother",
        "cookie": "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEaAhADIhwKBGR1aWQSFDEwMzMyNjc1NjM4MTc3OTkxNTMwKAM.42yzE29GWzXx74niJ1glb0PwbZNx2o5ap7Bt_MnuDP2qIX-ZjezmaSGcYyR4ka_tMsLs6eVOfu4_ZR6h42wmABMI63uZjOoZYikhularlHo9keGnc6TT7G1TVyU9CKf0KaMLO8IeL6ru0-J3K0xOziRtxS9o5M7DG5wDkB4izv8QQb5YS4mtvEAs7rzVgcAlm39juK4bBG60u0pFa92AZesx--1b-gwscWcJ0bzvAKg357Bsj1es_dv5lMXYLPP3ZN0BK7ekvtM-Xl06tFh5nSv7CzcvK2QJV0UM2Yj6b4aYvSVn6X2dfWxq2nyRPGZsf0_viRpJIlKbigxFak1kDulzlA45s4QSGgOrKVMx-LvH_zakVpdFx6Pg6MHdRbRsXW_46rcKQKPTC-AFN1YXQdEvtURolYLx-nUmx4hByYx1vkTAUBrenGgxEeVc7yA6XzDm-hUfnPZIt5wQB44qC8zTePu-9hQeA4P9DqNgyOtZC-FikCboEFlG4YwQJNtMbb1kH7R9atfASQvzTUp52q79p9TxW9-D6s5VJBIdO-OX8G4Xa6qX9ZWULUVPx5CWDB7htGNqCgazKKHrlAZ_zxZBEfb8w7Vn69VnnHbRnH9-wSxrElt-05rpmRWvzmPhv6PN7o7IWp899cTJJsD2vk951M4mifBWcfPTT6Ct0A9iYZ0iq7Bt3JrY3O4W5XqKsFDkgqWXxhJjUZpFrL85EJFiQ5LyJJgEWsiOq9WMG77l2dKCIBJpTJJDUuQ7yp0bhzv5_340az0kDF1ZwmX48xcUYrw",
        "emoji": "<:bottest:1528633941890826381>",
        "link": "https://www.roblox.com/share?code=af8326a49c2bbd4ab755948f6240c178&type=Server",
        "online": True
    },
    {
        "name": "Bloxloot267",
        "roblox_username": "Bloxloot267",
        "cookie": "_WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEaAhADIhwKBGR1aWQSFDEzMDI5ODI1MDE5MTgyMTUyMDg4KAM.Naap8_BMcV9pL5Zlmt_fN7T_GCqVyFXixoYR2dCO-QnCMOG1N780q5wAzYBm_bk8CTRWU7PTcQ9XVAyIGWv-JffDapT0820thqgVPLlj0rIWEyEZdcz3VuYP4iyl3QlfmrOADw8rd63MGGrr1I2swIiNrqIyC9ZdD1tSe5_q0dAzh6fgevKteQ6D662r2GygZjUJElgXfBK2iwlJc5df0XoJ9oGrLIYjOltmPTbuaaoth1Zkhc7jgF0p2VGKxc6EGUaBnyspLb6qNF29FDgcUPouZzWU6053bk8SGQgvaxRCWtUBDNzlyrScrZiaWORou3juSCPk_oUIUQIJ4bB1Gk5usNh7Gc9vtD7z6oGEXmBveGgsperrpCwzWh1a7ZsHf0zJM_c7yDgvn3umezARZOBs8ZfPxqftsX7m2TYO2yecf79Kzs_l1GjgmClRwa0tjK52xDGcK_ttW_3UZnlaGoeLwQFOtX7ZezZwr5mtclEDU6TpkyH9i19Afzr2hCXvYMDOe8Ojxg1g6m26VSc73t2t7B1EVXqiwtWua4JVEFpBzk3Ast9TgYlnzVokOQiyfSmgvB_74PPhggrnBXIFaBddHWQAFDfyk850v0QRNCYZgxjDaUvL7EO4ubLfNrQ1BBcQFaUVwmXb5vsriMe7_DRYS84EA_EmpHjyqqgtgiBnaxwogwMlZmEO38g28F9061F-wzMNCT6cIq_W30VItha5SWyTBVnrhItBdqwEZLuU7AdmzOd8_TqGjgVEMwDmhlsOOE3daxR1Usb50XQeHssmf9p_2cMBWODn3X1jqJQI8amcHM5h8yVFkCc7tZ3G3kRXNOmIOUGXWBXMTbgY2eJ_2rJ0x_2rJoteFlysqoZ_AbWT3e6YaeJ6jz7WFZ44gTRmZanrVMz2v135_ThecyLlUaa5xGeRc_KSXvjDyqsDZ0Rnl0hzJ_jX2M4yK-LkAWK9WA",
        "emoji": "<:bot2:1528625633574260846>",
        "link": "https://www.roblox.com/share?code=dc67aa3717b24c48b134ccf5bdcaae3a&type=Server",
        "online": False
    },
]
ADM_DEPOSIT_SERVERS = [
    {
        "name": "Bloxloot267 ",
        "roblox_username": "Bloxloot267 ",
        "cookie": "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEaAhADIhwKBGR1aWQSFDEwMzMyNjc1NjM4MTc3OTkxNTMwKAM.42yzE29GWzXx74niJ1glb0PwbZNx2o5ap7Bt_MnuDP2qIX-ZjezmaSGcYyR4ka_tMsLs6eVOfu4_ZR6h42wmABMI63uZjOoZYikhularlHo9keGnc6TT7G1TVyU9CKf0KaMLO8IeL6ru0-J3K0xOziRtxS9o5M7DG5wDkB4izv8QQb5YS4mtvEAs7rzVgcAlm39juK4bBG60u0pFa92AZesx--1b-gwscWcJ0bzvAKg357Bsj1es_dv5lMXYLPP3ZN0BK7ekvtM-Xl06tFh5nSv7CzcvK2QJV0UM2Yj6b4aYvSVn6X2dfWxq2nyRPGZsf0_viRpJIlKbigxFak1kDulzlA45s4QSGgOrKVMx-LvH_zakVpdFx6Pg6MHdRbRsXW_46rcKQKPTC-AFN1YXQdEvtURolYLx-nUmx4hByYx1vkTAUBrenGgxEeVc7yA6XzDm-hUfnPZIt5wQB44qC8zTePu-9hQeA4P9DqNgyOtZC-FikCboEFlG4YwQJNtMbb1kH7R9atfASQvzTUp52q79p9TxW9-D6s5VJBIdO-OX8G4Xa6qX9ZWULUVPx5CWDB7htGNqCgazKKHrlAZ_zxZBEfb8w7Vn69VnnHbRnH9-wSxrElt-05rpmRWvzmPhv6PN7o7IWp899cTJJsD2vk951M4mifBWcfPTT6Ct0A9iYZ0iq7Bt3JrY3O4W5XqKsFDkgqWXxhJjUZpFrL85EJFiQ5LyJJgEWsiOq9WMG77l2dKCIBJpTJJDUuQ7yp0bhzv5_340az0kDF1ZwmX48xcUYrw",
        "emoji": "<:bottest2:1528633950845538404>",
        "link": "https://www.roblox.com/share?code=9ff1077c64e0bd45b5631fc034cc4d84&type=Server",
        "online": True
    },
    {
        "name": "Bloxloot266",
        "roblox_username": "Bloxloot266",
        "cookie": "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_",
        "emoji": "<:bot1:1528625624821010534>",
        "link": "https://www.roblox.com/share?code=a6a3269504690c409d8fbcefed527506&type=Server",
        "online": False
    },
]

                                                                            
for _s in (MM2_DEPOSIT_SERVERS + ADM_DEPOSIT_SERVERS):
    if "roblox_username" not in _s:
                                                                            
        _s["roblox_username"] = _s.get("roblox_username") or _s.get("name")
    if "online" not in _s:
        _s["online"] = True


def format_deposit_server(server: dict) -> str:
    name = server.get("name", "Unknown")
    link = server.get("link", "")
    online = server.get("online", True)

    if not online:
        name = f"~~**{name}**~~"
        if link.startswith("http"):
            link_text = f"~~[Private Server]({link})~~"
        else:
            link_text = f"~~{link}~~"
    else:
        name = f"**{name}**"
        link_text = f"{('[Private Server](' + link + ')') if link.startswith('http') else link}"

    return f"{server.get('emoji', '')} {name} — {link_text}"


async def fetch_roblox_user_ids(usernames: list) -> Dict[str, int]:
    """Lookup Roblox user IDs from usernames using Roblox public API."""
    normalized = [str(username).strip() for username in usernames if str(username).strip()]
    if not normalized:
        return {}

    url = "https://users.roblox.com/v1/usernames/users"
    payload = {"usernames": normalized, "excludeBannedUsers": False}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=10) as response:
                if response.status != 200:
                    return {}
                data = await response.json()
    except Exception:
        return {}

    result = {}
    for entry in data.get("data", []):
        user_id = entry.get("id")
        username = entry.get("requestedUsername")
        if user_id and username:
            result[username.strip().lower()] = user_id
    return result


async def get_deposit_servers_status():
    """Return launched counts for MM2 and ADM deposit bot servers."""
    mm2_online, mm2_total = await get_servers_status(MM2_DEPOSIT_SERVERS)
    adm_online, adm_total = await get_servers_status(ADM_DEPOSIT_SERVERS)
    return mm2_online, mm2_total, adm_online, adm_total


async def get_servers_status(servers_list: list) -> Tuple[int, int]:
    """Return the number of successfully launched servers and the configured server total."""
    total = len(servers_list)
    if total == 0:
        return 0, 0

    launched = sum(1 for server in servers_list if server.get("launched", False))
    return launched, total


def _sync_launch_roblox_with_cookie(cookie_value: str, game_id: int = 920587237, timeout: int = 12) -> bool:
    """Synchronous helper that uses selenium to open a game page, inject cookie and press Play.

    Returns True on success, False otherwise. This mirrors the behavior in testld.py but
    is self-contained to avoid requiring an accounts.json file.
    """
    if webdriver is None:
        return False

                              
    try:
        cookie_value = cookie_value.strip()
        if cookie_value.startswith('.ROBLOSECURITY='):
            cookie_value = cookie_value.replace('.ROBLOSECURITY=', '')
        elif '|_' in cookie_value:
            cookie_value = cookie_value.split('|_')[-1]
    except Exception:
        return False

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-popup-blocking")

    game_url = f"https://www.roblox.com/games/{game_id}"

    global _LAUNCHER_DRIVER
    created_here = False
    driver = None

    try:
        with _LAUNCHER_LOCK:
                                                                                                
            if _LAUNCHER_DRIVER:
                try:
                    _ = _LAUNCHER_DRIVER.current_url
                    driver = _LAUNCHER_DRIVER
                    try:
                                                                          
                        driver.switch_to.new_window('tab')
                        handles = driver.window_handles
                        driver.switch_to.window(handles[-1])
                    except Exception:
                        try:
                                                                                   
                            driver.execute_script("window.open('');")
                            handles = driver.window_handles
                            driver.switch_to.window(handles[-1])
                        except Exception:
                            try:
                                                                                
                                driver.execute_cdp_cmd('Target.createTarget', {'url': game_url})
                                time.sleep(0.5)
                                handles = driver.window_handles
                                driver.switch_to.window(handles[-1])
                            except Exception:
                                                                                                                      
                                driver = None
                except Exception:
                    try:
                        _LAUNCHER_DRIVER.quit()
                    except Exception:
                        pass
                    _LAUNCHER_DRIVER = None
                    driver = None

                                           
            if not driver:
                try:
                    from webdriver_manager.chrome import ChromeDriverManager
                    service = Service(ChromeDriverManager().install())
                    driver = webdriver.Chrome(service=service, options=options)
                except Exception:
                    driver = webdriver.Chrome(options=options)
                created_here = True

            try:
                driver.maximize_window()
            except Exception:
                pass

            driver.get(game_url)
            time.sleep(2)

            driver.add_cookie({
                'name': '.ROBLOSECURITY',
                'value': cookie_value,
                'domain': '.roblox.com',
                'path': '/'
            })

            driver.refresh()
            time.sleep(3)

            try:
                driver.maximize_window()
            except Exception:
                pass

            if "login" in driver.current_url:
                if created_here and driver:
                    try:
                        driver.quit()
                    except Exception:
                        pass
                return False

                                            
            wait = WebDriverWait(driver, timeout)
            play_button = None
            selectors = [
                (By.CSS_SELECTOR, "button[class*='play-button']"),
                (By.CSS_SELECTOR, "[data-testid='game-play-button']"),
                (By.XPATH, "//button[contains(text(), 'Play')]"),
                (By.XPATH, "//a[contains(@class, 'play')]")
            ]

            for by, selector in selectors:
                try:
                    play_button = wait.until(EC.element_to_be_clickable((by, selector)))
                    if play_button:
                        break
                except Exception:
                    continue

            if not play_button:
                if created_here and driver:
                    try:
                        driver.quit()
                    except Exception:
                        pass
                return False

            try:
                play_button.click()
                time.sleep(1.5)

                clicked = False
                if pyautogui:
                    try:
                        time.sleep(0.3)
                        pyautogui.press('tab')
                        time.sleep(0.1)
                        pyautogui.press('tab')
                        time.sleep(0.1)
                        pyautogui.press('enter')
                        clicked = True
                    except Exception:
                        clicked = False

                if not clicked and pyautogui:
                    try:
                        pyautogui.hotkey('alt', 'tab')
                        time.sleep(0.2)
                        pyautogui.press('enter')
                    except Exception:
                        pass

                                                        
                time.sleep(10)

                if created_here:
                    try:
                        _LAUNCHER_DRIVER = driver
                    except Exception:
                        pass

                return True

            except Exception:
                if created_here and driver:
                    try:
                        driver.quit()
                    except Exception:
                        pass
                return False

    except Exception:
        if created_here and driver:
            try:
                driver.quit()
            except Exception:
                pass
        return False


def _arrange_and_minimize_roblox_windows(target_exe: Optional[str] = None, width: int = 400, height: int = 400, gap: int = 0):
    """Find top-level windows belonging to the Roblox player executable, resize to
    `width`x`height`, arrange them left-to-right and minimize them.

    This is a best-effort Windows-only helper that uses ctypes to call the
    Win32 APIs. Safe to call from a background thread via `asyncio.to_thread`.
    """
    if sys.platform != "win32":
        return

                                                                                    
    default_path = r"C:\Users\Levi\AppData\Local\Roblox\Versions\version-460909c4fe904aae\RobloxPlayerBeta.exe"
    target_exe = (target_exe or default_path).lower()

    user32 = ctypes.WinDLL('user32', use_last_error=True)
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

    EnumWindows = user32.EnumWindows
    EnumWindows.restype = wintypes.BOOL
                                                                                
    EnumWindowsProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

    GetWindowThreadProcessId = user32.GetWindowThreadProcessId
    GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]

    IsWindowVisible = user32.IsWindowVisible
    IsWindowVisible.argtypes = [wintypes.HWND]
    IsWindowVisible.restype = wintypes.BOOL

    MoveWindow = user32.MoveWindow
    MoveWindow.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, wintypes.BOOL]
    MoveWindow.restype = wintypes.BOOL

    ShowWindow = user32.ShowWindow
    ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]

    OpenProcess = kernel32.OpenProcess
    OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    OpenProcess.restype = wintypes.HANDLE

    QueryFullProcessImageNameW = kernel32.QueryFullProcessImageNameW
    QueryFullProcessImageNameW.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD)]
    QueryFullProcessImageNameW.restype = wintypes.BOOL

    CloseHandle = kernel32.CloseHandle
    CloseHandle.argtypes = [wintypes.HANDLE]
    CloseHandle.restype = wintypes.BOOL

    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    SW_MINIMIZE = 6

    hwnds = []

    def _enum_proc(hwnd, lParam):
        try:
            if not IsWindowVisible(hwnd):
                return True
            pid = wintypes.DWORD()
            GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            if not pid.value:
                return True
            hproc = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid.value)
            if not hproc:
                return True
            buf_len = wintypes.DWORD(260)
            buf = ctypes.create_unicode_buffer(buf_len.value)
            ok = QueryFullProcessImageNameW(hproc, 0, buf, ctypes.byref(buf_len))
            CloseHandle(hproc)
            if not ok:
                return True
            proc_path = buf.value.lower()
            if proc_path.endswith('robloxplayerbeta.exe') or proc_path == target_exe:
                hwnds.append(hwnd)
        except Exception:
            pass
        return True

                                                                    
    try:
        cb = EnumWindowsProc(_enum_proc)
        for _attempt in range(6):
            hwnds.clear()
            EnumWindows(cb, 0)
            if hwnds:
                break
            time.sleep(1)
    except Exception:
        return

                           
    for idx, hwnd in enumerate(hwnds):
        try:
            x = idx * (width + gap)
            y = 0
            MoveWindow(hwnd, x, y, width, height, True)
            ShowWindow(hwnd, SW_MINIMIZE)
        except Exception:
            continue

CRYPTO_CURRENCIES = {
    "Bitcoin": {
        "code": "BTC",
        "emoji": "<:Bitcoin:1528625118904057897>",
        "prefix": "bc1"
    },
    "Litecoin": {
        "code": "LTC",
        "emoji": "<:Litecoin:1528625110242820178>",
        "prefix": "ltc1"
    },
    "Ethereum": {
        "code": "ETH",
        "emoji": "<:Etherium:1528625127510638714>",
        "prefix": "0x"
    },
    "Solana": {
        "code": "SOL",
        "emoji": "<:Solana:1528625144409362572>",
        "prefix": "So"
    },
    "Tether": {
        "code": "USDT",
        "emoji": "<:Tether:1528625135852978248>",
        "prefix": "T"
    }
}


PRICE_CACHE = {
    "prices": {},
    "last_update": 0,
    "cache_duration": 300 
}
 


JACKPOT_CHANNEL_ID = DM @kem.dev for help!
JACKPOT_FILE = "active_jackpot_games.json"


MM2_WEBHOOK_USERNAME = "MM2 Autotrade" 
MM2_TRADE_MONITOR_CHANNEL_ID = DM @kem.dev for help! 
ADM_WEBHOOK_USERNAME = "AutoTrade"
ADM_TRADE_MONITOR_CHANNEL_ID = DM @kem.dev for help!


MIN_BET_VALUE = 0
MAX_BET_VALUE = 1000000
VERIFICATION_PREFIX = "Bloxloot"
HOUSE_TAX = 0.05 
WILD_MODE_CHANCE = 0.01


MINES_BOARD_SIZE = 5 
MINES_MIN_COUNT = 1  
MINES_MAX_COUNT = 10  
MINES_WILD_EXTRA_MINES = 1  
MINES_CELL_LABELS = [
    "1", "2", "3", "4", "5", 
    "6", "7", "8", "9", "10",
    "11", "12", "13", "14", "15", 
    "16", "17", "18", "19", "20",
    "21", "22", "23", "24", "25"
]


TOWERS_WIDTH = 3  
TOWERS_HEIGHT = 5  
TOWERS_TOTAL_CELLS = TOWERS_WIDTH * TOWERS_HEIGHT 
TOWERS_BOMB_COUNT = 5  
TOWERS_CELL_LABELS = [str(i) for i in range(1, TOWERS_TOTAL_CELLS + 1)]  


collections = {
    "1": {
        "name": "Xmas Juicer",
        "description": "",
        "emoji": "<:MM2Flip:1528625101644365998>",
        "Value": [
            {"id": 1, "name": "Chroma Evergun", "value": 56000, "emoji": "<:Evergun:1528631942923161730>", "chance": 0.5},
            {"id": 2, "name": "Chroma Bauble", "value": 15750, "emoji": "<:ChromaBauble:1528632287116136458>", "chance": 0.5},
            {"id": 3, "name": "Evergun", "value": 2850, "emoji": "<:Evergun:1528631942923161730>", "chance": 2.5},
            {"id": 4, "name": "Bauble", "value": 525, "emoji": "<:Bauble:1528631872114917456>", "chance": 4},
            {"id": 5, "name": "Icepiercer", "value": 375, "emoji": "<:Icepeircer:1528632066751594526>", "chance": 12.5},
            {"id": 6, "name": "Candy", "value": 195, "emoji": "<:Candy:1528632763173965996>", "chance": 30},
            {"id": 7, "name": "Suger", "value": 80, "emoji": "<:Sugar:1528632877632454788>", "chance": 50}
        ]
    },
    "2": {
        "name": "Frozen Fantasy",
        "description": "",
        "emoji": "<:MM2Flip:1528625101644365998>",
        "Value": [
            {"id": 1, "name": "Chroma Evergun", "value": 56000, "emoji": "<:Evergun:1528631942923161730>", "chance": 0.5},
            {"id": 2, "name": "Chroma Bauble", "value": 15750, "emoji": "<:ChromaBauble:1528632287116136458>", "chance": 0.5},
            {"id": 3, "name": "Evergun", "value": 2850, "emoji": "<:Evergun:1528631942923161730>", "chance": 2.5},
            {"id": 4, "name": "Bauble", "value": 525, "emoji": "<:Bauble:1528631872114917456>", "chance": 4},
            {"id": 5, "name": "Icepiercer", "value": 375, "emoji": "<:Icepeircer:1528632066751594526>", "chance": 12.5},
            {"id": 6, "name": "Candy", "value": 195, "emoji": "<:Candy:1528632763173965996>", "chance": 30},
            {"id": 7, "name": "Suger", "value": 80, "emoji": "<:Sugar:1528632877632454788>", "chance": 50}
        ]
    },
    "3": {
        "name": "Vampires Vault",
        "description": "",
        "emoji": "<:MM2Flip:1528625101644365998>",
        "Value": [
            {"id": 1, "name": "Chroma Evergun", "value": 56000, "emoji": "<:Evergun:1528631942923161730>", "chance": 0.5},
            {"id": 2, "name": "Chroma Bauble", "value": 15750, "emoji": "<:ChromaBauble:1528632287116136458>", "chance": 0.5},
            {"id": 3, "name": "Evergun", "value": 2850, "emoji": "<:Evergun:1528631942923161730>", "chance": 2.5},
            {"id": 4, "name": "Bauble", "value": 525, "emoji": "<:Bauble:1528631872114917456>", "chance": 4},
            {"id": 5, "name": "Icepiercer", "value": 375, "emoji": "<:Icepeircer:1528632066751594526>", "chance": 12.5},
            {"id": 6, "name": "Candy", "value": 195, "emoji": "<:Candy:1528632763173965996>", "chance": 30},
            {"id": 7, "name": "Suger", "value": 80, "emoji": "<:Sugar:1528632877632454788>", "chance": 50}
        ]
    },
    "4": {
        "name": "Chroma Chaos",
        "description": "",
        "emoji": "<:MM2Flip:1528625101644365998>",
        "Value": [
            {"id": 1, "name": "Chroma Evergun", "value": 56000, "emoji": "<:Evergun:1528631942923161730>", "chance": 0.5},
            {"id": 2, "name": "Chroma Bauble", "value": 15750, "emoji": "<:ChromaBauble:1528632287116136458>", "chance": 0.5},
            {"id": 3, "name": "Evergun", "value": 2850, "emoji": "<:Evergun:1528631942923161730>", "chance": 2.5},
            {"id": 4, "name": "Bauble", "value": 525, "emoji": "<:Bauble:1528631872114917456>", "chance": 4},
            {"id": 5, "name": "Icepiercer", "value": 375, "emoji": "<:Icepeircer:1528632066751594526>", "chance": 12.5},
            {"id": 6, "name": "Candy", "value": 195, "emoji": "<:Candy:1528632763173965996>", "chance": 30},
            {"id": 7, "name": "Suger", "value": 80, "emoji": "<:Sugar:1528632877632454788>", "chance": 50}
        ]
    },
    "5": {
        "name": "50/50 Harvester",
        "description": "",
        "emoji": "<:MM2Flip:1528625101644365998>",
        "Value": [
            {"id": 1, "name": "Chroma Evergun", "value": 56000, "emoji": "<:Evergun:1528631942923161730>", "chance": 0.5},
            {"id": 2, "name": "Chroma Bauble", "value": 15750, "emoji": "<:ChromaBauble:1528632287116136458>", "chance": 0.5},
            {"id": 3, "name": "Evergun", "value": 2850, "emoji": "<:Evergun:1528631942923161730>", "chance": 2.5},
            {"id": 4, "name": "Bauble", "value": 525, "emoji": "<:Bauble:1528631872114917456>", "chance": 4},
            {"id": 5, "name": "Icepiercer", "value": 375, "emoji": "<:Icepeircer:1528632066751594526>", "chance": 12.5},
            {"id": 6, "name": "Candy", "value": 195, "emoji": "<:Candy:1528632763173965996>", "chance": 30},
            {"id": 7, "name": "Suger", "value": 80, "emoji": "<:Sugar:1528632877632454788>", "chance": 50}
        ]
    },
    "6": {
        "name": "Candy Frenzy ",
        "description": "",
        "emoji": "<:MM2Flip:1528625101644365998>",
        "Value": [
            {"id": 1, "name": "Chroma Evergun", "value": 56000, "emoji": "<:Evergun:1528631942923161730>", "chance": 0.5},
            {"id": 2, "name": "Chroma Bauble", "value": 15750, "emoji": "<:ChromaBauble:1528632287116136458>", "chance": 0.5},
            {"id": 3, "name": "Evergun", "value": 2850, "emoji": "<:Evergun:1528631942923161730>", "chance": 2.5},
            {"id": 4, "name": "Bauble", "value": 525, "emoji": "<:Bauble:1528631872114917456>", "chance": 4},
            {"id": 5, "name": "Icepiercer", "value": 375, "emoji": "<:Icepeircer:1528632066751594526>", "chance": 12.5},
            {"id": 6, "name": "Candy", "value": 195, "emoji": "<:Candy:1528632763173965996>", "chance": 30},
            {"id": 7, "name": "Suger", "value": 80, "emoji": "<:Sugar:1528632877632454788>", "chance": 50}
        ]
    },
}


CASE_SECTIONS = collections


active_case_battles = {}


BLACKJACK_CARD_EMOJIS = {

    'A♥': '<:a_heart:1528625494084292711>',
    '2♥': '<:2_heart:1528625170493866124>',
    '3♥': '<:3_heart:1528625213535944804>',
    '4♥': '<:4_heart:1528625248877150378>',
    '5♥': '<:5_heart:1528625283563782215>',
    '6♥': '<:6_heart:1528625318724632648>',
    '7♥': '<:7_heart:1528625354363768943>',
    '8♥': '<:8_heart:1528625389390270555>',
    '9♥': '<:9_heart:1528625424480079943>',
    '10♥': '<:10_heart:1528625459284279417>',
    'J♥': '<:j_heart:1528625528612065301>',
    'Q♥': '<:q_heart:1528625597616492684>',
    'K♥': '<:k_heart:1528625562837450854>',
    

    'A♦': '<:a_diamond:1528625485171396658>',
    '2♦': '<:2_diamond:1528625161434304675>',
    '3♦': '<:3_diamond:1528625204807602278>',
    '4♦': '<:4_diamond:1528625239662264490>',
    '5♦': '<:5_diamond:1528625274885898382>',
    '6♦': '<:6_diamond:1528625310310863001>',
    '7♦': '<:7_diamond:1528625345643941939>',
    '8♦': '<:8_diamond:1528625380188225588>',
    '9♦': '<:9_diamond:1528625415667712160>',
    '10♦':'<:10_diamond:1528625450560258101>',
    'J♦': '<:j_diamond:1528625520110207018>',
    'Q♦': '<:q_diamond:1528625588514984047>',
    'K♦': '<:k_diamond:1528625554222219316>',
    

    'A♣': '<:a_club:1528625477030510692>',
    '2♣': '<:2_club:1528625152957354064>',
    '3♣': '<:3_club:1528625188856529080>',
    '4♣': '<:4_club:1528625230795378780>',
    '5♣': '<:5_club:1528625266308546662>',
    '6♣': '<:6_club:1528625301414740085>',
    '7♣': '<:7_club:1528625336307290195>',
    '8♣': '<:8_club:1528625371845623828>',
    '9♣': '<:9_club:1528625406016753777>',
    '10♣': '<:10_club:1528625442159071322>',
    'J♣': '<:j_club:1528625511645974528>',
    'Q♣': '<:q_club:1528625579950346292>',
    'K♣': '<:k_club:1528625545695199262>',
    

    'A♠': '<:a_spade:1528625503513346058>',
    '2♠': '<:2_spade:1528625180254142575>',
    '3♠': '<:3_spade:1528625222129946736>',
    '4♠': '<:4_spade:1528625258100424804>',
    '5♠': '<:5_spade:1528625292128686133>',
    '6♠': '<:6_spade:1528625327486799962>',
    '7♠': '<:7_spade:1528625362542530733>',
    '8♠': '<:8_spade:1528625397535870999>',
    '9♠': '<:9_spade:1528625433372000346>',
    '10♠': '<:10_spade:1528625468381728851>',
    'J♠': '<:j_spade:1528625537201733763>',
    'Q♠': '<:q_spade:1528625606265409577>',
    'K♠': '<:k_spade:1528625571523858554>',
    

    'BACK': '<:back:1528625616172089434>',
}


BLACKJACK_MIN_BET = 0
BLACKJACK_MAX_BET = 1000000


class GameType:
    MM2 = "MM2"
    ADM = "ADM"



def get_item_type(item_name: str) -> Optional[str]:
    """Get the type of an item (MM2, etc.)"""
    items = load_items()
    item_data = items.get(item_name, {})
    if isinstance(item_data, dict):
        return item_data.get('type')
    return None

def validate_items_same_type(items: List[str]) -> Tuple[bool, Optional[str], str]:
    """
    Validate that all items are of the same game type.
    Returns: (is_valid, game_type, error_message)
    """
    if not items:
        return False, None, "No items provided"
    
    first_item = items[0]
    first_type = get_item_type(first_item)
    
    if not first_type:
        return False, None, f"Item '{first_item}' has no type defined"
    
    for item in items[1:]:
        item_type = get_item_type(item)
        if not item_type:
            return False, None, f"Item '{item}' has no type defined"
        if item_type != first_type:
            return False, None, (
                f"Cannot mix different game types!\n"
                f"All items in a game must be from the same game."
            )
    
    return True, first_type, ""

                                        

class RPSGame:
    def __init__(self, creator_id: int, creator_items: List[str], bet_value: int, creator_choice: str = None):
        self.creator_id = creator_id
        self.creator_items = creator_items
        self.bet_value = bet_value
        self.creator_choice = creator_choice                         
        self.wild_mode = False
        self.opponent_id = None
        self.opponent_items = []
        self.opponent_choice = None
        self.status = "waiting"                                         
        self.game_id = f"rps_{creator_id}_{int(datetime.now().timestamp())}"
        self.created_at = datetime.now().isoformat()
        self.message_id = None
        
                                   
        self.creator_value = sum(get_item_value(item) for item in creator_items)
    
    def determine_winner(self, choice1: str, choice2: str) -> str:
        """Determine winner between two choices. Returns 'creator', 'opponent', or 'tie'"""
        if choice1 == choice2:
            return "tie"
        
        winning_rules = {
            "rock": "scissors",
            "paper": "rock",
            "scissors": "paper"
        }
        
        if winning_rules[choice1] == choice2:
            return "creator"
        else:
            return "opponent"
    
    def to_dict(self):
        return {
            "game_id": self.game_id,
            "creator_id": self.creator_id,
            "creator_items": self.creator_items,
            "creator_choice": self.creator_choice,
            "creator_value": self.creator_value,
            "wild_mode": self.wild_mode,
            "opponent_id": self.opponent_id,
            "opponent_items": self.opponent_items,
            "opponent_choice": self.opponent_choice,
            "status": self.status,
            "created_at": self.created_at,
            "message_id": self.message_id
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        game = cls(data["creator_id"], data["creator_items"], data["bet_value"], data.get("creator_choice"))
        game.game_id = data["game_id"]
        game.opponent_id = data.get("opponent_id")
        game.opponent_items = data.get("opponent_items", [])
        game.opponent_choice = data.get("opponent_choice")
        game.status = data.get("status", "waiting")
        game.created_at = data.get("created_at")
        game.creator_value = data.get("creator_value", 0)
        game.message_id = data.get("message_id")
        game.wild_mode = data.get("wild_mode", False)
        return game

def validate_inventory_items_same_type(user_id: str, items: List[str]) -> Tuple[bool, Optional[str], str]:
    """
    Validate that all selected items exist in user's inventory and are same type.
    """
                                   
    user_inventory = get_user_inventory(user_id)
    user_item_names = [item.get('name') for item in user_inventory]
    
    missing_items = []
    for item in items:
        if item not in user_item_names:
            missing_items.append(item)
    
    if missing_items:
        return False, None, f"You don't have these items: {', '.join(missing_items)}"
    
                            
    return validate_items_same_type(items)

                                             
async def log_taxed_items(source_game: str, winner_id: int, loser_id: int, tax_amount: int, items: List[str], pot_value: int):
    """Log taxed items to the tax log channel"""
    try:
        channel = bot.get_channel(TAX_LOG_CHANNEL_ID)
        if not channel:
            print(f"Tax log channel {TAX_LOG_CHANNEL_ID} not found!")
            return
        
                                 
        item_counts = {}
        total_items = 0
        for item in items:
            item_counts[item] = item_counts.get(item, 0) + 1
            total_items += 1
        
                           
        items_text = ""
        for item_name, count in list(item_counts.items())[:15]:
            item_value = get_item_value(item_name)
            item_emoji = get_item_emoji(item_name)
            display_value = format_item_value(item_value * count)
            items_text += f"{item_emoji} **{item_name}** x{count} - {VALUE_EMOJI} **{display_value}**\n"
        
        if len(item_counts) > 15:
            items_text += f"\n*...and {len(item_counts)-15} more item types*"
        
                                                       
        try:
            winner_user = await bot.fetch_user(winner_id)
        except discord.NotFound:
            winner_user = None
            print(f"Warning: Winner user {winner_id} not found in Discord")
        except Exception as e:
            winner_user = None
            print(f"Error fetching winner {winner_id}: {e}")
        
        try:
            loser_user = await bot.fetch_user(loser_id)
        except discord.NotFound:
            loser_user = None
            print(f"Warning: Loser user {loser_id} not found in Discord")
        except Exception as e:
            loser_user = None
            print(f"Error fetching loser {loser_id}: {e}")
        
                                                             
        if loser_id == 0:
            loser_user = None
        
        registrations = load_registrations()
        winner_reg = registrations.get(str(winner_id), {})
        loser_reg = registrations.get(str(loser_id), {})
        
                              
        embed = discord.Embed(
            title=f"TAX LOGGED - {source_game}",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        
        tax_rate = get_house_tax()
        embed.add_field(
            name="Game Details",
            value=f"**Source:** {source_game}\n**Pot Value:** {VALUE_EMOJI} **{format_value_with_commas(pot_value)}**\n**Tax Amount ({tax_rate * 100:.1f}%):** {VALUE_EMOJI} **{format_value_with_commas(tax_amount)}**",
            inline=False
        )
        
                               
        winner_display = "Unknown User"
        if winner_user:
            winner_display = winner_user.mention
        elif winner_id != 0:
            winner_display = f"Unknown User ({winner_id})"
        
        embed.add_field(
            name="Winner",
            value=f"{winner_display}\nRoblox: **{winner_reg.get('roblox_username', 'Unknown')}**",
            inline=True
        )
        
                              
        loser_display = "Unknown User"
        if loser_user:
            loser_display = loser_user.mention
        elif loser_id == 0:
            loser_display = "Jackpot System"
        elif loser_id != 0:
            loser_display = f"Unknown User ({loser_id})"
        
        embed.add_field(
            name="Loser",
            value=f"{loser_display}\nRoblox: **{loser_reg.get('roblox_username', 'Unknown')}**",
            inline=True
        )
        
        embed.add_field(
            name="Total Items",
            value=f"**{total_items}** items",
            inline=True
        )
        
        embed.add_field(
            name="Items Taxed",
            value=items_text or "No items",
            inline=False
        )
        
        embed.set_footer(text=f"Tax ID: {int(datetime.now().timestamp())}")
        
        await channel.send(embed=embed)
        
                          
        log_taxed_item_to_file(source_game, winner_id, loser_id, tax_amount, items, pot_value)
        
    except Exception as e:
        print(f"Error logging taxed items: {e}")

def log_taxed_item_to_file(source_game: str, winner_id: int, loser_id: int, tax_amount: int, items: List[str], pot_value: int):
    """Log taxed items to JSON file"""
    taxed_items = load_taxed_items()
    
    entry = {
        "source_game": source_game,
        "winner_id": winner_id,
        "loser_id": loser_id,
        "tax_amount": tax_amount,
        "items": items,
        "pot_value": pot_value,
        "timestamp": datetime.now().isoformat()
    }
    
    if isinstance(taxed_items, list):
        taxed_items.append(entry)
    else:
        taxed_items = [entry]
    
    save_json(TAX_ITEMS_FILE, taxed_items)

def calculate_tax(total_pot: int) -> float:
    """Calculate current tax on the total pot"""
    return total_pot * get_house_tax()

def calculate_net_winnings(total_pot: int) -> float:
    """Calculate net winnings after current tax"""
    tax = calculate_tax(total_pot)
    return total_pot - tax

def deduct_tax_from_items(items: List[str], tax_amount: int) -> Tuple[List[str], List[str]]:
    """
    Deduct tax amount from a list of items by taking items that are <= tax amount.
    If each player only has 1 item, no tax is taken.
    Returns (remaining_items, taxed_items)
    """
    if tax_amount <= 0:
        return items, []
    
                                                    
    item_list = []
    for item in items:
        item_value = get_item_value(item)
        if item_value > 0:                                 
            item_list.append((item, item_value))
    
    if not item_list:
        return items, []
    
                                          
                                    
    unique_items = {}
    for item in items:
        unique_items[item] = unique_items.get(item, 0) + 1
    
                                                                                     
    if len(items) == 2 and len(unique_items) == 2:
        return items, []
    
                                                                   
    item_list.sort(key=lambda x: x[1])
    
    remaining_items = list(items)                        
    taxed_items = []
    remaining_tax = tax_amount
    
                                                                    
                                                                           
                                                    
    
                                                                       
    eligible_items = [(item, value) for item, value in item_list if value <= remaining_tax]
    
    if eligible_items:
                                                                       
        temp_items = sorted(eligible_items, key=lambda x: x[1])                  
        selected_for_tax = []
        selected_value = 0
        
        for item, value in temp_items:
            if selected_value + value <= remaining_tax:
                selected_for_tax.append(item)
                selected_value += value
        
                                                                                            
        if selected_value >= remaining_tax * 0.5 or abs(selected_value - remaining_tax) <= remaining_tax * 0.1:
                                   
            for tax_item in selected_for_tax:
                if tax_item in remaining_items:
                    remaining_items.remove(tax_item)
                    taxed_items.append(tax_item)
            return remaining_items, taxed_items
    
                                                                                          
    eligible_items.sort(key=lambda x: x[1])                 
    
    for item, value in eligible_items:
                                                                     
        if abs(value - remaining_tax) <= remaining_tax * 0.1:
            remaining_items.remove(item)
            taxed_items.append(item)
            return remaining_items, taxed_items
    
                                                                           
    if eligible_items:
        largest_eligible = max(eligible_items, key=lambda x: x[1])
        if largest_eligible[1] <= remaining_tax:
            remaining_items.remove(largest_eligible[0])
            taxed_items.append(largest_eligible[0])
            return remaining_items, taxed_items
    
                                                                                  
                                                                  
    return items, []

                                       
def resolve_data_path(file_path: str) -> str:
    """Resolve a relative data file path against the bot script directory."""
    if os.path.isabs(file_path):
        return file_path
    return os.path.join(BASE_DIR, file_path)


def load_json(file_path: str, default=None):
    """Load JSON file, return default if file doesn't exist"""
    if default is None:
        default = {}
    file_path = resolve_data_path(file_path)
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return default
    return default


def save_json(file_path: str, data):
    """Save data to JSON file"""
    file_path = resolve_data_path(file_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def load_updates() -> List[Dict]:
    """Load stored update records from disk."""
    updates = load_json(UPDATES_FILE, [])
    if isinstance(updates, list):
        return [item for item in updates if isinstance(item, dict)]
    return []


def save_updates(updates: List[Dict]):
    """Save stored update records to disk."""
    save_json(UPDATES_FILE, updates)


def get_next_update_code() -> str:
    """Generate the next update code."""
    updates = load_updates()
    existing_codes = [item.get("code") for item in updates if isinstance(item.get("code"), str)]
    numbers = []
    for code in existing_codes:
        match = re.search(r"(\d+)$", code)
        if match:
            numbers.append(int(match.group(1)))
    next_number = max(numbers, default=0) + 1
    return f"UPD-{next_number:03d}"


def load_processed_trades() -> List[Dict]:
    """Load the processed trades record."""
    records = load_json(PROCESSED_TRADES_FILE, [])
    if isinstance(records, list):
        return [rec for rec in records if isinstance(rec, dict)]
    return []

def save_processed_trades(data: List[Dict]):
    """Save the processed trades record."""
    save_json(PROCESSED_TRADES_FILE, data)


def normalize_bot_username(bot_username: str) -> Optional[str]:
    """Normalize bot username strings from webhook footers."""
    if not bot_username:
        return None
    clean = re.sub(r'[*_`~]', '', bot_username).strip()
    lower = clean.lower()
    for prefix in ['bot user:', 'bot:', 'user:']:
        if lower.startswith(prefix):
            clean = clean[len(prefix):].strip()
            break
    return clean or None


def get_bot_holding_value(bot_username: str, game_type: str) -> float:
    """Return the total processed trade value for a bot and game type."""
    normalized_bot = normalize_bot_username(bot_username)
    if not normalized_bot:
        return 0.0
    total = 0.0
    for rec in load_processed_trades():
        if rec.get("game_type") == game_type and rec.get("bot_username"):
            try:
                if normalize_bot_username(rec["bot_username"]) == normalized_bot:
                    total += float(rec.get("total_value", 0) or 0)
            except Exception:
                continue
    return total


def match_deposit_server_username(footer_text: str, game_type: str) -> Optional[str]:
    """Match a webhook footer username to a configured deposit server username."""
    normalized = normalize_bot_username(footer_text)
    if not normalized:
        return None
    servers = MM2_DEPOSIT_SERVERS if game_type == GameType.MM2 else ADM_DEPOSIT_SERVERS
    norm_lower = normalized.lower()
    for server in servers:
        for key in ("roblox_username", "name"):
            candidate = server.get(key)
            if not candidate:
                continue
            cand_lower = candidate.strip().lower()
            if cand_lower == norm_lower or cand_lower in norm_lower or norm_lower in cand_lower:
                return server.get("roblox_username") or candidate
    return normalized

DAILY_CLAIMS_FILE = "daily_claims.json"

def load_daily_claims() -> dict:
    return load_json(DAILY_CLAIMS_FILE, {})

def save_daily_claims(data: dict):
    save_json(DAILY_CLAIMS_FILE, data)

def can_claim_daily(user_id: int) -> bool:
    claims = load_daily_claims()
    entry = claims.get(str(user_id), {})
    last = entry.get("last_daily")
    if last:
        try:
            last_dt = datetime.fromisoformat(last)
            return datetime.now() - last_dt >= timedelta(hours=24)
        except Exception:
            return True
    return True

def record_daily_claim(user_id: int):
    claims = load_daily_claims()
    entry = claims.setdefault(str(user_id), {})
    entry["last_daily"] = datetime.now().isoformat()
    save_daily_claims(claims)

def load_items() -> Dict:
    """Load items from items.json"""
    return load_json(ITEMS_FILE, {})

def load_inventories() -> Dict:
    """Load user inventories from inventory.json"""
    return load_json(INVENTORY_FILE, {})

def load_registrations() -> Dict:
    """Load user registrations"""
    return load_json(REGISTRATIONS_FILE, {})


def load_stock() -> List[Dict]:
    """Load stock items from stock.json."""
    stock_data = load_json(STOCK_FILE, [])
    if not isinstance(stock_data, list):
        return []
    cleaned = []
    for entry in stock_data:
        if not isinstance(entry, dict):
            continue
        name = entry.get("name")
        quantity = entry.get("quantity", 0)
        if not name:
            continue
        try:
            quantity = int(quantity)
        except Exception:
            continue
        if quantity <= 0:
            continue
        cleaned.append({"name": name, "quantity": quantity})
    return cleaned


def save_stock(data: List[Dict]):
    """Save stock items to stock.json."""
    save_json(STOCK_FILE, data)


def load_tag_reward_state() -> Dict:
    """Load the current tag reward state from disk."""
    return load_json(TAG_REWARD_STATE_FILE, {"users": {}})


def save_tag_reward_state(data: Dict):
    """Save the current tag reward state to disk."""
    save_json(TAG_REWARD_STATE_FILE, data)


def load_invite_reward_state() -> Dict:
    """Load the current invite reward state from disk."""
    return load_json(INVITE_REWARD_STATE_FILE, {"users": {}})


def save_invite_reward_state(data: Dict):
    """Save the current invite reward state to disk."""
    save_json(INVITE_REWARD_STATE_FILE, data)


def select_random_stock_item() -> Optional[Dict]:
    """Select a random stock item from available stock."""
    stock_items = load_stock()
    if not stock_items:
        return None
    return random.choice(stock_items)


def add_stock_item(item_name: str, quantity: int):
    stock_items = load_stock()
    item_name = item_name.strip()
    if not item_name or quantity <= 0:
        return
    for entry in stock_items:
        if entry["name"].strip().lower() == item_name.lower():
            entry["quantity"] += quantity
            entry["name"] = item_name
            save_stock(stock_items)
            return
    stock_items.append({"name": item_name, "quantity": quantity})
    save_stock(stock_items)


def remove_stock_item(item_name: str, quantity: int) -> bool:
    stock_items = load_stock()
    item_name = item_name.strip()
    if not item_name or quantity <= 0:
        return False
    for entry in stock_items:
        if entry["name"].strip().lower() == item_name.lower():
            current = entry["quantity"]
            if quantity >= current:
                stock_items.remove(entry)
            else:
                entry["quantity"] = current - quantity
            save_stock(stock_items)
            return True
    return False

def build_stock_summary() -> str:
    stock_items = load_stock()
    items = load_items()
    mm2_total_value = 0
    adm_total_value = 0
    for entry in stock_items:
        name = entry["name"]
        quantity = entry["quantity"]
        item_data = items.get(name, {})
        if isinstance(item_data, dict):
            value = item_data.get("value", 0) or 0
            item_type = item_data.get("type", GameType.MM2)
        else:
            value = 0
            item_type = GameType.MM2
        if item_type == GameType.ADM:
            adm_total_value += value * quantity
        else:
            mm2_total_value += value * quantity

    return (
        f"**MM2 -** {VALUE_EMOJI} **{format_value_with_commas(mm2_total_value)}**\n"
        f"**ADM -** {VALUE_EMOJI} **{format_value_with_commas(adm_total_value)}**"
    )


def build_stock_embed_embed(mode: str = GameType.MM2):
    stock_items = load_stock()
    base_description = "Use the buttons below to add or remove items from stock."
    embed = discord.Embed(
        title="Bloxloot Stock Panel",
        description=base_description,
        color=discord.Color.green()
    )

    if not stock_items:
        embed.description = f"{base_description}\n\nNo items currently in stock."
        embed.set_footer(text=f"Bloxloot Team members only! • Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return embed

    filtered_items = []
    if mode == GameType.ADM:
        filtered_items = [entry for entry in stock_items if get_item_type(entry["name"]) == GameType.ADM]
        section_title = "ADM Stock Items"
    else:
        filtered_items = [entry for entry in stock_items if get_item_type(entry["name"]) != GameType.ADM]
        section_title = "MM2 Stock Items"

    if not filtered_items:
        embed.description = f"{base_description}\n\nNo {mode} items currently in stock."
    else:
        lines = []
        for entry in filtered_items[:20]:
            name = entry["name"]
            quantity = entry["quantity"]
            value = get_item_value(name)
            display_value = format_item_value(value * quantity)
            lines.append(f"{get_item_emoji(name)} `{name}` x{quantity} - {VALUE_EMOJI} **{display_value}**")
        if len(filtered_items) > 20:
            lines.append(f"...+{len(filtered_items) - 20} more")
        embed.clear_fields()
        embed.add_field(
            name=section_title,
            value="\n".join(lines),
            inline=False
        )

    embed.set_footer(text=f"Bloxloot Team members only! • Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return embed


def build_stock_embed(mode: str = GameType.MM2):
    return build_stock_embed_embed(mode), StockActionView(mode)


def find_user_id_by_roblox(username: str):
    """Return the discord user id (int) for a given roblox username, or None."""
    regs = load_registrations()
    for uid, data in regs.items():
        if data.get('roblox_username', '').lower() == username.lower():
            try:
                return int(uid)
            except:
                return None
    return None


class AddItemModal(discord.ui.Modal, title="Add Items to User"):
    roblox_username = discord.ui.TextInput(label="Roblox Username", style=discord.TextStyle.short)
    item_name = discord.ui.TextInput(label="Item Name", style=discord.TextStyle.short)
    quantity = discord.ui.TextInput(label="Quantity", style=discord.TextStyle.short, default="1")

    async def on_submit(self, interaction: discord.Interaction):
                                
        allowed, uses, limit = increment_staff_use(interaction.user.id)
        if not allowed:
            await interaction.response.send_message(f"Staff action limit reached ({uses}/{limit}) — try again later.", ephemeral=True)
            return
        username = self.roblox_username.value.strip()
        item = self.item_name.value.strip()
        try:
            qty = max(1, int(self.quantity.value.strip()))
        except:
            qty = 1

        user_id = find_user_id_by_roblox(username)
        if not user_id:
            await interaction.response.send_message(f"No registered user found for Roblox username: {username}", ephemeral=True)
            return

        add_items_to_inventory(str(user_id), [item] * qty)
        await interaction.response.send_message(f"Added {qty} x {item} to <@{user_id}>'s inventory.", ephemeral=True)


class RemoveUserModal(discord.ui.Modal, title="Select User To Remove Items From"):
    roblox_username = discord.ui.TextInput(label="Roblox Username", style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        username = self.roblox_username.value.strip()
        user_id = find_user_id_by_roblox(username)
        if not user_id:
            await interaction.response.send_message(f"No registered user found for Roblox username: {username}", ephemeral=True)
            return

                               
        inventories = load_inventories()
        inv = inventories.get(str(user_id), [])
        if not inv:
            await interaction.response.send_message(f"User <@{user_id}> has no items in inventory.", ephemeral=True)
            return

                                                                                   
        view = RemoveSelectView(str(user_id), inv)
        embed = discord.Embed(title=f"Remove Items from {username}", description="Select items to remove from the dropdown below.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class RemoveSelectView(discord.ui.View):
    def __init__(self, user_id: str, inventory: List[Dict]):
        super().__init__(timeout=None)
        self.user_id = user_id
        options: List[discord.SelectOption] = []
                                                                         
        for idx, entry in enumerate(inventory):
            item_name = entry.get('name')
            item_emoji = get_item_emoji(item_name) or "📦"
            label = item_name[:25]
                                                          
            item_value = get_item_value(item_name)
            description = f"{format_item_value(item_value)}"
                                                           
            option_value = f"{item_name}:{idx}"
            options.append(discord.SelectOption(label=label, description=description[:100], value=option_value, emoji=item_emoji))
            if len(options) >= 25:
                break
        self.add_item(RemoveSelect(options))


class RemoveSelect(discord.ui.Select):
    def __init__(self, options: List[discord.SelectOption]):
        super().__init__(placeholder="Select items to remove...", min_values=1, max_values=min(25, len(options)), options=options)

    async def callback(self, interaction: discord.Interaction):
                                                                                                
        selected_values = self.values
        selected_names = [val.split(":", 1)[0] for val in selected_values]

        parent_view = self.view
        if not parent_view or not hasattr(parent_view, 'user_id'):
            await interaction.response.send_message("Unable to determine target user.", ephemeral=True)
            return
        target_user = parent_view.user_id

                                
        allowed, uses, limit = increment_staff_use(interaction.user.id)
        if not allowed:
            await interaction.response.send_message(f"Staff action limit reached ({uses}/{limit}) — try again later.", ephemeral=True)
            return

                                                                                       
        removed = remove_items_from_inventory(target_user, selected_names)
        await interaction.response.send_message(f"Removed {len(selected_names)} selected item(s) from <@{target_user}>.", ephemeral=True)


def add_user_wager(user_id: int, game_type: str, amount: int):
    """Increment a user's total wagered amount for a given game type in registrations.

    Creates a registration entry if missing. Amount should be an int (value).
    """
    try:
        regs = load_registrations()
        key = str(user_id)
        entry = regs.get(key, {})

        tw = entry.get('total_wagered', {}) or {}
        prev = int(tw.get(game_type, 0))
        tw[game_type] = prev + int(amount)
        entry['total_wagered'] = tw

        history = entry.get('wager_history', []) or []
        if not isinstance(history, list):
            history = []
        history.append({
            'game_type': game_type,
            'amount': int(amount),
            'timestamp': datetime.now().isoformat()
        })
        entry['wager_history'] = history

        regs[key] = entry
        save_json(REGISTRATIONS_FILE, regs)
        try:
            if "bot" in globals() and getattr(globals().get("bot"), "is_ready", lambda: False)():
                if get_active_race_channels_in_window():
                    bot.loop.create_task(refresh_active_race_channel_embeds())
        except Exception:
            pass
    except Exception as e:
        print(f"Error adding user wager for {user_id}: {e}")

def load_games() -> Dict:
    """Load active coinflip games"""
    return load_json(GAMES_FILE, {})

def save_games(data: dict):
    """Save active coinflip games"""
    save_json(GAMES_FILE, data)

def load_mines_games() -> Dict:
    """Load active mines games"""
    return load_json(MINES_GAMES_FILE, {})

def save_mines_games(data: dict):
    """Save active mines games"""
    save_json(MINES_GAMES_FILE, data)

def load_towers_games() -> Dict:
    """Load active towers games"""
    return load_json(TOWERS_GAMES_FILE, {})

def save_towers_games(data: dict):
    """Save active towers games"""
    save_json(TOWERS_GAMES_FILE, data)

def load_blackjack_games() -> Dict:
    """Load active blackjack games"""
    return load_json(BLACKJACK_GAMES_FILE, {})

def save_blackjack_games(data: dict):
    """Save active blackjack games"""
    save_json(BLACKJACK_GAMES_FILE, data)

def load_listings() -> Dict:
    """Load active listings"""
    return load_json(LISTINGS_FILE, {})

def save_listings(data: dict):
    """Save active listings"""
    save_json(LISTINGS_FILE, data)

def load_jackpot_games() -> Dict:
    """Load active jackpot games"""
    return load_json(JACKPOT_FILE, {})

def save_jackpot_games(data: dict):
    """Save active jackpot games"""
    save_json(JACKPOT_FILE, data)

def load_withdrawals() -> Dict:
    """Load active withdrawals"""
    return load_json(WITHDRAWALS_FILE, {})

def save_withdrawals(data: dict):
    """Save active withdrawals"""
    save_json(WITHDRAWALS_FILE, data)

def load_balances() -> Dict:
    """Load USD balances for users"""
    return load_json(BALANCES_FILE, {})

def save_balances(data: dict):
    """Save USD balances for users"""
    save_json(BALANCES_FILE, data)

def get_user_balance(user_id: str) -> float:
    balances = load_balances()
    return float(balances.get(user_id, 0.0))


def get_total_wagered(game_type: str) -> int:
    """Prefer authoritative totals stored in registrations; fall back to scanning active games."""
                                                                             
    try:
        completed = load_completed_games()
        if isinstance(completed, list) and completed:
            total = 0
            for rec in completed:
                try:
                    if rec.get('game_type') == game_type:
                        total += int(rec.get('total_pot', 0) or 0)
                except Exception:
                    continue
            return total
    except Exception:
        pass

    total = 0
    try:
        regs = load_registrations()
        for entry in regs.values():
            try:
                tw = entry.get('total_wagered', {}) or {}
                v = int(tw.get(game_type, 0))
                total += v
            except Exception:
                continue
        return total
    except Exception:
        pass

                                                                 
    total = 0
    try:
        for g in load_games().values():
            if not isinstance(g, dict):
                continue
            if any(g.get(k) == game_type for k in ('game_type', 'source', 'game', 'type')):
                for key in ('pot', 'bet', 'wager', 'total', 'value'):
                    v = g.get(key)
                    if isinstance(v, (int, float)):
                        total += int(v)
            else:
                items = g.get('items') or g.get('bets') or []
                if isinstance(items, list) and items:
                    try:
                        ok, ttype, _ = validate_items_same_type([it for it in items if isinstance(it, str)])
                        if ttype == game_type:
                            for key in ('pot', 'bet', 'wager', 'total', 'value'):
                                v = g.get(key)
                                if isinstance(v, (int, float)):
                                    total += int(v)
                    except Exception:
                        pass
    except Exception:
        pass

    for loader in (load_blackjack_games, load_mines_games, load_towers_games, load_jackpot_games):
        try:
            for g in loader().values():
                if not isinstance(g, dict):
                    continue
                for key in ('pot', 'bet', 'wager', 'total', 'value'):
                    v = g.get(key)
                    if isinstance(v, (int, float)):
                        total += int(v)
        except Exception:
            continue

    return total


def load_completed_games() -> List[Dict]:
    """Load the completed games log (list of records)"""
    return load_json(COMPLETED_GAMES_FILE, [])


def save_completed_games(data: list):
    """Save completed games log"""
    save_json(COMPLETED_GAMES_FILE, data)


def record_completed_game(record: dict):
    """Append a completed game record to the completed games log."""
    try:
        games = load_completed_games() or []
        if not isinstance(games, list):
            games = []
        games.append(record)
        save_completed_games(games)
                                                                 
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(update_admin_panel_embed())
        except RuntimeError:
                                     
            pass
    except Exception as e:
        print(f"Error recording completed game: {e}")

def set_user_balance(user_id: str, amount: float):
    balances = load_balances()
    balances[user_id] = round(max(amount, 0.0), 2)
    save_balances(balances)

def add_user_balance(user_id: str, amount: float):
    
    if amount <= 0:
        return
    current = get_user_balance(user_id)
    set_user_balance(user_id, current + amount)

def subtract_user_balance(user_id: str, amount: float) -> bool:
    current = get_user_balance(user_id)
    if amount <= 0 or amount > current:
        return False
    set_user_balance(user_id, current - amount)
    return True


def load_crypto_deposits() -> Dict:
    """Load active crypto deposit records"""
    return load_json(CRYPTO_DEPOSITS_FILE, {})

def save_crypto_deposits(data: dict):
    """Save active crypto deposit records"""
    save_json(CRYPTO_DEPOSITS_FILE, data)


def create_crypto_deposit_record(user_id: str, currency: str, usd_amount: float, crypto_amount: float, address: str, channel_id: int, message_id: int, deposit_id: str = None, oxa_invoice_id: str = None, payment_url: str = None):
    deposits = load_crypto_deposits()
    if deposit_id is None:
        deposit_id = f"deposit_{user_id}_{int(datetime.now().timestamp())}"
    deposits[deposit_id] = {
        "deposit_id": deposit_id,
        "user_id": user_id,
        "currency": currency,
        "usd_amount": round(usd_amount, 2),
        "crypto_amount": round(crypto_amount, 8),
        "address": address,
        "payment_url": payment_url,
        "status": "pending",
        "channel_id": channel_id,
        "message_id": message_id,
        "oxa_invoice_id": oxa_invoice_id,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    save_crypto_deposits(deposits)
    return deposits[deposit_id]


def load_crypto_withdrawals() -> Dict:
    """Load active crypto withdrawal records"""
    return load_json(CRYPTO_WITHDRAWALS_FILE, {})


def save_crypto_withdrawals(data: dict):
    """Save active crypto withdrawal records"""
    save_json(CRYPTO_WITHDRAWALS_FILE, data)


def create_crypto_withdrawal_record(user_id: str, currency: str, usd_amount: float, address: str, channel_id: int, message_id: int, withdrawal_id: str = None):
    withdrawals = load_crypto_withdrawals()
    if withdrawal_id is None:
        withdrawal_id = f"withdraw_{user_id}_{int(datetime.now().timestamp())}"
    withdrawals[withdrawal_id] = {
        "withdrawal_id": withdrawal_id,
        "user_id": user_id,
        "currency": currency,
        "usd_amount": round(usd_amount, 2),
        "crypto_amount": round(calculate_crypto_amount(usd_amount, currency), 8),
        "address": address,
        "status": "pending",
        "channel_id": channel_id,
        "message_id": message_id,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    save_crypto_withdrawals(withdrawals)
    return withdrawals[withdrawal_id]


def update_crypto_deposit_status(deposit_id: str, status: str):
    deposits = load_crypto_deposits()
    if deposit_id in deposits:
        deposits[deposit_id]["status"] = status
        deposits[deposit_id]["updated_at"] = datetime.now().isoformat()
        save_crypto_deposits(deposits)
        return deposits[deposit_id]
    return None


def generate_crypto_address(user_id: str, currency: str) -> str:
    seed = hashlib.sha256(f"{user_id}:{currency}:{datetime.now().timestamp()}".encode()).hexdigest()
    currency_info = CRYPTO_CURRENCIES.get(currency, {})
    prefix = currency_info.get("prefix", "x")
    return f"{prefix}{seed[:30]}"


def validate_crypto_address(address: str, currency: str) -> bool:
    """Validate crypto address format"""
    if not address:
        return False

    address = address.strip()
    if currency == "Bitcoin":
        return (
            (address.startswith("bc1") and 26 <= len(address) <= 62) or
            ((address.startswith("1") or address.startswith("3")) and 26 <= len(address) <= 35)
        )
    if currency == "Litecoin":
        return (
            address.startswith("ltc1") and 26 <= len(address) <= 62
        ) or (
            (address.startswith("L") or address.startswith("M")) and 26 <= len(address) <= 35
        )
    if currency == "Ethereum":
        return address.startswith("0x") and len(address) == 42
    if currency == "Solana":
        return 32 <= len(address) <= 44
    if currency == "Tether":
        return (
            address.startswith("0x") and len(address) == 42
        ) or (
            address.startswith("T") and 32 <= len(address) <= 36
        )

                                         
    return 26 <= len(address) <= 64


def get_qr_code_url(data: str) -> str:
    encoded_data = quote_plus(data)
    return f"https://api.qrserver.com/v1/create-qr-code/?size=320x320&data={encoded_data}"


async def fetch_crypto_prices() -> Dict[str, float]:
    """
    Fetch live crypto prices from CoinGecko API
    Returns dict with currency names as keys and USD prices as values
    """
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin,litecoin,ethereum,solana,tether",
            "vs_currencies": "usd"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    prices = {
                        "Bitcoin": data.get("bitcoin", {}).get("usd", 30000),
                        "Litecoin": data.get("litecoin", {}).get("usd", 90),
                        "Ethereum": data.get("ethereum", {}).get("usd", 1900),
                        "Solana": data.get("solana", {}).get("usd", 120),
                        "Tether": data.get("tether", {}).get("usd", 1.0)
                    }
                    print(f"[CRYPTO PRICES] Updated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"  BTC: ${prices['Bitcoin']:,.2f}")
                    print(f"  LTC: ${prices['Litecoin']:,.2f}")
                    print(f"  ETH: ${prices['Ethereum']:,.2f}")
                    print(f"  SOL: ${prices['Solana']:,.2f}")
                    print(f"  USDT: ${prices['Tether']:,.2f}")
                    return prices
    except Exception as e:
        print(f"[CRYPTO PRICES ERROR] Failed to fetch live prices: {e}")
        print(f"[CRYPTO PRICES] Using fallback prices")
    
                     
    return {
        "Bitcoin": 95000,
        "Litecoin": 150,
        "Ethereum": 3500,
        "Solana": 200,
        "Tether": 1.0
    }


def calculate_crypto_amount(usd_amount: float, currency: str) -> float:
    """
    Calculate crypto amount from USD amount using cached prices
    Updates cache every 5 minutes
    """
    current_time = datetime.now().timestamp()
    
                                 
    if (current_time - PRICE_CACHE["last_update"]) > PRICE_CACHE["cache_duration"]:
                                                   
        asyncio.create_task(update_price_cache())
    
                                  
    rate = PRICE_CACHE["prices"].get(currency)
    
    if rate is None:
                                          
        fallback_rates = {
            "Bitcoin": 95000,
            "Litecoin": 150,
            "Ethereum": 3500,
            "Solana": 200,
            "Tether": 1.0
        }
        rate = fallback_rates.get(currency, 1.0)
        print(f"[CALC] Using fallback rate for {currency}: ${rate}")
    
    result = round(usd_amount / rate, 8)
    print(f"[CALC] {currency}: ${usd_amount} USD = {result:.8f} {CRYPTO_CURRENCIES[currency]['code']} (Rate: ${rate})")
    return result


async def update_price_cache():
    """Update the price cache with live prices"""
    try:
        prices = await fetch_crypto_prices()
        PRICE_CACHE["prices"] = prices
        PRICE_CACHE["last_update"] = datetime.now().timestamp()
    except Exception as e:
        print(f"[PRICE CACHE ERROR] Failed to update: {e}")


def get_oxa_headers(use_payout: bool = False) -> dict:
    api_key = OXA_PAYOUT_API_KEY if use_payout and OXA_PAYOUT_API_KEY else OXA_MERCHANT_API_KEY
    headers = {
        "Content-Type": "application/json",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
        headers["merchant_api_key"] = api_key
        headers["merchant-api-key"] = api_key
    return headers


async def request_oxa_static_address(currency_code: str, order_id: str) -> dict:
    if not OXA_MERCHANT_API_KEY:
        print(f"[ADDRESS GEN] No OXA merchant API key configured")
        return {}

    print(f"\n[ADDRESS GEN] Generating deposit address for {currency_code}")
    print(f"[ADDRESS GEN] Order ID: {order_id}")

    network_map = {
        "BTC": "BITCOIN",
        "LTC": "LITECOIN",
        "ETH": "ETHEREUM",
        "SOL": "SOLANA",
        "USDT": "TRON"
    }
    payload = {
        "pay_currency": currency_code,
        "to_currency": "USDT",
        "order_id": order_id,
        "description": f"Static deposit address {order_id}",
        "auto_withdrawal": False,
        "mixed_payment": False,
        "fee_paid_by_payer": 1,
        "lifetime": 60
    }
    network = network_map.get(currency_code)
    if network:
        payload["network"] = network
        print(f"[ADDRESS GEN] Network: {network}")

    async def execute_request(network_override=None):
        if network_override:
            payload["network"] = network_override
            print(f"[ADDRESS GEN] Retrying with network: {network_override}")

        url = "https://api.oxapay.com/v1/payment/static-address"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=get_oxa_headers(), timeout=20) as response:
                    text = await response.text()
                    print(f"[ADDRESS GEN] API Response Status: {response.status}")
                    
                    if response.status in (200, 201):
                        data = json.loads(text)
                        response_data = data.get("data") or data
                        if isinstance(response_data, list):
                            response_data = response_data[0] if response_data else {}

                        address = (
                            response_data.get("address")
                            or response_data.get("payment_address")
                            or response_data.get("destination_address")
                            or response_data.get("wallet_address")
                            or response_data.get("address_to")
                        )
                        qr_url = (
                            response_data.get("qr_code_url")
                            or response_data.get("qr")
                            or response_data.get("qr_url")
                        )
                        payment_url = (
                            response_data.get("payment_url")
                            or response_data.get("url")
                        )
                        invoice_id = (
                            response_data.get("invoice_id")
                            or response_data.get("order_id")
                            or response_data.get("id")
                            or response_data.get("payment_id")
                        )
                        
                                                        
                        is_valid = validate_crypto_address(address, get_currency_from_code(currency_code))
                        
                        print(f"[ADDRESS GEN] Address generated successfully")
                        print(f"[ADDRESS VERIFY] Address: {address}")
                        print(f"[ADDRESS VERIFY] Valid Format: {'YES' if is_valid else 'NO'}")
                        print(f"[ADDRESS VERIFY] Invoice ID: {invoice_id}")
                        if payment_url:
                            print(f"[ADDRESS VERIFY] Payment URL: {payment_url}")
                        
                        return {
                            "address": address,
                            "qr_code_url": qr_url,
                            "payment_url": payment_url,
                            "crypto_amount": None,
                            "invoice_id": invoice_id,
                            "raw": response_data,
                            "status": response.status,
                            "response_text": text
                        }
                    else:
                        print(f"[ADDRESS GEN] API Error ({response.status}): {text[:200]}")
                        return {
                            "error": True,
                            "status": response.status,
                            "response_text": text,
                            "network": payload.get("network")
                        }
        except Exception as e:
            print(f"[ADDRESS GEN] ❌ Exception: {e}")
            return {"error": True, "exception": str(e), "network": payload.get("network")}

    result = await execute_request()
    if result.get("error") and currency_code == "USDT" and payload.get("network") == "TRON":
        result = await execute_request("TRC20")

    if result.get("error"):
        print(f"[ADDRESS GEN] Final failure - Oxa Pay static address request failed")
        return {}

    print(f"[ADDRESS GEN] Deposit address generation complete\n")
    return result


def get_currency_from_code(code: str) -> str:
    """Convert currency code to currency name"""
    code_map = {
        "BTC": "Bitcoin",
        "LTC": "Litecoin",
        "ETH": "Ethereum",
        "SOL": "Solana",
        "USDT": "Tether"
    }
    return code_map.get(code, code)


async def request_oxa_invoice(usd_amount: float, currency_code: str, order_id: str) -> dict:
    if not OXA_MERCHANT_API_KEY:
        return {}

    url = "https://api.oxapay.com/v1/payment/invoice"
    payload = {
        "amount": round(usd_amount, 2),
        "currency": "USD",
        "lifetime": 60,
        "fee_paid_by_payer": 1,
        "under_paid_coverage": 0,
        "pay_currency": currency_code,
        "to_currency": "USDT",
        "auto_withdrawal": False,
        "mixed_payment": True,
        "order_id": order_id,
        "description": f"Deposit {order_id}",
        "sandbox": False
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=get_oxa_headers(), timeout=20) as response:
                if response.status in (200, 201):
                    data = await response.json()
                    response_data = data.get("data") or data
                    if isinstance(response_data, list):
                        response_data = response_data[0] if response_data else {}

                    address = (
                        response_data.get("address")
                        or response_data.get("payment_address")
                        or response_data.get("destination_address")
                        or response_data.get("wallet_address")
                        or response_data.get("address_to")
                    )
                    qr_url = (
                        response_data.get("qr_code_url")
                        or response_data.get("qr")
                        or response_data.get("qr_url")
                    )
                    crypto_amount = (
                        response_data.get("crypto_amount")
                        or response_data.get("payment_amount")
                        or response_data.get("amount")
                    )
                    payment_url = (
                        response_data.get("payment_url")
                        or response_data.get("url")
                    )
                    invoice_id = (
                        response_data.get("invoice_id")
                        or response_data.get("order_id")
                        or response_data.get("id")
                        or response_data.get("payment_id")
                    )
                    if address or payment_url:
                        return {
                            "address": address,
                            "payment_url": payment_url,
                            "qr_code_url": qr_url,
                            "crypto_amount": crypto_amount,
                            "invoice_id": invoice_id,
                            "raw": response_data
                        }
                    print(f"Oxa Pay invoice response did not include address: {response_data}")
                else:
                    text = await response.text()
                    print(f"Oxa Pay invoice failed {response.status}: {text}")
    except Exception as e:
        print(f"Error requesting Oxa Pay invoice: {e}")

    return await request_oxa_static_address(currency_code, order_id)


def get_crypto_currency_label(currency: str) -> str:
    info = CRYPTO_CURRENCIES.get(currency, {})
    return f"{info.get('emoji', '')} {currency} ({info.get('code', currency)})"


def load_taxed_items() -> list:
    """Load taxed items log"""
    return load_json(TAX_ITEMS_FILE, [])

def save_taxed_items(data: list):
    """Save taxed items log"""
    save_json(TAX_ITEMS_FILE, data)

def load_tax_panel() -> Dict:
    """Load tax panel configuration and state"""
    return load_json(TAX_PANEL_FILE, {})


def load_deposit_panel() -> Dict:
    return load_json(DEPOSIT_PANEL_FILE, {})


def save_deposit_panel(data: dict):
    save_json(DEPOSIT_PANEL_FILE, data)


def load_withdraw_panel() -> Dict:
    return load_json(WITHDRAW_PANEL_FILE, {})


def save_withdraw_panel(data: dict):
    save_json(WITHDRAW_PANEL_FILE, data)


def load_event_panel() -> Dict:
    return load_json(EVENT_PANEL_FILE, {})


def save_event_panel(data: dict):
    save_json(EVENT_PANEL_FILE, data)


def load_rules_panel() -> Dict:
    return load_json(RULES_PANEL_FILE, {})


def save_rules_panel(data: dict):
    save_json(RULES_PANEL_FILE, data)


def load_verification_panel() -> Dict:
    return load_json(VERIFICATION_PANEL_FILE, {})


def save_verification_panel(data: dict):
    save_json(VERIFICATION_PANEL_FILE, data)


def set_race_channel_window(channel_id: int, race_type: str, start_time: datetime, end_time: datetime):
    event_panel_data = load_event_panel()
    windows = event_panel_data.get("race_windows", {}) or {}
    if not isinstance(windows, dict):
        windows = {}
    windows[str(channel_id)] = {
        "race_type": race_type,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
    }
    event_panel_data["race_windows"] = windows
    save_event_panel(event_panel_data)


def get_race_channel_window(channel_id: int):
    event_panel_data = load_event_panel()
    windows = event_panel_data.get("race_windows", {}) or {}
    if not isinstance(windows, dict):
        return None
    return windows.get(str(channel_id))


def set_race_channel_message_id(channel_id: int, message_id: int):
    event_panel_data = load_event_panel()
    windows = event_panel_data.get("race_windows", {}) or {}
    if not isinstance(windows, dict):
        windows = {}
    channel_window = windows.get(str(channel_id), {}) or {}
    channel_window["message_id"] = int(message_id)
    windows[str(channel_id)] = channel_window
    event_panel_data["race_windows"] = windows
    save_event_panel(event_panel_data)


def get_race_channel_message_id(channel_id: int):
    window = get_race_channel_window(channel_id)
    if not isinstance(window, dict):
        return None
    return window.get("message_id")


def _is_race_window_active(start_time: Optional[datetime], end_time: Optional[datetime]) -> bool:
    now = datetime.now()
    if start_time is not None and now < start_time:
        return False
    if end_time is not None and now > end_time:
        return False
    return True


def get_active_race_channels_in_window() -> List[int]:
    active_channels = get_active_race_channels()
    active_now = []
    for channel_id in active_channels:
        window = get_race_channel_window(channel_id)
        if not isinstance(window, dict):
            continue

        start_time = None
        end_time = None
        try:
            if window.get("start_time"):
                start_time = datetime.fromisoformat(window["start_time"])
        except Exception:
            start_time = None
        try:
            if window.get("end_time"):
                end_time = datetime.fromisoformat(window["end_time"])
        except Exception:
            end_time = None

        race_type = window.get("race_type")
        if start_time is None and end_time is None and race_type:
            start_time, end_time = get_default_race_window(race_type)

        if _is_race_window_active(start_time, end_time):
            active_now.append(channel_id)

    return active_now


async def refresh_race_channel_embed(channel_id: int):
    if "bot" not in globals():
        return
    if not getattr(globals().get("bot"), "is_ready", lambda: False)():
        return

    window = get_race_channel_window(channel_id)
    if not isinstance(window, dict):
        return

    race_type = window.get("race_type")
    if not race_type:
        return

    start_time = None
    end_time = None
    try:
        if window.get("start_time"):
            start_time = datetime.fromisoformat(window["start_time"])
    except Exception:
        start_time = None
    try:
        if window.get("end_time"):
            end_time = datetime.fromisoformat(window["end_time"])
    except Exception:
        end_time = None

    if start_time is None and end_time is None:
        start_time, end_time = get_default_race_window(race_type)

    channel = bot.get_channel(channel_id)
    if channel is None:
        try:
            channel = await bot.fetch_channel(channel_id)
        except Exception:
            return
    if not isinstance(channel, discord.TextChannel):
        return

    message = None
    message_id = get_race_channel_message_id(channel_id)
    if message_id is not None:
        try:
            message = await channel.fetch_message(int(message_id))
        except Exception:
            message = None

    if message is None:
        try:
            async for history_message in channel.history(limit=30):
                if history_message.author == bot.user and history_message.embeds:
                    message = history_message
                    break
        except Exception:
            message = None

    try:
        embed, banner_file = await build_race_channel_embed(race_type, start_time=start_time, end_time=end_time)
        if message is None:
            message = await channel.send(embed=embed, file=banner_file) if banner_file else await channel.send(embed=embed)
            set_race_channel_message_id(channel_id, message.id)
            return

        edit_kwargs = {"embed": embed}
        if banner_file:
            edit_kwargs["attachments"] = [banner_file]
        await message.edit(**edit_kwargs)
        set_race_channel_message_id(channel_id, message.id)
    except Exception as e:
        print(f"[RACE] refresh failed for channel {channel_id}: {e}")


async def refresh_active_race_channel_embeds():
    if "bot" not in globals():
        return
    if not getattr(globals().get("bot"), "is_ready", lambda: False)():
        return
    active_channels = get_active_race_channels_in_window()
    for channel_id in active_channels:
        await refresh_race_channel_embed(channel_id)


def get_active_race_channels() -> List[int]:
    event_panel_data = load_event_panel()
    raw_channels = event_panel_data.get("active_race_channels", [])
    normalized_channels = []
    for channel_id in raw_channels:
        try:
            normalized_channels.append(int(channel_id))
        except Exception:
            continue

    if normalized_channels != raw_channels:
        event_panel_data["active_race_channels"] = normalized_channels
        save_event_panel(event_panel_data)

    return normalized_channels


def add_active_race_channel(channel_id: int):
    event_panel_data = load_event_panel()
    active_channels = [int(c) for c in event_panel_data.get("active_race_channels", []) if isinstance(c, (int, str))]
    if channel_id not in active_channels:
        active_channels.append(channel_id)
        event_panel_data["active_race_channels"] = active_channels
        save_event_panel(event_panel_data)


def remove_active_race_channel(channel_id: int):
    event_panel_data = load_event_panel()
    active_channels = [int(c) for c in event_panel_data.get("active_race_channels", []) if isinstance(c, (int, str))]
    if channel_id in active_channels:
        active_channels = [c for c in active_channels if c != channel_id]
        event_panel_data["active_race_channels"] = active_channels
        save_event_panel(event_panel_data)


def get_race_winners() -> List[Dict]:
    event_panel_data = load_event_panel()
    winners = event_panel_data.get("race_winners", [])
    if not isinstance(winners, list):
        winners = []
    return winners


def add_race_winner(discord_id: int, items: dict):
    event_panel_data = load_event_panel()
    winners = event_panel_data.get("race_winners", [])
    if not isinstance(winners, list):
        winners = []
    winners.insert(0, {"discord_id": int(discord_id), "items": items})
    event_panel_data["race_winners"] = winners[:3]
    save_event_panel(event_panel_data)


def get_registration_avatar_emoji(user_id: int) -> str:
    registrations = load_registrations()
    user_data = registrations.get(str(user_id), {})
    emoji = user_data.get("roblox_emoji")
    if emoji:
        return emoji
    roblox_username = user_data.get("roblox_username", "")
    if not roblox_username:
        return "👤"
    first_char = roblox_username.strip()[0].upper()
    if "A" <= first_char <= "Z":
        return chr(ord("🇦") + (ord(first_char) - ord("A")))
    digit_map = {
        "0": "0️⃣", "1": "1️⃣", "2": "2️⃣", "3": "3️⃣", "4": "4️⃣",
        "5": "5️⃣", "6": "6️⃣", "7": "7️⃣", "8": "8️⃣", "9": "9️⃣"
    }
    return digit_map.get(first_char, "👤")


async def fetch_image_bytes(url: str, timeout: int = 15) -> Optional[bytes]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                if response.status == 200:
                    return await response.read()
    except Exception:
        pass
    return None


async def get_bot_application_id() -> Optional[int]:
    if "bot" not in globals():
        return None
    app_id = getattr(bot, "application_id", None)
    if app_id:
        return app_id
    try:
        app_info = await bot.application_info()
        return app_info.id
    except Exception:
        return None


async def get_application_emoji_mention(app_id: int, name: str) -> Optional[str]:
    try:
        emojis = await bot.http.get_application_emojis(app_id)
        for emoji in emojis:
            emoji_name = getattr(emoji, "name", None)
            emoji_id = getattr(emoji, "id", None)
            if emoji_name is None and isinstance(emoji, dict):
                emoji_name = emoji.get("name")
                emoji_id = emoji.get("id")
            if emoji_name == name and emoji_id is not None:
                return f"<:{emoji_name}:{emoji_id}>"
    except Exception:
        pass
    return None


async def ensure_registration_emoji(user_id: int, roblox_username: str, avatar_url: str) -> Optional[str]:
    if "bot" not in globals() or not getattr(bot, "is_ready", lambda: False)():
        return None
    app_id = await get_bot_application_id()
    if app_id is None:
        return None

    emoji_name = f"roblox_{user_id}"
    existing_mention = await get_application_emoji_mention(app_id, emoji_name)
    if existing_mention:
        return existing_mention

    image_bytes = await fetch_image_bytes(avatar_url)
    if not image_bytes:
        return None

    content_type = "image/png"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.head(avatar_url, timeout=aiohttp.ClientTimeout(total=10)) as head_resp:
                if head_resp.status == 200:
                    ct = str(head_resp.headers.get("Content-Type", "")).lower()
                    if ct.startswith("image/"):
                        content_type = ct.split(";")[0].strip()
    except Exception:
        pass

    image_b64 = base64.b64encode(image_bytes).decode()
    image_data = f"data:{content_type};base64,{image_b64}"

    try:
        emoji = await bot.http.create_application_emoji(app_id, emoji_name, image_data)
        emoji_name = getattr(emoji, "name", emoji_name)
        emoji_id = getattr(emoji, "id", None)
        if emoji_id is None and isinstance(emoji, dict):
            emoji_id = emoji.get("id")
        if emoji_id is not None:
            return f"<:{emoji_name}:{emoji_id}>"
    except Exception as e:
        print(f"[APP EMOJI] Could not create application emoji for {roblox_username}: {e}")
    return None


def format_race_winner_entry(winner: Dict) -> str:
    discord_id = winner.get("discord_id")
    if discord_id is None:
        return "Unknown winner"
    registrations = load_registrations()
    user_data = registrations.get(str(discord_id), {})
    roblox_username = user_data.get("roblox_username", "Unknown")
    avatar_emoji = get_registration_avatar_emoji(discord_id)
    mention = f"<@{discord_id}>"
    items = winner.get("items", {})
    if isinstance(items, dict):
        items_text = ", ".join(f"{name} x{count}" for name, count in items.items())
    elif isinstance(items, list):
        items_text = ", ".join(str(item) for item in items)
    else:
        items_text = str(items)
    return f"{avatar_emoji} {mention} ({roblox_username}) — {items_text}"


def load_staff_profiles() -> Dict:
    """Load staff profiles (uses/limits) from disk"""
    return load_json(STAFF_PROFILES_FILE, {})


def save_staff_profiles(data: dict):
    """Save staff profiles to disk"""
                                                                              
    if isinstance(data, dict):
        filtered = {k: v for k, v in data.items() if k not in TAX_PROFILES}
    else:
        filtered = data
    save_json(STAFF_PROFILES_FILE, filtered)


def load_developer_profiles() -> Dict:
    """Load developer profiles (uses/limits) from disk"""
    return load_json(DEVELOPER_PROFILES_FILE, {})


def save_developer_profiles(data: dict):
    """Save developer profiles to disk"""
    if isinstance(data, dict):
        filtered = {k: v for k, v in data.items() if k not in TAX_PROFILES}
    else:
        filtered = data
    save_json(DEVELOPER_PROFILES_FILE, filtered)


def ensure_developer_profiles():
    """Ensure developer_profiles.json exists and is seeded from DEVELOPER_PROFILES if empty."""
    profiles = load_developer_profiles()
    if not profiles:
        profiles = {}
        save_developer_profiles(profiles)
    return profiles


def increment_developer_use(user_id: int) -> Tuple[bool, int, int]:
    """Increment developer 'uses' for a user. Returns (allowed, uses, limit)."""
    profiles = load_developer_profiles()
    key = str(user_id)
    entry = profiles.get(key)
    if not entry:
        entry = {"emoji": "", "uses": 0, "limit": 20}
        profiles[key] = entry
    uses = int(entry.get("uses", 0))
    limit = int(entry.get("limit", 20))
    if uses >= limit:
        return False, uses, limit
    uses += 1
    entry["uses"] = uses
    profiles[key] = entry
    save_developer_profiles(profiles)
    return True, uses, limit


def load_event_host_profiles() -> Dict:
    return load_json(EVENT_HOST_PROFILES_FILE, {})


def save_event_host_profiles(data: dict):
    save_json(EVENT_HOST_PROFILES_FILE, data)


def ensure_event_host_profiles():
    """Ensure event host profiles exist and seed from EVENT_HOST_PROFILES if empty."""
    profiles = load_event_host_profiles()
    if not profiles:
        profiles = {k: v.copy() for k, v in EVENT_HOST_PROFILES.items()}
        save_event_host_profiles(profiles)
    return profiles


def increment_event_host_use(user_id: int) -> Tuple[bool, int, int]:
    """Increment event host 'uses' for a user. Returns (allowed, uses, limit)."""
    profiles = load_event_host_profiles()
    key = str(user_id)
    entry = profiles.get(key)
    if not entry:
        emoji = EVENT_HOST_PROFILES.get(key, {}).get("emoji", "")
        entry = {"emoji": emoji, "uses": 0, "limit": 3}
        profiles[key] = entry
    uses = int(entry.get("uses", 0))
    limit = int(entry.get("limit", 3))
    if uses >= limit:
        return False, uses, limit
    uses += 1
    entry["uses"] = uses
    profiles[key] = entry
    save_event_host_profiles(profiles)
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(update_event_panel_embed())
    except RuntimeError:
        pass
    return True, uses, limit


def reset_event_host_uses():
    """Reset all event host uses to 0."""
    profiles = load_event_host_profiles()
    if not profiles:
        return
    for entry in profiles.values():
        entry["uses"] = 0
    save_event_host_profiles(profiles)


def ensure_staff_profiles():
    """Ensure `staff_profiles.json` exists and is seeded from `STAFF_PROFILES` if empty.

    Note: TAX_PROFILES are intentionally separate and are not added to the
    staff profiles file or treated as limited staff members.
    """
    profiles = load_staff_profiles()
                                                                           
    if not profiles:
        profiles = {k: v.copy() for k, v in STAFF_PROFILES.items()}
                                                                                  
        save_staff_profiles(profiles)
    return profiles


def increment_staff_use(user_id: int) -> Tuple[bool, int, int]:
    """Increment staff 'uses' for a user. Returns (allowed, uses, limit)."""
    profiles = load_staff_profiles()
    key = str(user_id)
                                                                                
                                                                      
    if key in TAX_PROFILES:
        return True, 0, 0
    entry = profiles.get(key)
                                                                           
    if not entry:
                                           
        emoji = TAX_PROFILES.get(key, {}).get("emoji", "")
        entry = {"emoji": emoji, "uses": 0, "limit": 10}
        profiles[key] = entry
    uses = int(entry.get("uses", 0))
    limit = int(entry.get("limit", 10))
    if uses >= limit:
        return False, uses, limit
    uses += 1
    entry["uses"] = uses
    profiles[key] = entry
    save_staff_profiles(profiles)
                                                        
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(update_tax_panel_embed())
        loop.create_task(update_admin_panel_embed())
    except RuntimeError:
                                 
        pass
    return True, uses, limit


def reset_staff_uses():
    """Reset all staff uses to 0."""
    profiles = load_staff_profiles()
    if not profiles:
        return
    for entry in profiles.values():
        entry["uses"] = 0
    save_staff_profiles(profiles)

def save_tax_panel(data: dict):
    """Save tax panel configuration and state"""
    save_json(TAX_PANEL_FILE, data)

def get_house_tax() -> float:
    """Return current tax rate (saved or default)"""
    settings = load_tax_panel()
    return float(settings.get("tax_rate", HOUSE_TAX))

def set_house_tax(rate: float):
    """Save current tax rate"""
    settings = load_tax_panel()
    settings["tax_rate"] = rate
    save_tax_panel(settings)

async def update_all_game_embeds():
    """Update all active game embeds with current tax rate and sync to Discord"""
    try:
                               
        games = load_games()
        for game_id, game_data in games.items():
            if game_data.get('message_id') and game_data.get('status') == 'waiting':
                try:
                                                                                                     
                                                                      
                                                                                   
                    for guild in bot.guilds:
                        for channel in guild.text_channels:
                            try:
                                message = await channel.fetch_message(game_data['message_id'])
                                                                         
                                creator_value = game_data.get('creator_value', 0)
                                total_pot = creator_value * 2
                                tax_amount = calculate_tax(total_pot)
                                net_winnings = calculate_net_winnings(total_pot)
                                
                                embed = discord.Embed(
                                    title="COINFLIP GAME CREATED!",
                                    color=discord.Color.green()
                                )
                                
                                coin_emoji = HEADS_EMOJI if game_data['creator_side'].lower() == "heads" else TAILS_EMOJI
                                creator_user = bot.get_user(game_data['creator_id'])
                                creator_mention = creator_user.mention if creator_user else f"<@{game_data['creator_id']}>"
                                
                                embed.add_field(
                                    name="CREATOR",
                                    value=f"{creator_mention} {coin_emoji}",
                                    inline=True
                                )
                                
                                embed.add_field(
                                    name="BET VALUE",
                                    value=f"** {VALUE_EMOJI} {format_item_value(creator_value)}**",
                                    inline=True
                                )
                                
                                if game_data.get('wild_mode'):
                                    embed.add_field(
                                        name=f"{WILD_MODE_EMOJI} Wild Mode",
                                        value="**ENABLED**",
                                        inline=True
                                    )
                                
                                embed.add_field(
                                    name="Potential Winnings",
                                    value=(
                                        f"Total Pot: {VALUE_EMOJI} **{format_value_with_commas(total_pot)}**\n"
                                        f"Winner Gets: {VALUE_EMOJI} **{format_value_with_commas(net_winnings)}**\n"
                                        f"House Tax ({get_house_tax() * 100:.1f}%): {VALUE_EMOJI} **{format_value_with_commas(tax_amount)}**"
                                    ),
                                    inline=False
                                )
                                
                                if game_data.get('wild_mode'):
                                    embed.add_field(
                                        name="Wild Mode Effect",
                                        value=(
                                            f"• **LOSER gets the winnings**\n"
                                            f"• **WINNER loses their items**\n"
                                            f"• Complete reversal of outcome!"
                                        ),
                                        inline=False
                                    )
                                
                                embed.set_footer(text=f"Game ID: {game_id}")
                                
                                await message.edit(embed=embed)
                                print(f"Updated game embed {game_id} with new tax rate")
                                break
                            except discord.NotFound:
                                continue
                            except Exception:
                                continue
                except Exception:
                    continue
    except Exception as e:
        print(f"Error updating game embeds: {e}")

def load_admin_panel() -> Dict:
    """Load admin panel message data"""
    return load_json(ADMIN_PANEL_FILE, {})

def save_admin_panel(data: dict):
    """Save admin panel message data"""
    save_json(ADMIN_PANEL_FILE, data)

def log_taxed_item(item_name: str, item_value: int, source: str, timestamp: str):
    """Log a taxed item for admin review"""
    taxed_items = load_taxed_items()
    entry = {
        "item_name": item_name,
        "item_value": item_value,
        "source": source,
        "timestamp": timestamp
    }
    taxed_items.append(entry)
    save_taxed_items(taxed_items)

def get_item_value(item_name: str):
    """Get exact value of an item from ITEMS_FILE (mm2.json)"""
    items = load_items()
    item_data = items.get(item_name, {})
    
    if isinstance(item_data, dict):
        value = item_data.get('value', 0)
                                                   
        if isinstance(value, str):
            try:
                return float(value)
            except (ValueError, TypeError):
                return 0
        elif isinstance(value, (int, float)):
            return value
    
    return 0

def format_item_value(value):
    """Format item value to show exact amount, removing only trailing zeros/decimals"""
    if isinstance(value, (int, float)):
        if value == int(value):
            return str(int(value))
        else:
                                                                         
            formatted = f"{value:.2f}".rstrip('0').rstrip('.')
            return formatted
    return str(value)

def format_value_with_commas(value):
    """Format value with exact decimals and comma separators for thousands"""
    if not isinstance(value, (int, float)):
        return str(value)
    
    formatted = format_item_value(value)
    
                           
    if '.' in formatted:
        parts = formatted.split('.')
        integer_part = parts[0]
        decimal_part = parts[1]
                                    
        integer_with_commas = '{:,}'.format(int(integer_part)) if integer_part else '0'
        return f"{integer_with_commas}.{decimal_part}"
    else:
                                      
        return '{:,}'.format(int(formatted))

def get_item_details(item_name: str) -> Optional[Dict]:
    """Get full item details"""
    items = load_items()
    return items.get(item_name)

def get_item_emoji(item_name: str) -> str:
    """Get emoji of an item from items.json"""
    items = load_items()
    item_data = items.get(item_name, {})
    if isinstance(item_data, dict):
        emoji = item_data.get('emoji')
        if emoji:
            return emoji
    return VALUE_EMOJI                 

async def get_player_display_name(user_id: int) -> str:
    """Resolve a Discord user's display name or fallback to mention."""
    user = bot.get_user(user_id)
    if not user:
        try:
            user = await bot.fetch_user(user_id)
        except Exception:
            user = None
    if user:
        return user.name
    return f"<@{user_id}>"

def build_mm2_value_description() -> str:
    """Return a description listing all MM2-type items sorted by value descending."""
    items = load_items()
    mm2_items = [
        (name, data.get('value', 0))
        for name, data in items.items()
        if isinstance(data, dict) and data.get('type') == GameType.MM2
    ]
    sorted_items = sorted(mm2_items, key=lambda x: x[1], reverse=True)
    if not sorted_items:
        return "No MM2 items found."

    lines = []
    for name, value in sorted_items:
        lines.append(f"{get_item_emoji(name)} **{name}** - {VALUE_EMOJI} **{format_value_with_commas(value)}**")
    return "\n".join(lines)

def convert_value_to_items(value: int, game_type: str = GameType.MM2) -> List[str]:
    """Convert a numeric value into a list of items whose total is <= value."""
    items_db = load_items()
    type_items = [
        (name, data.get('value', 0)) 
        for name, data in items_db.items() 
        if isinstance(data, dict) and data.get('type') == game_type
    ]
    sorted_items = sorted(type_items, key=lambda x: x[1], reverse=True)
    remaining = value
    result = []
    for name, val in sorted_items:
        if val <= 0:
            continue
        while remaining >= val:
            result.append(name)
            remaining -= val
    return result

def format_items_display(items: List[str]) -> str:
    """Helper to format items list for display"""
    if not items:
        return "No items"
    
    item_counts = {}
    for item in items:
        item_counts[item] = item_counts.get(item, 0) + 1
    
    display_parts = []
    for item_name, count in list(item_counts.items())[:3]:
        display_parts.append(f"{get_item_emoji(item_name)} {item_name} x{count}")
    
    if len(item_counts) > 3:
        display_parts.append(f"...+{len(item_counts)-3} more")
    
    return " | ".join(display_parts)

                                             
class ValuePaginator(discord.ui.View):
    def __init__(self, items_pages: List[List[Tuple]], total_pages: int, game_type: str = GameType.MM2):
        super().__init__(timeout=None)
        self.items_pages = items_pages
        self.total_pages = total_pages
        self.current_page = 0
        self.game_type = game_type
        
    @discord.ui.button(label="◀ Previous", style=discord.ButtonStyle.secondary, disabled=True)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page -= 1
        await self.update_page(interaction)
    
    @discord.ui.button(label="Next ▶", style=discord.ButtonStyle.secondary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page += 1
        await self.update_page(interaction)

    @discord.ui.button(label="ADM", style=discord.ButtonStyle.secondary)
    async def toggle_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        new_type = GameType.ADM if self.game_type == GameType.MM2 else GameType.MM2
        self.game_type = new_type

        pages, total_pages = build_value_list_pages(self.game_type)
        if not pages:
            await interaction.response.send_message(
                f"No {self.game_type} items found in the database.",
                ephemeral=True
            )
            return

        self.items_pages = pages
        self.total_pages = total_pages
        self.current_page = 0

                                                                 
        button.label = "MM2" if self.game_type == GameType.ADM else "ADM"

        await self.update_page(interaction)
    
    async def update_page(self, interaction: discord.Interaction):
                              
        self.previous_button.disabled = self.current_page <= 0
        self.next_button.disabled = self.current_page >= self.total_pages - 1
        
                                       
        embed = discord.Embed(
            title=f"{self.game_type.upper()} Values (Page {self.current_page + 1}/{self.total_pages})",
            color=discord.Color.green()
        )
        
        items_text = ""
        for item_name, item_value in self.items_pages[self.current_page]:
            item_emoji = get_item_emoji(item_name)
            items_text += f"{item_emoji} **{item_name}** - {VALUE_EMOJI} **{format_value_with_commas(item_value)}**\n"
        
        embed.description = items_text
        embed.set_footer(text=f"Total items: {sum(len(page) for page in self.items_pages)}")
        
        await interaction.response.edit_message(embed=embed, view=self)

def build_value_list_pages(game_type: str = GameType.MM2) -> Tuple[List[List[Tuple]], int]:
    """Build paginated value list for specified game type"""
    items = load_items()
    type_items = [
        (name, data.get('value', 0))
        for name, data in items.items()
        if isinstance(data, dict) and data.get('type') == game_type
    ]
    sorted_items = sorted(type_items, key=lambda x: x[1], reverse=True)
    
                                          
    items_per_page = 10
    pages = []
    for i in range(0, len(sorted_items), items_per_page):
        pages.append(sorted_items[i:i + items_per_page])
    
    return pages, len(pages)

def build_values_response(game_type: str = GameType.MM2):
    """Build values response with pagination for specified game type"""
    pages, total_pages = build_value_list_pages(game_type)
    if not pages:
        return None, None

    embed = discord.Embed(
        title=f"{game_type.upper()} Values (Page 1/{total_pages})",
        color=discord.Color.green()
    )

    items_text = ""
    for item_name, item_value in pages[0]:
        item_emoji = get_item_emoji(item_name)
        items_text += f"{item_emoji} **{item_name}** - {VALUE_EMOJI} **{format_value_with_commas(item_value)}**\n"

    embed.description = items_text
    embed.set_footer(text=f"Total items: {sum(len(page) for page in pages)}")
    return embed, ValuePaginator(pages, total_pages, game_type)

class TaxedItemsPaginator(discord.ui.View):
    def __init__(self, items_pages: List[List[Tuple[str, int]]], total_pages: int, total_items: int, total_value: int):
        super().__init__(timeout=None)
        self.items_pages = items_pages
        self.total_pages = total_pages
        self.total_items = total_items
        self.total_value = total_value
        self.current_page = 0

    @discord.ui.button(label="◀ Previous", style=discord.ButtonStyle.secondary, disabled=True)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page -= 1
        await self.update_page(interaction)

    @discord.ui.button(label="Next ▶", style=discord.ButtonStyle.secondary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page += 1
        await self.update_page(interaction)

    async def update_page(self, interaction: discord.Interaction):
        self.previous_button.disabled = self.current_page <= 0
        self.next_button.disabled = self.current_page >= self.total_pages - 1

        embed = discord.Embed(
            title=f"Taxed Items (Page {self.current_page + 1}/{self.total_pages})",
            color=discord.Color.green()
        )

        items_text = ""
        for item_name, item_count in self.items_pages[self.current_page]:
            item_emoji = get_item_emoji(item_name)
            item_value = get_item_value(item_name)
            total_item_value = item_value * item_count
            items_text += f"{item_emoji} **{item_name}** x{item_count} - {VALUE_EMOJI} **{format_item_value(total_item_value)}**\n"

        embed.description = items_text or "No taxed items"
        embed.set_footer(text=f"Total taxed items: {self.total_items} | Total value: {format_value_with_commas(self.total_value)}")

        await interaction.response.edit_message(embed=embed, view=self)


def build_taxed_items_pages() -> Tuple[List[List[Tuple[str, int]]], int, int, int]:
    taxed_items = load_taxed_items()
    counts = {}
    total_value = 0
    total_items = 0

    for entry in taxed_items:
        for item_name in entry.get("items", []):
            counts[item_name] = counts.get(item_name, 0) + 1
            total_items += 1
            total_value += get_item_value(item_name)

    sorted_items = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    items_per_page = 10
    pages = []
    for i in range(0, len(sorted_items), items_per_page):
        pages.append(sorted_items[i:i + items_per_page])

    return pages, len(pages), total_items, total_value


def build_taxed_items_response():
    pages, total_pages, total_items, total_value = build_taxed_items_pages()
    if not pages:
        return None, None

    embed = discord.Embed(
        title=f"Taxed Items (Page 1/{total_pages})",
        color=discord.Color.green()
    )

    items_text = ""
    for item_name, item_count in pages[0]:
        item_emoji = get_item_emoji(item_name)
        item_value = get_item_value(item_name)
        total_item_value = item_value * item_count
        items_text += f"{item_emoji} **{item_name}** x{item_count} - {VALUE_EMOJI} **{format_item_value(total_item_value)}**\n"

    embed.description = items_text or "No taxed items"
    embed.set_footer(text=f"Total taxed items: {total_items} | Total value: {format_value_with_commas(total_value)}")
    return embed, TaxedItemsPaginator(pages, total_pages, total_items, total_value)


def roll_daily_case_reward(user_id: int) -> discord.Embed:
    case_key = random.choice(list(CASE_SECTIONS.keys()))
    case_info = CASE_SECTIONS[case_key]
    case_name = case_info["name"]
    value_list = case_info["Value"]
    total_chance = sum(item['chance'] for item in value_list)
    rand_num = random.random() * total_chance
    cumulative = 0
    won_item = None

    for item in value_list:
        cumulative += item['chance']
        if rand_num <= cumulative:
            won_item = item.copy()
            break

    if not won_item:
        won_item = value_list[-1].copy()

    if won_item['name'] != "Nothing":
        add_items_to_inventory(str(user_id), [won_item['name']])

    record_daily_claim(user_id)

    result_embed = discord.Embed(
        title="Daily Case Claimed!",
        description=f"You claimed your daily case: **{case_name}**",
        color=discord.Color.green()
    )

    if won_item['name'] != "Nothing":
        reward_text = f"{won_item['emoji']} **{won_item['name']}** - {VALUE_EMOJI} **{format_value_with_commas(won_item['value'])}**"
    else:
        reward_text = f"{won_item['emoji']} **Nothing** - {VALUE_EMOJI} **0**"

    result_embed.add_field(name="You Won:", value=reward_text, inline=False)
    result_embed.set_footer(text="Come back tomorrow for another free case!")
    return result_embed

def build_mm2_values_response():
    pages, total_pages = build_value_list_pages()
    if not pages:
        return None, None

    embed = discord.Embed(
        title=f"MM2 Values (Page 1/{total_pages})",
        color=discord.Color.green()
    )

    items_text = ""
    for item_name, item_value in pages[0]:
        item_emoji = get_item_emoji(item_name)
        items_text += f"{item_emoji} **{item_name}** - {VALUE_EMOJI} **{format_item_value(item_value)}**\n"

    embed.description = items_text
    embed.set_footer(text=f"Total items: {sum(len(page) for page in pages)}")
    return embed, ValuePaginator(pages, total_pages, GameType.MM2)

def is_user_registered(user_id: int) -> bool:
    """Check if user is registered and verified"""
    registrations = load_registrations()
    user_data = registrations.get(str(user_id), {})
    return user_data.get('verified', False)

def get_user_inventory(user_id: str) -> List[Dict]:
    """Get user's inventory"""
    inventories = load_inventories()
    return inventories.get(user_id, [])

def get_user_items_with_values(user_id: str) -> List[Tuple[str, int, Dict, int]]:
    """Get user's items with their values"""
    inventory = get_user_inventory(user_id)
    items_with_values = []
    
                       
    item_counts = {}
    for item_data in inventory:
        item_name = item_data.get('name')
        item_counts[item_name] = item_counts.get(item_name, 0) + 1
    
                                    
    for item_name, count in item_counts.items():
        item_details = get_item_details(item_name)
        if item_details:
            item_value = item_details.get('value', 0)
            items_with_values.append((item_name, item_value, item_details, count))
    
    return items_with_values

def get_user_all_items(user_id: str) -> List[Tuple[str, int]]:
    """Get all user items individually"""
    inventory = get_user_inventory(user_id)
    items = []
    
    for item_data in inventory:
        item_name = item_data.get('name')
        item_value = get_item_value(item_name)
        items.append((item_name, item_value))
    
    return items

def calculate_inventory_value(user_id: str) -> int:
    """Calculate total value of user's inventory"""
    items = get_user_all_items(user_id)
    return sum(value for _, value in items)

def remove_items_from_inventory(user_id: str, items_to_remove: List[str]):
    """Remove specific items from user's inventory"""
    inventories = load_inventories()
    user_inventory = inventories.get(str(user_id), [])
    
                                    
    new_inventory = []
    remove_count = {item: items_to_remove.count(item) for item in set(items_to_remove)}
    current_count = {}
    
    for item_data in user_inventory:
        item_name = item_data.get('name')
        current_count[item_name] = current_count.get(item_name, 0) + 1
        
        if item_name in remove_count and current_count[item_name] <= remove_count[item_name]:
            continue                              
        new_inventory.append(item_data)
    
    inventories[str(user_id)] = new_inventory
    save_json(INVENTORY_FILE, inventories)
    return new_inventory

def add_items_to_inventory(user_id: str, items_to_add: List[str]):
    """Add items to user's inventory"""
    inventories = load_inventories()
    user_inventory = inventories.get(str(user_id), [])
    
    for item_name in items_to_add:
        user_inventory.append({"name": item_name, "added_at": datetime.now().isoformat()})
    
    inventories[str(user_id)] = user_inventory
    save_json(INVENTORY_FILE, inventories)

def transfer_items(sender_id: str, receiver_id: str, items: List[str]):
    """Transfer ALL items between users"""
                                  
    remove_items_from_inventory(sender_id, items)
    
                               
    add_items_to_inventory(receiver_id, items)

                                           
def get_verification_code(user_id: int, discord_username: Optional[str] = None) -> str:
    """Generate verification code"""
    words = [
        "Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot", 
        "Mike", "November", "Oscar", "Papa", "Quebec", "Romeo", 
        "Sierra", "Tango", "Uniform", "Victor", "White", 
        "Xray", "Yankee", "Zulu", "Apple", "Banana", "Cherry",
        "Dragon", "Eagle", "Falcon", "Gemini", "Hawk", "Ice", 
        "Jupiter", "King", "Lion", "Mars", "Neptune", "Ocean",
        "Phoenix", "Queen", "Rocket", "Saturn", "Tiger", "Oval",
        "Venus", "Wolf"
    ]
    code_words = random.sample(words, 3)
    code = f"{VERIFICATION_PREFIX} {' '.join(code_words)}"
    
                            
    registrations = load_registrations()
    uid = str(user_id)
    if uid not in registrations:
        registrations[uid] = {}
    if discord_username:
        registrations[uid]['discord_username'] = discord_username
    registrations[uid]['verification_code'] = code
    registrations[uid]['registered_at'] = datetime.now().isoformat()
    registrations[uid]['verified'] = False
    save_json(REGISTRATIONS_FILE, registrations)
    
    return code

async def verify_roblox_account(username: str, verification_code: str) -> Tuple[bool, str, str, str, str]:
    """Verify Roblox account by checking bio"""
    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
            }
            
                                               
            async with session.post(
                "https://users.roblox.com/v1/usernames/users",
                headers=headers,
                json={"usernames": [username], "excludeBannedUsers": True}
            ) as response:
                if response.status != 200:
                    print(f"Username lookup failed: {response.status}")
                    return False, "", "", "", ""
                
                data = await response.json()
                if not data.get('data') or len(data['data']) == 0:
                    print(f"User not found: {username}")
                    return False, "", "", "", ""
                
                user_info = data['data'][0]
                user_id = user_info['id']
                roblox_username = user_info['name']
                display_name = user_info.get('displayName', roblox_username)
                
                print(f"Found user: {roblox_username} (Display: {display_name}) (ID: {user_id})")
            
                                                           
            async with session.get(
                f"https://users.roblox.com/v1/users/{user_id}",
                headers=headers
            ) as profile_response:
                if profile_response.status != 200:
                    print(f"Profile fetch failed: {profile_response.status}")
                    return False, "", "", "", ""
                
                profile_data = await profile_response.json()
                description = profile_data.get("description", "")
                
                print(f"Description length: {len(description)}")
                print(f"Looking for: '{verification_code}'")
                print(f"In description: '{description[:200]}...'")
                
                                                   
                clean_verification = verification_code.strip()
                clean_description = description.strip()
                
                                                              
                if clean_verification in clean_description:
                    print("Verification code found in description!")
                    
                                        
                    try:
                        avatar_url = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=420x420&format=Png&isCircular=false"
                        
                        async with session.get(avatar_url, headers=headers) as avatar_response:
                            if avatar_response.status == 200:
                                avatar_data = await avatar_response.json()
                                if avatar_data.get('data') and len(avatar_data['data']) > 0:
                                    avatar_image = avatar_data['data'][0]['imageUrl']
                                else:
                                                                 
                                    avatar_image = f"https://www.roblox.com/headshot-thumbnail/image?userId={user_id}&width=420&height=420&format=png"
                            else:
                                avatar_image = f"https://www.roblox.com/headshot-thumbnail/image?userId={user_id}&width=420&height=420&format=png"
                    except Exception as e:
                        print(f"Avatar fetch error: {e}")
                        avatar_image = f"https://www.roblox.com/headshot-thumbnail/image?userId={user_id}&width=420&height=420&format=png"
                    
                    return True, roblox_username, display_name, str(user_id), avatar_image
                else:
                    print("Verification code NOT found in description")
                    
                    lines = clean_description.split('\n')
                    for i, line in enumerate(lines):
                        if "Bloxloot" in line:
                            print(f"Line {i+1} with Bloxloot: '{line}'")
                    
                    return False, "", "", "", ""
    
    except aiohttp.ClientError as e:
        print(f"Network error during verification: {e}")
        return False, "", "", "", ""
    except Exception as e:
        print(f"Unexpected error during verification: {e}")
        import traceback
        traceback.print_exc()
        return False, "", "", "", ""

                                            
class BlackjackGame:
    def __init__(self, creator_id: int, creator_items: List[str], bet_value: int):
        self.creator_id = creator_id
        self.creator_items = creator_items
        self.bet_value = bet_value
        self.opponent_id = None
        self.opponent_items = []
        self.status = "waiting"                                         
        self.game_id = f"bj_{creator_id}_{int(datetime.now().timestamp())}"
        self.created_at = datetime.now().isoformat()
        self.message_id = None
        
                    
        self.server_seed = generate_server_seed("blackjack", self.game_id, creator_id, int(datetime.now().timestamp()))
        self.server_seed_hash = get_server_seed_hash(self.server_seed)
        self.deck = deterministic_shuffle(self.server_seed, self.create_deck(), "blackjack")
        self.creator_hand = []
        self.opponent_hand = []
        self.creator_score = 0
        self.opponent_score = 0
        self.creator_stand = False
        self.opponent_stand = False
        self.current_turn = creator_id                        
        self.winner = None
        self.loser = None
        self.reveal_opponent_card = False

                                                                
        self.creator_hand2: List[str] = []
        self.creator_score2: int = 0
        self.creator_stand2: bool = False
        self.creator_split: bool = False

        self.opponent_hand2: List[str] = []
        self.opponent_score2: int = 0
        self.opponent_stand2: bool = False
        self.opponent_split: bool = False

                                                       
        self.current_hand = 1
    
    def create_deck(self) -> List[str]:
        """Create a standard deck of 52 cards"""
        suits = ['♥', '♦', '♣', '♠']
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        deck = []
        for suit in suits:
            for value in values:
                deck.append(f"{value}{suit}")
        return deck * 1                              
    
    def draw_card(self) -> str:
        """Draw a card from the deck"""
        if len(self.deck) < 10:                            
            self.deck = deterministic_shuffle(self.server_seed, self.create_deck(), "blackjack")
        return self.deck.pop()

    def can_split(self, player_id: int) -> bool:
        """Return True if the player can split their hand"""
        if player_id == self.creator_id:
            hand = self.creator_hand
            if self.creator_split:
                return False
        elif player_id == self.opponent_id:
            hand = self.opponent_hand
            if self.opponent_split:
                return False
        else:
            return False

        if len(hand) == 2:
                                           
            return hand[0][:-1] == hand[1][:-1]
        return False

    def split(self, player_id: int) -> Tuple[bool, str]:
        """Perform a split for the specified player"""
        if not self.can_split(player_id):
            return False, "Cannot split your hand."
        if player_id == self.creator_id:
            card = self.creator_hand.pop()                                 
            self.creator_hand2 = [card]
                                        
            self.creator_hand.append(self.draw_card())
            self.creator_hand2.append(self.draw_card())
            self.creator_score = self.calculate_score(self.creator_hand)
            self.creator_score2 = self.calculate_score(self.creator_hand2)
            self.creator_split = True
                                  
            self.current_hand = 1
            return True, "Hand split into two hands. Play the first hand first."
        else:
            card = self.opponent_hand.pop()
            self.opponent_hand2 = [card]
            self.opponent_hand.append(self.draw_card())
            self.opponent_hand2.append(self.draw_card())
            self.opponent_score = self.calculate_score(self.opponent_hand)
            self.opponent_score2 = self.calculate_score(self.opponent_hand2)
            self.opponent_split = True
            self.current_hand = 1
            return True, "Hand split into two hands. Play the first hand first."
    
    def calculate_score(self, hand: List[str]) -> int:
        """Calculate blackjack score for a hand"""
        score = 0
        aces = 0
        
        for card in hand:
            value = card[:-1]               
            if value in ['J', 'Q', 'K']:
                score += 10
            elif value == 'A':
                aces += 1
                score += 11
            else:
                score += int(value)
        
                         
        while score > 21 and aces > 0:
            score -= 10
            aces -= 1
        
        return score
    
    def hit(self, player_id: int) -> Tuple[bool, str, bool]:
        """Player draws a card. Supports split hands and auto-hand shifting.
        Returns: (is_valid, message, game_ended)"""
        
                                         
        if player_id != self.current_turn:
            return False, "Not your turn!", False
        
                                           
        if player_id == self.creator_id:
            if self.creator_stand and (not self.creator_split or self.creator_stand2):
                return False, "You have already stood!", False
        else:
            if self.opponent_stand and (not self.opponent_split or self.opponent_stand2):
                return False, "You have already stood!", False
        
                                     
        if player_id == self.creator_id:
            if self.creator_split and self.current_hand == 1 and not self.creator_stand:
                hand = self.creator_hand
                score_attr = 'creator_score'
                stand_attr = 'creator_stand'
            elif self.creator_split and self.current_hand == 2 and not self.creator_stand2:
                hand = self.creator_hand2
                score_attr = 'creator_score2'
                stand_attr = 'creator_stand2'
            else:
                hand = self.creator_hand
                score_attr = 'creator_score'
                stand_attr = 'creator_stand'
        else:            
            if self.opponent_split and self.current_hand == 1 and not self.opponent_stand:
                hand = self.opponent_hand
                score_attr = 'opponent_score'
                stand_attr = 'opponent_stand'
            elif self.opponent_split and self.current_hand == 2 and not self.opponent_stand2:
                hand = self.opponent_hand2
                score_attr = 'opponent_score2'
                stand_attr = 'opponent_stand2'
            else:
                hand = self.opponent_hand
                score_attr = 'opponent_score'
                stand_attr = 'opponent_stand'
        
                   
        card = self.draw_card()
        hand.append(card)
        new_score = self.calculate_score(hand)
        setattr(self, score_attr, new_score)
        
                                  
        if new_score > 21:
            setattr(self, stand_attr, True)
            
                                                                    
            if player_id == self.creator_id and self.creator_split and self.current_hand == 1:
                self.current_hand = 2
                return True, f"Bust! You drew {self.get_card_emoji(card)} - Score: {new_score}. Now playing second hand.", False
            
            if player_id == self.opponent_id and self.opponent_split and self.current_hand == 1:
                self.current_hand = 2
                return True, f"Bust! You drew {self.get_card_emoji(card)} - Score: {new_score}. Now playing second hand.", False
            
                                                      
            self.switch_turn()
            return True, f"Bust! You drew {self.get_card_emoji(card)} - Score: {new_score}. Opponent's turn.", False
        
                      
        if new_score == 21:
            setattr(self, stand_attr, True)
            
                                                                    
            if player_id == self.creator_id and self.creator_split and self.current_hand == 1:
                self.current_hand = 2
                return True, f"Blackjack! You drew {self.get_card_emoji(card)} - Score: 21. Now playing second hand.", False
            
            if player_id == self.opponent_id and self.opponent_split and self.current_hand == 1:
                self.current_hand = 2
                return True, f"Blackjack! You drew {self.get_card_emoji(card)} - Score: 21. Now playing second hand.", False
            
                                      
            if self.check_game_over():
                self.determine_winner()
                return True, f"Blackjack! You drew {self.get_card_emoji(card)} - Score: 21.", True
            
            self.switch_turn()
            return True, f"Blackjack! You drew {self.get_card_emoji(card)} - Score: 21. Opponent's turn.", False
        
                                          
        if self.check_game_over():
            self.determine_winner()
            return True, f"Drew {self.get_card_emoji(card)} - New score: {new_score}", True
        
        return True, f"Drew {self.get_card_emoji(card)} - New score: {new_score}", False
    
    def stand(self, player_id: int) -> Tuple[bool, str, bool]:
        """Player stands. Returns: (is_valid, message, game_ended)"""
        
                                         
        if player_id != self.current_turn:
            return False, "Not your turn!", False
        
                            
        if player_id == self.creator_id:
            if self.creator_split and self.current_hand == 1 and not self.creator_stand:
                self.creator_stand = True
                self.current_hand = 2
                return True, "Stood on first hand. Now playing second hand.", False
            elif self.creator_split and self.current_hand == 2 and not self.creator_stand2:
                self.creator_stand2 = True
            else:
                self.creator_stand = True
        else:            
            if self.opponent_split and self.current_hand == 1 and not self.opponent_stand:
                self.opponent_stand = True
                self.current_hand = 2
                return True, "Stood on first hand. Now playing second hand.", False
            elif self.opponent_split and self.current_hand == 2 and not self.opponent_stand2:
                self.opponent_stand2 = True
            else:
                self.opponent_stand = True
        
                                  
        if self.check_game_over():
            self.determine_winner()
            return True, "Stand - Game Over", True
        
                                       
        self.switch_turn()
        return True, f"Stand - {self.get_current_player_name()}'s turn", False
    
    def check_game_over(self) -> bool:
        """Check if the game should end"""
        creator_done = self.creator_stand and (not self.creator_split or self.creator_stand2)
        opponent_done = self.opponent_stand and (not self.opponent_split or self.opponent_stand2)
        
                                                             
        if creator_done and opponent_done:
            return True
        
                                                                               
        creator_bust = (self.creator_score > 21 and (not self.creator_split or self.creator_score2 > 21))
        opponent_bust = (self.opponent_score > 21 and (not self.opponent_split or self.opponent_score2 > 21))
        
        if creator_bust and opponent_done:
            return True
        if opponent_bust and creator_done:
            return True
        
                                                    
        if self.creator_score == 21 or (self.creator_split and self.creator_score2 == 21):
            return True
        if self.opponent_score == 21 or (self.opponent_split and self.opponent_score2 == 21):
            return True
        
        return False
    
    def switch_turn(self):
        """Switch to the other player's turn"""
        if self.current_turn == self.creator_id:
            self.current_turn = self.opponent_id
        else:
            self.current_turn = self.creator_id
        self.current_hand = 1
    
    def get_current_player_name(self) -> str:
        """Get the name of the current player"""
        if self.current_turn == self.creator_id:
            return "CREATOR"
        else:
            return "Opponent"
    
    def determine_winner(self):
        """Determine the winner after both players have finished"""
                                                          
        creator_best = 0
        if self.creator_score <= 21:
            creator_best = max(creator_best, self.creator_score)
        if self.creator_split and self.creator_score2 <= 21:
            creator_best = max(creator_best, self.creator_score2)
        
        opponent_best = 0
        if self.opponent_score <= 21:
            opponent_best = max(opponent_best, self.opponent_score)
        if self.opponent_split and self.opponent_score2 <= 21:
            opponent_best = max(opponent_best, self.opponent_score2)
        
                          
        if creator_best > opponent_best:
            self.winner = self.creator_id
            self.loser = self.opponent_id
        elif opponent_best > creator_best:
            self.winner = self.opponent_id
            self.loser = self.creator_id
        else:
                        
            self.winner = None
            self.loser = None
        
        self.status = "completed"
        self.reveal_opponent_card = True
    
    def get_card_emoji(self, card: str) -> str:
        """Get emoji for a card"""
        return BLACKJACK_CARD_EMOJIS.get(card, f"`{card}`")
    
    def get_hand_display(self, hand: List[str], hidden: bool = False) -> str:
        """Get string display of a hand"""
        if not hand:
            return "No cards"
        
        if hidden:
                                                       
            display = []
            for i, card in enumerate(hand):
                if i == 0:
                    display.append(BLACKJACK_CARD_EMOJIS['BACK'])
                else:
                    display.append(self.get_card_emoji(card))
            return " ".join(display)
        else:
            return " ".join([self.get_card_emoji(card) for card in hand])
    
    def get_score_display(self, score: int, hand: List[str], hidden: bool = False) -> str:
        """Get score display"""
        if hidden and len(hand) > 0:
                                           
            visible_hand = hand[1:] if len(hand) > 1 else []
            if visible_hand:
                visible_score = self.calculate_score(visible_hand)
                return f"Score: ? + {visible_score} = ?"
            else:
                return "Score: ?"
        else:
            return f"Score: {score}"
    
    def to_dict(self):
        return {
            "game_id": self.game_id,
            "creator_id": self.creator_id,
            "creator_items": self.creator_items,
            "bet_value": self.bet_value,
            "opponent_id": self.opponent_id,
            "opponent_items": self.opponent_items,
            "status": self.status,
            "created_at": self.created_at,
            "message_id": self.message_id,
            "deck": self.deck,
            "creator_hand": self.creator_hand,
            "opponent_hand": self.opponent_hand,
            "creator_score": self.creator_score,
            "opponent_score": self.opponent_score,
            "creator_stand": self.creator_stand,
            "opponent_stand": self.opponent_stand,
            "creator_hand2": self.creator_hand2,
            "creator_score2": self.creator_score2,
            "creator_stand2": self.creator_stand2,
            "creator_split": self.creator_split,
            "opponent_hand2": self.opponent_hand2,
            "opponent_score2": self.opponent_score2,
            "opponent_stand2": self.opponent_stand2,
            "opponent_split": self.opponent_split,
            "current_hand": self.current_hand,
            "current_turn": self.current_turn,
            "winner": self.winner,
            "loser": self.loser,
            "reveal_opponent_card": self.reveal_opponent_card,
            "server_seed": self.server_seed,
            "server_seed_hash": self.server_seed_hash
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        game = cls(data["creator_id"], data["creator_items"], data["bet_value"])
        game.game_id = data["game_id"]
        game.opponent_id = data.get("opponent_id")
        game.opponent_items = data.get("opponent_items", [])
        game.status = data.get("status", "waiting")
        game.created_at = data.get("created_at")
        game.message_id = data.get("message_id")
        game.deck = data.get("deck", [])
        game.creator_hand = data.get("creator_hand", [])
        game.opponent_hand = data.get("opponent_hand", [])
        game.creator_score = data.get("creator_score", 0)
        game.opponent_score = data.get("opponent_score", 0)
        game.creator_stand = data.get("creator_stand", False)
        game.opponent_stand = data.get("opponent_stand", False)
                    
        game.creator_hand2 = data.get("creator_hand2", [])
        game.creator_score2 = data.get("creator_score2", 0)
        game.creator_stand2 = data.get("creator_stand2", False)
        game.creator_split = data.get("creator_split", False)
        game.opponent_hand2 = data.get("opponent_hand2", [])
        game.opponent_score2 = data.get("opponent_score2", 0)
        game.opponent_stand2 = data.get("opponent_stand2", False)
        game.opponent_split = data.get("opponent_split", False)
        game.current_hand = data.get("current_hand", 1)
        
        game.current_turn = data.get("current_turn")
        game.winner = data.get("winner")
        game.loser = data.get("loser")
        game.reveal_opponent_card = data.get("reveal_opponent_card", False)
        game.server_seed = data.get("server_seed") or generate_server_seed("blackjack", game.game_id, game.creator_id, int(datetime.now().timestamp()))
        game.server_seed_hash = data.get("server_seed_hash") or get_server_seed_hash(game.server_seed)
        
                                                 
        if game.status == "active" and len(game.creator_hand) == 0:
            game.creator_hand = [game.draw_card(), game.draw_card()]
            game.opponent_hand = [game.draw_card(), game.draw_card()]
            game.creator_score = game.calculate_score(game.creator_hand)
            game.opponent_score = game.calculate_score(game.opponent_hand)
        
        return game

def save_blackjack_game(game: BlackjackGame):
    """Save blackjack game to active games"""
    games = load_blackjack_games()
    games[game.game_id] = game.to_dict()
    save_blackjack_games(games)

def remove_blackjack_game(game_id: str):
    """Remove blackjack game from active games"""
    games = load_blackjack_games()
    if game_id in games:
        del games[game_id]
        save_blackjack_games(games)

                                      
class Listing:
    def __init__(self, seller_id: int, items: List[str], usd_price: float, listing_id: str = None):
        self.seller_id = seller_id
        self.items = items
        self.usd_price = usd_price
        self.listing_id = listing_id or f"listing_{seller_id}_{int(datetime.now().timestamp())}"
        self.created_at = datetime.now().isoformat()
        self.status = "active"                           
        self.buyer_id = None
        self.message_id = None
        self.channel_id = None
    
    def to_dict(self):
        return {
            "listing_id": self.listing_id,
            "seller_id": self.seller_id,
            "items": self.items,
            "usd_price": self.usd_price,
            "created_at": self.created_at,
            "status": self.status,
            "buyer_id": self.buyer_id,
            "message_id": self.message_id,
            "channel_id": self.channel_id
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        listing = cls(
            data["seller_id"],
            data["items"],
            data["usd_price"],
            data["listing_id"]
        )
        listing.created_at = data.get("created_at")
        listing.status = data.get("status", "active")
        listing.buyer_id = data.get("buyer_id")
        listing.message_id = data.get("message_id")
        listing.channel_id = data.get("channel_id")
        return listing

def save_listing(listing: Listing):
    """Save listing to active listings"""
    listings = load_listings()
    listings[listing.listing_id] = listing.to_dict()
    save_listings(listings)

def remove_listing(listing_id: str):
    """Remove listing from active listings"""
    listings = load_listings()
    if listing_id in listings:
        del listings[listing_id]
        save_listings(listings)

                                     
class ListingItemSelectionView(discord.ui.View):
    def __init__(self, user_items: List[Tuple[str, int]]):
        super().__init__(timeout=None)
        self.user_items = user_items
        self.selected_items = []
        
                      
        self.dropdown = ItemSelectDropdown(user_items, MAX_BET_VALUE)
        self.add_item(self.dropdown)
    
    @discord.ui.button(label="CONFIRM SELECTION", style=discord.ButtonStyle.secondary, row=1)
    async def confirm_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.dropdown.selected_items:
            await interaction.response.send_message(
                "Please select at least one item from the dropdown!",
                ephemeral=True
            )
            return
        
        self.selected_items = self.dropdown.selected_items
        self.selected_value = self.dropdown.selected_value
        
                                      
        valid, game_type, error_msg = validate_items_same_type(self.selected_items)
        if not valid:
            await interaction.response.send_message(
                f"❌ {error_msg}",
                ephemeral=True
            )
            return
        
                              
        modal = USDPriceModal(self.selected_items, self.selected_value)
        await interaction.response.send_modal(modal)
        
                          
        for child in self.children:
            child.disabled = True
        
        try:
            await interaction.message.edit(view=self)
        except:
            pass

class USDPriceModal(discord.ui.Modal, title="Set USD Price for Your Listing"):
    def __init__(self, selected_items: List[str], total_value: int):
        super().__init__()
        self.selected_items = selected_items
        self.total_value = total_value
    
    usd_price = discord.ui.TextInput(
        label="USD Price",
        placeholder="Enter the price in USD (e.g., 10.50)",
        required=True,
        max_length=10
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            usd_price = float(self.usd_price.value)
            if usd_price <= 0:
                await interaction.response.send_message(
                    "Price must be greater than 0!",
                    ephemeral=True
                )
                return
            
            if usd_price > 10000:                
                await interaction.response.send_message(
                    "Price cannot exceed $10,000!",
                    ephemeral=True
                )
                return
            
                                          
            valid, game_type, error_msg = validate_items_same_type(self.selected_items)
            if not valid:
                await interaction.response.send_message(
                    f"❌ {error_msg}",
                    ephemeral=True
                )
                return
            
                                                  
            remove_items_from_inventory(str(interaction.user.id), self.selected_items)
            
                            
            listing = Listing(interaction.user.id, self.selected_items, usd_price)
            
                                     
            listing_channel = bot.get_channel(LISTING_CHANNEL_ID)
            if not listing_channel:
                await interaction.response.send_message(
                    "Listing channel not found! Please contact an admin.",
                    ephemeral=True
                )
                                        
                add_items_to_inventory(str(interaction.user.id), self.selected_items)
                return
            
                                  
            total_item_value = self.total_value
            
                                     
            item_counts = {}
            for item in self.selected_items:
                item_counts[item] = item_counts.get(item, 0) + 1
            
            items_text = ""
            for item_name, count in item_counts.items():
                item_value = get_item_value(item_name)
                item_emoji = get_item_emoji(item_name)
                items_text += f"• {item_emoji} `{item_name}` x{count} ({VALUE_EMOJI} {format_item_value(item_value)} each)\n"
            
                                  
            embed = discord.Embed(
                title="NEW LISTING",
                color=discord.Color.green(),
                timestamp=datetime.now()
            )
            
                                                       
            registrations = load_registrations()
            user_data = registrations.get(str(interaction.user.id), {})
            roblox_username = user_data.get('roblox_username', interaction.user.display_name)
            roblox_avatar = user_data.get('roblox_avatar')
            
                                                            
            embed.set_thumbnail(url=roblox_avatar or interaction.user.display_avatar.url)
            
            embed.add_field(
                name="ITEMS:",
                value=items_text,
                inline=False
            )
            
            embed.add_field(
                name="PRICE",
                value=f"**${usd_price:.2f} USD**",
                inline=True
            )
            
            embed.add_field(
                name=f"TOTAL VALUE",
                value=f"{VALUE_EMOJI}**{format_item_value(total_item_value)}**",
                inline=True
            )
            
            embed.set_footer(text=f"Listing ID: {listing.listing_id}")
            
                                 
            view = ListingView(listing.listing_id, interaction.user.id, usd_price)
            
                                     
            message = await listing_channel.send(embed=embed, view=view)
            
                               
            listing.message_id = message.id
            listing.channel_id = listing_channel.id
            save_listing(listing)
            
                                         
            confirm_embed = discord.Embed(
                title="Listing Created Successfully!",
                color=discord.Color.green(),
                description=f"Your items have been listed for **${usd_price:.2f} USD** in {listing_channel.mention}."
            )
            
                                                      
            if roblox_avatar:
                confirm_embed.set_thumbnail(url=roblox_avatar)
            
            confirm_embed.add_field(
                name="Your Listing:",
                value=f"[Jump to Listing](https://discord.com/channels/{interaction.guild.id}/{listing_channel.id}/{message.id})",
                inline=False
            )
            
            confirm_embed.add_field(
                name="Important",
                value="• Items are removed from your inventory while listed!\n• You can cancel the listing anytime.\n• Once sold there are no refunds!",
                inline=False
            )
            
            await interaction.response.send_message(embed=confirm_embed, ephemeral=True)
            
        except ValueError:
            await interaction.response.send_message(
                "Please enter a valid number for the price!",
                ephemeral=True
            )
        except Exception as e:
            print(f"Error creating listing: {e}")
            await interaction.response.send_message(
                "An error occurred while creating the listing. Please try again.",
                ephemeral=True
            )

class ListingView(discord.ui.View):
    def __init__(self, listing_id: str, seller_id: int, asking_price: float):
        super().__init__(timeout=None)                   
        self.listing_id = listing_id
        self.seller_id = seller_id
        self.asking_price = asking_price
    
    @discord.ui.button(label="BUY", style=discord.ButtonStyle.secondary, row=0)
    async def buy_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_user_registered(interaction.user.id):
            await interaction.response.send_message(
                "You need to register first! Use `/register` to get started.",
                ephemeral=True
            )
            return

        if interaction.user.id == self.seller_id:
            await interaction.response.send_message(
                "You cannot buy your own listing.",
                ephemeral=True
            )
            return

        listings = load_listings()
        listing_data = listings.get(self.listing_id)

        if not listing_data or listing_data.get('status') != 'active':
            await interaction.response.send_message(
                "This listing is no longer available!",
                ephemeral=True
            )
            return

        price = float(listing_data.get('usd_price', 0.0))
        buyer_id = str(interaction.user.id)
        seller_id = str(self.seller_id)
        buyer_balance = get_user_balance(buyer_id)

        if buyer_balance < price:
            await interaction.response.send_message(
                f"Insufficient USD balance. You need **${price:.2f} USD** to buy this listing.",
                ephemeral=True
            )
            return

        if not subtract_user_balance(buyer_id, price):
            await interaction.response.send_message(
                "Unable to deduct your balance. Please try again.",
                ephemeral=True
            )
            return

        add_user_balance(seller_id, price)
        add_items_to_inventory(buyer_id, listing_data['items'])

        listing_data['status'] = 'sold'
        listing_data['buyer_id'] = interaction.user.id
        listings[self.listing_id] = listing_data
        save_listings(listings)

        try:
            channel = bot.get_channel(listing_data.get('channel_id', LISTING_CHANNEL_ID))
            if channel and listing_data.get('message_id'):
                message = await channel.fetch_message(listing_data['message_id'])
                
                if message.embeds:
                    embed = message.embeds[0]
                    embed.title = "LISTING SOLD"
                    embed.color = discord.Color.red()
                else:
                    embed = discord.Embed(
                        title="LISTING SOLD",
                        color=discord.Color.red(),
                        timestamp=datetime.now()
                    )

                for child in self.children:
                    child.disabled = True
                await message.edit(embed=embed, view=self)
        except Exception as e:
            print(f"Error updating sold listing message: {e}")

    
    @discord.ui.button(label="CANCEL", style=discord.ButtonStyle.danger, row=0)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                                     
        if interaction.user.id != self.seller_id:
            await interaction.response.send_message(
                "Only the seller can cancel this listing!",
                ephemeral=True
            )
            return
        
                     
        listings = load_listings()
        listing_data = listings.get(self.listing_id)
        
        if not listing_data:
            await interaction.response.send_message(
                "This listing no longer exists!",
                ephemeral=True
            )
            return
        
        if listing_data['status'] != 'active':
            await interaction.response.send_message(
                "This listing is already closed!",
                ephemeral=True
            )
            return
        
                                
        add_items_to_inventory(str(self.seller_id), listing_data['items'])
        
                               
        listing_data['status'] = 'cancelled'
        save_listings(listings)
        
                                  
        registrations = load_registrations()
        seller_data = registrations.get(str(self.seller_id), {})
        roblox_username = seller_data.get('roblox_username', "Unknown")
        
                                    
        try:
            channel = bot.get_channel(listing_data.get('channel_id', LISTING_CHANNEL_ID))
            if channel and listing_data.get('message_id'):
                message = await channel.fetch_message(listing_data['message_id'])
                
                embed = message.embeds[0]
                embed.color = discord.Color.red()
                embed.title = "LISTING CANCELLED"
                
                embed.set_footer(text=f"Listing ID: {self.listing_id}")
                
                                     
                for child in self.children:
                    child.disabled = True
                
                await message.edit(embed=embed, view=self)
        except Exception as e:
            print(f"Error updating cancelled listing: {e}")
        
                                     
        await interaction.response.send_message(
            "Listing cancelled! Your items have been returned to your inventory.",
            ephemeral=True
        )
        
                                         
        remove_listing(self.listing_id)

                                            
class BlackjackJoinView(discord.ui.View):
    def __init__(self, game_id: str, creator_id: int, bet_value: int):
        super().__init__(timeout=None)                   
        self.game_id = game_id
        self.creator_id = creator_id
        self.bet_value = bet_value
    
    @discord.ui.button(label="JOIN", style=discord.ButtonStyle.secondary, row=0)
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                                     
        if not is_user_registered(interaction.user.id):
            await interaction.response.send_message(
                "You need to register first! Use `/register` to get started.",
                ephemeral=True
            )
            return
        
                                                        
        if interaction.user.id == self.creator_id:
            await interaction.response.send_message(
                "You can't join your own game!",
                ephemeral=True
            )
            return
        
                  
        games = load_blackjack_games()
        game_data = games.get(self.game_id)
        
        if not game_data:
            await interaction.response.send_message(
                "This game no longer exists or has expired!",
                ephemeral=True
            )
            return
        
        if game_data.get('opponent_id'):
            await interaction.response.send_message(
                "This game already has an opponent!",
                ephemeral=True
            )
            return
        
        if game_data['status'] != 'waiting':
            await interaction.response.send_message(
                "This game is no longer accepting joins!",
                ephemeral=True
            )
            return
        
        required_value = game_data['bet_value']
        
                                                         
        min_allowed = required_value * 0.9
        max_allowed = required_value * 1.1
        
                                     
        user_items = get_user_all_items(str(interaction.user.id))
        
        if not user_items:
            await interaction.response.send_message(
                "You don't have any items to bet!",
                ephemeral=True
            )
            return
        
                                              
        user_total_value = calculate_inventory_value(str(interaction.user.id))
        if user_total_value < min_allowed:
            await interaction.response.send_message(
                f"You need at least {VALUE_EMOJI} **{format_value_with_commas(min_allowed)}** in items to join this game!\n"
                f"Your current inventory value: {VALUE_EMOJI} **{format_value_with_commas(user_total_value)}**",
                ephemeral=True
            )
            return
        
                                      
        embed = discord.Embed(
            title="Select Your Items",
            description=f"Select items worth between {VALUE_EMOJI} **{format_value_with_commas(min_allowed)}** and {VALUE_EMOJI} **{format_value_with_commas(max_allowed)}** to join this Blackjack game.",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="Instructions",
            value=f"1. Select items from the dropdown\n2. You can select multiple items\n3. Total value must be within 10% of the game bet ({VALUE_EMOJI} **{format_value_with_commas(required_value)}**)\n4. Click 'Confirm Selection' when done",
            inline=False
        )
        
        view = ItemSelectionView(user_items, required_value, self.game_id, is_blackjack=True, allow_range=True)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    @discord.ui.button(label="CANCEL", style=discord.ButtonStyle.danger, row=0)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                                      
        if interaction.user.id != self.creator_id:
            await interaction.response.send_message(
                "Only the game creator can cancel the game!",
                ephemeral=True
            )
            return
        
                  
        games = load_blackjack_games()
        game_data = games.get(self.game_id)
        
        if not game_data:
            await interaction.response.send_message(
                "This game no longer exists!",
                ephemeral=True
            )
            return
        
        if game_data.get('opponent_id'):
            await interaction.response.send_message(
                "Cannot cancel game with an opponent!",
                ephemeral=True
            )
            return
        
                                 
        creator_items = game_data['creator_items']
        add_items_to_inventory(str(self.creator_id), creator_items)
        
                     
        remove_blackjack_game(self.game_id)
        
                                 
        try:
            embed = discord.Embed(
                title="BLACKJACK GAME CANCELLED",
                description=f"This game has been cancelled by the creator.",
                color=discord.Color.red()
            )
            
            embed.add_field(
                name="Items Returned",
                value=f"All items have been returned to <@{self.creator_id}>",
                inline=False
            )
            
                                 
            for child in self.children:
                child.disabled = True
            
            await interaction.response.edit_message(embed=embed, view=self)
            
                                          
            await interaction.followup.send(
                f"Game cancelled! Your items have been returned to your inventory.",
                ephemeral=True
            )
        except Exception as e:
            print(f"Error cancelling game: {e}")
            await interaction.response.send_message(
                f"Game cancelled! Your items have been returned to your inventory.",
                ephemeral=True
            )

class BlackjackGameView(discord.ui.View):
    def __init__(self, game_id: str, current_player_id: int):
        super().__init__(timeout=None)
        self.game_id = game_id
        self.current_player_id = current_player_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
                                              
        games = load_blackjack_games()
        game_data = games.get(self.game_id)
        if not game_data:
            await interaction.response.send_message("This game no longer exists!", ephemeral=True)
            return False
        game = BlackjackGame.from_dict(game_data)
        if game.status == "completed":
            await interaction.response.send_message("Game is already finished.", ephemeral=True)
            return False
        return True
    
    @discord.ui.button(label="HIT", style=discord.ButtonStyle.secondary, row=0)
    async def hit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                                   
        games = load_blackjack_games()
        game_data = games.get(self.game_id)
        
        if not game_data:
            await interaction.response.send_message(
                "This game no longer exists!",
                ephemeral=True
            )
            return
        
        game = BlackjackGame.from_dict(game_data)
        
        if interaction.user.id != game.current_turn:
            player_name = await get_player_display_name(game.current_turn)
            await interaction.response.send_message(
                f"Not your turn! It's **{player_name}**'s turn.",
                ephemeral=True
            )
            return
        
        if interaction.user.id not in [game.creator_id, game.opponent_id]:
            await interaction.response.send_message(
                "You're not in this game!",
                ephemeral=True
            )
            return
        
                     
        success, message, game_ended = game.hit(interaction.user.id)
        
        if not success:
            await interaction.response.send_message(message, ephemeral=True)
            return
        
                         
        save_blackjack_game(game)
        
                        
        await update_blackjack_message(interaction, game)
        
                                 
        await interaction.response.send_message(message, ephemeral=True)
        
                             
        if game_ended or game.status == "completed":
            await complete_blackjack_game(interaction, game.game_id, game.to_dict())

    @discord.ui.button(label="SPLIT", style=discord.ButtonStyle.secondary, row=1)
    async def split_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                                          
        games = load_blackjack_games()
        game_data = games.get(self.game_id)
        if not game_data:
            await interaction.response.send_message("This game no longer exists!", ephemeral=True)
            return
        game = BlackjackGame.from_dict(game_data)
        if interaction.user.id != game.current_turn:
            player_name = await get_player_display_name(game.current_turn)
            await interaction.response.send_message(
                f"Not your turn! It's **{player_name}**'s turn.",
                ephemeral=True
            )
            return
        if interaction.user.id not in [game.creator_id, game.opponent_id]:
            await interaction.response.send_message("You're not in this game!", ephemeral=True)
            return
        success, msg = game.split(interaction.user.id)
        if not success:
            await interaction.response.send_message(msg, ephemeral=True)
            return
                         
        save_blackjack_game(game)
        await update_blackjack_message(interaction, game)
        await interaction.response.send_message(msg, ephemeral=True)
    
    @discord.ui.button(label="STAND", style=discord.ButtonStyle.secondary, row=0)
    async def stand_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                                   
        games = load_blackjack_games()
        game_data = games.get(self.game_id)
        
        if not game_data:
            await interaction.response.send_message(
                "This game no longer exists!",
                ephemeral=True
            )
            return
        
        game = BlackjackGame.from_dict(game_data)
        
        if interaction.user.id != game.current_turn:
            player_name = await get_player_display_name(game.current_turn)
            await interaction.response.send_message(
                f"Not your turn! It's **{player_name}**'s turn.",
                ephemeral=True
            )
            return
        
        if interaction.user.id not in [game.creator_id, game.opponent_id]:
            await interaction.response.send_message(
                "You're not in this game!",
                ephemeral=True
            )
            return
        
                       
        success, message, game_ended = game.stand(interaction.user.id)
        
        if not success:
            await interaction.response.send_message("Failed to stand!", ephemeral=True)
            return
        
                         
        save_blackjack_game(game)
        
                        
        await update_blackjack_message(interaction, game)
        
                                 
        await interaction.response.send_message(message, ephemeral=True)
        
                             
        if game_ended or game.status == "completed":
            await complete_blackjack_game(interaction, game.game_id, game.to_dict())

async def update_blackjack_message(interaction: discord.Interaction, game: BlackjackGame):
    """Update the blackjack game message"""
    try:
        channel = interaction.channel
        if isinstance(channel, discord.TextChannel) and game.message_id:
            message = await channel.fetch_message(game.message_id)
            
            creator = await bot.fetch_user(game.creator_id)
            opponent = await bot.fetch_user(game.opponent_id)
            
            embed = discord.Embed(
                title="BLACKJACK PVP",
                color=discord.Color.green()
            )
            
                                                       
            if game.status == "completed":
                if game.winner:
                    winner_user = await bot.fetch_user(game.winner)
                    embed.add_field(
                        name="RESULT",
                        value=f"**{winner_user.mention}** wins!",
                        inline=False
                    )
                else:
                    embed.add_field(
                        name="RESULT",
                        value="Push - tie game",
                        inline=False
                    )
            else:
                current_player = await bot.fetch_user(game.current_turn)
                embed.add_field(
                    name="TURN",
                    value=f"**{current_player.mention}**'s turn",
                    inline=False
                )
            
                                                 
            creator_hand_display = game.get_hand_display(game.creator_hand)
            creator_score_display = game.get_score_display(game.creator_score, game.creator_hand)
                                          
            if game.creator_split:
                c2_display = game.get_hand_display(game.creator_hand2)
                c2_score = game.get_score_display(game.creator_score2, game.creator_hand2)
                creator_hand_display = f"{creator_hand_display}\n---split---\n{c2_display}"
                creator_score_display = f"{creator_score_display}\n{c2_score}"
            
                                                  
            opponent_hidden = False
            opponent_hand_display = game.get_hand_display(game.opponent_hand, opponent_hidden)
            opponent_score_display = game.get_score_display(game.opponent_score, game.opponent_hand, opponent_hidden)
                                          
            if game.opponent_split:
                opp2_display = game.get_hand_display(game.opponent_hand2, opponent_hidden)
                opp2_score = game.get_score_display(game.opponent_score2, game.opponent_hand2, opponent_hidden)
                opponent_hand_display = f"{opponent_hand_display}\n---split---\n{opp2_display}"
                opponent_score_display = f"{opponent_score_display}\n{opp2_score}"
            
            embed.add_field(
                name=f"{creator.name}'s Hand",
                value=f"{creator_hand_display}\n{creator_score_display}" + 
                      ("\n**STAND**" if game.creator_stand else ""),
                inline=True
            )
            
            embed.add_field(
                name=f"{opponent.name}'s Hand",
                value=f"{opponent_hand_display}\n{opponent_score_display}" + 
                      ("\n**STAND**" if game.opponent_stand else ""),
                inline=True
            )
            
            embed.add_field(
                name="BET VALUE",
                value=f"{VALUE_EMOJI} **{format_value_with_commas(game.bet_value)}**",
                inline=True
            )
            
            embed.add_field(
                name="TOTAL POT",
                value=f"{VALUE_EMOJI} **{format_value_with_commas(game.bet_value * 2)}**",
                inline=True
            )
            
            embed.set_footer(text="Click HIT to draw a card, STAND to keep your hand")
            
            view = BlackjackGameView(game.game_id, game.current_turn)
                                                  
            if game.status == "completed":
                for child in view.children:
                    child.disabled = True
            else:
                                                                      
                for child in view.children:
                    if isinstance(child, discord.ui.Button) and child.label == "SPLIT":
                        child.disabled = not game.can_split(game.current_turn)
            await message.edit(embed=embed, view=view)
    
    except Exception as e:
        print(f"Error updating blackjack message: {e}")

async def complete_blackjack_game_setup(interaction: discord.Interaction, game_id: str, game_data: dict):
    """Complete blackjack game setup and start the game"""
               
    games = load_blackjack_games()
    game_dict = games.get(game_id)
    
    if not game_dict:
        await interaction.followup.send("Game not found!", ephemeral=True)
        return
    
    game = BlackjackGame.from_dict(game_dict)
    
                                 
    game.creator_hand = [game.draw_card(), game.draw_card()]
    game.opponent_hand = [game.draw_card(), game.draw_card()]
    game.creator_score = game.calculate_score(game.creator_hand)
    game.opponent_score = game.calculate_score(game.opponent_hand)
    game.status = "active"

                                             
    if game.creator_score == 21 or game.opponent_score == 21:
                                                             
        game.determine_winner()
        save_blackjack_game(game)
        await update_blackjack_message(interaction, game)
        msg = "Blackjack! "
        if game.winner is None:
            msg += "Both players got 21 – it's a push."
        else:
            msg += f"<@{game.winner}> wins with a natural 21!"
        await interaction.followup.send(msg, ephemeral=True)
        return
    
               
    save_blackjack_game(game)
    
                    
    await update_blackjack_message(interaction, game)
    
                       
    await interaction.followup.send(
        f"Blackjack game started! It's now **{game.current_turn}**'s turn.",
        ephemeral=True
    )

async def complete_blackjack_game(interaction: discord.Interaction, game_id: str, game_data: dict):
    """Complete the blackjack game"""
    game = BlackjackGame.from_dict(game_data)
    
                 
    winner = await bot.fetch_user(game.winner) if game.winner else None
    loser = await bot.fetch_user(game.loser) if game.loser else None
                                             
    all_items = game.creator_items + game.opponent_items
    try:
        valid, gtype, _ = validate_items_same_type(all_items)
    except Exception:
        valid, gtype = False, None
    creator = await bot.fetch_user(game.creator_id)
    opponent = await bot.fetch_user(game.opponent_id)
    
                              
    total_pot = game.bet_value * 2
    tax_amount = calculate_tax(total_pot)
    net_winnings = calculate_net_winnings(total_pot)
    
                                         
    if game.winner and game.loser:
                                      
        winner_id_str = str(game.winner)
        loser_id_str = str(game.loser)
        
                                          
        all_items = game.creator_items + game.opponent_items
        
                               
        remaining_items, taxed_items = deduct_tax_from_items(all_items, tax_amount)
        
                         
        await log_taxed_items(
            source_game="Blackjack",
            winner_id=game.winner,
            loser_id=game.loser,
            tax_amount=tax_amount,
            items=taxed_items,
            pot_value=total_pot
        )
        
        add_items_to_inventory(winner_id_str, remaining_items)
        
                                         
        item_counts = {}
        for item in remaining_items:
            item_counts[item] = item_counts.get(item, 0) + 1
        
        items_summary = ""
        for item_name, count in list(item_counts.items())[:10]:
            item_value = get_item_value(item_name)
            item_emoji = get_item_emoji(item_name)
            total_value = item_value * count
            items_summary += f"• {item_emoji} `{item_name}` x{count} ({VALUE_EMOJI} {format_value_with_commas(item_value)} each)\n"
        
        if len(item_counts) > 10:
            items_summary += f"• ...and {len(item_counts)-10} more item types\n"
        
        total_items_count = len(remaining_items)
        
    else:
                                                      
        add_items_to_inventory(str(game.creator_id), game.creator_items)
        add_items_to_inventory(str(game.opponent_id), game.opponent_items)
        tax_amount = 0
        total_items_count = 0
        items_summary = ""
    
                         
    result_embed = discord.Embed(
        title="BLACKJACK GAME OVER",
        color=discord.Color.green() if game.winner else discord.Color.greyple()
    )
    
    if game.winner and game.loser:
        result_embed.add_field(
            name="WINNER",
            value=winner.mention if winner else "Unknown",
            inline=True
        )
        
        result_embed.add_field(
            name="LOSER",
            value=loser.mention if loser else "Unknown",
            inline=True
        )
        
        result_embed.add_field(
            name="WINNINGS",
            value=f"{VALUE_EMOJI} **{format_value_with_commas(total_pot)}**",
            inline=True
        )
        
                        
        if items_summary:
            result_embed.add_field(
                name=f"Items Won",
                value=items_summary,
                inline=False
            )
        else:
            result_embed.add_field(
                name="Items Won",
                value="No items won",
                inline=False
            )
        
    else:
        result_embed.add_field(
            name="RESULT",
            value="PUSH! Bets returned to both players.",
            inline=False
        )
        
        result_embed.add_field(
            name="SCORES",
            value=f"{creator.name}: **{game.creator_score}**\n{opponent.name}: **{game.opponent_score}**",
            inline=False
        )
    
                      
    result_embed.add_field(
        name=f"{creator.name}'s Final Hand",
        value=f"{game.get_hand_display(game.creator_hand)}\nScore: **{game.creator_score}**",
        inline=True
    )
    
    result_embed.add_field(
        name=f"{opponent.name}'s Final Hand",
        value=f"{game.get_hand_display(game.opponent_hand)}\nScore: **{game.opponent_score}**",
        inline=True
    )
    
    result_embed.set_footer(text="Game Complete")
    
                                   
    remove_blackjack_game(game_id)

                                                                     
    try:
        all_items = game.creator_items + game.opponent_items
        ok, gtype, _ = validate_items_same_type(all_items)
        if ok and gtype in (GameType.MM2, GameType.ADM):
                                                              
            creator_wager = sum(get_item_value(it) for it in game.creator_items)
            opponent_wager = sum(get_item_value(it) for it in game.opponent_items)
            try:
                add_user_wager(game.creator_id, gtype, creator_wager)
            except Exception:
                pass
            try:
                add_user_wager(game.opponent_id, gtype, opponent_wager)
            except Exception:
                pass
                                             
            try:
                record_completed_game({
                    "game_id": game_id,
                    "game_type": gtype,
                    "participants": [int(game.creator_id), int(game.opponent_id)],
                    "per_player": {
                        str(game.creator_id): creator_wager,
                        str(game.opponent_id): opponent_wager
                    },
                    "total_pot": total_pot,
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                print(f"Error recording completed blackjack game: {e}")
    except Exception:
        pass
    
                                        
    try:
        if game.message_id:
            channel = interaction.channel
            if isinstance(channel, discord.TextChannel):
                message = await channel.fetch_message(game.message_id)
                
                                     
                for child in message.components:
                    for button in child.children:
                        button.disabled = True
                
                                           
                await message.edit(
                    content="",
                    embed=result_embed,
                    view=None
                )
                
                await interaction.followup.send("Game completed! Check the updated game message above.", ephemeral=True)
                return
    
    except Exception as e:
        print(f"Error updating blackjack message: {e}")
    
                                
    await interaction.followup.send(embed=result_embed)

                                          
class MinesGame:
    def __init__(self, creator_id: int, creator_items: List[str], bet_value: int, mine_count: int = 1):
        self.creator_id = creator_id
        self.creator_items = creator_items
        self.bet_value = bet_value
        self.mine_count = mine_count
        self.opponent_id = None
        self.opponent_items = []
        self.status = "waiting"                                         
        self.game_id = f"mines_{creator_id}_{int(datetime.now().timestamp())}"
        self.server_seed = generate_server_seed("mines", self.game_id, creator_id, int(datetime.now().timestamp()))
        self.server_seed_hash = get_server_seed_hash(self.server_seed)
        self.created_at = datetime.now().isoformat()
        self.message_id = None
        
                    
        self.board_size = MINES_BOARD_SIZE
        self.total_cells = self.board_size * self.board_size
        self.wild_mode = False
        
                             
        if self.mine_count < MINES_MIN_COUNT:
            self.mine_count = MINES_MIN_COUNT
        elif self.mine_count > MINES_MAX_COUNT:
            self.mine_count = MINES_MAX_COUNT
        
                                
        self.mines = []                                
        self.revealed = set()                                       
        self.current_turn = None                                            
        self.winner = None
        self.loser = None
        
                                             
        self.mines_generated = False
    
    def generate_board(self):
        """Generate mines for the game"""
        all_cells = list(range(self.total_cells))
        
                                         
        self.wild_mode = deterministic_boolean(self.server_seed, "mines", "wild_mode", WILD_MODE_CHANCE)
        
                                         
        if self.wild_mode:
            self.mine_count += MINES_WILD_EXTRA_MINES
        
                                                            
        if self.mine_count >= self.total_cells:
            self.mine_count = self.total_cells - 1
        
                                        
        self.mines = deterministic_sample(self.server_seed, all_cells, self.mine_count, "mines")
        
                                    
        self.current_turn = deterministic_choice(self.server_seed, [self.creator_id, self.opponent_id], "mines_turn")
        self.mines_generated = True
    
    def make_move(self, player_id: int, cell_index: int) -> Tuple[bool, bool]:
        """
        Make a move on the board
        Returns: (is_valid_move, is_mine_hit)
        """
                                     
        if player_id != self.current_turn:
            return False, False
        
                                           
        if cell_index in self.revealed:
            return False, False
        
                                
        if not (0 <= cell_index < self.total_cells):
            return False, False
        
                         
        self.revealed.add(cell_index)
        
                              
        if cell_index in self.mines:
                                                   
            if self.wild_mode:
                self.winner = player_id                                              
                self.loser = self.opponent_id if player_id == self.creator_id else self.creator_id
            else:
                self.winner = self.opponent_id if player_id == self.creator_id else self.creator_id
                self.loser = player_id
            self.status = "completed"
            return True, True
        
                      
        self.current_turn = self.opponent_id if player_id == self.creator_id else self.creator_id
        
                                                                             
        safe_cells = self.total_cells - self.mine_count
        if len(self.revealed) == safe_cells:
                                             
            self.winner = player_id
            self.loser = self.opponent_id if player_id == self.creator_id else self.creator_id
            self.status = "completed"
        
        return True, False
    
    def get_board_display(self) -> str:
        """Get string representation of current board state"""
        board_str = ""
        for row in range(self.board_size):
            row_str = ""
            for col in range(self.board_size):
                cell_index = row * self.board_size + col
                
                if cell_index in self.revealed:
                    if cell_index in self.mines:
                        row_str += f"{MINES_HIT_EMOJI} "
                    else:
                        row_str += f"{MINES_SAFE_EMOJI} "
                else:
                                                     
                    row_str += f"{MINES_CELL_LABELS[cell_index]} "
            
            board_str += row_str + "\n"
        
        return board_str.strip()
    
    def get_simple_board_display(self) -> str:
        """Get simple board display like your old system"""
        safe_count = len([c for c in self.revealed if c not in self.mines])
        mine_hits = len([c for c in self.revealed if c in self.mines])
        
        return f"**Board:** 5x5\n" \
               f"**Safe cells revealed:** {safe_count}\n" \
               f"**Mines hit:** {mine_hits}\n" \
               f"**Mines remaining:** {self.mine_count - mine_hits}\n" \
               f"**Cells remaining:** {self.total_cells - len(self.revealed)}"
    
    def get_final_board_display(self, losing_cell=None) -> str:
        """Get final board display like your old system"""
        display = []
        
        for i in range(self.total_cells):
            if i == losing_cell:
                display.append(f"{MINES_HIT_EMOJI}")
            elif i in self.mines:
                display.append(f"{MINES_HIT_EMOJI}")
            elif i in self.revealed:
                display.append(f"{MINES_SAFE_EMOJI}")
            else:
                display.append("<:value3:1528632728197660793>")                          
        
        rows = []
        for i in range(0, len(display), 5):
            row = display[i:i + 5]
            rows.append(' '.join(row))
        
        return '\n'.join(rows)
    
    def to_dict(self):
        return {
            "game_id": self.game_id,
            "creator_id": self.creator_id,
            "creator_items": self.creator_items,
            "bet_value": self.bet_value,
            "mine_count": self.mine_count,
            "opponent_id": self.opponent_id,
            "opponent_items": self.opponent_items,
            "status": self.status,
            "created_at": self.created_at,
            "message_id": self.message_id,
            "board_size": self.board_size,
            "total_cells": self.total_cells,
            "wild_mode": self.wild_mode,
            "mines": self.mines if self.mines_generated else [],
            "revealed": list(self.revealed),
            "current_turn": self.current_turn,
            "winner": self.winner,
            "loser": self.loser,
            "mines_generated": self.mines_generated,
            "server_seed": self.server_seed,
            "server_seed_hash": self.server_seed_hash
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        game = cls(data["creator_id"], data["creator_items"], data["bet_value"], data.get("mine_count", 1))
        game.game_id = data["game_id"]
        game.opponent_id = data.get("opponent_id")
        game.opponent_items = data.get("opponent_items", [])
        game.status = data.get("status", "waiting")
        game.created_at = data.get("created_at")
        game.message_id = data.get("message_id")
        game.wild_mode = data.get("wild_mode", False)
        game.mines = data.get("mines", [])
        game.revealed = set(data.get("revealed", []))
        game.current_turn = data.get("current_turn")
        game.winner = data.get("winner")
        game.loser = data.get("loser")
        game.mines_generated = data.get("mines_generated", False)
        game.server_seed = data.get("server_seed") or generate_server_seed("mines", game.game_id, game.creator_id, int(datetime.now().timestamp()))
        game.server_seed_hash = data.get("server_seed_hash") or get_server_seed_hash(game.server_seed)
        return game

def save_mines_game(game: MinesGame):
    """Save mines game to active games"""
    games = load_mines_games()
    games[game.game_id] = game.to_dict()
    save_mines_games(games)

def remove_mines_game(game_id: str):
    """Remove mines game from active games"""
    games = load_mines_games()
    if game_id in games:
        del games[game_id]
        save_mines_games(games)

                                         
class TowersGame:
    def __init__(self, creator_id: int, creator_items: List[str], bet_value: int):
        self.creator_id = creator_id
        self.creator_items = creator_items
        self.bet_value = bet_value
        self.opponent_id = None
        self.opponent_items = []
        self.status = "waiting"                                         
        self.game_id = f"towers_{creator_id}_{int(datetime.now().timestamp())}"
        self.server_seed = generate_server_seed("towers", self.game_id, creator_id, int(datetime.now().timestamp()))
        self.server_seed_hash = get_server_seed_hash(self.server_seed)
        self.created_at = datetime.now().isoformat()
        self.message_id = None
        
                    
        self.width = TOWERS_WIDTH             
        self.height = TOWERS_HEIGHT          
        self.total_cells = TOWERS_TOTAL_CELLS            
        self.bomb_count = TOWERS_BOMB_COUNT          
        
                                
        self.bombs = set()                                
        self.revealed = set()                                       
        self.current_turn = None                                            
        self.winner = None
        self.loser = None
        self.round = 1                                                
        
                                            
        self.bomb_generated = False
                                                                                 
        self.past_revealed = set()
                                                                   
        self.next_row = 0
    
    def generate_board(self):
        """Generate bomb positions for the game - one bomb per row"""
        self.bombs = set()
        
                                    
        for row in range(self.height):          
            row_start = row * self.width                  
            row_cells = [row_start + col for col in range(self.width)]                          
            bomb_cell = deterministic_choice(self.server_seed, row_cells, f"towers_row_{row}")
            self.bombs.add(bomb_cell)
        
                                    
        self.current_turn = deterministic_choice(self.server_seed, [self.creator_id, self.opponent_id], "towers_turn")
        self.bomb_generated = True
                                  
        self.next_row = 0
    
    def is_row_clicked(self, cell_index: int) -> bool:
        """Check if any cell in the same row has already been clicked"""
        row = cell_index // self.width
        row_cells = [row * self.width + i for i in range(self.width)]
        return any(cell in self.revealed for cell in row_cells)
    
    def make_move(self, player_id: int, cell_index: int) -> Tuple[bool, bool]:
        """
        Make a move on the board
        Returns: (is_valid_move, is_bomb_hit)
        """
                                     
        if player_id != self.current_turn:
            return False, False
        
                                           
        if cell_index in self.revealed:
            return False, False
        
                                
        if not (0 <= cell_index < self.total_cells):
            return False, False
                                                                                    
        row = cell_index // self.width
        if row != self.next_row:
            return False, False
        
                         
        self.revealed.add(cell_index)
        
                                
        if cell_index in self.bombs:
                                             
            self.winner = self.opponent_id if player_id == self.creator_id else self.creator_id
            self.loser = player_id
            self.status = "completed"
            return True, True
        
                      
        self.current_turn = self.opponent_id if player_id == self.creator_id else self.creator_id
                                            
        self.next_row += 1
                                                                      
        if row == self.height - 1:                                  
                                                                                    
            self.round += 1
            self.reset_round()
        
        return True, False
    
    def reset_round(self):
        """Reset the board for a new round while keeping game active"""
                                                         
        self.past_revealed |= self.revealed
        self.revealed.clear()
        self.bombs = set()

        for row in range(self.height):
            row_start = row * self.width
            row_cells = [row_start + col for col in range(self.width)]
            bomb_cell = deterministic_choice(self.server_seed, row_cells, f"towers_round_{self.round}_row_{row}")
            self.bombs.add(bomb_cell)
                                          
                                                
        self.next_row = 0

    def get_board_display(self) -> str:
        """Get string representation of current board state"""
        board_str = ""
                                                                                           
        for row_start in range((self.height - 1) * self.width, -1, -self.width):
            row_str = ""
            for col in range(self.width):
                cell_index = row_start + col

                if cell_index in self.revealed:
                    if cell_index in self.bombs:
                        row_str += f"{WILD_MODE_EMOJI} "
                    else:
                        row_str += f"{MINES_SAFE_EMOJI} "
                else:
                                                     
                    row_str += f"{TOWERS_CELL_LABELS[cell_index]} "

            board_str += row_str + "\n"
        
        return board_str.strip()
    
    def get_simple_board_display(self) -> str:
        """Get simple board display"""
        safe_count = len([c for c in self.revealed if c not in self.bombs])
        bomb_hits = 1 if any(c in self.bombs for c in self.revealed) else 0
        
        return f"**Board:** 3x5 (15 cells)\n" \
               f"**Safe cells revealed:** {safe_count}\n" \
               f"**Bomb hit:** {'Yes' if bomb_hits else 'No'}\n" \
               f"**Cells remaining:** {self.total_cells - len(self.revealed)}"
    
    def get_final_board_display(self, losing_cell=None) -> str:
        """Get final board display"""
        display = []
        
        for i in range(self.total_cells):
                                            
            if i == losing_cell:
                display.append(f"{WILD_MODE_EMOJI}")
                                                                
            elif i in self.revealed or i in getattr(self, 'past_revealed', set()):
                display.append(f"{MINES_SAFE_EMOJI}")
                                  
            elif i in self.bombs:
                display.append(f"{WILD_MODE_EMOJI}")
            else:
                display.append("<:value3:1528632728197660793>")                          
        
        rows = []
                                                                                  
        for row_start in range((self.height - 1) * self.width, -1, -self.width):
            row = display[row_start:row_start + self.width]
            rows.append(' '.join(row))

        return '\n'.join(rows)
    
    def to_dict(self):
        return {
            "game_id": self.game_id,
            "creator_id": self.creator_id,
            "creator_items": self.creator_items,
            "bet_value": self.bet_value,
            "opponent_id": self.opponent_id,
            "opponent_items": self.opponent_items,
            "status": self.status,
            "created_at": self.created_at,
            "message_id": self.message_id,
            "width": self.width,
            "height": self.height,
            "total_cells": self.total_cells,
            "bomb_count": self.bomb_count,
            "bomb": list(self.bombs),
            "revealed": list(self.revealed),
            "past_revealed": list(self.past_revealed),
            "current_turn": self.current_turn,
            "winner": self.winner,
            "loser": self.loser,
            "bomb_generated": self.bomb_generated,
            "round": self.round,
            "next_row": self.next_row,
            "server_seed": self.server_seed,
            "server_seed_hash": self.server_seed_hash
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        game = cls(data["creator_id"], data["creator_items"], data["bet_value"])
        game.game_id = data["game_id"]
        game.opponent_id = data.get("opponent_id")
        game.opponent_items = data.get("opponent_items", [])
        game.status = data.get("status", "waiting")
        game.created_at = data.get("created_at")
        game.message_id = data.get("message_id")
        game.bombs = set(data.get("bomb", []))
        game.revealed = set(data.get("revealed", []))
        game.past_revealed = set(data.get("past_revealed", []))
        game.current_turn = data.get("current_turn")
        game.winner = data.get("winner")
        game.loser = data.get("loser")
        game.bomb_generated = data.get("bomb_generated", False)
        game.round = data.get("round", 1)
        game.next_row = data.get("next_row", 0)
        game.server_seed = data.get("server_seed") or generate_server_seed("towers", game.game_id, game.creator_id, int(datetime.now().timestamp()))
        game.server_seed_hash = data.get("server_seed_hash") or get_server_seed_hash(game.server_seed)
        return game

def save_towers_game(game: TowersGame):
    """Save towers game to active games"""
    games = load_towers_games()
    games[game.game_id] = game.to_dict()
    save_towers_games(games)

def remove_towers_game(game_id: str):
    """Remove towers game from active games"""
    games = load_towers_games()
    if game_id in games:
        del games[game_id]
        save_towers_games(games)

                                        
class MinesCreationModal(discord.ui.Modal, title="CREATE MINES PVP GAME"):
    def __init__(self):
        super().__init__()
    
    mine_count = discord.ui.TextInput(
        label="NUMBER OF MINES (1-10)",
        placeholder="Enter number of mines to hide",
        default="1",
        required=True,
        max_length=2
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)
        
        try:
            mine_count = int(self.mine_count.value)
            if mine_count < MINES_MIN_COUNT or mine_count > MINES_MAX_COUNT:
                await interaction.followup.send(
                    f"Mine count must be between {MINES_MIN_COUNT} and {MINES_MAX_COUNT}!",
                    ephemeral=True
                )
                return
        except ValueError:
            await interaction.followup.send(
                "Please enter a valid number for mine count!",
                ephemeral=True
            )
            return
        
                          
        user_items = get_user_all_items(str(interaction.user.id))
        
        if not user_items:
            await interaction.followup.send(
                "You don't have any items to bet!",
                ephemeral=True
            )
            return
        
        embed = discord.Embed(
            title="Select Items to Bet",
            description=f"Select items worth at least {VALUE_EMOJI} **{format_value_with_commas(MIN_BET_VALUE)}** and at most {VALUE_EMOJI} **{format_value_with_commas(MAX_BET_VALUE)}**.\n\n**Mines:** {mine_count}",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="Instructions",
            value="1. Select items from the dropdown\n2. You can select multiple items\n3. Total value must be between 0 and 1,000,000\n4. Click 'Confirm Selection' when done",
            inline=False
        )
        
                                    
        view = ItemSelectionView(user_items, MAX_BET_VALUE, creating=True, is_mines=True, mine_count=mine_count)
        await interaction.followup.send(embed=embed, view=view, ephemeral=True)

                                         
                                                         
class ItemSelectDropdown(discord.ui.Select):
    def __init__(self, user_items: List[Tuple[str, int]], max_value: int, required_value: int = None):
        options = []
        self.item_options = {}
        option_counter = 1
        
                                             
        sorted_items = sorted(user_items, key=lambda x: x[1], reverse=True)
        
        for item_name, item_value in sorted_items:
            if item_value == 0:
                continue
                
            item_emoji = get_item_emoji(item_name)
            
                                                                   
            option_key = str(option_counter)
            label = item_name[:25]
            description = format_value_with_commas(item_value)
            
            options.append(discord.SelectOption(
                label=label,
                description=description[:100],
                value=option_key,
                emoji=item_emoji if item_emoji else "📦"                                 
            ))
            
            self.item_options[option_key] = (item_name, 1, item_value)
            option_counter += 1
        
                                                   
        max_options = min(len(options), 25)
        
        super().__init__(
            placeholder=f"Select items... (Choose multiple)",
            min_values=1,
            max_values=max_options,
            options=options[:max_options]
        )
        
        self.selected_items = []
        self.selected_value = 0
    
    async def callback(self, interaction: discord.Interaction):
        self.selected_items = []
        self.selected_value = 0
        
        for value in self.values:
            item_data = self.item_options.get(value)
            if item_data is None:
                                                    
                item_name = value
                item_value = 0
                if ":" in value:
                    parts = value.split(":", 1)
                    item_name = parts[0]
                    try:
                        item_value = int(float(parts[1]))
                    except Exception:
                        item_value = 0
            else:
                item_name, _, item_value = item_data

            self.selected_items.append(item_name)
            self.selected_value += item_value
        
        await interaction.response.defer()

class ItemSelectionView(discord.ui.View):
    def __init__(self, user_items: List[Tuple[str, int]], required_value: int, game_id: str = None, 
                 side: str = None, creating: bool = False, is_mines: bool = False, 
                 is_blackjack: bool = False, mine_count: int = 1, is_casebattle: bool = False, 
                 case_meta: dict = None, allow_range: bool = False, is_towers: bool = False):
        super().__init__(timeout=None)
        self.user_items = user_items
        self.required_value = required_value
        self.game_id = game_id
        self.side = side
        self.creating = creating
        self.is_mines = is_mines
        self.is_blackjack = is_blackjack
        self.is_casebattle = is_casebattle
        self.is_towers = is_towers
        self.case_meta = case_meta or {}
        self.mine_count = mine_count
        self.allow_range = allow_range
        self.selected_items = []
        self.selected_value = 0
        
                      
        self.dropdown = ItemSelectDropdown(user_items, MAX_BET_VALUE, required_value)
        self.add_item(self.dropdown)
    
    @discord.ui.button(label="CONFIRM SELECTION", style=discord.ButtonStyle.secondary, row=1)
    async def confirm_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.dropdown.selected_items:
            await interaction.response.send_message(
                "Please select at least one item from the dropdown!",
                ephemeral=True
            )
            return
        
        self.selected_items = self.dropdown.selected_items
        self.selected_value = self.dropdown.selected_value
        
                                      
        valid, game_type, error_msg = validate_items_same_type(self.selected_items)
        if not valid:
            await interaction.response.send_message(
                f"❌ {error_msg}",
                ephemeral=True
            )
            return
        
                                                    
        if self.selected_value < MIN_BET_VALUE:
            await interaction.response.send_message(
                f"Minimum bet is {VALUE_EMOJI} **{format_value_with_commas(MIN_BET_VALUE)}**!",
                ephemeral=True
            )
            return
        
        if self.selected_value > MAX_BET_VALUE:
            await interaction.response.send_message(
                f"Maximum bet is {VALUE_EMOJI} **{format_value_with_commas(MAX_BET_VALUE)}**!",
                ephemeral=True
            )
            return
        
                                                                
        min_allowed = self.required_value * 0.9
        max_allowed = self.required_value * 1.1
        
        if self.is_mines:
                                                             
            if not self.creating:
                if self.selected_value < min_allowed or self.selected_value > max_allowed:
                    await interaction.response.send_message(
                        f"You must bet within 10% of {VALUE_EMOJI} **{format_value_with_commas(self.required_value)}** to join this game!\n"
                        f"Allowed range: {VALUE_EMOJI} **{format_value_with_commas(min_allowed)}** - {VALUE_EMOJI} **{format_value_with_commas(max_allowed)}**\n"
                        f"Your current selection: {VALUE_EMOJI} **{format_value_with_commas(self.selected_value)}**",
                        ephemeral=True
                    )
                    return
        elif self.is_blackjack:
                                                                 
            if not self.creating:
                if self.selected_value < min_allowed or self.selected_value > max_allowed:
                    await interaction.response.send_message(
                        f"You must bet within 10% of {VALUE_EMOJI} **{format_value_with_commas(self.required_value)}** to join this game!\n"
                        f"Allowed range: {VALUE_EMOJI} **{format_value_with_commas(min_allowed)}** - {VALUE_EMOJI} **{format_value_with_commas(max_allowed)}**\n"
                        f"Your current selection: {VALUE_EMOJI} **{format_value_with_commas(self.selected_value)}**",
                        ephemeral=True
                    )
                    return
        elif not self.creating and self.allow_range:
                                                                   
            if self.selected_value < min_allowed or self.selected_value > max_allowed:
                await interaction.response.send_message(
                    f"You must bet within 10% of {VALUE_EMOJI} **{format_value_with_commas(self.required_value)}** to join this game!\n"
                    f"Allowed range: {VALUE_EMOJI} **{format_value_with_commas(min_allowed)}** - {VALUE_EMOJI} **{format_value_with_commas(max_allowed)}**\n"
                    f"Your current selection: {VALUE_EMOJI} **{format_value_with_commas(self.selected_value)}**",
                    ephemeral=True
                )
                return
        elif not self.creating and not self.allow_range:
                                                             
            if self.selected_value < min_allowed or self.selected_value > max_allowed:
                await interaction.response.send_message(
                    f"You must bet within 10% of {VALUE_EMOJI} **{format_value_with_commas(self.required_value)}** to join this game!\n"
                    f"Allowed range: {VALUE_EMOJI} **{format_value_with_commas(min_allowed)}** - {VALUE_EMOJI} **{format_value_with_commas(max_allowed)}**\n"
                    f"Your current selection: {VALUE_EMOJI} **{format_value_with_commas(self.selected_value)}**",
                    ephemeral=True
                )
                return
        
                                
        for child in self.children:
            child.disabled = True
        
        try:
            await interaction.response.edit_message(view=self)
        except discord.NotFound:
                                                             
            await interaction.response.send_message(
                "Selection confirmed! Processing your game...",
                ephemeral=True
            )
            return
        
                                 
        item_counts = {}
        for item in self.selected_items:
            item_counts[item] = item_counts.get(item, 0) + 1
        
        items_text = ""
        for item_name, count in item_counts.items():
            item_value = get_item_value(item_name)
            item_emoji = get_item_emoji(item_name)
            items_text += f"• {item_emoji} `{item_name}` x{count} ({VALUE_EMOJI} {format_value_with_commas(item_value)} each)\n"
        
                                           
        if self.creating and self.is_blackjack:
                                                   
                                                   
            remove_items_from_inventory(str(interaction.user.id), self.selected_items)
            
                                       
            game = BlackjackGame(interaction.user.id, self.selected_items, self.selected_value)
            
                               
            embed = discord.Embed(
                title="BLACKJACK PVP GAME",
                color=discord.Color.green()
            )
            
            embed.add_field(
                name="CREATOR",
                value=f"{interaction.user.mention}",
                inline=True
            )
            
            embed.add_field(
                name="BET VALUE",
                value=f"{VALUE_EMOJI} **{format_value_with_commas(self.selected_value)}**",
                inline=True
            )
            
            embed.add_field(
                name="TOTAL POT",
                value=f"{VALUE_EMOJI} **{format_value_with_commas(self.selected_value * 2)}**",
                inline=True
            )
            
            

            
                                            
            items_summary = ""
            for item_name, count in list(item_counts.items())[:5]:
                item_value = get_item_value(item_name)
                item_emoji = get_item_emoji(item_name)
                items_summary += f"• {item_emoji} `{item_name}` x{count} ({VALUE_EMOJI} {format_value_with_commas(item_value)} each)\n"
            
            if len(item_counts) > 5:
                items_summary += f"• ...and {len(item_counts)-5} more item types\n"
            
            embed.add_field(
                name="ITEMS BET",
                value=items_summary or "No items",
                inline=False
            )
            
            embed.add_field(
                name="GAME RULES",
                value="Closest to 21 without busting wins. Both bust = push. Tie = push.",
                inline=False
            )
            
            embed.add_field(
                name="STATUS",
                value="**Waiting for opponent...**",
                inline=False
            )
            
            embed.set_footer(text=f"Game ID: {game.game_id}   Click JOIN to challenge!")
            
                                            
            view = BlackjackJoinView(game.game_id, interaction.user.id, self.selected_value)
            message = await interaction.followup.send(
                content="",
                embed=embed,
                view=view,
                wait=True
            )
            
                                     
            game.message_id = message.id
            save_blackjack_game(game)
            
            await interaction.followup.send(
                "Blackjack PVP game created! Waiting for an opponent...", 
                ephemeral=True
            )
        elif self.creating and self.is_casebattle:
                                                
                                                   
            remove_items_from_inventory(str(interaction.user.id), self.selected_items)

                              
            case_section_num = str(self.case_meta.get('case_section', 1))
            selected_cases = self.case_meta.get('selected_cases', [case_section_num])
            rounds_num = self.case_meta.get('rounds', 3)
            crazy_mode = self.case_meta.get('crazy_mode', False)

            game_id = f"case-{interaction.user.id}-{int(datetime.now().timestamp())}"
            case_section = CASE_SECTIONS[case_section_num]

            embed = discord.Embed(
                title="CASE BATTLE GAME CREATED",
                color=discord.Color.green()
            )

            embed.add_field(
                name="CREATOR",
                value=f"{interaction.user.mention}",
                inline=True
            )

            if len(selected_cases) > 1:
                embed.add_field(
                    name="CASES",
                    value=f"{' '.join([CASE_SECTIONS[str(c)]['emoji'] for c in selected_cases])}",
                    inline=True
                )
            else:
                embed.add_field(
                    name="CASES",
                    value=f"{case_section['emoji']}",
                    inline=True
                )

            embed.add_field(
                name="ROUNDS",
                value=f"**{rounds_num} rounds**",
                inline=True
            )

                                                             
            items_summary = ""
            for item_name, count in list(item_counts.items())[:10]:
                item_value = get_item_value(item_name)
                item_emoji = get_item_emoji(item_name)
                items_summary += f"• {item_emoji} `{item_name}` x{count} ({VALUE_EMOJI} {format_value_with_commas(item_value)} each)\n"
            if len(item_counts) > 10:
                items_summary += f"• ...and {len(item_counts)-10} more item types\n"

            embed.add_field(
                name="ITEMS BET",
                value=items_summary or "No items",
                inline=False
            )

            total_pot_value = self.selected_value * 2
            embed.add_field(
                name="TOTAL POT",
                value=f"{VALUE_EMOJI} **{total_pot_value:,.0f}**",
                inline=True
            )

            embed.add_field(
                name="STATUS",
                value="**Waiting for opponent...**",
                inline=False
            )

                                               
            view = CaseBattleJoinView(game_id, interaction.user.id, self.selected_value, None, rounds_num, int(case_section_num), selected_cases, crazy_mode)
            message = await interaction.followup.send(content="", embed=embed, view=view, wait=True)

                                                        
            active_case_battles[game_id] = {
                'creator': interaction.user.id,
                'creator_items': self.selected_items,
                'bet_amount': self.selected_value,
                'rounds': rounds_num,
                'case_section': int(case_section_num),
                'selected_cases': selected_cases,
                'current_round': 1,
                'creator_score': 0,
                'joiner_score': 0,
                'creator_rounds_won': 0,
                'joiner_rounds_won': 0,
                'round_history': [],
                'channel_id': message.channel.id,
                'message_id': message.id,
                'joined_players': [interaction.user.id],
                'game_started': False,
                'game_over': False,
                'view': view,
                'crazy_mode': crazy_mode,
                'game_type': game_type,
                'server_seed': generate_server_seed('casebattle', game_id, interaction.user.id, int(datetime.now().timestamp())),
                'server_seed_hash': get_server_seed_hash(generate_server_seed('casebattle', game_id, interaction.user.id, int(datetime.now().timestamp())))
            }

            await interaction.followup.send(
                f"Case Battle created! {case_section['name']} with {rounds_num} rounds. Waiting for opponent...",
                ephemeral=True
            )
                                       
        elif self.creating and self.is_mines:
                                               
                                                   
            remove_items_from_inventory(str(interaction.user.id), self.selected_items)
            
                                   
            game = MinesGame(interaction.user.id, self.selected_items, self.selected_value, self.mine_count)
            
                               
            embed = discord.Embed(
                title="MINES PVP GAME",
                color=discord.Color.green()
            )
            
            embed.add_field(
                name="CREATOR",
                value=f"{interaction.user.mention}",
                inline=True
            )
            
            embed.add_field(
                name="BOARD SIZE",
                value=f"5x5 (25 cells)",
                inline=True
            )
            
            embed.add_field(
                name="MINES",
                value=f"**{self.mine_count} hidden mine{'s' if self.mine_count > 1 else ''}**",
                inline=True
            )
            
                                            
            items_summary = ""
            for item_name, count in list(item_counts.items())[:5]:
                item_value = get_item_value(item_name)
                item_emoji = get_item_emoji(item_name)
                items_summary += f"• {item_emoji} `{item_name}` x{count} ({VALUE_EMOJI} {format_value_with_commas(item_value)} each)\n"
            
            if len(item_counts) > 5:
                items_summary += f"• ...and {len(item_counts)-5} more item types\n"
            
            embed.add_field(
                name="ITEMS BET",
                value=items_summary or "No items",
                inline=False
            )
            
            board_display = f"**5x5 board** with **{self.mine_count} hidden mine{'s' if self.mine_count > 1 else ''}**\nClick JOIN to see the game board!"
            
            embed.add_field(
                name="STATUS",
                value="**Waiting for opponent...**",
                inline=False
            )
            
            embed.set_footer(text=f"Powered by Bloxloot  •  Seed Hash: {game.server_seed_hash}")
            
                                            
            view = MinesJoinView(game.game_id, interaction.user.id, self.selected_value, self.mine_count)
            message = await interaction.followup.send(
                content="",
                embed=embed,
                view=view,
                wait=True
            )
            
                                     
            game.message_id = message.id
            save_mines_game(game)
            
            await interaction.followup.send(
                f"Mines PVP game created! {self.mine_count} mine{'s' if self.mine_count > 1 else ''} hidden on a 5x5 board.", 
                ephemeral=True
            )
        elif self.creating and self.is_towers:
                                                
                                                   
            remove_items_from_inventory(str(interaction.user.id), self.selected_items)
            
                                    
            game = TowersGame(interaction.user.id, self.selected_items, self.selected_value)
            
                               
            embed = discord.Embed(
                title="TOWERS PVP GAME",
                color=discord.Color.green()
            )
            
            embed.add_field(
                name="CREATOR",
                value=f"{interaction.user.mention}",
                inline=True
            )
            
            embed.add_field(
                name="BOARD SIZE",
                value=f"3x7 (21 tiles)",
                inline=True
            )
            
            embed.add_field(
                name="BOMBS",
                value=f"**5 bombs**",
                inline=True
            )
            
                                            
            items_summary = ""
            for item_name, count in list(item_counts.items())[:5]:
                item_value = get_item_value(item_name)
                item_emoji = get_item_emoji(item_name)
                items_summary += f"• {item_emoji} `{item_name}` x{count} ({VALUE_EMOJI} {format_value_with_commas(item_value)} each)\n"
            
            if len(item_counts) > 5:
                items_summary += f"• ...and {len(item_counts)-5} more item types\n"
            
            embed.add_field(
                name="ITEMS BET",
                value=items_summary or "No items",
                inline=False
            )
            
            embed.add_field(
                name="STATUS",
                value="**Waiting for opponent...**",
                inline=False
            )
            
            embed.set_footer(text=f"Powered by Bloxloot  •  ID: {game.game_id}")
            
                                            
            view = TowersJoinView(game.game_id, interaction.user.id, self.selected_value)
            message = await interaction.followup.send(
                content="",
                embed=embed,
                view=view,
                wait=True
            )
            
                                     
            game.message_id = message.id
            save_towers_game(game)
            
            await interaction.followup.send(
                f"Towers PVP game created! 5 bombs hidden on a 3x7 board.", 
                ephemeral=True
            )
        elif self.is_mines and self.game_id:
                                              
                                                    
            remove_items_from_inventory(str(interaction.user.id), self.selected_items)
            
                                           
            games = load_mines_games()
            game_data = games.get(self.game_id)
            
            if game_data and game_data['status'] == 'waiting':
                game_data['opponent_id'] = interaction.user.id
                game_data['opponent_items'] = self.selected_items
                game_data['status'] = 'active'
                save_mines_games(games)
                
                                               
                await complete_mines_game_setup(interaction, self.game_id, game_data)
        elif self.is_blackjack and self.game_id:
                                                  
                                                    
            remove_items_from_inventory(str(interaction.user.id), self.selected_items)
            
                                               
            games = load_blackjack_games()
            game_data = games.get(self.game_id)
            
            if game_data and game_data['status'] == 'waiting':
                game_data['opponent_id'] = interaction.user.id
                game_data['opponent_items'] = self.selected_items
                game_data['status'] = 'active'
                save_blackjack_games(games)
                
                                                   
                await complete_blackjack_game_setup(interaction, self.game_id, game_data)
        elif self.is_towers and self.game_id:
                                               
                                                    
            remove_items_from_inventory(str(interaction.user.id), self.selected_items)
            
                                            
            games = load_towers_games()
            game_data = games.get(self.game_id)
            
            if game_data and game_data['status'] == 'waiting':
                game_data['opponent_id'] = interaction.user.id
                game_data['opponent_items'] = self.selected_items
                game_data['status'] = 'active'
                save_towers_games(games)
                
                                                
                await complete_towers_game_setup(interaction, self.game_id, game_data)
        elif self.game_id and not self.creating and self.game_id in active_case_battles:
                                        
                                                    
            remove_items_from_inventory(str(interaction.user.id), self.selected_items)

                                                     
            game = active_case_battles.get(self.game_id)
            if game and not game.get('game_started'):
                                                           
                creator_type = game.get('game_type')
                if creator_type and game_type != creator_type:
                                          
                    add_items_to_inventory(str(interaction.user.id), self.selected_items)
                    await interaction.response.send_message(
                        "❌ Your selected items do not match the creator's item requirements!",
                        ephemeral=True
                    )
                    return
                
                game['opponent_id'] = interaction.user.id
                game['joiner_items'] = self.selected_items
                game['joined_players'].append(interaction.user.id)
                game['game_started'] = True
                game['status'] = 'Fetching EOS Block..'
                game['eos_block'] = build_casebattle_eos_block(self.game_id, game.get('creator'), interaction.user.id, game.get('server_seed'))
                game['server_seed'] = generate_server_seed('casebattle', self.game_id, game.get('creator'), interaction.user.id, game['eos_block']['height'], game['eos_block']['id'])
                game['server_seed_hash'] = get_server_seed_hash(game['server_seed'])
                active_case_battles[self.game_id] = game
                await update_casebattle_status(self.game_id, 'Fetching EOS Block..', game['eos_block'])

                                                                                       
                try:
                    orig_view = game.get('view')
                    if orig_view:
                        for child in orig_view.children:
                            child.disabled = True
                    channel = bot.get_channel(game.get('channel_id')) if game.get('channel_id') else None
                    if channel and game.get('message_id'):
                        try:
                            msg = await channel.fetch_message(game.get('message_id'))
                            await msg.edit(view=orig_view)
                        except Exception:
                            pass
                except Exception:
                    pass

                                            
                try:
                    asyncio.create_task(play_casebattle(self.game_id))
                except Exception:
                    pass
        elif self.game_id and not self.creating and not self.is_mines and not self.is_blackjack:
                                                 
                                                    
            remove_items_from_inventory(str(interaction.user.id), self.selected_items)
            
                                              
            games = load_games()
            game_data = games.get(self.game_id)
            
            if game_data and game_data['status'] == 'waiting':
                game_data['opponent_id'] = interaction.user.id
                game_data['opponent_items'] = self.selected_items
                game_data['status'] = 'active'
                save_games(games)
                
                                        
                await complete_flip_game(interaction, self.game_id, game_data)

        elif self.creating:
                                                                            
            embed = discord.Embed(
                title="Enable Wild Mode?",
                description=f"Wild Mode {WILD_MODE_EMOJI} **REVERSES WINNINGS** if activated!\n\n**Your bet:** {VALUE_EMOJI} **{format_value_with_commas(self.selected_value)}**",
                color=discord.Color.green()
            )
            
            embed.add_field(
                name="How Wild Mode Works",
                value=f"• If activated: **Loser gets winnings, winner loses**\n• Complete reversal of outcome!\n• Optional - you can skip it",
                inline=False
            )
            
            class WildModeView(discord.ui.View):
                def __init__(self, creator_id: int, items: List[str], total_value: int, game_type: str):
                    super().__init__(timeout=None)
                    self.creator_id = creator_id
                    self.items = items
                    self.total_value = total_value
                    self.game_type = game_type
                    self.wild_mode = False
                    self.side = None
                
                @discord.ui.button(label="ENABLE WILD MODE", style=discord.ButtonStyle.secondary, row=0)
                async def enable_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                    self.wild_mode = True
                    await self.ask_for_side(interaction)
                
                @discord.ui.button(label="SKIP WILD MODE", style=discord.ButtonStyle.secondary, row=0)
                async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                    self.wild_mode = False
                    await self.ask_for_side(interaction)
                
                async def ask_for_side(self, interaction: discord.Interaction):
                                                                       
                    remove_items_from_inventory(str(self.creator_id), self.items)
                    
                                                   
                    embed = discord.Embed(
                        title="Choose Your Side",
                        description=f"Select **Heads** or **Tails** for your coinflip.\n\n**Your bet:** {VALUE_EMOJI} **{format_value_with_commas(self.total_value)}**\n**Wild Mode:** {'ENABLED' if self.wild_mode else 'DISABLED'}",
                        color=discord.Color.green()
                    )
                    
                    class SideSelectionView(discord.ui.View):
                        def __init__(self, creator_id: int, items: List[str], total_value: int, wild_mode: bool, game_type: str):
                            super().__init__(timeout=None)
                            self.creator_id = creator_id
                            self.items = items
                            self.total_value = total_value
                            self.wild_mode = wild_mode
                            self.game_type = game_type
                        
                        @discord.ui.button(label="HEADS", style=discord.ButtonStyle.secondary, row=0)
                        async def heads_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                                                         
                            await interaction.response.defer(ephemeral=True)
                            await self.create_game(interaction, "heads")
                        
                        @discord.ui.button(label="TAILS", style=discord.ButtonStyle.secondary, row=0)
                        async def tails_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                                                         
                            await interaction.response.defer(ephemeral=True)
                            await self.create_game(interaction, "tails")
                        
                        async def create_game(self, interaction: discord.Interaction, side: str):
                                             
                            game = CoinflipGame(self.creator_id, self.items, side, self.wild_mode)
                            
                                               
                            embed = discord.Embed(
                                title="COINFLIP GAME CREATED!",
                                color=discord.Color.green()
                            )
                            
                            coin_emoji = HEADS_EMOJI if side.lower() == "heads" else TAILS_EMOJI
                            embed.add_field(
                                name="CREATOR",
                                value=f"{interaction.user.mention} {coin_emoji}",
                                inline=True
                            )
                
                            embed.add_field(
                                name=f"BET VALUE",
                                value=f"** {VALUE_EMOJI} {format_value_with_commas(self.total_value)}**",
                                inline=True
                            )
                            
                            if self.wild_mode:
                                embed.add_field(
                                    name=f"{WILD_MODE_EMOJI} Wild Mode",
                                    value="**ENABLED**",
                                    inline=True
                                )
                            
                                                
                            item_counts = {}
                            for item in self.items:
                                item_counts[item] = item_counts.get(item, 0) + 1
                            
                            items_text = ""
                            for item_name, count in list(item_counts.items())[:5]:
                                item_value = get_item_value(item_name)
                                item_emoji = get_item_emoji(item_name)
                                items_text += f"• {item_emoji} `{item_name}` x{count} ({VALUE_EMOJI} {format_value_with_commas(item_value)} each)\n"
                            
                            if len(item_counts) > 5:
                                items_text += f"• ...and {len(item_counts)-5} more item types\n"
                            
                            embed.add_field(
                                name="Items Bet",
                                value=items_text or "No items",
                                inline=False
                            )
                            
                                                        
                            total_pot = self.total_value * 2
                            tax_amount = calculate_tax(total_pot)
                            net_winnings = calculate_net_winnings(total_pot)
                            
                            embed.add_field(
                                name="Potential Winnings",
                                value=(
                                    f"Total Pot: {VALUE_EMOJI} **{format_value_with_commas(total_pot)}**\n"
                                    f"Winner Gets: {VALUE_EMOJI} **{format_value_with_commas(net_winnings)}**\n"
                                    f"House Tax ({get_house_tax() * 100:.1f}%): {VALUE_EMOJI} **{format_value_with_commas(tax_amount)}**"
                                ),
                                inline=False
                            )
                            
                            if self.wild_mode:
                                embed.add_field(
                                    name="Wild Mode Effect",
                                    value=(
                                        f"• **LOSER gets the winnings**\n"
                                        f"• **WINNER loses their items**\n"
                                        f"• Complete reversal of outcome!"
                                    ),
                                    inline=False
                                )
                            
                            embed.set_footer(text=f"Game ID: {game.game_id}")
                            
                                                            
                            try:
                                message = await interaction.followup.send(
                                    content="",
                                    embed=embed,
                                    view=JoinGameView(game.game_id, interaction.user.id, side),
                                    wait=True
                                )
                                
                                                         
                                game.message_id = message.id
                                save_game(game)
                                
                                                                                   
                                for child in self.children:
                                    child.disabled = True
                                
                                                                        
                                try:
                                    await interaction.message.edit(view=self)
                                except:
                                    pass                                    
                                    
                            except Exception as e:
                                print(f"Error creating game: {e}")
                                await interaction.followup.send(
                                    "Failed to create game. Please try again.",
                                    ephemeral=True
                                )
                    
                                                             
                    await interaction.response.send_message(embed=embed, view=SideSelectionView(
                        self.creator_id, self.items, self.total_value, self.wild_mode, self.game_type
                    ), ephemeral=True)
            
            view = WildModeView(interaction.user.id, self.selected_items, self.selected_value, game_type)
            await interaction.followup.send(embed=embed, view=view, ephemeral=True)

                                        
class MinesJoinView(discord.ui.View):
    def __init__(self, game_id: str, creator_id: int, bet_value: int, mine_count: int):
        super().__init__(timeout=None)                   
        self.game_id = game_id
        self.creator_id = creator_id
        self.bet_value = bet_value
        self.mine_count = mine_count
        self.game_started = False
        self.buttons_added = False
    
    @discord.ui.button(label="JOIN", style=discord.ButtonStyle.secondary, row=0)
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                                     
        if not is_user_registered(interaction.user.id):
            await interaction.response.send_message(
                "You need to register first! Use `/register` to get started.",
                ephemeral=True
            )
            return
        
                                                        
        if interaction.user.id == self.creator_id:
            await interaction.response.send_message(
                "You can't join your own game!",
                ephemeral=True
            )
            return
        
                  
        games = load_mines_games()
        game_data = games.get(self.game_id)
        
        if not game_data:
            await interaction.response.send_message(
                "This game no longer exists or has expired!",
                ephemeral=True
            )
            return
        
        if game_data.get('opponent_id'):
            await interaction.response.send_message(
                "This game already has an opponent!",
                ephemeral=True
            )
            return
        
        if game_data['status'] != 'waiting':
            await interaction.response.send_message(
                "This game is no longer accepting joins!",
                ephemeral=True
            )
            return
        
        required_value = game_data['bet_value']
        
                                                     
        min_allowed = required_value * 0.9
        max_allowed = required_value * 1.1
        
                                     
        user_items = get_user_all_items(str(interaction.user.id))
        
        if not user_items:
            await interaction.response.send_message(
                "You don't have any items to bet!",
                ephemeral=True
            )
            return
        
                                              
        user_total_value = calculate_inventory_value(str(interaction.user.id))
        if user_total_value < min_allowed:
            await interaction.response.send_message(
                f"You need at least {VALUE_EMOJI} **{format_value_with_commas(min_allowed)}** in items to join this game!\n"
                f"Your current inventory value: {VALUE_EMOJI} **{format_value_with_commas(user_total_value)}**",
                ephemeral=True
            )
            return
        
                                      
        embed = discord.Embed(
            title="Select Your Items",
            description=f"Select items worth between {VALUE_EMOJI} **{format_value_with_commas(min_allowed)}** and {VALUE_EMOJI} **{format_value_with_commas(max_allowed)}** to join this game.\n\n"
                       f"**Mines:** {self.mine_count}\n"
                       f"**Board:** 5x5 ({25 - self.mine_count} safe cells)",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="Instructions",
            value=f"1. Select items from the dropdown\n2. You can select multiple items\n3. Total value must be within 10% of the game bet ({VALUE_EMOJI} **{format_value_with_commas(required_value)}**)\n4. Click 'Confirm Selection' when done",
            inline=False
        )
        
        view = ItemSelectionView(user_items, required_value, self.game_id, is_mines=True, allow_range=True)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    @discord.ui.button(label="CANCEL", style=discord.ButtonStyle.danger, row=0)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                                      
        if interaction.user.id != self.creator_id:
            await interaction.response.send_message(
                "Only the game creator can cancel the game!",
                ephemeral=True
            )
            return
        
                  
        games = load_mines_games()
        game_data = games.get(self.game_id)
        
        if not game_data:
            await interaction.response.send_message(
                "This game no longer exists!",
                ephemeral=True
            )
            return
        
        if game_data.get('opponent_id'):
            await interaction.response.send_message(
                "Cannot cancel game with an opponent!",
                ephemeral=True
            )
            return
        
                                 
        creator_items = game_data['creator_items']
        add_items_to_inventory(str(self.creator_id), creator_items)
        
                     
        remove_mines_game(self.game_id)
        
                                 
        try:
            embed = discord.Embed(
                title="MINES GAME CANCELLED",
                description=f"This game has been cancelled by the creator.",
                color=discord.Color.red()
            )
            
            embed.add_field(
                name="Items Returned",
                value=f"All items have been returned to <@{self.creator_id}>",
                inline=False
            )
            
                                 
            for child in self.children:
                child.disabled = True
            
            await interaction.response.edit_message(embed=embed, view=self)
            
                                          
            await interaction.followup.send(
                f"Game cancelled! Your items have been returned to your inventory.",
                ephemeral=True
            )
        except Exception as e:
            print(f"Error cancelling game: {e}")
            await interaction.response.send_message(
                f"Game cancelled! Your items have been returned to your inventory.",
                ephemeral=True
            )

class MinesGameView(discord.ui.View):
    def __init__(self, game_id: str, current_player_id: int):
        super().__init__(timeout=None)
        self.game_id = game_id
        self.current_player_id = current_player_id
        self.buttons_created = False
        self.create_board_buttons()
    
    def create_board_buttons(self):
        """Create the 5x5 grid board buttons"""
        if self.buttons_created:
            return
            
                                    
        for row in range(5):
            for col in range(5):
                cell_index = row * 5 + col
                                                                                
                button_label = "\u200b"
                button = discord.ui.Button(
                    style=discord.ButtonStyle.secondary,
                    label=button_label,
                    row=row,
                    custom_id=f"cell_{cell_index}"
                )
                button.callback = self.create_cell_callback(cell_index)
                self.add_item(button)
        
        self.buttons_created = True
    
    def create_cell_callback(self, cell_index: int):
        async def cell_callback(interaction: discord.Interaction):
                                                     
            await interaction.response.defer(ephemeral=True)
            
                      
            games = load_mines_games()
            game_data = games.get(self.game_id)
            
            if not game_data:
                                                            
                await interaction.followup.send(
                    "This game no longer exists!",
                    ephemeral=True
                )
                return
            
                              
            game = MinesGame.from_dict(game_data)
            
                                       
            if interaction.user.id != game.current_turn:
                player_name = await get_player_display_name(game.current_turn)
                                                            
                await interaction.followup.send(
                    f"Not your turn! It's **{player_name}**'s turn.",
                    ephemeral=True
                )
                return
            
            if interaction.user.id not in [game.creator_id, game.opponent_id]:
                await interaction.followup.send(
                    "You're not in this game!",
                    ephemeral=True
                )
                return
            
                           
            valid_move, hit_mine = game.make_move(interaction.user.id, cell_index)
            
            if not valid_move:
                await interaction.followup.send(
                    "Invalid move! Cell already revealed.",
                    ephemeral=True
                )
                return
            
                                     
            save_mines_game(game)
            
                                 
            try:
                channel = interaction.channel
                if isinstance(channel, discord.TextChannel) and game.message_id:
                    message = await channel.fetch_message(game.message_id)
                    
                    if game.status == "completed":
                                                  
                        await complete_mines_game(interaction, self.game_id, game.to_dict(), losing_cell=cell_index if hit_mine else None)
                    else:
                                                       
                        creator = await bot.fetch_user(game.creator_id)
                        opponent = await bot.fetch_user(game.opponent_id)
                        
                        embed = discord.Embed(
                            title="MINES PVP GAME",
                            color=discord.Color.green()
                        )
                        
                        if game.wild_mode:
                            embed.add_field(
                                name=f"{WILD_MODE_EMOJI} WILD MODE ACTIVE!",
                                value="**OUTCOME REVERSAL ENABLED!**\nHitting a mine makes you WIN!",
                                inline=False
                            )
                        
                        embed.add_field(
                            name="PLAYERS",
                            value=f"{creator.mention} vs {opponent.mention}",
                            inline=True
                        )

                        current_player_obj = await bot.fetch_user(game.current_turn)
                        embed.add_field(
                            name="TURN",
                            value=f"{current_player_obj.mention}",
                            inline=True
                        )
                        
                        embed.add_field(
                            name="SAFE CLICKS",
                            value=f"**{len(game.revealed)}** cells revealed",
                            inline=True
                        )
                        
                        embed.add_field(
                            name="BET VALUE",
                            value=f"{VALUE_EMOJI} **{format_value_with_commas(game.bet_value)}**",
                            inline=False
                        )
                        
                        pot_value = game.bet_value * 2
                        embed.add_field(
                            name="TOTAL POT",
                            value=f"{VALUE_EMOJI} **{format_value_with_commas(pot_value)}**",
                            inline=True
                        )
                        
                        board_display = game.get_simple_board_display()
                        embed.add_field(
                            name="GAME STATUS",
                            value=board_display,
                            inline=False
                        )
                        
                                              
                        for child in self.children:
                            if child.custom_id and child.custom_id.startswith("cell_"):
                                cell_idx = int(child.custom_id.split("_")[1])
                                if cell_idx in game.revealed:
                                    if cell_idx in game.mines:
                                        child.disabled = True
                                        child.style = discord.ButtonStyle.danger
                                        child.label = "💣"
                                    else:
                                        child.disabled = True
                                        child.style = discord.ButtonStyle.success
                                        child.label = "✓"
                        
                        embed.set_footer(text=f"Select a tile to reveal it. Mines remaining: {game.mine_count}")
                        
                        await message.edit(embed=embed, view=self)
                        
                                                                        
                                                         
            
            except Exception as e:
                print(f"Error updating mines game: {e}")
                                                            
                pass
        
        return cell_callback

                                            
async def complete_mines_game_setup(interaction: discord.Interaction, game_id: str, game_data: dict):
    """Complete mines game setup and start the game"""
               
    games = load_mines_games()
    game_dict = games.get(game_id)
    
    if not game_dict:
        await interaction.followup.send(
            "Game not found!",
            ephemeral=True
        )
        return
    
    game = MinesGame.from_dict(game_dict)
    
                    
    game.generate_board()
    
                            
    save_mines_game(game)
    
                 
    creator = await bot.fetch_user(game.creator_id)
    opponent = await bot.fetch_user(game.opponent_id)
    
                              
    all_items = game.creator_items + game.opponent_items
    valid, game_type, _ = validate_items_same_type(all_items)
    
                       
    embed = discord.Embed(
        title="MINES PVP GAME STARTED",
        color=discord.Color.green()
    )
    
    if game.wild_mode:
        embed.add_field(
            name=f"{WILD_MODE_EMOJI} WILD MODE ACTIVE!",
            value="**OUTCOME REVERSAL ENABLED!**\nHitting a mine makes you WIN!",
            inline=False
        )
    
    embed.add_field(
        name="PLAYERS",
        value=f"{creator.mention} vs {opponent.mention}",
            inline=True
        )

    current_player = await bot.fetch_user(game.current_turn)
    embed.add_field(
        name="FIRST TURN",
        value=f"{current_player.mention}",
        inline=True
    )
    
    embed.add_field(
        name="MINES",
        value=f"**{game.mine_count} hidden mine{'s' if game.mine_count > 1 else ''}**",
        inline=True
    )
    
    embed.add_field(
        name="BET VALUE",
        value=f"{VALUE_EMOJI} **{format_value_with_commas(game.bet_value)}**",
        inline=False
    )
    
    pot_value = game.bet_value * 2
    embed.add_field(
        name="TOTAL POT",
        value=f"{VALUE_EMOJI} **{format_value_with_commas(pot_value)}**",
        inline=True
    )
    
    embed.set_footer(text="Select a tile to reveal it. Mines remaining: same as total")
    
                      
    view = MinesGameView(game_id, game.current_turn)
    
                                      
    try:
        channel = interaction.channel
        if isinstance(channel, discord.TextChannel) and game.message_id:
            message = await channel.fetch_message(game.message_id)
            await message.edit(embed=embed, view=view)
            
                                           
            await interaction.followup.send(
                f"Mines game started! It's now **{current_player.name}**'s turn.",
                ephemeral=True
            )
    except Exception as e:
        print(f"Error updating mines game message: {e}")
                                    
        message = await interaction.followup.send(embed=embed, view=view, wait=True)
        
                           
        game.message_id = message.id
        save_mines_game(game)

async def complete_mines_game(interaction: discord.Interaction, game_id: str, game_data: dict, 
                             winner_id: int = None, loser_id: int = None, forfeited: bool = False,
                             losing_cell: int = None):
    """Complete the mines game"""
               
    games = load_mines_games()
    game_dict = games.get(game_id)
    
    if not game_dict:
        return
    
    game = MinesGame.from_dict(game_dict)
    
                   
    all_items = game.creator_items + game.opponent_items
    valid, game_type, _ = validate_items_same_type(all_items)
    
                                                 
    if winner_id is None:
        winner_id = game.winner
    if loser_id is None:
        loser_id = game.loser
    
                 
    winner = await bot.fetch_user(winner_id) if winner_id else None
    loser = await bot.fetch_user(loser_id) if loser_id else None
    
                              
    total_pot = game.bet_value * 2
    tax_amount = calculate_tax(total_pot)
    net_winnings = calculate_net_winnings(total_pot)
                                         
    winner_id_str = str(winner_id)
    loser_id_str = str(loser_id)
    
                              
    all_items = game.creator_items + game.opponent_items
    
                           
    remaining_items, taxed_items = deduct_tax_from_items(all_items, tax_amount)
    
                              
    item_counts = {}
    for item in remaining_items:
        item_counts[item] = item_counts.get(item, 0) + 1
    
    items_summary = ""
    for item_name, count in list(item_counts.items())[:10]:
        item_value = get_item_value(item_name)
        item_emoji = get_item_emoji(item_name)
        total_value = item_value * count
        items_summary += f"• {item_emoji} `{item_name}` x{count} ({VALUE_EMOJI} {format_value_with_commas(item_value)} each)\n"
    
    if len(item_counts) > 10:
        items_summary += f"• ...and {len(item_counts)-10} more item types\n"
    
                     
    await log_taxed_items(
        source_game="Mines",
        winner_id=winner_id,
        loser_id=loser_id,
        tax_amount=tax_amount,
        items=taxed_items,
        pot_value=total_pot
    )
    
    add_items_to_inventory(winner_id_str, remaining_items)
    
                                               
    result_embed = discord.Embed(
        title="**MINE HIT! GAME OVER**",
        color=discord.Color.red() if not game.wild_mode else discord.Color.dark_blue()
    )
    
    if game.wild_mode:
        result_embed.add_field(
            name=f"{WILD_MODE_EMOJI} WILD MODE ACTIVE!",
            value="**OUTCOME REVERSED!**\nHitting a mine made you the WINNER!",
            inline=False
        )
    
    result_embed.add_field(
        name="WINNER",
        value=winner.mention if winner else "Unknown",
        inline=True
    )
    
    result_embed.add_field(
        name="LOSER",
        value=loser.mention if loser else "Unknown",
        inline=True
    )
    
    result_embed.add_field(
        name="WINNINGS",
        value=f"{VALUE_EMOJI} **{format_value_with_commas(total_pot)}**",
        inline=True
    )
    
    if items_summary:
        result_embed.add_field(
            name="Items Won",
            value=items_summary,
            inline=False
        )
    
    final_board = game.get_final_board_display(losing_cell)
    result_embed.add_field(
        name="FINAL BOARD",
        value=final_board,
        inline=False
    )
    
    result_embed.set_footer(text="Game Complete")
    
                                   
    remove_mines_game(game_id)
                                      
    try:
        if valid and game_type in (GameType.MM2, GameType.ADM):
            creator_wager = sum(get_item_value(it) for it in game.creator_items)
            opponent_wager = sum(get_item_value(it) for it in game.opponent_items)
            try:
                add_user_wager(int(game.creator_id), game_type, int(creator_wager))
            except Exception:
                pass
            try:
                add_user_wager(int(game.opponent_id), game_type, int(opponent_wager))
            except Exception:
                pass
            try:
                record_completed_game({
                    "game_id": game_id,
                    "game_type": game_type,
                    "participants": [int(game.creator_id), int(game.opponent_id)],
                    "per_player": {
                        str(game.creator_id): creator_wager,
                        str(game.opponent_id): opponent_wager
                    },
                    "total_pot": total_pot,
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                print(f"Error recording completed mines game: {e}")
    except Exception:
        pass
    
                                             
    try:
        if game.message_id:
            channel = interaction.channel
            if isinstance(channel, discord.TextChannel):
                message = await channel.fetch_message(game.message_id)
                
                                     
                for child in message.components:
                    for button in child.children:
                        button.disabled = True
                
                                           
                await message.edit(
                    content="",
                    embed=result_embed,
                    view=None                      
                )
                
                                             
                await interaction.followup.send("Game completed! Check the updated game message above.", ephemeral=True)
                return
    
    except Exception as e:
        print(f"Error updating mines game message: {e}")
    
                                                                     
    await interaction.followup.send(embed=result_embed)

                                         
class TowersJoinView(discord.ui.View):
    def __init__(self, game_id: str, creator_id: int, bet_value: int):
        super().__init__(timeout=None)                   
        self.game_id = game_id
        self.creator_id = creator_id
        self.bet_value = bet_value
    
    @discord.ui.button(label="JOIN", style=discord.ButtonStyle.secondary, row=0)
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                                     
        if not is_user_registered(interaction.user.id):
            await interaction.response.send_message(
                "You need to register first! Use `/register` to get started.",
                ephemeral=True
            )
            return
        
                                                        
        if interaction.user.id == self.creator_id:
            await interaction.response.send_message(
                "You can't join your own game!",
                ephemeral=True
            )
            return
        
                  
        games = load_towers_games()
        game_data = games.get(self.game_id)
        
        if not game_data:
            await interaction.response.send_message(
                "This game no longer exists or has expired!",
                ephemeral=True
            )
            return
        
        if game_data.get('opponent_id'):
            await interaction.response.send_message(
                "This game already has an opponent!",
                ephemeral=True
            )
            return
        
        if game_data['status'] != 'waiting':
            await interaction.response.send_message(
                "This game is no longer accepting joins!",
                ephemeral=True
            )
            return
        
        required_value = game_data['bet_value']
        
                                            
        min_allowed = required_value * 0.9
        max_allowed = required_value * 1.1
        
                                     
        user_items = get_user_all_items(str(interaction.user.id))
        
        if not user_items:
            await interaction.response.send_message(
                "You don't have any items to bet!",
                ephemeral=True
            )
            return
        
                                              
        user_total_value = calculate_inventory_value(str(interaction.user.id))
        if user_total_value < min_allowed:
            await interaction.response.send_message(
                f"You need at least {VALUE_EMOJI} **{format_value_with_commas(min_allowed)}** in items to join this game!\n"
                f"Your current inventory value: {VALUE_EMOJI} **{format_value_with_commas(user_total_value)}**",
                ephemeral=True
            )
            return
        
                                      
        embed = discord.Embed(
            title="Select Your Items",
            description=f"Select items worth between {VALUE_EMOJI} **{format_value_with_commas(min_allowed)}** and {VALUE_EMOJI} **{format_value_with_commas(max_allowed)}** to join this game.\n\n"
                       f"**Board:** 3x7 (20 safe cells)",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="Instructions",
            value=f"1. Select items from the dropdown\n2. You can select multiple items\n3. Total value must be within 10% of the game bet ({VALUE_EMOJI} **{format_value_with_commas(required_value)}**)\n4. Click 'Confirm Selection' when done",
            inline=False
        )
        
        view = ItemSelectionView(user_items, required_value, self.game_id, is_towers=True, allow_range=True)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    @discord.ui.button(label="CANCEL", style=discord.ButtonStyle.danger, row=0)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                                      
        if interaction.user.id != self.creator_id:
            await interaction.response.send_message(
                "Only the game creator can cancel the game!",
                ephemeral=True
            )
            return
        
                  
        games = load_towers_games()
        game_data = games.get(self.game_id)
        
        if not game_data:
            await interaction.response.send_message(
                "This game no longer exists!",
                ephemeral=True
            )
            return
        
        if game_data.get('opponent_id'):
            await interaction.response.send_message(
                "Cannot cancel game with an opponent!",
                ephemeral=True
            )
            return
        
                                 
        creator_items = game_data['creator_items']
        add_items_to_inventory(str(self.creator_id), creator_items)
        
                     
        remove_towers_game(self.game_id)
        
                                 
        try:
            embed = discord.Embed(
                title="TOWERS GAME CANCELLED",
                description=f"This game has been cancelled by the creator.",
                color=discord.Color.red()
            )
            
            embed.add_field(
                name="Items Returned",
                value=f"All items have been returned to <@{self.creator_id}>",
                inline=False
            )
            
                                 
            for child in self.children:
                child.disabled = True
            
            await interaction.response.edit_message(embed=embed, view=self)
            
                                          
            await interaction.followup.send(
                f"Game cancelled! Your items have been returned to your inventory.",
                ephemeral=True
            )
        except Exception as e:
            print(f"Error cancelling game: {e}")
            await interaction.response.send_message(
                f"Game cancelled! Your items have been returned to your inventory.",
                ephemeral=True
            )

class TowersGameView(discord.ui.View):
    def __init__(self, game_id: str, current_player_id: int):
        super().__init__(timeout=None)
        self.game_id = game_id
        self.current_player_id = current_player_id
        self.buttons_created = False
        self.create_board_buttons()
    
    def create_board_buttons(self):
        """Create the 3x5 grid board buttons (all 15 cells, arranged bottom-to-top)"""
        if self.buttons_created:
            return
            
                                                                 
                                                                       
        for cell_index in range(15):
                                                             
            button_label = "\u200b"
                                                              
                                                                                                       
            row = 4 - (cell_index // 3)
            button = discord.ui.Button(
                style=discord.ButtonStyle.secondary,
                label=button_label,
                row=row,
                custom_id=f"tower_cell_{cell_index}"
            )
            button.callback = self.create_cell_callback(cell_index)
            self.add_item(button)
        
        self.buttons_created = True
    
    def reset_buttons(self):
        """Reset all buttons back to their initial state."""
        for child in self.children:
            if child.custom_id and child.custom_id.startswith("tower_cell_"):
                cell_idx = int(child.custom_id.split("_")[2])
                child.disabled = False
                child.style = discord.ButtonStyle.secondary
                child.label = "\u200b"
    
    def create_cell_callback(self, cell_index: int):
        async def cell_callback(interaction: discord.Interaction):
                                                     
            await interaction.response.defer(ephemeral=True)
            
                      
            games = load_towers_games()
            game_data = games.get(self.game_id)
            
            if not game_data:
                await interaction.followup.send(
                    "This game no longer exists!",
                    ephemeral=True
                )
                return
            
                              
            game = TowersGame.from_dict(game_data)
            
                                       
            if interaction.user.id != game.current_turn:
                player_name = await get_player_display_name(game.current_turn)
                await interaction.followup.send(
                    f"Not your turn! It's **{player_name}**'s turn.",
                    ephemeral=True
                )
                return
            
            if interaction.user.id not in [game.creator_id, game.opponent_id]:
                await interaction.followup.send(
                    "You're not in this game!",
                    ephemeral=True
                )
                return
            
                           
            valid_move, hit_bomb = game.make_move(interaction.user.id, cell_index)
            
            if not valid_move:
                row = cell_index // game.width
                                                       
                if row != game.next_row:
                    await interaction.followup.send(
                        "You must click the bottom-most available row first.",
                        ephemeral=True
                    )
                else:
                    row_cells = [row * game.width + i for i in range(game.width)]
                    if any(cell in game.revealed for cell in row_cells):
                        await interaction.followup.send(
                            "You can't click this row! One cell in this row has already been revealed.",
                            ephemeral=True
                        )
                    elif cell_index in game.revealed:
                        await interaction.followup.send(
                            "Invalid move! Cell already revealed.",
                            ephemeral=True
                        )
                    else:
                        await interaction.followup.send(
                            "Invalid move.",
                            ephemeral=True
                        )
                return
            
                                     
            save_towers_game(game)
            
                                 
            try:
                channel = interaction.channel
                if isinstance(channel, discord.TextChannel) and game.message_id:
                    message = await channel.fetch_message(game.message_id)
                    
                    if game.status == "completed":
                                                  
                        await complete_towers_game(interaction, self.game_id, game.to_dict(), losing_cell=cell_index if hit_bomb else None)
                    else:
                                                                        
                        if len(game.revealed) == 0 and game.round > 1:
                                                                                      
                            new_view = TowersGameView(self.game_id, game.current_turn)
                        else:
                            new_view = self
                        
                                                       
                        creator = await bot.fetch_user(game.creator_id)
                        opponent = await bot.fetch_user(game.opponent_id)
                        
                        embed = discord.Embed(
                            title="TOWERS PVP GAME",
                            color=discord.Color.green()
                        )
                        
                        embed.add_field(
                            name="PLAYERS",
                            value=f"{creator.mention} vs {opponent.mention}",
                            inline=True
                        )

                        current_player_obj = await bot.fetch_user(game.current_turn)
                        embed.add_field(
                            name="TURN",
                            value=f"{current_player_obj.mention}",
                            inline=True
                        )
                        
                        embed.add_field(
                            name="SAFE CLICKS",
                            value=f"**{len(game.revealed)}** cells revealed",
                            inline=True
                        )
                        
                        embed.add_field(
                            name="BET VALUE",
                            value=f"{VALUE_EMOJI} **{format_value_with_commas(game.bet_value)}**",
                            inline=False
                        )
                        
                        pot_value = game.bet_value * 2
                        embed.add_field(
                            name="TOTAL POT",
                            value=f"{VALUE_EMOJI} **{format_value_with_commas(pot_value)}**",
                            inline=True
                        )
                        
                                              
                        for child in new_view.children:
                            if child.custom_id and child.custom_id.startswith("tower_cell_"):
                                cell_idx = int(child.custom_id.split("_")[2])
                                if cell_idx in game.revealed:
                                    if cell_idx in game.bombs:
                                        child.disabled = True
                                        child.style = discord.ButtonStyle.danger
                                        child.label = "💣"
                                    else:
                                        child.disabled = True
                                        child.style = discord.ButtonStyle.success
                                        child.label = "✓"
                        
                        remaining_bombs = len(game.bombs - game.revealed)
                        embed.set_footer(text=f"Select a tile to reveal it. Bombs: {remaining_bombs} remaining")
                        
                        await message.edit(embed=embed, view=new_view)
            
            except Exception as e:
                print(f"Error updating towers game: {e}")
                pass
        
        return cell_callback

                                             
async def complete_towers_game_setup(interaction: discord.Interaction, game_id: str, game_data: dict):
    """Complete towers game setup and start the game"""
               
    games = load_towers_games()
    game_dict = games.get(game_id)
    
    if not game_dict:
        await interaction.followup.send(
            "Game not found!",
            ephemeral=True
        )
        return
    
    game = TowersGame.from_dict(game_dict)
    
                    
    game.generate_board()
    
                            
    save_towers_game(game)
    
                 
    creator = await bot.fetch_user(game.creator_id)
    opponent = await bot.fetch_user(game.opponent_id)
    
                       
    embed = discord.Embed(
        title="TOWERS PVP GAME STARTED",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="PLAYERS",
        value=f"{creator.mention} vs {opponent.mention}",
        inline=True
    )

    current_player = await bot.fetch_user(game.current_turn)
    embed.add_field(
        name="FIRST TURN",
        value=f"{current_player.mention}",
        inline=True
    )
    
    embed.add_field(
                name="BOMBS",
                value=f"**5 hidden bombs**",
    )
    
    embed.add_field(
        name="BET VALUE",
        value=f"{VALUE_EMOJI} **{format_value_with_commas(game.bet_value)}**",
        inline=False
    )
    
    pot_value = game.bet_value * 2
    embed.add_field(
        name="TOTAL POT",
        value=f"{VALUE_EMOJI} **{format_value_with_commas(pot_value)}**",
        inline=True
    )
    
    embed.set_footer(text="Select a tile (1-15) to reveal it. Bombs: 5 remaining")
    
                                                      
    view = TowersGameView(game_id, game.current_turn)
    
                                      
    try:
        channel = interaction.channel
        if isinstance(channel, discord.TextChannel) and game.message_id:
            message = await channel.fetch_message(game.message_id)
            await message.edit(embed=embed, view=view)
            
                                           
            started_player_name = current_player.name if current_player else f"<@{game.current_turn}>"
            await interaction.followup.send(
                f"Towers game started! It's now **{started_player_name}**'s turn.",
                ephemeral=True
            )
    except Exception as e:
        print(f"Error updating towers game message: {e}")
                                    
        message = await interaction.followup.send(embed=embed, view=view, wait=True)

async def complete_towers_game(interaction: discord.Interaction, game_id: str, game_data: dict, losing_cell: int = None):
    """Complete the towers game"""
               
    games = load_towers_games()
    game_dict = games.get(game_id)
    
    if not game_dict:
        return
    
    game = TowersGame.from_dict(game_dict)
    
                 
    winner = await bot.fetch_user(game.winner) if game.winner else None
    loser = await bot.fetch_user(game.loser) if game.loser else None
    
                              
    total_pot = game.bet_value * 2
    tax_amount = calculate_tax(total_pot)
    net_winnings = calculate_net_winnings(total_pot)
    
                                         
    winner_id_str = str(game.winner)
    loser_id_str = str(game.loser)
    
                              
    all_items = game.creator_items + game.opponent_items
    
                           
    remaining_items, taxed_items = deduct_tax_from_items(all_items, tax_amount)
    
                              
    item_counts = {}
    for item in remaining_items:
        item_counts[item] = item_counts.get(item, 0) + 1
    
    items_summary = ""
    for item_name, count in list(item_counts.items())[:10]:
        item_value = get_item_value(item_name)
        item_emoji = get_item_emoji(item_name)
        total_value = item_value * count
        items_summary += f"• {item_emoji} `{item_name}` x{count} ({VALUE_EMOJI} {format_value_with_commas(item_value)} each)\n"
    
    if len(item_counts) > 10:
        items_summary += f"• ...and {len(item_counts)-10} more item types\n"
    
                     
    await log_taxed_items(
        source_game="Towers",
        winner_id=game.winner,
        loser_id=game.loser,
        tax_amount=tax_amount,
        items=taxed_items,
        pot_value=total_pot
    )
    
    add_items_to_inventory(winner_id_str, remaining_items)
    
                         
    result_embed = discord.Embed(
        title="**BOMB HIT! GAME OVER**",
        color=discord.Color.red()
    )
    
    result_embed.add_field(
        name="WINNER",
        value=winner.mention if winner else "Unknown",
        inline=True
    )
    
    result_embed.add_field(
        name="LOSER",
        value=loser.mention if loser else "Unknown",
        inline=True
    )
    
    result_embed.add_field(
        name="WINNINGS",
        value=f"{VALUE_EMOJI} **{format_value_with_commas(total_pot)}**",
        inline=True
    )
    
    if items_summary:
        result_embed.add_field(
            name="Items Won",
            value=items_summary,
            inline=False
        )
    
    final_board = game.get_final_board_display(losing_cell)
    result_embed.add_field(
        name="FINAL BOARD",
        value=final_board,
        inline=False
    )
    
    result_embed.set_footer(text="Game Complete")
    
                                   
    remove_towers_game(game_id)
                                                        
    all_items = game.creator_items + game.opponent_items
    try:
        valid, gtype, _ = validate_items_same_type(all_items)
    except Exception:
        valid, gtype = False, None
                                      
    try:
        if valid and gtype in (GameType.MM2, GameType.ADM):
            creator_wager = sum(get_item_value(it) for it in game.creator_items)
            opponent_wager = sum(get_item_value(it) for it in game.opponent_items)
            try:
                add_user_wager(int(game.creator_id), gtype, int(creator_wager))
            except Exception:
                pass
            try:
                add_user_wager(int(game.opponent_id), gtype, int(opponent_wager))
            except Exception:
                pass
            try:
                record_completed_game({
                    "game_id": game_id,
                    "game_type": gtype,
                    "participants": [int(game.creator_id), int(game.opponent_id)],
                    "per_player": {
                        str(game.creator_id): creator_wager,
                        str(game.opponent_id): opponent_wager
                    },
                    "total_pot": total_pot,
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                print(f"Error recording completed towers game: {e}")
    except Exception:
        pass
    
                                             
    try:
        if game.message_id:
            channel = interaction.channel
            if isinstance(channel, discord.TextChannel):
                message = await channel.fetch_message(game.message_id)
                
                                     
                for child in message.components:
                    for button in child.children:
                        button.disabled = True
                
                                           
                await message.edit(
                    content="",
                    embed=result_embed,
                    view=None
                )
                
                                             
                await interaction.followup.send("Game completed! Check the updated game message above.", ephemeral=True)
                return
    
    except Exception as e:
        print(f"Error updating towers game message: {e}")
    
                                                                     
    await interaction.followup.send(embed=result_embed)

class CoinflipGame:
    def __init__(self, creator_id: int, creator_items: List[str], side: str, wild_mode: bool):
        self.creator_id = creator_id
        self.creator_items = creator_items
        self.creator_side = side.lower()
        self.wild_mode = wild_mode
        self.opponent_id = None
        self.opponent_items = []
        self.status = "waiting"                                         
        self.game_id = f"flip_{creator_id}_{int(datetime.now().timestamp())}"
        self.created_at = datetime.now().isoformat()
        self.message_id = None
        
                                   
        self.creator_value = sum(get_item_value(item) for item in creator_items)
    
    def to_dict(self):
        return {
            "game_id": self.game_id,
            "creator_id": self.creator_id,
            "creator_items": self.creator_items,
            "creator_side": self.creator_side,
            "wild_mode": self.wild_mode,
            "opponent_id": self.opponent_id,
            "opponent_items": self.opponent_items,
            "status": self.status,
            "created_at": self.created_at,
            "message_id": self.message_id,
            "creator_value": self.creator_value                 
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        game = cls(data["creator_id"], data["creator_items"], data["creator_side"], data.get("wild_mode", False))
        game.game_id = data["game_id"]
        game.opponent_id = data.get("opponent_id")
        game.opponent_items = data.get("opponent_items", [])
        game.status = data.get("status", "waiting")
        game.created_at = data.get("created_at")
        game.creator_value = data.get("creator_value", 0)                        
        game.message_id = data.get("message_id")
        return game

def save_game(game: CoinflipGame):
    """Save game to active games"""
    games = load_games()
    games[game.game_id] = game.to_dict()
    save_games(games)

def remove_game(game_id: str):
    """Remove game from active games"""
    games = load_games()
    if game_id in games:
        del games[game_id]
        save_games(games)

                                      
class JoinGameView(discord.ui.View):
    def __init__(self, game_id: str, creator_id: int, creator_side: str):
        super().__init__(timeout=None)                   
        self.game_id = game_id
        self.creator_id = creator_id
        self.creator_side = creator_side
    
    @discord.ui.button(label="JOIN", style=discord.ButtonStyle.secondary, row=0)
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                                     
        if not is_user_registered(interaction.user.id):
            await interaction.response.send_message(
                "You need to register first! Use `/register` to get started.",
                ephemeral=True
            )
            return
        
                                                        
        if interaction.user.id == self.creator_id:
            await interaction.response.send_message(
                "You can't join your own game!",
                ephemeral=True
            )
            return
        
                  
        games = load_games()
        game_data = games.get(self.game_id)
        
        if not game_data:
            await interaction.response.send_message(
                "This game no longer exists or has expired!",
                ephemeral=True
            )
            return
        
        if game_data.get('opponent_id'):
            await interaction.response.send_message(
                "This game already has an opponent!",
                ephemeral=True
            )
            return
        
        if game_data['status'] != 'waiting':
            await interaction.response.send_message(
                "This game is no longer accepting joins!",
                ephemeral=True
            )
            return
        
        required_value = game_data['creator_value']
        
                                                        
        min_allowed = required_value * 0.9
        max_allowed = required_value * 1.1
        
                                     
        user_items = get_user_all_items(str(interaction.user.id))
        
        if not user_items:
            await interaction.response.send_message(
                "You don't have any items to bet!",
                ephemeral=True
            )
            return
        
                                              
        user_total_value = calculate_inventory_value(str(interaction.user.id))
        if user_total_value < min_allowed:
            await interaction.response.send_message(
                f"You need at least {VALUE_EMOJI} **{format_value_with_commas(min_allowed)}** in items to join this game!\n"
                f"Your current inventory value: {VALUE_EMOJI} **{format_value_with_commas(user_total_value)}**",
                ephemeral=True
            )
            return
        
                                   
        opponent_side = "tails" if self.creator_side == "heads" else "heads"
        
                                      
        embed = discord.Embed(
            title="Select Your Items",
            description=f"Select items worth between {VALUE_EMOJI} **{format_value_with_commas(min_allowed)}** and {VALUE_EMOJI} **{format_value_with_commas(max_allowed)}** to join this game.\n\n"
                       f"**Creator's side:** {self.creator_side.upper()}\n"
                       f"**Your side (auto-assigned):** {opponent_side.upper()}",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="Instructions",
            value=f"1. Select items from the dropdown\n2. You can select multiple items\n3. Total value must be within 10% of the game bet ({VALUE_EMOJI} **{format_value_with_commas(required_value)}**)\n4. Click 'Confirm Selection' when done",
            inline=False
        )
        
        view = ItemSelectionView(user_items, required_value, self.game_id, opponent_side, allow_range=True)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    @discord.ui.button(label="CANCEL", style=discord.ButtonStyle.danger, row=0)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                                      
        if interaction.user.id != self.creator_id:
            await interaction.response.send_message(
                "Only the game creator can cancel the game!",
                ephemeral=True
            )
            return
        
                  
        games = load_games()
        game_data = games.get(self.game_id)
        
        if not game_data:
            await interaction.response.send_message(
                "This game no longer exists!",
                ephemeral=True
            )
            return
        
        if game_data.get('opponent_id'):
            await interaction.response.send_message(
                "Cannot cancel game with an opponent!",
                ephemeral=True
            )
            return
        
                                 
        creator_items = game_data['creator_items']
        add_items_to_inventory(str(self.creator_id), creator_items)
        
                     
        remove_game(self.game_id)
        
                                 
        try:
            embed = discord.Embed(
                title="COINFLIP GAME CANCELLED",
                description=f"This game has been cancelled by the creator.",
                color=discord.Color.red()
            )
            
            embed.add_field(
                name="Items Returned",
                value=f"All items have been returned to <@{self.creator_id}>",
                inline=False
            )
            
                                 
            for child in self.children:
                child.disabled = True
            
            await interaction.response.edit_message(embed=embed, view=self)
            
                                          
            await interaction.followup.send(
                f"Game cancelled! Your items have been returned to your inventory.",
                ephemeral=True
            )
        except Exception as e:
            print(f"Error cancelling game: {e}")
            await interaction.response.send_message(
                f"Game cancelled! Your items have been returned to your inventory.",
                ephemeral=True
            )

async def complete_flip_game(interaction: discord.Interaction, game_id: str, game_data: dict):
    """Complete the flip game with Wild Mode reversal and improved tax deduction"""
                             
    creator_items = game_data['creator_items']
    opponent_items = game_data['opponent_items']
    creator_side = game_data['creator_side']
    opponent_side = "tails" if creator_side == "heads" else "heads"
    wild_mode_enabled = game_data.get('wild_mode', False)
    
                           
    creator_value = game_data['creator_value']
    total_pot = creator_value * 2
    tax_amount = calculate_tax(total_pot)
    net_winnings = calculate_net_winnings(total_pot)
    
                   
    all_items = creator_items + opponent_items
    valid, game_type, _ = validate_items_same_type(all_items)
    
                  
    result = random.choice(["heads", "tails"])
    
                                    
    wild_mode_activated = False
    
    if wild_mode_enabled:
        wild_mode_activated = random.random() < WILD_MODE_CHANCE
    
                                           
    creator_wins_normal = creator_side == result
    
                                           
    if wild_mode_activated:
        creator_wins = not creator_wins_normal                       
    else:
        creator_wins = creator_wins_normal
    
                      
    creator_id_str = str(game_data['creator_id'])
    opponent_id_str = str(game_data['opponent_id'])
    
                                                                            
                                                                             
    
    if creator_wins:
        winner_id = creator_id_str
        winner_name = f"<@{game_data['creator_id']}>"
        loser_id = opponent_id_str
        loser_name = f"<@{game_data['opponent_id']}>"
        
                                                              
        remove_items_from_inventory(opponent_id_str, opponent_items)
        
                                                                                             
        all_items = creator_items + opponent_items
        
                               
        remaining_items, taxed_items = deduct_tax_from_items(all_items, tax_amount)
        
                         
        await log_taxed_items(
            source_game="Coinflip",
            winner_id=int(winner_id),
            loser_id=int(loser_id),
            tax_amount=tax_amount,
            items=taxed_items,
            pot_value=total_pot
        )
        
        add_items_to_inventory(winner_id, remaining_items)
                                                                     
    try:
        if valid and game_type in (GameType.MM2, GameType.ADM):
                                                                       
            try:
                add_user_wager(int(game_data['creator_id']), game_type, int(creator_value))
            except Exception:
                pass
            try:
                add_user_wager(int(game_data['opponent_id']), game_type, int(creator_value))
            except Exception:
                pass
                                                        
            try:
                record_completed_game({
                    "game_id": game_id,
                    "game_type": game_type,
                    "participants": [int(game_data.get('creator_id', 0)), int(game_data.get('opponent_id', 0))],
                    "per_player": {
                        str(game_data.get('creator_id', "")): int(creator_value),
                        str(game_data.get('opponent_id', "")): int(creator_value)
                    },
                    "total_pot": int(total_pot),
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                print(f"Error recording completed flip game: {e}")
    except Exception:
        pass
        
    else:
        winner_id = opponent_id_str
        winner_name = f"<@{game_data['opponent_id']}>"
        loser_id = creator_id_str
        loser_name = f"<@{game_data['creator_id']}>"
        
                                                                                              
        remove_items_from_inventory(opponent_id_str, opponent_items)
        
                                              
        all_items = creator_items + opponent_items
        
                               
        remaining_items, taxed_items = deduct_tax_from_items(all_items, tax_amount)
        
                         
        await log_taxed_items(
            source_game="Coinflip",
            winner_id=int(winner_id),
            loser_id=int(loser_id),
            tax_amount=tax_amount,
            items=taxed_items,
            pot_value=total_pot
        )
        
        add_items_to_inventory(winner_id, remaining_items)
                                                                                   
    result_embed = discord.Embed(
        title="COINFLIP RESULT",
        color=discord.Color.green() if not wild_mode_activated else discord.Color.orange()
    )
    
                                            
    if result == "heads" and os.path.exists(HEADS_IMAGE_PATH):
        file = discord.File(HEADS_IMAGE_PATH, filename="heads.png")
        result_embed.set_thumbnail(url="attachment://heads.png")
    elif result == "tails" and os.path.exists(TAILS_IMAGE_PATH):
        file = discord.File(TAILS_IMAGE_PATH, filename="tails.png")
        result_embed.set_thumbnail(url="attachment://tails.png")
    else:
        file = None                     
    
    result_embed.add_field(
        name="Flip Result",
        value=f"**{result.upper()}**",
        inline=True
    )
    
    result_embed.add_field(
        name="Winner",
        value=winner_name,
        inline=True
    )
    
    result_embed.add_field(
        name="Loser",
        value=loser_name,
        inline=True
    )
    
    if wild_mode_activated:
        result_embed.add_field(
            name=f"{WILD_MODE_EMOJI} WILD MODE ACTIVATED!",
            value=f"**OUTCOME REVERSED!**\n",
            inline=False
        )
    elif wild_mode_enabled and not wild_mode_activated:
        result_embed.add_field(
            name="Wild Mode",
            value=f"Was enabled but did not activate (1% chance)",
            inline=False
        )
    
                               
    all_items_count = len(creator_items) + len(opponent_items)
    result_embed.add_field(
        name="Winnings",
        value=f"{winner_name} wins {VALUE_EMOJI} **{format_value_with_commas(total_pot)}** worth of items!\n(Total: **{all_items_count}** items)",
        inline=False
    )
    
                                   
    all_items_combined = creator_items + opponent_items
    winner_items_text = ""
    item_counts = {}
    for item in all_items_combined:
        item_counts[item] = item_counts.get(item, 0) + 1
    
    for item_name, count in list(item_counts.items())[:5]:
        item_emoji = get_item_emoji(item_name)
        item_value = get_item_value(item_name)
        winner_items_text += f"• {item_emoji} `{item_name}` x{count} ({VALUE_EMOJI} {format_value_with_commas(item_value)} each)\n"
    
    if len(item_counts) > 5:
        winner_items_text += f"• ...and {len(item_counts)-5} more item types\n"
    
    result_embed.add_field(
        name="Items Won",
        value=winner_items_text or "No items",
        inline=False
    )
    
                                   
    remove_game(game_id)
    
                                                            
    if game_data['creator_id'] in bot.creating_users:
        bot.creating_users.remove(game_data['creator_id'])
    
                                             
    try:
        if game_data.get('message_id'):
            channel = interaction.channel
            if isinstance(channel, discord.TextChannel):
                message = await channel.fetch_message(game_data['message_id'])
                
                                                                       
                if file:
                    await message.edit(
                        content="",
                        embed=result_embed,
                        attachments=[file],                                        
                        view=None                                  
                    )
                else:
                    await message.edit(
                        content="",
                        embed=result_embed,
                        view=None
                    )
                
                                             
                await interaction.followup.send("Game completed! Check the updated game message above.", ephemeral=True)
                return
    
    except Exception as e:
        print(f"Error updating game message: {e}")
    
                                                                     
    if file:
        await interaction.followup.send(file=file, embed=result_embed)
    else:
        await interaction.followup.send(embed=result_embed)

                                         
class Withdrawal:
    def __init__(self, user_id: int, items: List[str], withdrawal_id: str = None):
        self.user_id = user_id
        self.items = items
        self.withdrawal_id = withdrawal_id or f"withdraw_{user_id}_{int(datetime.now().timestamp())}"
        self.created_at = datetime.now().isoformat()
        self.status = "pending"                                
        self.ticket_channel_id = None
        self.ticket_message_id = None
        self.total_value = sum(get_item_value(item) for item in items)
    
    def to_dict(self):
        return {
            "withdrawal_id": self.withdrawal_id,
            "user_id": self.user_id,
            "items": self.items,
            "total_value": self.total_value,
            "created_at": self.created_at,
            "status": self.status,
            "ticket_channel_id": self.ticket_channel_id,
            "ticket_message_id": self.ticket_message_id
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        withdrawal = cls(
            data["user_id"],
            data["items"],
            data["withdrawal_id"]
        )
        withdrawal.total_value = data.get("total_value", 0)
        withdrawal.created_at = data.get("created_at")
        withdrawal.status = data.get("status", "pending")
        withdrawal.ticket_channel_id = data.get("ticket_channel_id")
        withdrawal.ticket_message_id = data.get("ticket_message_id")
        return withdrawal

def save_withdrawal(withdrawal: Withdrawal):
    """Save withdrawal to active withdrawals"""
    withdrawals = load_withdrawals()
    withdrawals[withdrawal.withdrawal_id] = withdrawal.to_dict()
    save_withdrawals(withdrawals)

def remove_withdrawal(withdrawal_id: str):
    """Remove withdrawal from active withdrawals"""
    withdrawals = load_withdrawals()
    if withdrawal_id in withdrawals:
        del withdrawals[withdrawal_id]
        save_withdrawals(withdrawals)

class WithdrawalItemSelectionView(discord.ui.View):
    def __init__(self, user_items: List[Tuple[str, int]]):
        super().__init__(timeout=None)
        self.user_items = user_items
        self.selected_items = []
        
                      
        self.dropdown = ItemSelectDropdown(user_items, MAX_BET_VALUE)
        self.add_item(self.dropdown)
    
    @discord.ui.button(label="CONFIRM WITHDRAWAL", style=discord.ButtonStyle.secondary, row=1)
    async def confirm_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.dropdown.selected_items:
            await interaction.response.send_message(
                "Please select at least one item to withdraw!",
                ephemeral=True
            )
            return
        
        self.selected_items = self.dropdown.selected_items
        self.selected_value = self.dropdown.selected_value
        
                                      
        valid, game_type, error_msg = validate_items_same_type(self.selected_items)
        if not valid:
            await interaction.response.send_message(
                f"❌ {error_msg}",
                ephemeral=True
            )
            return
        
                                                        
        remove_items_from_inventory(str(interaction.user.id), self.selected_items)
        
                           
        withdrawal = Withdrawal(interaction.user.id, self.selected_items)
        
                                     
        category = bot.get_channel(WITHDRAWAL_CATEGORY_ID)
        if not category or not isinstance(category, discord.CategoryChannel):
                                                              
            category = bot.get_channel(WITHDRAWAL_CATEGORY_ID)
            if not category:
                await interaction.response.send_message(
                    "Withdrawal category not found! Please contact an admin.",
                    ephemeral=True
                )
                                      
                add_items_to_inventory(str(interaction.user.id), self.selected_items)
                return
        
                               
        guild = interaction.guild
        support_role = guild.get_role(SUPPORT_TEAM_ROLE_ID)
        
                         
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        if support_role:
            overwrites[support_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        
                        
        channel_name = f"withdraw-{interaction.user.name[:20]}-{withdrawal.withdrawal_id[-6:]}"
        ticket_channel = await guild.create_text_channel(
            name=channel_name,
            category=category if isinstance(category, discord.CategoryChannel) else None,
            overwrites=overwrites,
            topic=f"Withdrawal request from {interaction.user.name} (ID: {interaction.user.id})"
        )
        
                         
        withdrawal.ticket_channel_id = ticket_channel.id
        save_withdrawal(withdrawal)
        
                                
        registrations = load_registrations()
        user_data = registrations.get(str(interaction.user.id), {})
        roblox_username = user_data.get('roblox_username', 'Not registered')
        roblox_avatar = user_data.get('roblox_avatar')
        
                                 
        item_counts = {}
        for item in self.selected_items:
            item_counts[item] = item_counts.get(item, 0) + 1
        
        items_text = ""
        for item_name, count in item_counts.items():
            item_value = get_item_value(item_name)
            item_emoji = get_item_emoji(item_name)
            total_value = item_value * count
            items_text += f"• {item_emoji} **{item_name}** x{count} - {VALUE_EMOJI} **{format_value_with_commas(total_value)}**\n"
        
                                 
        embed = discord.Embed(
            title="WITHDRAWAL REQUEST",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        
                                                       
        if roblox_avatar:
            embed.set_thumbnail(url=roblox_avatar)
        
                       
        embed.add_field(
            name="User",
            value=f"{interaction.user.mention}",
            inline=True
        )
        
        embed.add_field(
            name="Roblox Username",
            value=f"**{roblox_username}**",
            inline=True
        )
        
        embed.add_field(
            name="Withdrawal ID",
            value=f"`{withdrawal.withdrawal_id}`",
            inline=False
        )
        
        embed.add_field(
            name="Items to Withdraw",
            value=items_text or "No items",
            inline=True
        )
        
        embed.add_field(
            name="Total Value",
            value=f"{VALUE_EMOJI} **{format_value_with_commas(self.selected_value)}**",
            inline=True
        )
        
        embed.set_footer(text=f"User ID: {interaction.user.id}")
        
                            
        view = WithdrawalTicketView(withdrawal.withdrawal_id, interaction.user.id)
        
                                        
        message = await ticket_channel.send(
            content=f"{support_role.mention if support_role else ''} {interaction.user.mention}",
            embed=embed,
            view=view
        )
        
                         
        withdrawal.ticket_message_id = message.id
        save_withdrawal(withdrawal)
        
                                   
        confirm_embed = discord.Embed(
            title="Withdrawal Request Submitted",
            color=discord.Color.green(),
            description=f"Your withdrawal request has been created in {ticket_channel.mention}."
        )
        
        confirm_embed.add_field(
            name="Next Steps",
            value="1. A support team member will review your request\n2. They will verify the items and process your withdrawal\n3. You will be notified when completed\n4. You can cancel the withdrawal anytime using the button in the ticket",
            inline=False
        )
        
        await interaction.response.send_message(embed=confirm_embed, ephemeral=True)
        
                          
        for child in self.children:
            child.disabled = True
        
        try:
            await interaction.message.edit(view=self)
        except:
            pass

class WithdrawalTicketView(discord.ui.View):
    def __init__(self, withdrawal_id: str, user_id: int):
        super().__init__(timeout=None)
        self.withdrawal_id = withdrawal_id
        self.user_id = user_id
    
    @discord.ui.button(label="APPROVE", style=discord.ButtonStyle.secondary, row=0)
    async def approve_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                                
        if interaction.user.id not in ADMIN_USER_IDS:
            await interaction.response.send_message(
                "Only admins can approve withdrawal requests!",
                ephemeral=True
            )
            return
        
                        
        withdrawals = load_withdrawals()
        withdrawal_data = withdrawals.get(self.withdrawal_id)
        
        if not withdrawal_data:
            await interaction.response.send_message(
                "Withdrawal not found!",
                ephemeral=True
            )
            return
        
        if withdrawal_data['status'] != 'pending':
            await interaction.response.send_message(
                f"This withdrawal is already {withdrawal_data['status']}!",
                ephemeral=True
            )
            return
        
                       
        withdrawal_data['status'] = 'approved'
        save_withdrawals(withdrawals)
        
                          
        embed = interaction.message.embeds[0]
        embed.color = discord.Color.green()
        embed.title = embed.title.replace("WITHDRAWAL REQUEST", "WITHDRAWAL APPROVED")
        
                           
        embed.add_field(
            name="Approved By",
            value=f"{interaction.user.mention}",
            inline=False
        )
        
        embed.add_field(
            name="Approved At",
            value=f"<t:{int(datetime.now().timestamp())}:F>",
            inline=False
        )
        
                             
        for child in self.children:
            child.disabled = True
        
        await interaction.response.edit_message(embed=embed, view=self)
        
                                                   
    
    @discord.ui.button(label="CANCEL", style=discord.ButtonStyle.danger, row=0)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                                                        
        support_role = interaction.guild.get_role(SUPPORT_TEAM_ROLE_ID)
        is_support = support_role and support_role in interaction.user.roles
        
        if interaction.user.id != self.user_id and not is_support:
            await interaction.response.send_message(
                "Only the requester or support team can cancel this withdrawal!",
                ephemeral=True
            )
            return
        
                        
        withdrawals = load_withdrawals()
        withdrawal_data = withdrawals.get(self.withdrawal_id)
        
        if not withdrawal_data:
            await interaction.response.send_message(
                "Withdrawal not found!",
                ephemeral=True
            )
            return
        
        if withdrawal_data['status'] != 'pending':
            await interaction.response.send_message(
                f"This withdrawal is already {withdrawal_data['status']}!",
                ephemeral=True
            )
            return
        
                              
        add_items_to_inventory(str(self.user_id), withdrawal_data['items'])
        
                       
        withdrawal_data['status'] = 'cancelled'
        save_withdrawals(withdrawals)
        
                          
        embed = interaction.message.embeds[0]
        embed.color = discord.Color.red()
        embed.title = embed.title.replace("WITHDRAWAL REQUEST", "WITHDRAWAL CANCELLED")
        
                               
        embed.add_field(
            name="Cancelled By",
            value=f"{interaction.user.mention}",
            inline=False
        )
        
        embed.add_field(
            name="Items Returned",
            value="Items have been returned to user's inventory",
            inline=False
        )
        
                             
        for child in self.children:
            child.disabled = True
        
        await interaction.response.edit_message(embed=embed, view=self)

        ticket_channel = interaction.message.channel
        try:
            await ticket_channel.delete(reason=f"Withdrawal {self.withdrawal_id} cancelled")
        except Exception:
            pass
        
                                                    

                                   
class AddItemModal(discord.ui.Modal, title="ADD ITEMS TO USER"):
    def __init__(self):
        super().__init__()

    roblox_username = discord.ui.TextInput(
        label="Roblox Username",
        placeholder="Enter the user's Roblox username",
        required=True,
        max_length=50
    )

    item_name = discord.ui.TextInput(
        label="Item Name",
        placeholder="Enter the exact item name",
        required=True,
        max_length=100
    )

    quantity = discord.ui.TextInput(
        label="Quantity",
        placeholder="Enter quantity (default: 1)",
        default="1",
        required=True,
        max_length=3
    )

    async def on_submit(self, interaction: discord.Interaction):
                                
        allowed, uses, limit = increment_staff_use(interaction.user.id)
        if not allowed:
            await interaction.response.send_message(f"Staff action limit reached ({uses}/{limit}) — try again later.", ephemeral=True)
            return
        username = self.roblox_username.value.strip()
        item_name = self.item_name.value.strip()
        try:
            quantity = int(self.quantity.value.strip())
        except Exception:
            await interaction.response.send_message(
                "Invalid quantity provided.",
                ephemeral=True
            )
            return

                                                 
        user_id = find_user_id_by_roblox(username)
        if not user_id:
            await interaction.response.send_message(
                f"No registered user found for Roblox username `{username}`. They must register first.",
                ephemeral=True
            )
            return

                                                
        if not is_user_registered(user_id):
            await interaction.response.send_message(
                f"User for Roblox `{username}` is not registered! They need to use `/register` first.",
                ephemeral=True
            )
            return

                                                
        items = load_items()
        if item_name not in items:
                                  
            available_items = list(items.keys())
            available_items_str = "\n".join([f"• `{item}`" for item in available_items[:10]])
            if len(available_items) > 10:
                available_items_str += f"\n• ...and {len(available_items)-10} more"

            embed = discord.Embed(
                title="Item Not Found",
                description=f"Item `{item_name}` does not exist in the items database.",
                color=discord.Color.red()
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

                           
        if quantity <= 0:
            await interaction.response.send_message(
                "Quantity must be a positive number!",
                ephemeral=True
            )
            return

        if quantity > 100:
            await interaction.response.send_message(
                "Maximum quantity per command is 100!",
                ephemeral=True
            )
            return

                          
        item_details = items[item_name]
        item_value = item_details.get('value', 0)
        item_emoji = item_details.get('emoji', VALUE_EMOJI)
        item_type = item_details.get('type', 'Unknown')
        total_value = item_value * quantity

                                       
        items_to_add = [item_name] * quantity
        add_items_to_inventory(str(user_id), items_to_add)

                                     
        updated_value = calculate_inventory_value(str(user_id))

                              
        embed = discord.Embed(
            title="Items Added Successfully",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Recipient",
            value=f"<@{user_id}>",
            inline=True
        )

        embed.add_field(
            name="Item Added",
            value=f"{item_emoji} `{item_name}` x{quantity}",
            inline=True
        )

        embed.add_field(
            name="Type",
            value=f"**{item_type}**",
            inline=True
        )

        embed.add_field(
            name="Value",
            value=f"{VALUE_EMOJI} **{format_value_with_commas(total_value)}**",
            inline=True
        )

        embed.add_field(
            name="Added By",
            value=f"{interaction.user.mention}",
            inline=False
        )

        embed.timestamp = datetime.now()

        await interaction.response.send_message(embed=embed, ephemeral=True)

class RemoveItemModal(discord.ui.Modal, title="REMOVE ITEMS FROM USER"):
    def __init__(self, user_id: str = None):
        super().__init__()
        self.user_id = user_id

    user_id_input = discord.ui.TextInput(
        label="USER ID",
        placeholder="Enter the user's Discord ID",
        required=True,
        max_length=20
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            user_id = int(self.user_id_input.value.strip())
        except ValueError:
            await interaction.followup.send(
                "Invalid user ID! Must be a number.",
                ephemeral=True
            )
            return

                                                
        if not is_user_registered(user_id):
            await interaction.followup.send(
                f"User with ID `{user_id}` is not registered!",
                ephemeral=True
            )
            return

                              
        user_inventory = get_user_inventory(str(user_id))
        if not user_inventory:
            await interaction.followup.send(
                f"User <@{user_id}> has no items in their inventory!",
                ephemeral=True
            )
            return

                                            
        class ItemSelectView(discord.ui.View):
            def __init__(self, user_id: int, user_inventory: list):
                super().__init__(timeout=None)
                self.user_id = user_id
                self.user_inventory = user_inventory

                                               
                item_counts = {}
                for item in user_inventory:
                    item_name = item["name"] if isinstance(item, dict) else item
                    item_counts[item_name] = item_counts.get(item_name, 0) + 1

                                    
                options = []
                for item_name, count in item_counts.items():
                    item_emoji = get_item_emoji(item_name)
                    item_value = get_item_value(item_name)
                    label = f"{item_name} (x{count})"
                    description = format_value_with_commas(item_value)

                                          
                    if len(label) > 100:
                        label = label[:97] + "..."
                    if len(description) > 100:
                        description = description[:97] + "..."

                    options.append(discord.SelectOption(
                        label=label,
                        description=description,
                        value=item_name,
                        emoji=item_emoji
                    ))

                                                     
                if len(options) > 25:
                    options = options[:25]

                select = discord.ui.Select(
                    placeholder="Select an item to remove",
                    options=options,
                    custom_id="remove_item_select"
                )

                async def select_callback(interaction: discord.Interaction):
                    selected_item = select.values[0]

                                                 
                    class QuantityModal(discord.ui.Modal, title=f"REMOVE {selected_item.upper()}"):
                        def __init__(self):
                            super().__init__()

                        quantity = discord.ui.TextInput(
                            label="QUANTITY TO REMOVE",
                            placeholder=f"Available: {item_counts[selected_item]}",
                            default="1",
                            required=True,
                            max_length=3
                        )

                        async def on_submit(self, interaction: discord.Interaction):
                            try:
                                quantity = int(self.quantity.value.strip())
                            except ValueError:
                                try:
                                    await interaction.followup.send(
                                        "Invalid quantity! Must be a number.",
                                        ephemeral=True
                                    )
                                except discord.errors.NotFound:
                                    pass
                                return

                            if quantity <= 0:
                                try:
                                    await interaction.followup.send(
                                        "Quantity must be a positive number!",
                                        ephemeral=True
                                    )
                                except discord.errors.NotFound:
                                    pass
                                return

                            available = item_counts[selected_item]
                            if quantity > available:
                                try:
                                    await interaction.followup.send(
                                        f"User only has {available} of this item!",
                                        ephemeral=True
                                    )
                                except discord.errors.NotFound:
                                    pass
                                return

                                                         
                            items_to_remove = [selected_item] * quantity
                            remove_items_from_inventory(str(self.user_id), items_to_remove)

                                            
                            item_value = get_item_value(selected_item)
                            item_emoji = get_item_emoji(selected_item)
                            total_value = item_value * quantity

                                                  
                            embed = discord.Embed(
                                title="Items Removed Successfully",
                                color=discord.Color.red()
                            )

                            embed.add_field(
                                name="Target User",
                                value=f"<@{self.user_id}>",
                                inline=True
                            )

                            embed.add_field(
                                name="Item Removed",
                                value=f"{item_emoji} `{selected_item}` x{quantity}",
                                inline=True
                            )

                            embed.add_field(
                                name="Value",
                                value=f"{VALUE_EMOJI} **{format_value_with_commas(total_value)}**",
                                inline=True
                            )

                            embed.add_field(
                                name="Removed By",
                                value=f"{interaction.user.mention}",
                                inline=False
                            )

                            embed.timestamp = datetime.now()

                            try:
                                await interaction.followup.send(embed=embed, ephemeral=True)
                            except discord.errors.NotFound:
                                channel = interaction.client.get_channel(ADMIN_PANEL_CHANNEL_ID)
                                if channel:
                                    await channel.send(embed=embed)

                    modal = QuantityModal()
                    modal.user_id = self.user_id
                    await interaction.response.send_modal(modal)

                select.callback = select_callback
                self.add_item(select)

        view = ItemSelectView(user_id, user_inventory)
        embed = discord.Embed(
            title="Select Item to Remove",
            description=f"Select an item from <@{user_id}>'s inventory to remove.",
            color=discord.Color.orange()
        )

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)




class AddStockItemModal(discord.ui.Modal, title="ADD ITEM TO STOCK"):
    item_name = discord.ui.TextInput(
        label="Item Name",
        placeholder="Enter the exact item name",
        required=True,
        max_length=100
    )

    quantity = discord.ui.TextInput(
        label="Quantity",
        placeholder="Enter quantity (default: 1)",
        default="1",
        required=True,
        max_length=3
    )

    async def on_submit(self, interaction: discord.Interaction):
        item_name = self.item_name.value.strip()
        try:
            quantity = int(self.quantity.value.strip())
        except Exception:
            await interaction.response.send_message("Invalid quantity provided.", ephemeral=True)
            return

        if quantity <= 0:
            await interaction.response.send_message("Quantity must be a positive number!", ephemeral=True)
            return

        if quantity > 100:
            await interaction.response.send_message("Maximum quantity per addition is 100!", ephemeral=True)
            return

        items = load_items()
        if item_name not in items:
            await interaction.response.send_message(
                f"Item `{item_name}` does not exist in the items database.",
                ephemeral=True
            )
            return

        add_stock_item(item_name, quantity)
        try:
            await update_event_panel_embed()
        except Exception:
            pass

        embed = discord.Embed(
            title="Stock Updated",
            description=f"Added {get_item_emoji(item_name)} `{item_name}` x{quantity} to stock.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

        stock_refreshed = False
        if getattr(self, 'parent_view', None) is not None:
            try:
                if getattr(self.parent_view, 'message', None) is not None:
                    mode = getattr(self.parent_view, 'mode', GameType.MM2)
                    updated_embed, _ = build_stock_embed(mode)
                    await self.parent_view.message.edit(embed=updated_embed, view=self.parent_view)
                    stock_refreshed = True
            except Exception:
                stock_refreshed = False

        if not stock_refreshed and getattr(self, 'parent_view', None) is not None:
            try:
                if getattr(self.parent_view, 'message', None) is not None:
                    await self.parent_view.message.delete()
            except Exception:
                pass
            try:
                mode = getattr(self.parent_view, 'mode', GameType.MM2)
                updated_embed, updated_view = build_stock_embed(mode)
                await interaction.followup.send(embed=updated_embed, view=updated_view, ephemeral=True)
            except Exception:
                pass


class RemoveStockItemModal(discord.ui.Modal, title="REMOVE ITEM FROM STOCK"):
    item_name = discord.ui.TextInput(
        label="Item Name",
        placeholder="Enter the exact item name",
        required=True,
        max_length=100
    )

    quantity = discord.ui.TextInput(
        label="Quantity",
        placeholder="Enter quantity to remove (default: 1)",
        default="1",
        required=True,
        max_length=3
    )

    async def on_submit(self, interaction: discord.Interaction):
        item_name = self.item_name.value.strip()
        try:
            quantity = int(self.quantity.value.strip())
        except Exception:
            await interaction.response.send_message("Invalid quantity provided.", ephemeral=True)
            return

        if quantity <= 0:
            await interaction.response.send_message("Quantity must be a positive number!", ephemeral=True)
            return

        stock_items = load_stock()
        matching = next((entry for entry in stock_items if entry["name"].strip().lower() == item_name.lower()), None)
        if not matching:
            await interaction.response.send_message(
                f"Item `{item_name}` is not currently in stock.",
                ephemeral=True
            )
            return

        if quantity > matching["quantity"]:
            await interaction.response.send_message(
                f"Only {matching['quantity']} of `{item_name}` are in stock.",
                ephemeral=True
            )
            return

        remove_stock_item(item_name, quantity)
        try:
            await update_event_panel_embed()
        except Exception:
            pass

        embed = discord.Embed(
            title="Stock Updated",
            description=f"Removed {get_item_emoji(item_name)} `{item_name}` x{quantity} from stock.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

        stock_refreshed = False
        if getattr(self, 'parent_view', None) is not None:
            try:
                if getattr(self.parent_view, 'message', None) is not None:
                    mode = getattr(self.parent_view, 'mode', GameType.MM2)
                    updated_embed, _ = build_stock_embed(mode)
                    await self.parent_view.message.edit(embed=updated_embed, view=self.parent_view)
                    stock_refreshed = True
            except Exception:
                stock_refreshed = False

        if not stock_refreshed and getattr(self, 'parent_view', None) is not None:
            try:
                if getattr(self.parent_view, 'message', None) is not None:
                    await self.parent_view.message.delete()
            except Exception:
                pass
            try:
                mode = getattr(self.parent_view, 'mode', GameType.MM2)
                updated_embed, updated_view = build_stock_embed(mode)
                await interaction.followup.send(embed=updated_embed, view=updated_view, ephemeral=True)
            except Exception:
                pass


class TaxPanelView(discord.ui.View):

    @discord.ui.button(label="5%", style=discord.ButtonStyle.secondary, row=0, custom_id="tax_rate_5")
    async def tax_rate_5(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_tax_rate(interaction, 0.05)

    @discord.ui.button(label="7.5%", style=discord.ButtonStyle.secondary, row=0, custom_id="tax_rate_7_5")
    async def tax_rate_7_5(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_tax_rate(interaction, 0.075)

    @discord.ui.button(label="10%", style=discord.ButtonStyle.secondary, row=0, custom_id="tax_rate_10")
    async def tax_rate_10(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_tax_rate(interaction, 0.10)

    @discord.ui.button(label="TAXED ITEMS", style=discord.ButtonStyle.secondary, row=0, custom_id="tax_panel_taxed_items")
    async def taxed_items_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                                                                           
        staff_profiles = ensure_staff_profiles()
        if staff_profiles and str(interaction.user.id) in staff_profiles:
            await interaction.response.send_message("Bloxloot staff are not allowed to interact with the tax panel.", ephemeral=True)
            return

        if interaction.user.id not in ADMIN_USER_IDS:
            await interaction.response.send_message("You don't have permission to use this panel!", ephemeral=True)
            return

                                                
        allowed, uses, limit = increment_staff_use(interaction.user.id)
        if not allowed:
            await interaction.response.send_message(f"You have reached your daily panel interactions ({uses}/{limit}).", ephemeral=True)
            return
        try:
            await update_tax_panel_embed()
        except Exception:
            pass

        taxed_items = load_taxed_items()
        if not taxed_items:
            await interaction.response.send_message("No taxed items have been logged yet.", ephemeral=True)
            return

        embed, view = build_taxed_items_response()
        if not embed or not view:
            await interaction.response.send_message("No taxed items have been logged yet.", ephemeral=True)
            return

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    async def handle_tax_rate(self, interaction: discord.Interaction, rate: float):
                                                                           
        staff_profiles = ensure_staff_profiles()
        if staff_profiles and str(interaction.user.id) in staff_profiles:
            await interaction.response.send_message("Bloxloot staff are not allowed to interact with the tax panel.", ephemeral=True)
            return

        if interaction.user.id not in ADMIN_USER_IDS:
            await interaction.response.send_message("You don't have permission to use this panel!", ephemeral=True)
            return

                                                       
        allowed, uses, limit = increment_staff_use(interaction.user.id)
        if not allowed:
            await interaction.response.send_message(f"You have reached your daily panel interactions ({uses}/{limit}).", ephemeral=True)
            return

        set_house_tax(rate)
        try:
            await create_tax_panel()
                                                             
            await update_all_game_embeds()
        except Exception as e:
            print(f"Failed to update tax panel after rate change: {e}")

        try:
            await update_tax_panel_embed()
        except Exception:
            pass

        await interaction.response.send_message(
            f"Tax rate updated to **{rate * 100:.1f}%**.",
            ephemeral=True
        )


class UpdatePanelSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Create Update", value="create_update", description="Start a new update build", emoji="<:ye:1530518980765286452>"),
            discord.SelectOption(label="Schedule Update", value="schedule_update", description="Plan a future update", emoji="<:ye:1530518980765286452>"),
        ]
        super().__init__(placeholder="Choose an update action...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0] if self.values else "unknown"
        if selected == "create_update":
            view = CreateUpdateEditorView()
            embed = view.build_embed()
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
            try:
                view.message = await interaction.original_message()
            except Exception:
                view.message = None
            return

        await interaction.response.send_message(
            f"Selected **{selected.replace('_', ' ').title()}**. More update actions will be added soon.",
            ephemeral=True
        )


class UpdatePanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(UpdatePanelSelect())


class EditUpdateTextModal(discord.ui.Modal):
    def __init__(self, parent_view, kind: str, current_value: str = ""):
        self.parent_view = parent_view
        self.kind = kind
        title_text = {
            "title": "Edit Update Title",
            "description": "Edit Update Description",
            "footer": "Edit Update Footer",
        }.get(kind, "Edit Update Field")
        super().__init__(title=title_text)
        label_text = {
            "title": "Title",
            "description": "Description",
            "footer": "Footer",
        }.get(kind, "Value")
        self.input = discord.ui.TextInput(
            label=label_text,
            required=False,
            default=current_value,
            style=discord.TextStyle.paragraph if kind in {"description", "footer"} else discord.TextStyle.short,
        )
        self.add_item(self.input)

    async def on_submit(self, interaction: discord.Interaction):
        value = self.input.value.strip()
        if self.kind == "title":
            self.parent_view.title = value or "Bloxloot Update V1.0"
        elif self.kind == "description":
            self.parent_view.description = value
        elif self.kind == "footer":
            self.parent_view.footer = value or "Powered by Bloxloot"

        await self.parent_view.refresh_message(interaction)


class AddUpdateFieldModal(discord.ui.Modal):
    def __init__(self, parent_view):
        self.parent_view = parent_view
        super().__init__(title="Add Update Field")
        self.name_input = discord.ui.TextInput(label="Field Name", required=False, placeholder="Example: New Feature")
        self.value_input = discord.ui.TextInput(label="Field Value", required=False, style=discord.TextStyle.paragraph, placeholder="Example: Added a new update system")
        self.inline_input = discord.ui.TextInput(label="Inline (true/false)", required=False, default="false", placeholder="Leave blank or type false")
        self.add_item(self.name_input)
        self.add_item(self.value_input)
        self.add_item(self.inline_input)

    async def on_submit(self, interaction: discord.Interaction):
        name = self.name_input.value.strip() or "Update Details"
        value = self.value_input.value.strip() or " "
        inline = self.inline_input.value.strip().lower() in {"true", "1", "yes", "y"}
        self.parent_view.fields.append({"name": name, "value": value, "inline": inline})
        self.parent_view.field_name = name
        self.parent_view.field_value = value
        await self.parent_view.refresh_message(interaction)


class AddItemToUpdateFieldModal(discord.ui.Modal):
    def __init__(self, parent_view):
        self.parent_view = parent_view
        super().__init__(title="Add Item to Field")
        self.field_input = discord.ui.TextInput(
            label="Field Name",
            required=False,
            default=parent_view.field_name or "MM2 Items",
            placeholder="Example: MM2 Items",
        )
        self.item_input = discord.ui.TextInput(
            label="Item Name",
            required=True,
            placeholder="Example: Sparkle Sword",
        )
        self.add_item(self.field_input)
        self.add_item(self.item_input)

    async def on_submit(self, interaction: discord.Interaction):
        field_name = self.field_input.value.strip() or self.parent_view.field_name or "MM2 Items"
        raw_items = self.item_input.value.strip()
        if not raw_items:
            await interaction.response.send_message("Please enter an item name first.", ephemeral=True)
            return

        parsed_items = []
        item_database = load_items()
        for raw_item in raw_items.split(","):
            item_name = raw_item.strip()
            if not item_name:
                continue
            normalized_name = item_name.lower()
            matched_name = next((name for name in item_database if name.lower() == normalized_name), None)
            item_display_name = matched_name or item_name
            item_emoji = get_item_emoji(item_display_name) or "📦"
            item_value = get_item_value(item_display_name)
            formatted_item = f"{item_emoji} `{item_display_name}`"
            if item_value is not None:
                formatted_item += f" ({VALUE_EMOJI} {format_value_with_commas(item_value)})"
            parsed_items.append(formatted_item)

        target_field = next((field for field in self.parent_view.fields if field.get("name") == field_name), None)
        if target_field is None:
            self.parent_view.fields.append({"name": field_name, "value": "", "inline": False})
            target_field = self.parent_view.fields[-1]

        existing_value = target_field.get("value", "") or ""
        if existing_value and not existing_value.endswith("\n"):
            existing_value += "\n"
        if parsed_items:
            existing_value += "\n".join(parsed_items)
        target_field["value"] = existing_value.strip()
        self.parent_view.field_name = field_name
        self.parent_view.field_value = target_field["value"]
        await self.parent_view.refresh_message(interaction)


class EditUpdateFieldsModal(discord.ui.Modal):
    def __init__(self, parent_view, current_fields: list):
        self.parent_view = parent_view
        super().__init__(title="Bloxloot Field Editor")
        current_value = "\n".join(
            f"{field.get('name', 'Update Details')} | {field.get('value', ' ')} | {'true' if field.get('inline', False) else 'false'}"
            for field in current_fields
        )
        self.fields_input = discord.ui.TextInput(
            label="Fields",
            required=False,
            default=current_value,
            style=discord.TextStyle.paragraph,
            placeholder="One field per line: Name | Value | true/false",
        )
        self.add_item(self.fields_input)

    async def on_submit(self, interaction: discord.Interaction):
        raw_text = self.fields_input.value.strip()
        parsed_fields = []
        if raw_text:
            for line in raw_text.splitlines():
                line = line.strip()
                if not line:
                    continue
                parts = [part.strip() for part in line.split("|")]
                if len(parts) >= 2:
                    name = parts[0] or "Update Details"
                    value = parts[1] or " "
                    inline = len(parts) > 2 and parts[2].lower() in {"true", "1", "yes", "y"}
                    parsed_fields.append({"name": name, "value": value, "inline": inline})

        if parsed_fields:
            self.parent_view.fields = parsed_fields
            self.parent_view.field_name = parsed_fields[0]["name"]
            self.parent_view.field_value = parsed_fields[0]["value"]
        else:
            self.parent_view.fields = self.parent_view.get_default_fields()
            self.parent_view.field_name = ""
            self.parent_view.field_value = ""
        await self.parent_view.refresh_message(interaction)


class EditUpdateBannerModal(discord.ui.Modal):
    def __init__(self, parent_view, current_value: str = ""):
        self.parent_view = parent_view
        super().__init__(title="Edit Banner Image")
        self.image_input = discord.ui.TextInput(
            label="Image URL",
            required=False,
            default=current_value,
            placeholder="Paste a direct image URL here",
        )
        self.add_item(self.image_input)

    async def on_submit(self, interaction: discord.Interaction):
        self.parent_view.image_url = self.image_input.value.strip()
        await self.parent_view.refresh_message(interaction)


class CreateUpdateEditorView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.title = "Bloxloot Update V1.0"
        self.description = "Hello Looters! We hope you enjoy this update, more coming soon!"
        self.field_name = ""
        self.field_value = ""
        self.fields = self.get_default_fields()
        self.image_url = ""
        self.footer = "Powered by Bloxloot   •   The innovative In-Game bot with the best rewards!"
        self.message = None

    def get_default_fields(self) -> list:
        return [
            {"name": "Update Details", "value": "Add your update details here", "inline": False},
            {"name": "MM2 Items", "value": "", "inline": True},
            {"name": "ADM Items", "value": "", "inline": True},
        ]

    def build_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title=self.title,
            description=self.description or " ",
            color=discord.Color.green(),
        )
        if self.image_url:
            embed.set_image(url=self.image_url)
        fields_to_render = self.fields if self.fields else self.get_default_fields()
        for field in fields_to_render:
            embed.add_field(
                name=field.get("name", "Update Details"),
                value=field.get("value") or " ",
                inline=field.get("inline", False),
            )
        embed.set_footer(text=self.footer)
        return embed

    async def refresh_message(self, interaction: discord.Interaction):
        embed = self.build_embed()
        if self.message is not None:
            await self.message.edit(embed=embed, view=self)
            await interaction.response.defer()
            return

        await interaction.response.send_message(embed=embed, view=self, ephemeral=True)

    @discord.ui.button(label="Edit Title", style=discord.ButtonStyle.secondary, row=0)
    async def edit_title_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EditUpdateTextModal(self, "title", self.title))

    @discord.ui.button(label="Edit Description", style=discord.ButtonStyle.secondary, row=0)
    async def edit_description_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EditUpdateTextModal(self, "description", self.description))

    @discord.ui.button(label="Upload Banner", style=discord.ButtonStyle.secondary, row=0)
    async def edit_banner_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EditUpdateBannerModal(self, self.image_url))

    @discord.ui.button(label="Add Field", style=discord.ButtonStyle.secondary, row=1)
    async def add_field_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(AddUpdateFieldModal(self))

    @discord.ui.button(label="Items to Field", style=discord.ButtonStyle.secondary, row=1)
    async def add_items_to_field_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(AddItemToUpdateFieldModal(self))

    @discord.ui.button(label="Manage Fields", style=discord.ButtonStyle.secondary, row=1)
    async def edit_fields_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EditUpdateFieldsModal(self, self.fields))

    @discord.ui.button(label="Reset Defaults", style=discord.ButtonStyle.secondary, row=1)
    async def reset_fields_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.fields = self.get_default_fields()
        self.field_name = self.fields[0]["name"]
        self.field_value = self.fields[0]["value"]
        await self.refresh_message(interaction)

    @discord.ui.button(label="Release Update", style=discord.ButtonStyle.secondary, row=2)
    async def release_update_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = getattr(interaction, "guild", None)
        channel = None
        if guild is not None:
            channel = guild.get_channel(UPDATE_LOG_CHANNEL_ID)
        bot_instance = globals().get("bot")
        if channel is None and bot_instance is not None:
            channel = bot_instance.get_channel(UPDATE_LOG_CHANNEL_ID)

        if channel is None:
            await interaction.response.send_message("The update log channel could not be found.", ephemeral=True)
            return

        embed = self.build_embed()
        message = await channel.send(embed=embed)
        update_code = get_next_update_code()
        update_record = {
            "code": update_code,
            "title": self.title,
            "description": self.description,
            "fields": self.fields if self.fields else self.get_default_fields(),
            "image_url": self.image_url,
            "footer": self.footer,
            "message_id": message.id,
            "channel_id": channel.id,
            "message_link": message.jump_url,
            "created_at": datetime.now().isoformat(),
            "created_by": str(interaction.user.id),
        }
        updates = load_updates()
        updates.append(update_record)
        save_updates(updates)

        await interaction.response.send_message(
            f"Released {update_code} to {channel.mention}.",
            ephemeral=True,
        )

    @discord.ui.button(label="Edit Footer", style=discord.ButtonStyle.secondary, row=2)
    async def edit_footer_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EditUpdateTextModal(self, "footer", self.footer))


async def build_update_panel_embed(interaction: discord.Interaction):
    guild = getattr(interaction, "guild", None)
    guild_id = getattr(guild, "id", None)
    update_channel_id = UPDATE_LOG_CHANNEL_ID

    embed = discord.Embed(
        title="Bloxloot Update Panel",
        description="Use the dropdown below to build and release a new update.",
        color=discord.Color.green()
    )

    update_value = "No updates found yet."
    update_log_link = "Not configured yet."

    if update_channel_id:
        channel = None
        if guild is not None:
            channel = guild.get_channel(update_channel_id)
        bot_instance = globals().get("bot")
        if channel is None and bot_instance is not None:
            channel = bot_instance.get_channel(update_channel_id)

        if channel is not None:
            update_log_link = f"https://discord.com/channels/{guild_id or '@me'}/{channel.id}" if guild_id else f"<#{channel.id}>"

            updates = load_updates()
            if updates:
                latest_update = updates[-1]
                message_link = latest_update.get("message_link") or ""
                code = latest_update.get("code") or ""
                if code and message_link:
                    update_value = f"{code}: {message_link}"
                elif code:
                    update_value = code
                elif message_link:
                    update_value = message_link
            else:
                update_value = "No updates found yet."
        else:
            update_log_link = f"https://discord.com/channels/{guild_id or '@me'}/{update_channel_id}" if guild_id else f"Channel ID: {update_channel_id}"

    embed.add_field(name="Bloxloot Updates", value=update_value, inline=True)

    developer_profiles = ensure_developer_profiles()
    developer_text = ""
    if developer_profiles:
        for user_id_str, profile in developer_profiles.items():
            emoji = profile.get("emoji", "")
            uses = profile.get("uses", 0)
            limit = profile.get("limit", 20)
            developer_text += f"{emoji} <@{user_id_str}> - **{uses}/{limit}**\n"
    embed.add_field(name="Bloxloot Developer", value=developer_text or "No developer profiles configured", inline=True)

    embed.add_field(name="Bloxloot Update Logs", value=update_log_link, inline=False)
    embed.set_footer(text=f"Bloxloot Team members Only!  •  Last Updated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return embed, UpdatePanelView()


class AdminPanelView(discord.ui.View):
    pass


class EventPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    def _can_use(self, interaction: discord.Interaction) -> Tuple[bool, str]:
        if interaction.user.id in ADMIN_USER_IDS:
            return True, ""
        event_hosts = ensure_event_host_profiles()
        if str(interaction.user.id) not in event_hosts:
            return False, "You don't have permission to use this panel!"
        allowed, uses, limit = increment_event_host_use(interaction.user.id)
        if not allowed:
            return False, f"You have reached your daily event panel interactions ({uses}/{limit})."
        return True, ""

    @discord.ui.button(label="RACE", style=discord.ButtonStyle.secondary, row=0, custom_id="event_panel_race")
    async def race_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        allowed, reason = self._can_use(interaction)
        if not allowed:
            await interaction.response.send_message(reason, ephemeral=True)
            return

        embed, view = build_race_panel_embed()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        try:
            view.message = await interaction.original_message()
        except Exception:
            try:
                view.message = await interaction.original_response()
            except Exception:
                view.message = None

        if view.message is not None:
            ACTIVE_RACE_PANEL_VIEWS.append(view)

    @discord.ui.button(label="MINIGAME", style=discord.ButtonStyle.secondary, row=0, custom_id="event_panel_minigame")
    async def minigame_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        allowed, reason = self._can_use(interaction)
        if not allowed:
            await interaction.response.send_message(reason, ephemeral=True)
            return

        embed, view = build_minigame_panel_embed()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @discord.ui.button(label="STOCK", style=discord.ButtonStyle.secondary, row=0, custom_id="event_panel_stock")
    async def stock_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in ADMIN_USER_IDS:
            await interaction.response.send_message("You don't have permission to use the stock panel.", ephemeral=True)
            return

        embed, view = build_stock_embed()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        try:
            view.message = await interaction.original_message()
        except Exception:
            try:
                view.message = await interaction.original_response()
            except Exception:
                view.message = None


class StockActionView(discord.ui.View):
    def __init__(self, mode: str = GameType.MM2):
        super().__init__(timeout=None)
        self.mode = mode
        self.message = None
        self.toggle_button.label = "ADM" if self.mode == GameType.MM2 else "MM2"

    def _can_use(self, interaction: discord.Interaction) -> Tuple[bool, str]:
        if interaction.user.id in ADMIN_USER_IDS:
            return True, ""
        return False, "You don't have permission to manage stock."

    @discord.ui.button(label="ADD", style=discord.ButtonStyle.secondary, row=0, custom_id="stock_add_button")
    async def add_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        allowed, reason = self._can_use(interaction)
        if not allowed:
            await interaction.response.send_message(reason, ephemeral=True)
            return
        modal = AddStockItemModal()
        modal.parent_view = self
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="REMOVE", style=discord.ButtonStyle.secondary, row=0, custom_id="stock_remove_button")
    async def remove_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        allowed, reason = self._can_use(interaction)
        if not allowed:
            await interaction.response.send_message(reason, ephemeral=True)
            return
        modal = RemoveStockItemModal()
        modal.parent_view = self
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="ADM", style=discord.ButtonStyle.secondary, row=0, custom_id="stock_toggle_filter")
    async def toggle_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        allowed, reason = self._can_use(interaction)
        if not allowed:
            await interaction.response.send_message(reason, ephemeral=True)
            return

        self.mode = GameType.ADM if self.mode == GameType.MM2 else GameType.MM2
        self.toggle_button.label = "MM2" if self.mode == GameType.ADM else "ADM"
        updated_embed = build_stock_embed_embed(self.mode)
        await interaction.response.edit_message(embed=updated_embed, view=self)


def _parse_emoji(e: str):
    if not e:
        return None
    try:
        return discord.PartialEmoji.from_str(e)
    except Exception:
        return None


class AdminPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

                                                                           
        options: List[discord.SelectOption] = []
        for idx, s in enumerate(MM2_DEPOSIT_SERVERS):
            emoji_obj = _parse_emoji(s.get('emoji', ''))
            label = s.get('roblox_username', s.get('name', 'Unknown'))[:100]
            options.append(discord.SelectOption(label=label, description="MM2", value=f"MM2::{idx}", emoji=emoji_obj))
        for idx, s in enumerate(ADM_DEPOSIT_SERVERS):
            emoji_obj = _parse_emoji(s.get('emoji', ''))
            label = s.get('roblox_username', s.get('name', 'Unknown'))[:100]
            options.append(discord.SelectOption(label=label, description="ADM", value=f"ADM::{idx}", emoji=emoji_obj))

                                                                                                
        self.selected_server = None

        select_button = discord.ui.Button(label="CONFIGURE", style=discord.ButtonStyle.secondary, custom_id="admin_selected_server_btn", row=0)

        async def _select_button_callback(interaction: discord.Interaction):
                                                               
                                                                                     
            outer_panel = self

            class _EphemeralSelect(discord.ui.Select):
                def __init__(self, opts: List[discord.SelectOption]):
                    super().__init__(placeholder="Launch a bot...", min_values=1, max_values=1, options=opts)

                async def callback(self, inter: discord.Interaction):
                    val = self.values[0]
                    try:
                        typ, idx = val.split("::", 1)
                        idx = int(idx)
                    except Exception:
                        await inter.response.send_message(f"Selected: {val}", ephemeral=True)
                        return

                    server = MM2_DEPOSIT_SERVERS[idx] if typ == "MM2" and 0 <= idx < len(MM2_DEPOSIT_SERVERS) else (
                        ADM_DEPOSIT_SERVERS[idx] if typ == "ADM" and 0 <= idx < len(ADM_DEPOSIT_SERVERS) else None
                    )
                                                                                               
                    try:
                        outer_panel.selected_server = server
                        if server:
                            select_button.label = server.get('roblox_username', server.get('name', 'Unknown'))
                    except Exception:
                        pass
                    self.view.stop()
                                           
                    await inter.response.send_message(f"Selected {server.get('roblox_username', server.get('name','Unknown'))} ({typ})", ephemeral=True)
                                                                                        
                    try:
                        cookie = server.get('cookie', '') if server else ''
                        username = server.get('roblox_username') or server.get('name') if server else 'Unknown'
                        async def _ephemeral_launch():
                            success = await asyncio.to_thread(_sync_launch_roblox_with_cookie, cookie)
                            if server is not None:
                                server["launched"] = bool(success)
                            try:
                                await inter.followup.send(f"Launch {'succeeded' if success else 'failed'} for {username}.", ephemeral=True)
                                try:
                                    asyncio.create_task(asyncio.to_thread(_arrange_and_minimize_roblox_windows))
                                except Exception:
                                    pass
                                if success:
                                    try:
                                        await update_admin_panel_embed()
                                    except Exception:
                                        pass
                            except Exception:
                                pass
                        asyncio.create_task(_ephemeral_launch())
                    except Exception:
                        pass

            v = discord.ui.View(timeout=60)
            v.add_item(_EphemeralSelect(options))
            
                                                  
            mm2_count = len(MM2_DEPOSIT_SERVERS)
            adm_count = len(ADM_DEPOSIT_SERVERS)
            
            staff_profiles = ensure_staff_profiles()
            user_uses = staff_profiles.get(str(interaction.user.id), {}).get('uses', 0)
            user_limit = staff_profiles.get(str(interaction.user.id), {}).get('limit', 10)
            remaining = max(0, user_limit - user_uses)
            
                                                                    
            mm2_bots_info = []
            def format_bot_value(value: float) -> str:
                return f"{value:,.2f}" if isinstance(value, float) else f"{format_value_with_commas(value)}"

            for s in MM2_DEPOSIT_SERVERS:
                emoji = s.get('emoji', '')
                username = s.get('roblox_username', s.get('name', 'Unknown'))
                value_total = get_bot_holding_value(username, GameType.MM2)
                mm2_bots_info.append(f"{emoji} **{username}** - {VALUE_EMOJI} **{format_bot_value(value_total)}**")

            adm_bots_info = []
            for s in ADM_DEPOSIT_SERVERS:
                emoji = s.get('emoji', '')
                username = s.get('roblox_username', s.get('name', 'Unknown'))
                value_total = get_bot_holding_value(username, GameType.ADM)
                adm_bots_info.append(f"{emoji} **{username}** - {VALUE_EMOJI} **{format_bot_value(value_total)}**")

            mm2_bots_text = "\n".join(mm2_bots_info) if mm2_bots_info else "No MM2 bots available"
            adm_bots_text = "\n".join(adm_bots_info) if adm_bots_info else "No ADM bots available"

            embed = discord.Embed(
                title="Bloxloot Bot Panel",
                description=f"Choose a bot to launch from the dropdown below.",
                color=discord.Color.green()
            )

            embed.add_field(
                name=f"MM2 Bots ({len(MM2_DEPOSIT_SERVERS)})",
                value=mm2_bots_text,
                inline=False
            )

            embed.add_field(
                name=f"ADM Bots ({len(ADM_DEPOSIT_SERVERS)})",
                value=adm_bots_text,
                inline=False
            )
            
            embed.add_field(
                name="How To Use",
                value="**1.** Select a bot from the dropdown\n**2.** Bot will launch automatically (VPS)\n**3.** If bot fails to launch, Contact <@&1507265955753885706>",
                inline=False
            )
            
            embed.set_footer(text=f"Bloxloot Team Members Only • Selection expires in 60 seconds")
            
            await interaction.response.send_message(embed=embed, view=v, ephemeral=True)

        select_button.callback = _select_button_callback
        self.add_item(select_button)

                                                                     
        add_btn = discord.ui.Button(label="ADD", style=discord.ButtonStyle.secondary, custom_id="admin_add_button", row=0)
        remove_btn = discord.ui.Button(label="REMOVE", style=discord.ButtonStyle.secondary, custom_id="admin_remove_button", row=0)
        update_btn = discord.ui.Button(label="UPDATE", style=discord.ButtonStyle.secondary, custom_id="admin_update_button", row=0)

        async def _add_callback(interaction: discord.Interaction):
            await interaction.response.send_modal(AddItemModal())

        async def _remove_callback(interaction: discord.Interaction):
            await interaction.response.send_modal(RemoveUserModal())

        async def _update_callback(interaction: discord.Interaction):
            staff_profiles = ensure_staff_profiles()
            developer_profiles = ensure_developer_profiles()
            has_access = interaction.user.id in ADMIN_USER_IDS or str(interaction.user.id) in staff_profiles or str(interaction.user.id) in developer_profiles
            if not has_access:
                await interaction.response.send_message("You don't have permission to use this panel!", ephemeral=True)
                return

            embed, view = await build_update_panel_embed(interaction)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

        add_btn.callback = _add_callback
        remove_btn.callback = _remove_callback
        update_btn.callback = _update_callback

        self.add_item(add_btn)
        self.add_item(remove_btn)
        self.add_item(update_btn)

class AdminServerSelect(discord.ui.Select):
    def __init__(self, options: List[discord.SelectOption]):
        super().__init__(custom_id="admin_server_select", placeholder="Select a bot..", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
                                                                           
        parent = self.view
        if not parent:
            await interaction.response.send_message("Selection failed: view not found.", ephemeral=True)
            return
        val = self.values[0]
                                   
        try:
            typ, idx = val.split("::", 1)
            idx = int(idx)
        except Exception:
            await interaction.response.send_message(f"Selected: {val}", ephemeral=True)
            parent.selected_server = val
            return

        if typ == "MM2":
            server = MM2_DEPOSIT_SERVERS[idx] if 0 <= idx < len(MM2_DEPOSIT_SERVERS) else None
        else:
            server = ADM_DEPOSIT_SERVERS[idx] if 0 <= idx < len(ADM_DEPOSIT_SERVERS) else None

                                                
        allowed, uses, limit = increment_staff_use(interaction.user.id)
        if not allowed:
            await interaction.response.send_message(f"Staff action limit reached ({uses}/{limit}) — try again later.", ephemeral=True)
            return

        parent.selected_server = server
        label = f"{server.get('emoji','')} {server.get('roblox_username', server.get('name','Unknown'))}" if server else str(val)
        game_type = typ
        await interaction.response.send_message(f"Selected {label} ({game_type}) — launching...", ephemeral=True)

        async def _run_launch_and_report():
            cookie = server.get('cookie', '') if server else ''
            username = server.get('roblox_username') or server.get('name') if server else 'Unknown'
            success = await asyncio.to_thread(_sync_launch_roblox_with_cookie, cookie)
            if server is not None:
                server['launched'] = bool(success)
            try:
                await interaction.followup.send(f"Launch {'succeeded' if success else 'failed'} for {username}.", ephemeral=True)
                try:
                    asyncio.create_task(asyncio.to_thread(_arrange_and_minimize_roblox_windows))
                except Exception:
                    pass
                if success:
                    try:
                        await update_admin_panel_embed()
                    except Exception:
                        pass
            except Exception:
                pass

        asyncio.create_task(_run_launch_and_report())

async def create_admin_panel():
    """Create or update the admin panel in the configured channel"""
    await bot.wait_until_ready()
    
    channel = bot.get_channel(ADMIN_PANEL_CHANNEL_ID)
    if not channel:
        print(f"Admin panel channel {ADMIN_PANEL_CHANNEL_ID} not found!")
        return
    
                                   
    panel_data = load_admin_panel()
    panel_message_id = panel_data.get("message_id")
    
    embed = discord.Embed(
        title="Bloxloot Staff Panel",
        description="Use the buttons below to manage user inventories and Moderation.",
        color=discord.Color.green()
    )

                                        
                                                                                    
                                                    
    staff_profiles = ensure_staff_profiles()
    staff_text = ""
    if staff_profiles:
        for user_id_str, profile in staff_profiles.items():
            if user_id_str in TAX_PROFILES:
                continue
            emoji = profile.get("emoji", "")
            uses = profile.get("uses", 0)
            limit = profile.get("limit", 10)
            staff_text += f"{emoji} <@{user_id_str}> - **{uses}/{limit}**\n"
                                                                 
    private_links = (
        "https://discord.com/channels/1497891147664588870/1507356202206629888",
        "https://discord.com/channels/1497891147664588870/1507356534047244328",
    )
                                                                                        
    mm2_online, mm2_total = await get_servers_status(MM2_DEPOSIT_SERVERS)
    adm_online, adm_total = await get_servers_status(ADM_DEPOSIT_SERVERS)
    private_text = (
        f"{private_links[0]} **{mm2_online}/{mm2_total}**\n"
        f"{private_links[1]} **{adm_online}/{adm_total}**"
    )

                                                           
    mm2_total_wagered = get_total_wagered(GameType.MM2)
    adm_total_wagered = get_total_wagered(GameType.ADM)

    embed.add_field(
        name="Bloxloot Overview",
        value=(
            f"**MM2 -** {VALUE_EMOJI} **{format_value_with_commas(mm2_total_wagered)}**\n"
            f"**ADM -** {VALUE_EMOJI} **{format_value_with_commas(adm_total_wagered)}**"
        ),
        inline=True
    )

    embed.add_field(
        name="Bloxloot Staff",
        value=staff_text or "No staff profiles configured",
        inline=True
    )

    embed.add_field(name="Bloxloot In-Game", value=private_text, inline=False)
    
    embed.set_footer(text=f"Bloxloot Team members only! • Last Updated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    view = AdminPanelView()
    
    if panel_message_id:
        try:
            message = await channel.fetch_message(panel_message_id)
            await message.edit(embed=embed, view=view)
            print("Staff panel updated successfully")
            return
        except:
            pass
    
                      
    message = await channel.send(embed=embed, view=view)
    save_admin_panel({"message_id": message.id})
    print("Staff panel created successfully")


def build_event_panel_embed():
    embed = discord.Embed(
        title="Bloxloot Event Panel",
        description="Use the buttons below to enable either an event or a wager race.",
        color=discord.Color.green()
    )
    event_hosts = ensure_event_host_profiles()
    event_host_text = ""
    if event_hosts:
        for user_id_str, profile in event_hosts.items():
            emoji = profile.get("emoji", "")
            uses = profile.get("uses", 0)
            limit = profile.get("limit", 3)
            event_host_text += f"{emoji} <@{user_id_str}> - **{uses}/{limit}**\n"
    embed.add_field(
        name="Bloxloot Stock",
        value=build_stock_summary(),
        inline=True
    )
    embed.add_field(
        name="Bloxloot Hosts",
        value=event_host_text or "No event hosts configured",
        inline=True
    )
    embed.add_field(
        name="Bloxloot Event Logs",
        value="https://discord.com/channels/1497891147664588870/1510157246997205072\nhttps://discord.com/channels/1497891147664588870/1509187988897398834",
        inline=False
    )

    embed.set_footer(text=f"Bloxloot Team members only! • Last Updated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return embed, EventPanelView()


def build_race_panel_embed():
    embed = discord.Embed(
        title="Bloxloot Race Panel",
        description="Use the buttons below to manage or start a wager race.",
        color=discord.Color.green()
    )

    race_winners = get_race_winners()
    if race_winners:
        winner_lines = [format_race_winner_entry(winner) for winner in race_winners[:3]]
        embed.add_field(
            name="Bloxloot Winners",
            value="\n".join(winner_lines),
            inline=False
        )
    else:
        embed.add_field(
            name="Bloxloot Winners",
            value="No recent race winners yet.",
            inline=False
        )

    active_race_channels = get_active_race_channels()
    if active_race_channels:
        race_links = "\n".join(f"<#{channel_id}>" for channel_id in active_race_channels)
        embed.add_field(
            name="Bloxloot Races",
            value=race_links,
            inline=False
        )
    else:
        embed.add_field(
            name="Bloxloot Races",
            value="No active race channels.",
            inline=False
        )

    embed.set_footer(text=f"Bloxloot Team members only! • Last Updated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return embed, RacePanelView()


def build_minigame_panel_embed():
    embed = discord.Embed(
        title="Bloxloot Minigame Panel",
        description="Use the dropdown below to start a minigame event",
        color=discord.Color.green()
    )

    race_winners = get_race_winners()
    if race_winners:
        winner_lines = [format_race_winner_entry(winner) for winner in race_winners[:3]]
        embed.add_field(
            name="Bloxloot Winners",
            value="\n".join(winner_lines),
            inline=False
        )
    else:
        embed.add_field(
            name="Bloxloot Winners",
            value="No recent winners yet.",
            inline=False
        )

    embed.set_footer(text=f"Bloxloot Team members only! • Last Updated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return embed, MinigamePanelView()


def get_race_prize_items(race_type: str, placement: int):
    race_type_key = str(race_type).lower()
    placement_prizes = RACE_PRIZE_CONFIG.get(race_type_key, {})
    prize_entry = placement_prizes.get(placement)
    if prize_entry is None:
        return []
    if isinstance(prize_entry, str):
        return [prize_entry]
    if isinstance(prize_entry, dict):
        if "item" in prize_entry:
            count = prize_entry.get("count", 1)
            return [{"item": prize_entry["item"], "count": count}]
        if "items" in prize_entry and isinstance(prize_entry["items"], dict):
            return [{"item": name, "count": count} for name, count in prize_entry["items"].items()]
        return [prize_entry]
    if isinstance(prize_entry, list):
        return prize_entry
    return [str(prize_entry)]


def format_race_prize_text(prizes):
    if prizes is None:
        return "No prize set"
    if isinstance(prizes, dict):
        return " ".join(
            f"{get_item_emoji(item_name)} x{count}"
            for item_name, count in prizes.items()
        )
    if isinstance(prizes, list):
        parts = []
        for prize in prizes:
            if isinstance(prize, dict):
                item_name = prize.get("item") or str(prize)
                count = prize.get("count", 1)
                parts.append(f"{get_item_emoji(item_name)} x{count}")
            else:
                parts.append(get_item_emoji(str(prize)) if isinstance(prize, str) else str(prize))
        return " ".join(parts) if parts else "No prize set"
    if isinstance(prizes, str):
        return get_item_emoji(prizes)
    return str(prizes)


def _get_wagered_in_window(entry: dict, game_type: str, start_time: Optional[datetime], end_time: Optional[datetime]) -> int:
    """Calculate total wagered within the given timeframe from wager_history."""
    if start_time is None and end_time is None:
        return 0
    total = 0
    history = entry.get('wager_history', []) or []
    if not isinstance(history, list):
        return 0
    
    for wager in history:
        try:
            if wager.get('game_type') != game_type:
                continue
            timestamp = wager.get('timestamp')
            if not timestamp:
                continue
            wager_time = datetime.fromisoformat(timestamp)
            if start_time and wager_time < start_time:
                continue
            if end_time and wager_time > end_time:
                continue
            # Ensure amount is a valid number
            amount = wager.get('amount', 0)
            if isinstance(amount, (int, float)):
                total += int(amount)
        except Exception:
            continue
    return total


def get_race_placements_from_registrations(race_type: str, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None, limit: int = 10) -> List[dict]:
    """Return top wagerers for a race type based on registrations total_wagered filtered by timeframe."""
    race_type_key = str(race_type).lower()
    game_type = GameType.ADM if race_type_key.startswith("adm") else GameType.MM2
    placements = []
    
    # If no timeframe provided, use default (last 24 hours for daily, etc.)
    if start_time is None and end_time is None:
        start_time, end_time = get_default_race_window(race_type)
    
    try:
        registrations = load_registrations()
        for discord_id, entry in registrations.items():
            try:
                # Use the window filter
                amount = _get_wagered_in_window(entry, game_type, start_time, end_time)
                if amount > 0:
                    placements.append({
                        "discord_id": int(discord_id),
                        "wagered": amount,
                    })
            except Exception:
                continue
        placements.sort(key=lambda entry: (-entry["wagered"], entry.get("discord_id", 0)))
    except Exception:
        placements = []
    return placements[:limit]


def build_race_leaderboard_lines(race_type: str, placements=None, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None) -> List[str]:
    if placements is None:
        placements = get_race_placements_from_registrations(race_type, start_time=start_time, end_time=end_time)

    lines = []
    for placement in range(1, 6):  # Top 5 placements
        if isinstance(placements, list) and placement <= len(placements) and isinstance(placements[placement - 1], dict):
            entry = placements[placement - 1]
            lines.append(
                format_race_channel_placement(
                    placement,
                    entry.get("discord_id", 0),
                    entry.get("wagered", 0),
                    entry.get("prizes", None),
                    race_type
                )
            )
        else:
            prize_text = format_race_prize_text(get_race_prize_items(race_type, placement))
            lines.append(f"**#{placement} - Waiting... - {prize_text}**")
    return lines


def get_default_race_window(race_type: str):
    now = datetime.now()
    race_type_key = str(race_type).lower()
    if race_type_key == "daily":
        return now, now + timedelta(days=1)
    if race_type_key == "weekly":
        return now, now + timedelta(days=7)
    if race_type_key == "monthly":
        return now, now + timedelta(days=30)
    return now, now + timedelta(hours=1)


def format_race_time_field(start_time: Optional[datetime], end_time: Optional[datetime]) -> str:
    if start_time is None and end_time is None:
        return "Start: TBD\nEnd: TBD"
    parts = []
    if start_time is not None:
        parts.append(f"<t:{int(start_time.timestamp())}:F>")
    else:
        parts.append("TBD")
    if end_time is not None:
        parts.append(f"<t:{int(end_time.timestamp())}:F>")
    else:
        parts.append("TBD")
    return "\n".join(parts)


def get_race_banner_url(race_type: str) -> Optional[str]:
    race_type_key = str(race_type).lower()
    banner_url = RACE_BANNER_CONFIG.get(race_type_key, "")
    if isinstance(banner_url, str):
        banner_url = banner_url.strip()
        return banner_url or None
    return None


def _build_fallback_race_banner(race_type: str) -> Image.Image:
    width, height = 2600, 652
    fallback_path = os.path.join(BASE_DIR, THUMBNAIL_PATH)
    if os.path.exists(fallback_path):
        try:
            with Image.open(fallback_path) as base_image:
                base_image = base_image.convert("RGBA")
                if base_image.size != (width, height):
                    base_image = base_image.resize((width, height), Image.LANCZOS)
                return base_image
        except Exception:
            pass

    banner = Image.new("RGBA", (width, height), (16, 20, 34, 255))
    draw = ImageDraw.Draw(banner)
    draw.rounded_rectangle((30, 30, width - 30, height - 30), radius=24, fill=(28, 38, 58, 255), outline=(255, 200, 96, 220), width=8)
    draw.text((80, 90), f"Bloxloot {str(race_type).capitalize()} Race", fill=(255, 255, 255, 255), font=ImageFont.load_default())
    return banner


def _build_fallback_race_avatar(size: int) -> Image.Image:
    avatar = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(avatar)
    outline = 16
    draw.ellipse((0, 0, size - 1, size - 1), fill=(255, 95, 31, 255), outline=(255, 255, 255, 255), width=outline)
    draw.ellipse((outline + 8, outline + 8, size - outline - 9, size - outline - 9), fill=(255, 180, 90, 255))
    draw.ellipse((size // 3, size // 3, size - size // 3, size - size // 3), fill=(0, 0, 0, 0))
    return avatar


async def _load_race_banner_avatar(size: int) -> Image.Image:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(RACE_BANNER_AVATAR_URL) as response:
                if response.status != 200:
                    raise RuntimeError("avatar fetch failed")
                avatar_bytes = await response.read()
    except Exception:
        return _build_fallback_race_avatar(size)

    try:
        avatar_image = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA")
        if avatar_image.size != (size, size):
            avatar_image = avatar_image.resize((size, size), Image.LANCZOS)
        return avatar_image
    except Exception:
        return _build_fallback_race_avatar(size)


async def build_race_banner_attachment(race_type: str) -> Optional[discord.File]:
    banner_url = get_race_banner_url(race_type)
    if not banner_url:
        return None

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(banner_url) as response:
                if response.status != 200:
                    raise RuntimeError("banner fetch failed")
                image_bytes = await response.read()
        with Image.open(io.BytesIO(image_bytes)).convert("RGBA") as banner_image:
            banner_image = banner_image.copy()
    except Exception:
        banner_image = _build_fallback_race_banner(race_type)

    try:
        avatar_image = await _load_race_banner_avatar(RACE_BANNER_PLACEHOLDER_SIZE)
        for placement, (x, y) in RACE_BANNER_PLACEHOLDER_COORDS.items():
            paste_x = x
            paste_y = y
            if paste_x + avatar_image.width <= banner_image.width and paste_y + avatar_image.height <= banner_image.height:
                banner_image.paste(avatar_image, (paste_x, paste_y), avatar_image)

        output = io.BytesIO()
        banner_image.save(output, format="PNG")
        output.seek(0)
        return discord.File(output, filename="race_banner.png")
    except Exception:
        return None


def format_race_channel_placement(position: int, discord_id: int, wagered, prizes, race_type: str) -> str:
    registrations = load_registrations()
    user_data = registrations.get(str(discord_id), {})
    emoji = get_registration_avatar_emoji(discord_id)
    name_display = user_data.get("roblox_username") or user_data.get("roblox_display_name") or f"<@{discord_id}>"
    mention = f"<@{discord_id}>"
    display_prefix = f"{emoji} " if emoji else ""
    wager_text = f"{VALUE_EMOJI} **{format_value_with_commas(wagered)}**" if isinstance(wagered, (int, float)) else str(wagered)
    prize_items = prizes
    if not prize_items:
        prize_items = get_race_prize_items(race_type, position)
    prize_text = format_race_prize_text(prize_items)
    return f"**#{position} - {display_prefix}{mention} ({name_display}) - {wager_text} - {prize_text}**"


async def build_race_channel_embed(race_type: str, placements=None, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None):
    title = f"Bloxloot {race_type.capitalize()} Race"
    embed = discord.Embed(
        title=title,
        description="Bloxloot Race leaderboard. The top 10 placements appear below.",
        color=discord.Color.green()
    )
    if start_time is None and end_time is None:
        start_time, end_time = get_default_race_window(race_type)

    banner_file = await build_race_banner_attachment(race_type)
    if banner_file:
        embed.set_image(url="attachment://race_banner.png")

    mm2_lines = build_race_leaderboard_lines(race_type, placements, start_time=start_time, end_time=end_time)
    adm_lines = build_race_leaderboard_lines(f"adm_{race_type}", None, start_time=start_time, end_time=end_time)

    embed.add_field(
        name="MM2 Leaderboard",
        value="\n".join(mm2_lines),
        inline=True
    )
    embed.add_field(
        name="ADM Leaderboard",
        value="\n".join(adm_lines),
        inline=True
    )
    embed.add_field(
        name="Race Timeframe",
        value=format_race_time_field(start_time, end_time),
        inline=False
    )
    embed.set_footer(text=f"All winning accounts will be reviewed.  •  Last Updated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return embed, banner_file


class RacePanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.message = None

    def _can_use(self, interaction: discord.Interaction) -> Tuple[bool, str]:
        if interaction.user.id in ADMIN_USER_IDS:
            return True, ""
        event_hosts = ensure_event_host_profiles()
        if str(interaction.user.id) not in event_hosts:
            return False, "You don't have permission to use this panel!"
        allowed, uses, limit = increment_event_host_use(interaction.user.id)
        if not allowed:
            return False, f"You have reached your daily event panel interactions ({uses}/{limit})."
        return True, ""

    async def _create_race_channel(self, interaction: discord.Interaction, channel_name: str, race_type: str):
        """Create a new race channel with the specified name and type."""
        allowed, reason = self._can_use(interaction)
        if not allowed:
            await interaction.response.send_message(reason, ephemeral=True)
            return

        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
            return

        existing_channel = discord.utils.get(guild.text_channels, name=channel_name)
        if existing_channel:
            await interaction.response.send_message(f"Channel {existing_channel.mention} already exists.", ephemeral=True)
            return

        try:
            category = guild.get_channel(RACE_CHANNEL_CATEGORY_ID)
            channel = await guild.create_text_channel(
                name=channel_name,
                topic=f"{race_type} Bloxloot race channel created via the event panel.",
                category=category if isinstance(category, discord.CategoryChannel) else None
            )
            add_active_race_channel(channel.id)
            start_time, end_time = get_default_race_window(race_type)
            set_race_channel_window(channel.id, race_type, start_time, end_time)
            embed, _ = build_race_panel_embed()
            await interaction.response.edit_message(embed=embed, view=self)
            
            # Create and send the race embed
            race_embed, race_banner_file = await build_race_channel_embed(race_type, start_time=start_time, end_time=end_time)
            message = await channel.send(embed=race_embed, file=race_banner_file) if race_banner_file else await channel.send(embed=race_embed)
            
            # Store the correct message ID
            set_race_channel_message_id(channel.id, message.id)
            
            await interaction.followup.send(
                f"Created race channel {channel.mention}.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"Failed to create race channel: {e}",
                ephemeral=True
            )

    @discord.ui.button(label="DAILY", style=discord.ButtonStyle.secondary, row=0, custom_id="race_panel_daily")
    async def daily_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._create_race_channel(interaction, "🏁・1000-daily", "daily")

    @discord.ui.button(label="WEEKLY", style=discord.ButtonStyle.secondary, row=0, custom_id="race_panel_weekly")
    async def weekly_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._create_race_channel(interaction, "🏁・2500-weekly", "weekly")

    @discord.ui.button(label="MONTHLY", style=discord.ButtonStyle.secondary, row=0, custom_id="race_panel_monthly")
    async def monthly_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._create_race_channel(interaction, "🏁・5000-monthly", "monthly")


class GuessTheCryptoModal(discord.ui.Modal, title="Guess The Crypto"):
    symbol = discord.ui.TextInput(label="Crypto Symbol", placeholder="e.g., BTC, ETH, DOGE")
    usd_prize = discord.ui.TextInput(label="USD Prize Amount", placeholder="e.g., 100")

    async def on_submit(self, interaction: discord.Interaction):
        if GUESS_CRYPTO_CHANNEL_ID is None:
            await interaction.response.send_message("Guess The Crypto channel not configured!", ephemeral=True)
            return

        crypto_symbol = self.symbol.value.upper().strip()
        
        if crypto_symbol not in CRYPTO_SYMBOLS_CONFIG:
            await interaction.response.send_message(
                f"Invalid crypto symbol. Available symbols: {', '.join(CRYPTO_SYMBOLS_CONFIG.keys())}",
                ephemeral=True
            )
            return
        
        try:
            usd_amount = float(self.usd_prize.value.strip())
            if usd_amount <= 0:
                await interaction.response.send_message("USD prize must be greater than 0!", ephemeral=True)
                return
        except ValueError:
            await interaction.response.send_message("Invalid USD amount!", ephemeral=True)
            return
        
        correct_emoji = CRYPTO_SYMBOLS_CONFIG[crypto_symbol]["emoji"]
        crypto_emojis = [config["emoji"] for config in CRYPTO_SYMBOLS_CONFIG.values()]
        available_emojis = [emoji for emoji in crypto_emojis if emoji != correct_emoji]
        
        if len(available_emojis) >= 3:
            wrong_options = random.sample(available_emojis, 3)
        else:
            wrong_options = available_emojis.copy()
        
        options = wrong_options.copy()
        options.append(correct_emoji)
        random.shuffle(options)
        
        channel = bot.get_channel(GUESS_CRYPTO_CHANNEL_ID)
        
        ACTIVE_CRYPTO_GAMES[GUESS_CRYPTO_CHANNEL_ID] = {
            "correct_emoji": correct_emoji,
            "correct_symbol": crypto_symbol,
            "usd_prize": usd_amount,
            "host": interaction.user,
        }
        
        thumbnail_url = CRYPTO_SYMBOLS_CONFIG[crypto_symbol].get("image", "")
        
        embed = discord.Embed(
            title="Guess The Crypto",
            description=(
                f"**What crypto is {crypto_symbol}?**\n\n"
                f"**Prize:** ${usd_amount}\n"
                f"**Hosted by:** {interaction.user.mention}\n\n"
            ),
            color=discord.Color.green()
        )
        
        if thumbnail_url:
            embed.set_thumbnail(url=thumbnail_url)
        embed.set_footer(text="First correct guess wins - Click the right crypto button!")
        
        view = CryptoGameView(options, correct_emoji, crypto_symbol, usd_amount, interaction.user)
        
        await interaction.response.send_message("Crypto game started!", ephemeral=True)
        await channel.send(embed=embed, view=view)


class CryptoGameView(discord.ui.View):
    def __init__(self, options, correct_emoji, correct_symbol, usd_prize, host):
        super().__init__(timeout=None)
        self.correct_emoji = correct_emoji
        self.correct_symbol = correct_symbol
        self.usd_prize = usd_prize
        self.host = host
        self.game_active = True
        
        for emoji in options:
            if emoji.startswith("<:") and emoji.endswith(">"):
                parts = emoji.split(":")
                emoji_id = int(parts[2].replace(">", ""))
                emoji_name = parts[1]
                
                custom_emoji = discord.PartialEmoji(name=emoji_name, id=emoji_id)
                
                button = discord.ui.Button(
                    label=" ",
                    emoji=custom_emoji,
                    style=discord.ButtonStyle.secondary,
                    custom_id=f"crypto_{emoji}"
                )
            else:
                button = discord.ui.Button(
                    label=emoji,
                    style=discord.ButtonStyle.secondary,
                    custom_id=f"crypto_{emoji}"
                )
            
            button.callback = self.create_callback(emoji)
            self.add_item(button)
    
    def create_callback(self, emoji):
        async def callback(interaction: discord.Interaction):
            if not self.game_active:
                await interaction.response.send_message("This game has already ended!", ephemeral=True)
                return
            
            if emoji == self.correct_emoji:
                                               
                registrations = load_registrations()
                winner_id_str = str(interaction.user.id)
                
                if winner_id_str not in registrations:
                    winner_embed = discord.Embed(
                        title="WINNER!",
                        description=f"{interaction.user.mention} guessed correctly!\n\n**Crypto:** {self.correct_symbol}\n**Prize:** ${self.usd_prize}\n\n⚠️ You must be registered to claim your prize!",
                        color=discord.Color.gold()
                    )
                    await interaction.response.send_message(embed=winner_embed)
                else:
                                                      
                    add_user_balance(winner_id_str, self.usd_prize)
                    
                    winner_embed = discord.Embed(
                        title="WINNER!",
                        description=f"{interaction.user.mention} guessed correctly!\n\n**Crypto:** {self.correct_symbol}\n**Prize:** ${self.usd_prize}\n\nPrize credited to your balance!",
                        color=discord.Color.green()
                    )
                    await interaction.response.send_message(embed=winner_embed)
                
                self.game_active = False
                for item in self.children:
                    item.disabled = True
                await interaction.message.edit(view=self)
                
                if GUESS_CRYPTO_CHANNEL_ID and GUESS_CRYPTO_CHANNEL_ID in ACTIVE_CRYPTO_GAMES:
                    del ACTIVE_CRYPTO_GAMES[GUESS_CRYPTO_CHANNEL_ID]
            else:
                await interaction.response.send_message(f"Wrong guess! That's not {self.correct_symbol}. Try again!", ephemeral=True)
        
        return callback


class GuessTheSetModal(discord.ui.Modal, title="Guess The Set"):
    set_name = discord.ui.TextInput(label="Set Name", placeholder="e.g., Flowerwood Set, Bringer Set")

    async def on_submit(self, interaction: discord.Interaction):
        if GUESS_SET_CHANNEL_ID is None:
            await interaction.response.send_message("Guess The Set channel not configured!", ephemeral=True)
            return

        set_name = self.set_name.value.strip()
        
        if set_name not in SET_NAMES_CONFIG:
            await interaction.response.send_message(
                f"Invalid set name. Available sets: {', '.join(SET_NAMES_CONFIG.keys())}",
                ephemeral=True
            )
            return
        
        correct_emoji = SET_NAMES_CONFIG[set_name]["emoji"]
        set_emojis = [config["emoji"] for config in SET_NAMES_CONFIG.values()]
        available_emojis = [emoji for emoji in set_emojis if emoji != correct_emoji]
        
        if len(available_emojis) >= 3:
            wrong_options = random.sample(available_emojis, 3)
        else:
            wrong_options = available_emojis.copy()
        
        options = wrong_options.copy()
        options.append(correct_emoji)
        random.shuffle(options)
        
        channel = bot.get_channel(GUESS_SET_CHANNEL_ID)
        
        ACTIVE_SET_GAMES[GUESS_SET_CHANNEL_ID] = {
            "correct_emoji": correct_emoji,
            "correct_set": set_name,
            "host": interaction.user,
        }
        
        thumbnail_url = SET_NAMES_CONFIG[set_name].get("image", "")
        
        embed = discord.Embed(
            title="Guess The Set",
            description=(
                f"**What set is this?**\n\n"
                f"**Prize:** {set_name}\n"
                f"**Hosted by:** {interaction.user.mention}\n\n"
            ),
            color=discord.Color.green()
        )
        
        if thumbnail_url:
            embed.set_thumbnail(url=thumbnail_url)
        embed.set_footer(text="First correct guess wins - Click the right set button!")
        
        view = SetGameView(options, correct_emoji, set_name, interaction.user)
        
        await interaction.response.send_message("Set game started!", ephemeral=True)
        await channel.send(embed=embed, view=view)


class SetGameView(discord.ui.View):
    def __init__(self, options, correct_emoji, correct_set, host):
        super().__init__(timeout=None)
        self.correct_emoji = correct_emoji
        self.correct_set = correct_set
        self.host = host
        self.game_active = True
        
        for emoji in options:
            if emoji.startswith("<:") and emoji.endswith(">"):
                parts = emoji.split(":")
                emoji_id = int(parts[2].replace(">", ""))
                emoji_name = parts[1]
                
                custom_emoji = discord.PartialEmoji(name=emoji_name, id=emoji_id)
                
                button = discord.ui.Button(
                    label=" ",
                    emoji=custom_emoji,
                    style=discord.ButtonStyle.secondary,
                    custom_id=f"set_{emoji}"
                )
            else:
                button = discord.ui.Button(
                    label=emoji,
                    style=discord.ButtonStyle.secondary,
                    custom_id=f"set_{emoji}"
                )
            
            button.callback = self.create_callback(emoji)
            self.add_item(button)
    
    def create_callback(self, emoji):
        async def callback(interaction: discord.Interaction):
            if not self.game_active:
                await interaction.response.send_message("This game has already ended!", ephemeral=True)
                return
            
            if emoji == self.correct_emoji:
                                               
                inventories = load_inventories()
                winner_id_str = str(interaction.user.id)
                
                if winner_id_str not in inventories:
                    winner_embed = discord.Embed(
                        title="WINNER!",
                        description=f"{interaction.user.mention} guessed correctly!",
                        color=discord.Color.gold()
                    )
                    winner_embed.add_field(name="Notice", value="You must be registered to claim your prize!", inline=False)
                    await interaction.response.send_message(embed=winner_embed)
                else:
                                                                 
                    set_items = SET_NAMES_CONFIG[self.correct_set].get("items", [])
                    if set_items:
                                                          
                        items_data = load_items()
                        valid_items = [item for item in set_items if item in items_data]
                        invalid_items = [item for item in set_items if item not in items_data]
                        
                        if valid_items:
                            add_items_to_inventory(winner_id_str, valid_items)
                            
                                                  
                            item_counts = {}
                            for item in valid_items:
                                item_counts[item] = item_counts.get(item, 0) + 1
                            
                            items_summary = ""
                            for item_name, count in item_counts.items():
                                item_emoji = get_item_emoji(item_name)
                                item_value = get_item_value(item_name)
                                items_summary += f"• {item_emoji} `{item_name}` x{count} ({VALUE_EMOJI} {format_value_with_commas(item_value)} each)\n"
                            
                            if invalid_items:
                                items_summary += f"\n{len(invalid_items)} item(s) not found in mm2.json: {', '.join(invalid_items)}"
                            
                            winner_embed = discord.Embed(
                                title="WINNER!",
                                description=f"{interaction.user.mention} guessed correctly!",
                                color=discord.Color.green()
                            )
                            winner_embed.add_field(name="Items Won", value=items_summary, inline=False)
                            await interaction.response.send_message(embed=winner_embed)
                        else:
                            winner_embed = discord.Embed(
                                title="WINNER!",
                                description=f"{interaction.user.mention} guessed correctly!",
                                color=discord.Color.gold()
                            )
                            winner_embed.add_field(name="Error", value=f"Items not found in mm2.json: {', '.join(invalid_items)}", inline=False)
                            await interaction.response.send_message(embed=winner_embed)
                    else:
                        winner_embed = discord.Embed(
                            title="WINNER!",
                            description=f"{interaction.user.mention} guessed correctly!",
                            color=discord.Color.green()
                        )
                        winner_embed.add_field(name="Items Won", value="No items configured for this set", inline=False)
                        await interaction.response.send_message(embed=winner_embed)
                
                self.game_active = False
                for item in self.children:
                    item.disabled = True
                await interaction.message.edit(view=self)
                
                if GUESS_SET_CHANNEL_ID and GUESS_SET_CHANNEL_ID in ACTIVE_SET_GAMES:
                    del ACTIVE_SET_GAMES[GUESS_SET_CHANNEL_ID]
            else:
                await interaction.response.send_message(f"Wrong guess! That's not {self.correct_set}. Try again!", ephemeral=True)
        
        return callback


class GuessThePetModal(discord.ui.Modal, title="Guess The Pet"):
    pet_name = discord.ui.TextInput(label="Pet Name", placeholder="e.g., Neon Fury, Star")

    async def on_submit(self, interaction: discord.Interaction):
        if GUESS_PET_CHANNEL_ID is None:
            await interaction.response.send_message("Guess The Pet channel not configured!", ephemeral=True)
            return

        pet_name = self.pet_name.value.strip()
        
        if pet_name not in PET_NAMES_CONFIG:
            await interaction.response.send_message(
                f"Invalid pet name. Available pets: {', '.join(PET_NAMES_CONFIG.keys())}",
                ephemeral=True
            )
            return
        
        correct_emoji = PET_NAMES_CONFIG[pet_name]["emoji"]
        pet_emojis = [config["emoji"] for config in PET_NAMES_CONFIG.values() if config["emoji"]]
        available_emojis = [emoji for emoji in pet_emojis if emoji and emoji != correct_emoji]
        
        if len(available_emojis) >= 3:
            wrong_options = random.sample(available_emojis, 3)
        else:
            wrong_options = available_emojis.copy()
        
        options = wrong_options.copy()
        if correct_emoji:
            options.append(correct_emoji)
        random.shuffle(options)
        
        channel = bot.get_channel(GUESS_PET_CHANNEL_ID)
        
        ACTIVE_PET_GAMES[GUESS_PET_CHANNEL_ID] = {
            "correct_emoji": correct_emoji,
            "correct_pet": pet_name,
            "host": interaction.user,
        }
        
        thumbnail_url = PET_NAMES_CONFIG[pet_name].get("image", "")
        
        embed = discord.Embed(
            title="Guess The Pet",
            description=(
                f"**What pet is this?**\n\n"
                f"**Prize:** {pet_name}\n"
                f"**Hosted by:** {interaction.user.mention}\n\n"
            ),
            color=discord.Color.purple()
        )
        
        if thumbnail_url:
            embed.set_thumbnail(url=thumbnail_url)
        embed.set_footer(text="First correct guess wins - Click the right pet button!")
        
        view = PetGameView(options, correct_emoji, pet_name, interaction.user)
        
        await interaction.response.send_message("Pet game started!", ephemeral=True)
        await channel.send(embed=embed, view=view)


class PetGameView(discord.ui.View):
    def __init__(self, options, correct_emoji, correct_pet, host):
        super().__init__(timeout=None)
        self.correct_emoji = correct_emoji
        self.correct_pet = correct_pet
        self.host = host
        self.game_active = True
        
        for emoji in options:
            if emoji and emoji.startswith("<:") and emoji.endswith(">"):
                parts = emoji.split(":")
                emoji_id = int(parts[2].replace(">", ""))
                emoji_name = parts[1]
                
                custom_emoji = discord.PartialEmoji(name=emoji_name, id=emoji_id)
                
                button = discord.ui.Button(
                    label=" ",
                    emoji=custom_emoji,
                    style=discord.ButtonStyle.secondary,
                    custom_id=f"pet_{emoji}"
                )
            else:
                button = discord.ui.Button(
                    label=emoji,
                    style=discord.ButtonStyle.secondary,
                    custom_id=f"pet_{emoji}"
                )
            
            button.callback = self.create_callback(emoji)
            self.add_item(button)
    
    def create_callback(self, emoji):
        async def callback(interaction: discord.Interaction):
            if not self.game_active:
                await interaction.response.send_message("This game has already ended!", ephemeral=True)
                return
            
            if emoji == self.correct_emoji:
                                               
                inventories = load_inventories()
                winner_id_str = str(interaction.user.id)
                
                if winner_id_str not in inventories:
                    winner_embed = discord.Embed(
                        title="WINNER!",
                        description=f"{interaction.user.mention} guessed correctly!\n\n**Pet:** {self.correct_pet}",
                        color=discord.Color.gold()
                    )
                    winner_embed.add_field(name="Notice", value="⚠️ You must be registered to claim your prize!", inline=False)
                    await interaction.response.send_message(embed=winner_embed)
                else:
                                                                 
                    pet_items = PET_NAMES_CONFIG[self.correct_pet].get("items", [])
                    if pet_items:
                                                          
                        items_data = load_items()
                        valid_items = [item for item in pet_items if item in items_data]
                        invalid_items = [item for item in pet_items if item not in items_data]
                        
                        if valid_items:
                            add_items_to_inventory(winner_id_str, valid_items)
                            
                                                  
                            item_counts = {}
                            for item in valid_items:
                                item_counts[item] = item_counts.get(item, 0) + 1
                            
                            items_summary = ""
                            for item_name, count in item_counts.items():
                                item_emoji = get_item_emoji(item_name)
                                item_value = get_item_value(item_name)
                                items_summary += f"• {item_emoji} `{item_name}` x{count} ({VALUE_EMOJI} {format_value_with_commas(item_value)} each)\n"
                            
                            if invalid_items:
                                items_summary += f"\n⚠️ {len(invalid_items)} item(s) not found in mm2.json: {', '.join(invalid_items)}"
                            
                            winner_embed = discord.Embed(
                                title="WINNER!",
                                description=f"{interaction.user.mention} guessed correctly!\n\n**Pet:** {self.correct_pet}",
                                color=discord.Color.purple()
                            )
                            winner_embed.add_field(name="Items Won", value=items_summary, inline=False)
                            await interaction.response.send_message(embed=winner_embed)
                        else:
                            winner_embed = discord.Embed(
                                title="WINNER!",
                                description=f"{interaction.user.mention} guessed correctly!\n\n**Pet:** {self.correct_pet}",
                                color=discord.Color.gold()
                            )
                            winner_embed.add_field(name="Error", value=f"Items not found in mm2.json: {', '.join(invalid_items)}", inline=False)
                            await interaction.response.send_message(embed=winner_embed)
                    else:
                        winner_embed = discord.Embed(
                            title="WINNER!",
                            description=f"{interaction.user.mention} guessed correctly!\n\n**Pet:** {self.correct_pet}",
                            color=discord.Color.purple()
                        )
                        winner_embed.add_field(name="Items Won", value="No items configured for this pet", inline=False)
                        await interaction.response.send_message(embed=winner_embed)
                
                self.game_active = False
                for item in self.children:
                    item.disabled = True
                await interaction.message.edit(view=self)
                
                if GUESS_PET_CHANNEL_ID and GUESS_PET_CHANNEL_ID in ACTIVE_PET_GAMES:
                    del ACTIVE_PET_GAMES[GUESS_PET_CHANNEL_ID]
            else:
                await interaction.response.send_message(f"Wrong guess! That's not {self.correct_pet}. Try again!", ephemeral=True)
        
        return callback


class VCRouletteModal(discord.ui.Modal, title="VC Roulette"):
    prize = discord.ui.TextInput(label="Prize Name")
    thumbnail = discord.ui.TextInput(label="Prize Thumbnail URL", required=False)

    async def on_submit(self, interaction: discord.Interaction):
        if VC_ROULETTE_TEXT_CHANNEL_ID is None:
            await interaction.response.send_message("VC Roulette text channel not configured!", ephemeral=True)
            return
            
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
            return
        
        category = guild.get_channel(VC_ROULETTE_CATEGORY_ID)
        if not isinstance(category, discord.CategoryChannel):
            await interaction.response.send_message("VC Roulette category not found!", ephemeral=True)
            return
        
        text_channel = bot.get_channel(VC_ROULETTE_TEXT_CHANNEL_ID)
        if not text_channel:
            await interaction.response.send_message("VC Roulette text channel not found!", ephemeral=True)
            return
        
        try:
                                                         
            voice_channel = await guild.create_voice_channel(
                name="🔊・vc-roullete",
                category=category
            )
        except Exception as e:
            await interaction.response.send_message(f"Failed to create voice channel: {e}", ephemeral=True)
            return
        
        await interaction.response.send_message("Roulette voice channel created! Join the voice channel and the game will start in 10 seconds.", ephemeral=True)
        
                                                    
        await asyncio.sleep(10)
        
        members_in_vc = [member for member in voice_channel.members if not member.bot]
        
        if not members_in_vc:
            await voice_channel.delete()
            try:
                await interaction.followup.send("No users joined the voice channel, game cancelled.", ephemeral=True)
            except Exception:
                pass
            return
        
        ACTIVE_ROULETTE_GAMES[voice_channel.id] = {
            "members": members_in_vc,
            "prize": self.prize.value,
            "thumbnail": self.thumbnail.value or None,
            "host": interaction.user,
            "is_active": True,
            "voice_channel": voice_channel,
        }
        
        embed = discord.Embed(
            title="VC Roulette",
            description=(
                f"**Prize:** {self.prize.value}\n"
                f"**Hosted by:** {interaction.user.mention}"
            ),
            color=discord.Color.green()
        )
        
        if self.thumbnail.value:
            embed.set_thumbnail(url=self.thumbnail.value)
        
        embed.set_footer(text="Starting roulette in 5 seconds...")
        
        try:
            await interaction.followup.send("Game starting! Spinning the roulette...", ephemeral=True)
        except Exception:
            pass
        message = await text_channel.send(embed=embed)
        
        await asyncio.sleep(5)
        await self._start_roulette_animation(text_channel, message, members_in_vc, voice_channel.id)
    
    async def _start_roulette_animation(self, channel, message, members, voice_channel_id):
        game_data = ACTIVE_ROULETTE_GAMES.get(voice_channel_id)
        
        animation_duration = 5
        cycle_interval = 0.1
        cycles = int(animation_duration / cycle_interval)
        
        for i in range(cycles):
            if not game_data["is_active"]:
                return
            
            current_user = random.choice(members)
            
            embed = discord.Embed(
                title="VC Roulette",
                description=(
                    f"**Prize:** {game_data['prize']}\n"
                    f"**Hosted by:** {game_data['host'].mention}\n\n"
                    f"**Spinning...**\n"
                    f"**Current:** {current_user.mention}"
                ),
                color=discord.Color.green()
            )
            
            if game_data["thumbnail"]:
                embed.set_thumbnail(url=game_data["thumbnail"])
            
            embed.set_footer(text=f"Spinning... {int(animation_duration - (i * cycle_interval))}s remaining")
            
            await message.edit(embed=embed)
            await asyncio.sleep(cycle_interval)
        
        if game_data and game_data["is_active"]:
            winner = random.choice(members)
            
            winner_embed = discord.Embed(
                title="WINNER!",
                description=(
                    f"**Winner:** {winner.mention}\n"
                    f"**Prize:** {game_data['prize']}\n"
                    f"**Hosted by:** {game_data['host'].mention}"
                ),
                color=discord.Color.green()
            )
            
            if game_data["thumbnail"]:
                winner_embed.set_thumbnail(url=game_data["thumbnail"])
            
            winner_embed.set_footer(text="Congratulations - Ticket to claim!")
            
            await message.edit(embed=winner_embed)
            
            game_data["is_active"] = False
                                                      
            try:
                voice_channel = game_data.get("voice_channel")
                if voice_channel:
                    await voice_channel.delete()
            except Exception:
                pass
            
            if voice_channel_id in ACTIVE_ROULETTE_GAMES:
                del ACTIVE_ROULETTE_GAMES[voice_channel_id]


class MinigamePanelSelect(discord.ui.Select):
    def __init__(self):
        options = []
        for minigame in MINIGAME_NAMES:
            emoji = minigame.get("emoji", "")
            emoji_obj = _parse_emoji(emoji) if emoji else None
            options.append(
                discord.SelectOption(
                    label=minigame["name"],
                    value=minigame["name"],
                    description="Powered by Bloxloot",
                    emoji=emoji_obj
                )
            )
        super().__init__(
            custom_id="minigame_select",
            placeholder="Select a minigame...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]
        
        if selected == "Guess the Crypto":
            modal = GuessTheCryptoModal()
            await interaction.response.send_modal(modal)
        elif selected == "Guess the Pet":
            modal = GuessThePetModal()
            await interaction.response.send_modal(modal)
        elif selected == "Guess the Set":
            modal = GuessTheSetModal()
            await interaction.response.send_modal(modal)
        elif selected == "VC Roullete":
            modal = VCRouletteModal()
            await interaction.response.send_modal(modal)
        else:
            await interaction.response.send_message(f"Started **{selected}** minigame event!", ephemeral=True)


class MinigamePanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(MinigamePanelSelect())


async def ensure_race_category_position(bot_client: discord.Client):
    category = bot_client.get_channel(RACE_CHANNEL_CATEGORY_ID)
    if not isinstance(category, discord.CategoryChannel):
        return

    target_channel = bot_client.get_channel(RACE_CHANNEL_CATEGORY_BEFORE_ID)
    if not isinstance(target_channel, discord.abc.GuildChannel):
        return

    try:
        desired_position = max(0, target_channel.position - 1)
        if category.position >= target_channel.position:
            await category.edit(position=desired_position)
    except Exception as e:
        print(f"Error moving race category above channel {RACE_CHANNEL_CATEGORY_BEFORE_ID}: {e}")


async def create_event_panel():
    await bot.wait_until_ready()
    event_panel_data = load_event_panel()
    channel_id = EVENT_PANEL_CHANNEL_ID or event_panel_data.get("channel_id")
    if not channel_id:
        print("Event panel channel is not configured; skipping event panel creation.")
        return

    channel = bot.get_channel(channel_id)
    if not channel:
        print(f"Event panel channel {channel_id} not found!")
        return

    panel_message_id = event_panel_data.get("message_id")
    embed, view = build_event_panel_embed()
    if panel_message_id:
        try:
            message = await channel.fetch_message(panel_message_id)
            await message.edit(embed=embed, view=view)
            print("Event panel updated successfully")
            return
        except Exception:
            pass

    message = await channel.send(embed=embed, view=view)
    save_event_panel({"message_id": message.id})
    print("Event panel created successfully")


async def update_event_panel_embed():
    await bot.wait_until_ready()
    event_panel_data = load_event_panel()
    channel_id = EVENT_PANEL_CHANNEL_ID or event_panel_data.get("channel_id")
    if not channel_id:
        return

    channel = bot.get_channel(channel_id)
    if not channel:
        return

    panel_message_id = event_panel_data.get("message_id")
    if not panel_message_id:
        return

    try:
        message = await channel.fetch_message(panel_message_id)
        embed, view = build_event_panel_embed()
        await message.edit(embed=embed, view=view)
    except Exception:
        return


def build_tax_panel_embed():
    tax_rate = get_house_tax()
    tax_panel_data = load_tax_panel()
    channel_id = TAX_PANEL_CHANNEL_ID or tax_panel_data.get("channel_id")
    embed = discord.Embed(
        title="Bloxloot Tax Panel",
        description="Use the buttons below to select the tax rate and view taxed items.",
        color=discord.Color.green()
    )
    embed.add_field(
        name="Bloxloot Tax Rate",
        value=f"**{tax_rate * 100:.1f}%**",
        inline=True
    )

    if TAX_PROFILES:
        profiles_text = ""
        for user_id_str, profile in TAX_PROFILES.items():
            emoji = profile.get("emoji", "")
            rate = profile.get("tax_rate", tax_rate)
            profiles_text += f"{emoji} <@{user_id_str}> - **{rate * 100:.1f}%**\n"
        embed.add_field(
            name="Bloxloot Shareholders",
            value=profiles_text.strip(),
            inline=True
        )
                                                                                  
    embed.add_field(
        name="Tax Log Channel",
        value=f"<#{TAX_LOG_CHANNEL_ID}>",
        inline=False
    )

    if channel_id:
        embed.set_footer(text=f"Bloxloot Team Members Only • Last Updated {datetime.now().strftime('%d %b %Y %I:%M %p')}")
    else:
        embed.set_footer(text="Tax panel channel is not configured yet.")
    return embed, TaxPanelView()


async def create_tax_panel():
    await bot.wait_until_ready()
    tax_panel_data = load_tax_panel()
    channel_id = TAX_PANEL_CHANNEL_ID or tax_panel_data.get("channel_id")
    if not channel_id:
        print("Tax panel channel is not configured; skipping tax panel creation.")
        return

    channel = bot.get_channel(channel_id)
    if not channel:
        print(f"Tax panel channel {channel_id} not found!")
        return

    panel_message_id = tax_panel_data.get("message_id")
    embed, view = build_tax_panel_embed()

    if panel_message_id:
        try:
            message = await channel.fetch_message(panel_message_id)
            await message.edit(embed=embed, view=view)
            print("Tax panel updated successfully")
            return
        except Exception:
            pass

    message = await channel.send(embed=embed, view=view)
    tax_panel_data["message_id"] = message.id
    save_tax_panel(tax_panel_data)
    print("Tax panel created successfully")


def _resolve_role_from_names(guild: discord.Guild, *role_names: str) -> Optional[discord.Role]:
    if not guild:
        return None
    normalized_names = {name.lower() for name in role_names if name}
    for role in guild.roles:
        if role.name.lower() in normalized_names:
            return role
    return None


def _get_captcha_image_paths(base_directory: str) -> List[str]:
    image_dirs = [
        os.path.join(base_directory, "pets"),
        os.path.join(base_directory, "mm2images"),
    ]

    image_extensions = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"}
    image_paths: List[str] = []
    for image_dir in image_dirs:
        if not os.path.isdir(image_dir):
            continue
        for root, _, files in os.walk(image_dir):
            for filename in files:
                if os.path.splitext(filename)[1].lower() in image_extensions:
                    image_paths.append(os.path.join(root, filename))
    return image_paths


def _generate_verification_captcha_image(output_path: str) -> str:
    output_dir = os.path.dirname(output_path) or "."
    os.makedirs(output_dir, exist_ok=True)
    if os.path.exists(output_path):
        os.remove(output_path)

    width, height = 720, 260
    base = Image.new("RGBA", (width, height), color=(20, 20, 24, 255))
    draw = ImageDraw.Draw(base)

    for _ in range(24):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line([(x1, y1), (x2, y2)], fill=(random.randint(70, 110), random.randint(70, 110), random.randint(70, 110)), width=random.randint(1, 3))

    for _ in range(220):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=(random.randint(90, 140), random.randint(90, 140), random.randint(90, 140)))

    for _ in range(18):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line([(x1, y1), (x2, y2)], fill=(random.randint(20, 70), random.randint(20, 70), random.randint(20, 70)), width=1)

    captcha_image_paths = _get_captcha_image_paths(BASE_DIR)
    if captcha_image_paths:
        for _ in range(16):
            image_path = random.choice(captcha_image_paths)
            try:
                captcha_image = Image.open(image_path).convert("RGBA")
            except Exception:
                continue

            size = random.randint(36, 74)
            captcha_image = captcha_image.resize((size, size), Image.LANCZOS)
            left = random.randint(0, max(0, width - size))
            top = random.randint(0, max(0, height - size))
            base.alpha_composite(captcha_image, dest=(left, top))
    else:
        for _ in range(16):
            x = random.randint(0, width)
            y = random.randint(0, height)
            radius = random.randint(18, 48)
            draw.ellipse([
                x - radius,
                y - radius,
                x + radius,
                y + radius,
            ], fill=(random.randint(80, 140), random.randint(80, 140), random.randint(80, 140)), outline=None)

    letters = "".join(random.choice(string.ascii_uppercase) for _ in range(5))
    for idx, letter in enumerate(letters):
        x = 52 + idx * 116 + random.randint(-18, 18)
        y = random.randint(76, 126)
        font_size = random.randint(52, 66)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()
        letter_color = (random.randint(140, 220), random.randint(140, 220), random.randint(140, 220))
        draw.text((x, y), letter, fill=letter_color, font=font)
        draw.line([(x - 24, y + 20), (x + 64, y + 20)], fill=(random.randint(70, 110), random.randint(70, 110), random.randint(70, 110)), width=2)
        draw.line([(x - 10, y + 12), (x + 38, y + 46)], fill=(random.randint(70, 110), random.randint(70, 110), random.randint(70, 110)), width=2)
        draw.line([(x + 6, y - 8), (x + 58, y + 8)], fill=(random.randint(70, 110), random.randint(70, 110), random.randint(70, 110)), width=2)

    image = base.filter(ImageFilter.GaussianBlur(radius=1.0))
    image.save(output_path)
    return letters


class VerificationCaptchaModal(discord.ui.Modal, title="Enter the Captcha"):
    def __init__(self, expected_answer: str):
        super().__init__(timeout=None)
        self.expected_answer = expected_answer
        self.captcha_input = discord.ui.TextInput(
            label="Type the 5 letters from the image",
            placeholder="Example: ABCDE",
            required=True,
            min_length=5,
            max_length=5,
        )
        self.add_item(self.captcha_input)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        submitted = self.captcha_input.value.strip().upper().replace(" ", "")
        expected = self.expected_answer.upper()
        if submitted != expected:
            return

        guild = interaction.guild
        if not guild:
            return

        member = interaction.user
        if not isinstance(member, discord.Member):
            return

        looter_role = _resolve_role_from_names(guild, "Looter")
        unverified_role = _resolve_role_from_names(guild, "Unverified", "unverified")

        if unverified_role and unverified_role in member.roles:
            await member.remove_roles(unverified_role, reason="Captcha verification passed")
        if looter_role and looter_role not in member.roles:
            await member.add_roles(looter_role, reason="Captcha verification passed")


class VerificationPanelView(discord.ui.View):
    def __init__(self, expected_answer: str = ""):
        super().__init__(timeout=None)
        self.expected_answer = expected_answer
        self.add_item(discord.ui.Button(
            label="Rewards",
            style=discord.ButtonStyle.link,
            url=REFERRALS_URL,
            row=0
        ))

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.secondary, row=0, custom_id="verification_panel_verify")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(VerificationCaptchaModal(self.expected_answer))


def build_verification_panel_embed():
    captcha_path = os.path.join(BASE_DIR, "verification_captcha.png")
    captcha_answer = _generate_verification_captcha_image(captcha_path)
    captcha_filename = os.path.basename(captcha_path)

    embed = discord.Embed(
        title="Bloxloot Verification",
        description="Use the verify button to solve the captcha and input your answer.",
        color=discord.Color.green()
    )
    embed.set_image(url=f"attachment://{captcha_filename}")
    embed.set_footer(text=f"Powered by Bloxloot  •  Safe & Trusted  •  Last Updated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    view = VerificationPanelView(captcha_answer)
    file = discord.File(captcha_path, filename=captcha_filename)
    return embed, view, file


async def refresh_verification_panel_message():
    if "bot" not in globals():
        return
    if not getattr(globals().get("bot"), "is_ready", lambda: False)():
        return

    verification_panel_data = load_verification_panel()
    channel_id = VERIFICATION_CHANNEL_ID or verification_panel_data.get("channel_id")
    if not channel_id:
        return

    channel = bot.get_channel(channel_id)
    if not channel:
        return

    panel_message_id = verification_panel_data.get("message_id")
    if not panel_message_id:
        return

    try:
        message = await channel.fetch_message(panel_message_id)
    except Exception:
        return

    embed, view, file = build_verification_panel_embed()
    try:
        await message.edit(embed=embed, view=view, attachments=[file])
    except Exception as exc:
        print(f"Failed to refresh verification panel: {exc}")


async def create_verification_panel():
    await bot.wait_until_ready()
    verification_panel_data = load_verification_panel()
    channel_id = VERIFICATION_CHANNEL_ID or verification_panel_data.get("channel_id")
    if not channel_id:
        print("Verification panel channel is not configured; skipping verification panel creation.")
        return

    channel = bot.get_channel(channel_id)
    if not channel:
        print(f"Verification panel channel {channel_id} not found!")
        return

    panel_message_id = verification_panel_data.get("message_id")
    embed, view, file = build_verification_panel_embed()

    if panel_message_id:
        try:
            message = await channel.fetch_message(panel_message_id)
            await message.edit(embed=embed, view=view, attachments=[file])
            print("Verification panel updated successfully")
            return
        except Exception:
            pass

    message = await channel.send(embed=embed, view=view, file=file)
    verification_panel_data["message_id"] = message.id
    save_verification_panel(verification_panel_data)
    print("Verification panel created successfully")


async def update_tax_panel_embed():
    """Update the existing tax panel message embed to reflect current staff uses."""
    await bot.wait_until_ready()
    tax_panel_data = load_tax_panel()
    channel_id = TAX_PANEL_CHANNEL_ID or tax_panel_data.get("channel_id")
    if not channel_id:
        return
    channel = bot.get_channel(channel_id)
    if not channel:
        return
    panel_message_id = tax_panel_data.get("message_id")
    if not panel_message_id:
        return
    try:
        message = await channel.fetch_message(panel_message_id)
        embed, view = build_tax_panel_embed()
        await message.edit(embed=embed, view=view)
    except Exception:
        return


async def update_admin_panel_embed():
    """Update the existing admin/staff panel message embed to reflect current staff uses."""
    await bot.wait_until_ready()
    panel_data = load_admin_panel()
    channel_id = ADMIN_PANEL_CHANNEL_ID or panel_data.get("channel_id")
    if not channel_id:
        return
    channel = bot.get_channel(channel_id)
    if not channel:
        return
    panel_message_id = panel_data.get("message_id")
    if not panel_message_id:
        return
    try:
        message = await channel.fetch_message(panel_message_id)
                                                                
                                                                                  
        embed = discord.Embed(
            title="Bloxloot Staff Panel",
            description="Use the buttons below to manage user inventories and Moderation.",
            color=discord.Color.green()
        )
        staff_profiles = ensure_staff_profiles()
        staff_text = ""
        if staff_profiles:
            for user_id_str, profile in staff_profiles.items():
                if user_id_str in TAX_PROFILES:
                    continue
                emoji = profile.get("emoji", "")
                uses = profile.get("uses", 0)
                limit = profile.get("limit", 10)
                staff_text += f"{emoji} <@{user_id_str}> - **{uses}/{limit}**\n"
                                                                     
        private_links = (
            "https://discord.com/channels/1497891147664588870/1507356202206629888",
            "https://discord.com/channels/1497891147664588870/1507356534047244328",
        )
        mm2_online, mm2_total = await get_servers_status(MM2_DEPOSIT_SERVERS)
        adm_online, adm_total = await get_servers_status(ADM_DEPOSIT_SERVERS)
        private_text = (
            f"{private_links[0]} **{mm2_online}/{mm2_total}**\n"
            f"{private_links[1]} **{adm_online}/{adm_total}**"
        )

                                                               
        mm2_total_wagered = get_total_wagered(GameType.MM2)
        adm_total_wagered = get_total_wagered(GameType.ADM)

        embed.add_field(
            name="Bloxloot Overview",
            value=(
                f"**MM2 -** {VALUE_EMOJI} **{format_value_with_commas(mm2_total_wagered)}**\n"
                f"**ADM -** {VALUE_EMOJI} **{format_value_with_commas(adm_total_wagered)}**"
            ),
            inline=True
        )

        embed.add_field(name="Bloxloot Staff", value=staff_text or "No staff profiles configured", inline=True)

        embed.add_field(name="Bloxloot In-Game", value=private_text, inline=False)
        embed.set_footer(text=f"Bloxloot Team members only! • Last Updated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        await message.edit(embed=embed)
    except Exception:
        return

                                         
async def create_and_post_jackpot(bot_instance):
    """Creates and posts a new jackpot game in the jackpot channel."""
    await bot_instance.wait_until_ready()
    channel = bot_instance.get_channel(JACKPOT_CHANNEL_ID)
    if not channel:
        print(f"Jackpot channel {JACKPOT_CHANNEL_ID} not found!")
        return

    jackpots = load_jackpot_games()
                                              
    for jp in jackpots.values():
        if jp.get('status') == 'open':
            print("An open jackpot already exists, not creating a new one.")
            return

                        
    jp_id = f"jackpot_{int(datetime.now().timestamp())}"
    end_time = int((datetime.now() + timedelta(seconds=60)).timestamp())
    jackpot = {
        "jackpot_id": jp_id,
        "status": "open",
        "created_at": datetime.now().isoformat(),
        "end_time": end_time,
        "total_value": 0,
        "participants": {},
        "channel_id": JACKPOT_CHANNEL_ID,
    }

    embed = discord.Embed(
        title="JACKPOT",
        color=discord.Color.green(),
        timestamp=datetime.now()
    )
    embed.add_field(name="Time Remaining", value="60s", inline=False)
    embed.add_field(name="Participants", value="No participants yet", inline=False)
    embed.set_footer(text=f"Total Pot: 0")

    view = JackpotJoinView(jp_id)
    message = await channel.send(embed=embed, view=view)

    jackpot["message_id"] = message.id
    jackpots[jp_id] = jackpot
    save_jackpot_games(jackpots)

                          
    asyncio.create_task(_run_jackpot_countdown(jp_id))

                                         
class JackpotJoinView(discord.ui.View):
    def __init__(self, jackpot_id: str):
        super().__init__(timeout=None)
        self.jackpot_id = jackpot_id

    @discord.ui.button(label="JOIN", style=discord.ButtonStyle.secondary, row=0)
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                            
        if not is_user_registered(interaction.user.id):
            await interaction.response.send_message("You need to register first! Use `/register`.", ephemeral=True)
            return

                                     
        user_items = get_user_all_items(str(interaction.user.id))
        if not user_items:
            await interaction.response.send_message("You have no items to join with!", ephemeral=True)
            return

        view = JackpotItemSelectionView(user_items, self.jackpot_id)
        embed = discord.Embed(
            title="Select Items to Join Jackpot",
            description=f"Minimum bet: {VALUE_EMOJI} **{format_value_with_commas(MIN_BET_VALUE)}**\nSelect items worth at least the minimum.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

                                                   
class JackpotItemSelectionView(discord.ui.View):
    def __init__(self, user_items: List[Tuple[str, int]], jackpot_id: str):
        super().__init__(timeout=None)
        self.user_items = user_items
        self.jackpot_id = jackpot_id
        self.dropdown = ItemSelectDropdown(user_items, MAX_BET_VALUE)
        self.add_item(self.dropdown)

    @discord.ui.button(label="CONFIRM SELECTION", style=discord.ButtonStyle.secondary, row=1)
    async def confirm_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.dropdown.selected_items:
            await interaction.response.send_message("Please select at least one item!", ephemeral=True)
            return

        selected_items = self.dropdown.selected_items
        selected_value = self.dropdown.selected_value

        if selected_value < MIN_BET_VALUE:
            await interaction.response.send_message(
                f"Minimum bet for jackpot is {VALUE_EMOJI} **{format_value_with_commas(MIN_BET_VALUE)}**",
                ephemeral=True
            )
            return
        
                                      
        valid, game_type, error_msg = validate_items_same_type(selected_items)
        if not valid:
            await interaction.response.send_message(
                f"❌ {error_msg}",
                ephemeral=True
            )
            return

                                                        
        remove_items_from_inventory(str(interaction.user.id), selected_items)

                                 
        jackpots = load_jackpot_games()
        jp = jackpots.get(self.jackpot_id)
        if not jp or jp.get('status') != 'open':
                                            
            add_items_to_inventory(str(interaction.user.id), selected_items)
            await interaction.response.send_message("This jackpot is no longer accepting joins.", ephemeral=True)
            return

                         
        participants = jp.get('participants', {})
        uid = str(interaction.user.id)
        if uid in participants:
                                               
            add_items_to_inventory(str(interaction.user.id), selected_items)
            await interaction.response.send_message("You have already joined this jackpot.", ephemeral=True)
            return

        participants[uid] = {
            'items': selected_items,
            'value': selected_value,
            'joined_at': datetime.now().isoformat(),
            'game_type': game_type
        }

                           
        total = jp.get('total_value', 0) + selected_value
        jp['participants'] = participants
        jp['total_value'] = total
        jackpots[self.jackpot_id] = jp
        save_jackpot_games(jackpots)

                                                           
        try:
            channel = bot.get_channel(jp['channel_id'])
            if channel and jp.get('message_id'):
                message = await channel.fetch_message(jp['message_id'])
                
                                          
                remaining = int(jp['end_time'] - datetime.now().timestamp())
                hours = remaining // 3600
                minutes = (remaining % 3600) // 60
                
                embed = discord.Embed(
                    title="JACKPOT",
                    color=discord.Color.green(),
                    timestamp=datetime.fromisoformat(jp['created_at'])
                )

                           
                embed.add_field(name="Time Remaining", value=f"{hours}h {minutes}m", inline=False)

                                                                               
                parts_text = []
                for p_uid, pdata in participants.items():
                    mention = f"<@{p_uid}>"
                    
                                                          
                    registrations = load_registrations()
                    user_data = registrations.get(p_uid, {})
                    roblox_name = user_data.get('roblox_username', 'Unknown')
                    
                    pct = (pdata['value'] / total * 100) if total > 0 else 0
                    game_type_display = pdata.get('game_type', 'Unknown')
                    
                                                                                  
                    item_counts = {}
                    for item in pdata.get('items', []):
                        item_counts[item] = item_counts.get(item, 0) + 1
                    
                    items_summary = ""
                    for item_name, count in list(item_counts.items())[:5]:                      
                        item_value = get_item_value(item_name)
                        item_emoji = get_item_emoji(item_name)
                        items_summary += f"• {item_emoji} `{item_name}` x{count} ({VALUE_EMOJI} {format_value_with_commas(item_value)} each)\n"
                    
                    if len(item_counts) > 5:
                        items_summary += f"• ...and {len(item_counts)-5} more item types\n"
                    
                                                       
                    parts_text.append(f"{mention} — {pct:.1f}%\n{items_summary}\n")

                embed.add_field(name="Participants", value="\n".join(parts_text) or "No participants yet", inline=False)
                embed.set_footer(text=f"Total Pot: {format_value_with_commas(total)}")

                await message.edit(embed=embed)
        except Exception:
            pass

        await interaction.response.send_message(f"You joined the jackpot with {VALUE_EMOJI} **{format_value_with_commas(selected_value)}** !", ephemeral=True)

                                         
async def _run_jackpot_countdown(jackpot_id: str):
    jackpots = load_jackpot_games()
    jp = jackpots.get(jackpot_id)
    if not jp:
        return

    channel = bot.get_channel(jp['channel_id'])
    if not channel:
        return

                                
    while True:
        jp = load_jackpot_games().get(jackpot_id)
        if not jp or jp.get('status') != 'open':
            return
        now_ts = datetime.now().timestamp()
        remaining = int(jp['end_time'] - now_ts)
        try:
            if jp.get('message_id'):
                message = await channel.fetch_message(jp['message_id'])
                embed = discord.Embed(
                    title="JACKPOT",
                    color=discord.Color.green(),
                    timestamp=datetime.fromisoformat(jp['created_at'])
                )
                
                           
                if remaining > 60:
                    minutes = remaining // 60
                    seconds = remaining % 60
                    embed.add_field(name="Time Remaining", value=f"{minutes}m {seconds}s", inline=False)
                else:
                    embed.add_field(name="Time Remaining", value=f"{remaining}s", inline=False)
                
                participants = jp.get('participants', {})
                total = jp.get('total_value', 0)
                
                if participants:
                    parts_text = []
                    for p_uid, pdata in participants.items():
                        mention = f"<@{p_uid}>"
                        
                                                              
                        registrations = load_registrations()
                        user_data = registrations.get(p_uid, {})
                        roblox_name = user_data.get('roblox_username', 'Unknown')
                        
                        pct = (pdata['value'] / total * 100) if total > 0 else 0
                        game_type_display = pdata.get('game_type', 'Unknown')
                        
                                                                                      
                        item_counts = {}
                        for item in pdata.get('items', []):
                            item_counts[item] = item_counts.get(item, 0) + 1
                        
                        items_summary = ""
                        for item_name, count in list(item_counts.items())[:5]:                      
                            item_value = get_item_value(item_name)
                            item_emoji = get_item_emoji(item_name)
                            items_summary += f"• {item_emoji} `{item_name}` x{count} ({VALUE_EMOJI} {format_value_with_commas(item_value)} each)\n"
                        
                        if len(item_counts) > 5:
                            items_summary += f"• ...and {len(item_counts)-5} more item types\n"
                        
                                                           
                        parts_text.append(f"{mention} — {pct:.1f}%\n{items_summary}\n")

                    embed.add_field(name="Participants", value="\n".join(parts_text) or "No participants yet", inline=False)
                else:
                    embed.add_field(name="Participants", value="No participants yet", inline=False)
                
                embed.set_footer(text=f"Total Pot: {format_value_with_commas(total)}")
                
                await message.edit(embed=embed)
        except Exception as e:
            print(f"Error updating jackpot countdown: {e}")

        if remaining <= 0:
            break
        await asyncio.sleep(1)

                         
    jackpots = load_jackpot_games()
    jp = jackpots.get(jackpot_id)
    if not jp:
        return
    jp['status'] = 'resolving'
    save_jackpot_games(jackpots)

    participants = jp.get('participants', {})
    total = jp.get('total_value', 0)

    if not participants:
                                 
        try:
            if jp.get('message_id'):
                message = await channel.fetch_message(jp['message_id'])
                embed = discord.Embed(title="JACKPOT CANCELLED", description="No participants joined.", color=discord.Color.red())
                await message.edit(embed=embed, view=None)
        except Exception:
            pass
                           
        jackpots = load_jackpot_games()
        if jackpot_id in jackpots:
            del jackpots[jackpot_id]
            save_jackpot_games(jackpots)
                                                    
        try:
            await asyncio.sleep(5)
            asyncio.create_task(create_and_post_jackpot(bot))
        except Exception:
            pass
        return

                   
    user_ids = list(participants.keys())
    weights = [participants[uid]['value'] for uid in user_ids]
    try:
        winner_uid = str(random.choices(user_ids, weights=weights, k=1)[0])
    except Exception:
        winner_uid = user_ids[0]

                                           
    all_items = []
    for pdata in participants.values():
        all_items.extend(pdata['items'])

                           
    remaining_items = all_items                          
    taxed_items = []                  
    tax_amount = 0          
    
                     
    await log_taxed_items(
        source_game="Jackpot",
        winner_id=int(winner_uid),
        loser_id=0,
        tax_amount=calculate_tax(total),
        items=taxed_items,
        pot_value=total
    )
    
    add_items_to_inventory(winner_uid, remaining_items)

                                 
    try:
        if jp.get('message_id'):
            message = await channel.fetch_message(jp['message_id'])
            winner_mention = f"<@{winner_uid}>"
            
                                      
            registrations = load_registrations()
            winner_data = registrations.get(winner_uid, {})
            
            embed = discord.Embed(
                title="JACKPOT - WINNER!",
                color=discord.Color.green()
            )
            
                                                                  
            if winner_data.get('roblox_avatar'):
                embed.set_thumbnail(url=winner_data['roblox_avatar'])
            
            embed.add_field(
                name="Winner", 
                value=f"{winner_mention}\n", 
                inline=True
            )
            
            embed.add_field(
                name="Total Pot", 
                value=f"{VALUE_EMOJI} **{format_value_with_commas(total)}**", 
                inline=True
            )

                                                
            item_counts = {}
            for it in remaining_items:
                item_counts[it] = item_counts.get(it, 0) + 1

            summary = ""
            for name, cnt in list(item_counts.items())[:10]:
                item_value = get_item_value(name)
                item_emoji = get_item_emoji(name)
                total_value = item_value * cnt
                summary += f"• {item_emoji} `{name}` x{cnt} ({VALUE_EMOJI} {format_value_with_commas(item_value)} each)\n"
                
            if len(item_counts) > 10:
                summary += f"...and {len(item_counts)-10} more types"

            embed.add_field(name="Items Won", value=summary or "No items", inline=False)
            
            await message.edit(embed=embed, view=None)
    except Exception as e:
        print(f"Error updating jackpot winner message: {e}")

                            
    jackpots = load_jackpot_games()
    if jackpot_id in jackpots:
        del jackpots[jackpot_id]
        save_jackpot_games(jackpots)

                                                
    try:
        await asyncio.sleep(5)
        asyncio.create_task(create_and_post_jackpot(bot))
    except Exception:
        pass

                                         
class BloxlootBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True
        intents.guilds = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.creating_users = set()                                         
                                                                              
                                                                                       
        self.last_processed_trade_id = None                                          
        self.last_processed_adm_id = None                                          
        self.trade_webhook_id = None                                   
        self.trade_channel = None                                        
        self.adm_webhook_id = None
        self.adm_channel = None
        self.crypto_panel_sent = False
    
    async def setup_hook(self):
        await self.tree.sync()
        print("Commands synced globally!")
        self.add_view(AdminPanelView())
        self.add_view(DepositCryptoSelectView(owner_id=None, timeout=None))
        self.add_view(CryptoWithdrawSelectView(owner_id=None, timeout=None))
                                               
        try:
            asyncio.create_task(self.reset_staff_uses_loop())
        except Exception:
            pass
                                          
        try:
            asyncio.create_task(self.tag_reward_loop())
        except Exception:
            pass
                                      
        try:
            asyncio.create_task(self.invite_reward_loop())
        except Exception:
            pass

        try:
            asyncio.create_task(self.verification_captcha_refresh_loop())
        except Exception:
            pass

    async def update_presence(self):
        """Update the bot presence to show the current verified looter count."""
        try:
            registrations = load_registrations()
            if not isinstance(registrations, dict):
                looter_count = 0
            else:
                looter_count = sum(
                    1 for entry in registrations.values()
                    if isinstance(entry, dict) and entry.get("verified")
                )
            await self.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.playing,
                    name=f"Bloxloot | {looter_count} Looters"
                )
            )
        except Exception as e:
            print(f"Failed to set presence: {e}")

    async def reset_staff_uses_loop(self, interval: int = 86400):
        """Reset staff uses every `interval` seconds (default 24 hours)."""
        await self.wait_until_ready()
                                                                                      
        await asyncio.sleep(interval)
        while not self.is_closed():
            try:
                reset_staff_uses()
            except Exception as e:
                print(f"Error resetting staff uses: {e}")
            await asyncio.sleep(interval)

    async def admin_panel_status_loop(self, interval: int = 60):
        """Background task: periodically refresh the admin panel embed to show live deposit server status.

        Default interval is 60 seconds for near-real-time updates.
        """
        await self.wait_until_ready()
        while not self.is_closed():
            try:
                await update_admin_panel_embed()
            except Exception as e:
                print(f"Error updating admin panel status: {e}")
            await asyncio.sleep(interval)

    async def tag_reward_loop(self, interval: int = 3600):
        """Background loop to grant random stock rewards to active tag adopters every 24 hours."""
        await self.wait_until_ready()
        while not self.is_closed():
            try:
                state = load_tag_reward_state()
                users = state.get("users", {})
                now = datetime.now(timezone.utc)
                updated = False

                for user_id_str, entry in list(users.items()):
                    if not entry.get("active", False):
                        continue
                    last_rewarded = entry.get("last_rewarded_at") or entry.get("adopted_at")
                    if not last_rewarded:
                        continue
                    try:
                        last_rewarded_dt = datetime.fromisoformat(last_rewarded)
                    except Exception:
                        continue
                    if last_rewarded_dt + timedelta(hours=24) <= now:
                        user_id = int(user_id_str)
                        await self._grant_tag_reward(user_id)
                        users[user_id_str]["last_rewarded_at"] = now.isoformat()
                        updated = True

                if updated:
                    save_tag_reward_state(state)
            except Exception as e:
                print(f"Error in tag reward loop: {e}")
            await asyncio.sleep(interval)

    async def invite_reward_loop(self, interval: int = 300):
        """Background loop to monitor invite rewards. Checks periodically for invite message updates."""
        await self.wait_until_ready()
        while not self.is_closed():
            try:
                                                                                 
                                                                
                await asyncio.sleep(interval)
            except Exception as e:
                print(f"Error in invite reward loop: {e}")
                await asyncio.sleep(interval)

    async def race_refresh_loop(self, interval: int = 10):
        """Background loop to refresh race channel leaderboard embeds."""
        await self.wait_until_ready()
        while not self.is_closed():
            try:
                await refresh_active_race_channel_embeds()
            except Exception as e:
                print(f"Error refreshing race channel embeds: {e}")
            await asyncio.sleep(interval)

    async def verification_captcha_refresh_loop(self, interval: int = 60):
        """Background loop to rotate the verification captcha image each minute."""
        await self.wait_until_ready()
        while not self.is_closed():
            try:
                await refresh_verification_panel_message()
            except Exception as e:
                print(f"Error refreshing verification captcha panel: {e}")
            await asyncio.sleep(interval)

        content = message.content.strip()
        if not content:
            return

        adopted_match = re.search(r"(?:✅|\u2705)\s*(?P<subject>.+?) adopted server tag and was given the role\.", content, re.IGNORECASE)
        removed_match = re.search(r"(?:ℹ️|\u2139)\s*(?P<subject>.+?) removed the server tag, role was removed\.", content, re.IGNORECASE)
        if not adopted_match and not removed_match:
            return

        event_type = "adopted" if adopted_match else "removed"
        subject_text = (adopted_match or removed_match).group("subject").strip()
        target_user = await self._resolve_tag_target_user(message, subject_text)

        if not target_user:
                                                                                         
            await self._post_tag_event_embed(subject_text, event_type, None, None)
            return

        discord_user_id = target_user.id
        if event_type == "adopted":
            self._activate_tag_reward_for_user(discord_user_id, target_user.name)
            await self._post_tag_event_embed(f"<@{discord_user_id}>", event_type, discord_user_id, target_user)
        else:
            self._deactivate_tag_reward_for_user(discord_user_id)
            await self._post_tag_event_embed(f"<@{discord_user_id}>", event_type, discord_user_id, target_user)

    async def _resolve_tag_target_user(self, message: discord.Message, subject_text: str) -> Optional[discord.User]:
        if message.raw_mentions:
            try:
                return await self.fetch_user(message.raw_mentions[0])
            except Exception:
                pass

        if message.mentions:
            return message.mentions[0]

        mention_id_match = re.search(r"<@!?(?P<id>\d+)>", subject_text)
        if mention_id_match:
            try:
                return await self.fetch_user(int(mention_id_match.group("id")))
            except Exception:
                pass

        if message.guild:
            normalized_text = subject_text.lower().strip()
            for member in message.guild.members:
                member_name = member.name.lower().strip()
                member_display = member.display_name.lower().strip()
                if member_name == normalized_text or member_display == normalized_text:
                    return member
            for member in message.guild.members:
                member_name = member.name.lower()
                member_display = member.display_name.lower()
                if normalized_text in member_name or normalized_text in member_display:
                    return member

                                                                                 
        matched_id = self._find_registration_user_id_by_username(subject_text)
        if matched_id is not None:
            try:
                return await self.fetch_user(matched_id)
            except Exception:
                pass

        return None

    def _get_registration_avatar_url(self, user_id: int) -> Optional[str]:
        registrations = load_registrations()
        user_data = registrations.get(str(user_id), {})
        avatar = user_data.get("roblox_avatar") or user_data.get("pending_roblox_avatar")
        if avatar:
            return avatar
        roblox_id = user_data.get("roblox_id") or user_data.get("pending_roblox_id")
        if roblox_id:
            return f"https://www.roblox.com/headshot-thumbnail/image?userId={roblox_id}&width=420&height=420&format=png"
        return None

    def _get_registration_username(self, user_id: int) -> str:
        registrations = load_registrations()
        user_data = registrations.get(str(user_id), {})
        return user_data.get("roblox_username") or user_data.get("pending_roblox_username") or user_data.get("pending_roblox_display_name") or "Unknown"

    def _find_registration_user_id_by_username(self, username: str) -> Optional[int]:
        registrations = load_registrations()
        normalized = username.lower().strip()
        for uid, user_data in registrations.items():
            discord_username = user_data.get("discord_username")
            if discord_username and discord_username.lower().strip() == normalized:
                try:
                    return int(uid)
                except Exception:
                    continue
        return None

    def _activate_tag_reward_for_user(self, user_id: int, discord_name: str):
        state = load_tag_reward_state()
        users = state.setdefault("users", {})
        users[str(user_id)] = {
            "active": True,
            "adopted_at": datetime.now(timezone.utc).isoformat(),
            "last_rewarded_at": datetime.now(timezone.utc).isoformat(),
            "discord_name": discord_name,
        }
        save_tag_reward_state(state)

    def _deactivate_tag_reward_for_user(self, user_id: int):
        state = load_tag_reward_state()
        users = state.get("users", {})
        if str(user_id) in users:
            users[str(user_id)]["active"] = False
            users[str(user_id)]["removed_at"] = datetime.now(timezone.utc).isoformat()
            save_tag_reward_state(state)

    async def _grant_tag_reward(self, user_id: int):
        stock_item = select_random_stock_item()
        if not stock_item:
            return

        item_name = stock_item.get("name")
        if not item_name:
            return

        success = remove_stock_item(item_name, 1)
        if not success:
            return

        add_items_to_inventory(str(user_id), [item_name])

        registrations = load_registrations()
        user_data = registrations.get(str(user_id), {})
        
                                                     
        if not user_data:
            return
        
        roblox_avatar = self._get_registration_avatar_url(user_id)
        roblox_username = self._get_registration_username(user_id)

        embed = discord.Embed(
            title="Bloxloot Tag Reward",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        if roblox_avatar:
            embed.set_thumbnail(url=roblox_avatar)

        item_value = get_item_value(item_name)
        item_emoji = get_item_emoji(item_name)
        items_text = f"• {item_emoji} `{item_name}` x1"
        if item_value:
            items_text += f" ({VALUE_EMOJI} {format_value_with_commas(item_value)} each)"
        
        next_reward_time = datetime.now() + timedelta(hours=24)
        next_reward_timestamp = int(next_reward_time.timestamp())
        next_reward_str = f"<t:{next_reward_timestamp}:R>"
        
        embed.add_field(name="Tag Member", value=f"<@{user_id}>", inline=True)
        embed.add_field(name="Next Reward In", value=next_reward_str, inline=True)
        embed.add_field(name="Items Rewarded", value=items_text, inline=False)
        embed.set_footer(text="Bloxloot Rewards • Do not remove the tag to continue receiving rewards!")

        event_channel = self.get_channel(TAG_EVENT_CHANNEL_ID)
        if event_channel:
            try:
                await event_channel.send(embed=embed)
            except Exception as e:
                print(f"Failed to send tag reward embed: {e}")

    async def _post_tag_event_embed(self, subject: str, event_type: str, user_id: Optional[int], user: Optional[discord.User]):
        title = "Bloxloot Tag Adopted" if event_type == "adopted" else "Bloxloot Tag Removed"
        color = discord.Color.green() if event_type == "adopted" else discord.Color.red()
        reward_time = datetime.now() + timedelta(hours=24)
        reward_timestamp = int(reward_time.timestamp())
        reward_value = f"<t:{reward_timestamp}:R>"

                                                       
        registrations = load_registrations()
        
        if user_id is not None:
            user_data = registrations.get(str(user_id), {})
            if not user_data:
                                                       
                return
            resolved_user_id = user_id
        else:
                                          
            matched_id = self._find_registration_user_id_by_username(subject)
            if matched_id is None:
                                                                   
                return
            resolved_user_id = matched_id

        embed = discord.Embed(
            title=title,
            color=color,
            timestamp=reward_time
        )

        stock_items = load_stock()
        available_rewards_text = "No rewards available"
        if stock_items:
            adm_items = [entry for entry in stock_items if get_item_type(entry["name"]) == GameType.ADM]
            mm2_items = [entry for entry in stock_items if get_item_type(entry["name"]) == GameType.MM2]
            reward_options = []
            if adm_items:
                reward_options.append(random.choice(adm_items))
            if mm2_items:
                reward_options.append(random.choice(mm2_items))
            if not reward_options:
                reward_options = random.sample(stock_items, min(2, len(stock_items)))

            available_rewards_text = ""
            for item in reward_options[:2]:
                item_name = item.get("name")
                if not item_name:
                    continue
                item_value = get_item_value(item_name)
                item_emoji = get_item_emoji(item_name)
                available_rewards_text += f"• {item_emoji} `{item_name}` x1"
                if item_value:
                    available_rewards_text += f" ({VALUE_EMOJI} {format_value_with_commas(item_value)} each)"
                available_rewards_text += "\n"
            available_rewards_text = available_rewards_text.strip() or "No rewards available"

        roblox_avatar = self._get_registration_avatar_url(resolved_user_id)
        if roblox_avatar:
            embed.set_thumbnail(url=roblox_avatar)
        elif user is not None:
            embed.set_thumbnail(url=user.display_avatar.url)

        member_display = user.mention if user is not None else f"<@{resolved_user_id}>"
        embed.add_field(name="Tag Member", value=member_display, inline=True)
        embed.add_field(name="Reward In", value=reward_value, inline=True)
        embed.set_footer(text="Bloxloot Rewards • Do not remove the tag to receive your reward")

        embed.add_field(name="Possible Rewards", value=available_rewards_text, inline=False)

        event_channel = self.get_channel(TAG_EVENT_CHANNEL_ID)
        if event_channel:
            try:
                await event_channel.send(embed=embed)
            except Exception as e:
                print(f"Failed to send tag event embed: {e}")

    async def _process_invite_message(self, message: discord.Message):
        """Process invite log messages and grant rewards."""
        content = message.content.strip()
        if not content:
            return

                                                                                
        invite_match = re.search(
            r"(?P<invited>.+?)\s+has been invited by\s+(?P<inviter>.+?)\s+and has now\s+(?P<count>\d+)\s+invites",
            content,
            re.IGNORECASE
        )
        
        if not invite_match:
            return

        invited_text = invite_match.group("invited").strip()
        inviter_text = invite_match.group("inviter").strip()

                          
        invited_user = await self._resolve_user_from_text(message, invited_text)
        inviter_user = await self._resolve_user_from_text(message, inviter_text)

        if not inviter_user or not invited_user:
            return

        state = load_invite_reward_state()
        
                                                                           
        if "rewarded_pairs" not in state:
            state["rewarded_pairs"] = []

        pair_key = f"{inviter_user.id}:{invited_user.id}"
        
                                                      
        if pair_key in state["rewarded_pairs"]:
            return

                                        
        await self._grant_invite_reward(inviter_user.id, invited_user, inviter_user)
        
                                    
        state["rewarded_pairs"].append(pair_key)
        save_invite_reward_state(state)

    async def _resolve_user_from_text(self, message: discord.Message, user_text: str) -> Optional[discord.User]:
        """Resolve a user from text that may contain mentions or usernames."""
        user_text = user_text.strip()
        
                                 
        user_text = re.sub(r'[\U0001F300-\U0001F9FF]+', '', user_text).strip()
        
                                     
        mention_match = re.search(r"<@!?(?P<id>\d+)>", user_text)
        if mention_match:
            try:
                return await self.fetch_user(int(mention_match.group("id")))
            except Exception:
                pass

                              
        if message.mentions:
            for mention in message.mentions:
                if mention.name.lower() in user_text.lower() or mention.display_name.lower() in user_text.lower():
                    return mention

                                       
        if message.guild:
            normalized_text = user_text.lower().strip()
            for member in message.guild.members:
                if member.name.lower() == normalized_text or member.display_name.lower() == normalized_text:
                    return member
                           
            for member in message.guild.members:
                if normalized_text in member.name.lower() or normalized_text in member.display_name.lower():
                    return member

        return None

    async def _grant_invite_reward(self, inviter_id: int, invited_user: Optional[discord.User], inviter_user: discord.User):
        """Grant a random stock item reward to an inviter."""
        stock_item = select_random_stock_item()
        if not stock_item:
            return

        item_name = stock_item.get("name")
        if not item_name:
            return

        success = remove_stock_item(item_name, 1)
        if not success:
            return

        add_items_to_inventory(str(inviter_id), [item_name])

                                                        
        registrations = load_registrations()
        inviter_data = registrations.get(str(inviter_id), {})
        if not inviter_data:
            return

                                     
        roblox_avatar = self._get_registration_avatar_url(inviter_id)

        embed = discord.Embed(
            title="Bloxloot Invite Reward",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        
        if roblox_avatar:
            embed.set_thumbnail(url=roblox_avatar)

        item_value = get_item_value(item_name)
        item_emoji = get_item_emoji(item_name)
        item_text = f"• {item_emoji} `{item_name}` x1"
        if item_value:
            item_text += f" ({VALUE_EMOJI} {format_value_with_commas(item_value)} each)"

        invited_mention = invited_user.mention if invited_user else "Unknown User"
        
        embed.add_field(name="Inviter", value=f"<@{inviter_id}>", inline=True)
        embed.add_field(name="Invited", value=invited_mention, inline=True)
        embed.add_field(name="Item Rewarded", value=item_text, inline=False)
        embed.set_footer(text="Bloxloot Rewards • Invite members using your link to receive rewards")

        event_channel = self.get_channel(INVITE_EVENT_CHANNEL_ID)
        if event_channel:
            try:
                await event_channel.send(embed=embed)
            except Exception as e:
                print(f"Failed to send invite reward embed: {e}")

    async def post_crypto_deposit_panel(self):
        await self.wait_until_ready()
        if getattr(self, "crypto_panel_sent", False):
            return

        deposit_channel = self.get_channel(DEPOSIT_CHANNEL_ID)
        if not deposit_channel:
            print(f"Deposit channel {DEPOSIT_CHANNEL_ID} not found.")
            return

        embed = discord.Embed(
            title="Bloxloot Deposits",
            color=0x2ecc71,
            timestamp=datetime.now()
        )
        servers_text = "\n".join(
            format_deposit_server(server)
            for server in MM2_DEPOSIT_SERVERS
        )
        servers_textadm = "\n".join(
            format_deposit_server(server)
            for server in ADM_DEPOSIT_SERVERS
        )

        embed.add_field(
            name="Deposit MM2",
            value=servers_text or "No private servers configured.",
            inline=True
        )

        embed.add_field(
            name="Deposit ADM",
            value=servers_textadm or "No private servers configured.",
            inline=True
        )

        embed.add_field(
            name="Deposit Crypto",
            value="\n".join([
            f"{CRYPTO_CURRENCIES[name]['emoji']} **{name}** ({CRYPTO_CURRENCIES[name]['code']})"
            for name in CRYPTO_CURRENCIES.keys()]),
            inline=False
        )
        
        embed.set_footer(text="Please validate the usernames of our bots before trading them.")

        try:
                                                                                            
                panel_data = load_deposit_panel()
                panel_message_id = panel_data.get("message_id")
                if panel_message_id:
                    try:
                        message = await deposit_channel.fetch_message(panel_message_id)
                        await message.edit(embed=embed, view=DepositCryptoSelectView(owner_id=None, timeout=None))
                        self.crypto_panel_sent = True
                    except Exception:
                                                         
                        message = await deposit_channel.send(embed=embed, view=DepositCryptoSelectView(owner_id=None, timeout=None))
                        save_deposit_panel({"message_id": message.id})
                        self.crypto_panel_sent = True
                else:
                    message = await deposit_channel.send(embed=embed, view=DepositCryptoSelectView(owner_id=None, timeout=None))
                    save_deposit_panel({"message_id": message.id})
                    self.crypto_panel_sent = True
        except Exception as e:
            print(f"Error posting crypto deposit panel: {e}")

    async def post_crypto_withdrawal_panel(self):
        await self.wait_until_ready()
        if getattr(self, "withdraw_panel_sent", False):
            return

        withdraw_channel = self.get_channel(WITHDRAW_CHANNEL_ID)
        if not withdraw_channel:
            print(f"Withdraw channel {WITHDRAW_CHANNEL_ID} not found.")
            return

        embed = discord.Embed(
            title="Bloxloot Withdrawals",
            color=0x2ecc71,
            timestamp=datetime.now()
        )
        servers_text = "\n".join(
            format_deposit_server(server)
            for server in MM2_DEPOSIT_SERVERS
        )
        servers_textadm = "\n".join(
            format_deposit_server(server)
            for server in ADM_DEPOSIT_SERVERS
        )

        embed.add_field(
            name="Withdraw MM2",
            value=servers_text or "No private servers configured.",
            inline=True
        )
        embed.add_field(
            name="Withdraw ADM",
            value=servers_textadm or "No private servers configured.",
            inline=True
        )
        embed.add_field(
            name="Withdraw Crypto",
            value="\n".join([
                f"{CRYPTO_CURRENCIES[name]['emoji']} **{name}** ({CRYPTO_CURRENCIES[name]['code']})"
                for name in CRYPTO_CURRENCIES.keys()]),
            inline=False
        )

        embed.set_footer(text="Please validate the usernames of our bots before trading them.")

        try:
            panel_data = load_withdraw_panel()
            panel_message_id = panel_data.get("message_id")
            if panel_message_id:
                try:
                    message = await withdraw_channel.fetch_message(panel_message_id)
                    await message.edit(embed=embed, view=CryptoWithdrawSelectView(owner_id=None, timeout=None))
                    self.withdraw_panel_sent = True
                except Exception:
                    message = await withdraw_channel.send(embed=embed, view=CryptoWithdrawSelectView(owner_id=None, timeout=None))
                    save_withdraw_panel({"message_id": message.id})
                    self.withdraw_panel_sent = True
            else:
                message = await withdraw_channel.send(embed=embed, view=CryptoWithdrawSelectView(owner_id=None, timeout=None))
                save_withdraw_panel({"message_id": message.id})
                self.withdraw_panel_sent = True
        except Exception as e:
            print(f"Error posting crypto withdrawal panel: {e}")
    
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        print(f'Bot is in {len(self.guilds)} guilds')

        await self.update_presence()
        
                                       
        print("[STARTUP] Initializing crypto price cache...")
        await update_price_cache()
        
                                                   
        if not os.path.exists(ITEMS_FILE):
                                 
            default_items = {
                "NightStar": {"value": 11000, "emoji": "<:Nightstar:1468422697280213213>", "type": GameType.MM2},
                "Travelers Axe": {"value": 8400, "emoji": "<:TravelersAxe:1528632154152767529>", "type": GameType.MM2},
                "Gingerscope": {"value": 16500, "emoji": "<:Gingerscope:1528632145185214484>", "type": GameType.MM2},
                "Celestial": {"value": 16500, "emoji": "<:Celestial:1528632057516003369>", "type": GameType.MM2},
                "Harvester": {"value": 425, "emoji": "<:Harvester:1528632092806611108>", "type": GameType.MM2},
                "Icepiercer": {"value": 325, "emoji": "<:Icepiercer:1468538995137970229>", "type": GameType.MM2},
                "Batwing": {"value": 57, "emoji": "<:Batwing:1528632084099239967>", "type": GameType.MM2},
                "Darkshot": {"value": 1060, "emoji": "<:Darkshot:1528632039958646865>", "type": GameType.MM2},
                "Darksword": {"value": 1040, "emoji": "<:Darksword:1528632031527960646>", "type": GameType.MM2},
                "Heartblade": {"value": 115, "emoji": "<:HeartBlade:1468582185685483709>", "type": GameType.MM2},
                "Australis": {"value": 100, "emoji": "<:Australis:1528632754177052673>", "type": GameType.MM2},
                "Icebreaker": {"value": 115, "emoji": "<:icebreaker:1468539005971988604>", "type": GameType.MM2},
                "Logchopper": {"value": 20, "emoji": "<:Logchopper:1528632075513495612>", "type": GameType.MM2},
                "Swirly Axe": {"value": 55, "emoji": "<:SwirlyAxe:1528632101597872289>", "type": GameType.MM2},
                "Vampires Axe": {"value": 825, "emoji": "<:VampiresAxe:1528632127602561107>", "type": GameType.MM2},
                "Icewing": {"value": 12, "emoji": "<:Icewing:1528632136788082838>", "type": GameType.MM2},
                "Blue Seer": {"value": 3, "emoji": "<:BlueSeer:1528633478814371911>", "type": GameType.MM2},
                "Purple Seer": {"value": 3, "emoji": "<:PurpleSeer:1528633487827927111>", "type": GameType.MM2},
                "Red Seer": {"value": 3, "emoji": "<:RedSeer:1528633496933896332>", "type": GameType.MM2},
                "Seer": {"value": 3, "emoji": "<:Seer:1528633505750323210>", "type": GameType.MM2},
                "Orange Seer": {"value": 2, "emoji": "<:OrangeSeer:1528633515539824690>", "type": GameType.MM2},
                "Yellow Seer": {"value": 2, "emoji": "<:YellowSeer:1528633523593019484>", "type": GameType.MM2},
            }
            save_json(ITEMS_FILE, default_items)
            print("Created default items.json with MM2 items")
        
        if not os.path.exists(INVENTORY_FILE):
            save_json(INVENTORY_FILE, {})
            print("Created empty inventory.json")
        
        if not os.path.exists(REGISTRATIONS_FILE):
            save_json(REGISTRATIONS_FILE, {})
            print("Created empty registrations.json")
        
        if not os.path.exists(MINES_GAMES_FILE):
            save_json(MINES_GAMES_FILE, {})
            print("Created empty active_mines_games.json")

        if not os.path.exists(BLACKJACK_GAMES_FILE):
            save_json(BLACKJACK_GAMES_FILE, {})
            print("Created empty active_blackjack_games.json")
            
        if not os.path.exists(LISTINGS_FILE):
            save_json(LISTINGS_FILE, {})
            print("Created empty active_listings.json")
        
        if not os.path.exists(WITHDRAWALS_FILE):
            save_json(WITHDRAWALS_FILE, {})
            print("Created empty active_withdrawals.json")
        
        if not os.path.exists(TAX_ITEMS_FILE):
            save_json(TAX_ITEMS_FILE, [])
            print("Created empty taxed_items.json")

        if not os.path.exists(BALANCES_FILE):
            save_json(BALANCES_FILE, {})
            print("Created empty balances.json")

        if not os.path.exists(CRYPTO_DEPOSITS_FILE):
            save_json(CRYPTO_DEPOSITS_FILE, {})
            print("Created empty crypto_deposits.json")

        if not os.path.exists(TAG_REWARD_STATE_FILE):
            save_json(TAG_REWARD_STATE_FILE, {"users": {}})
            print("Created empty tag_reward_state.json")
        
                                
        self.loop.create_task(self.setup_trade_monitoring())
                                      
        self.loop.create_task(self.background_check_crypto_deposits())
                                                                          
        try:
            jackpots = load_jackpot_games()
            for jp_id, jp in jackpots.items():
                if jp.get('status') == 'open':
                    try:
                        self.loop.create_task(_run_jackpot_countdown(jp_id))
                        print(f"Resuming jackpot countdown for {jp_id}")
                    except Exception:
                        print(f"Failed to resume jackpot countdown for {jp_id}")
        except Exception as e:
            print(f"Error resuming jackpots on startup: {e}")

                                                        
        try:
            self.loop.create_task(create_and_post_jackpot(self))
        except Exception:
            pass

                                                      
        try:
            self.loop.create_task(self.post_crypto_deposit_panel())
            self.loop.create_task(self.post_crypto_withdrawal_panel())
            self.loop.create_task(self.post_rules_panel())
        except Exception as e:
            print(f"Failed to post crypto deposit, withdrawal, or rules panel: {e}")

                            
        try:
            await create_admin_panel()
        except Exception as e:
            print(f"Failed to create admin panel: {e}")

                          
        try:
            await create_tax_panel()
        except Exception as e:
            print(f"Failed to create tax panel: {e}")

                            
        try:
            await create_event_panel()
        except Exception as e:
            print(f"Failed to create event panel: {e}")

                            
        try:
            await create_verification_panel()
        except Exception as e:
            print(f"Failed to create verification panel: {e}")

                                                                   
        try:
            await ensure_race_category_position(self)
        except Exception as e:
            print(f"Failed to position race category: {e}")

                                                           
        try:
            self.loop.create_task(self.admin_panel_status_loop())
        except Exception as e:
            print(f"Failed to start admin panel status loop: {e}")

    async def post_rules_panel(self):
        await self.wait_until_ready()
        if not RULES_CHANNEL_ID:
            print("RULES_CHANNEL_ID is not configured.")
            return

        channel = self.get_channel(RULES_CHANNEL_ID)
        if not channel:
            print(f"Rules channel {RULES_CHANNEL_ID} not found!")
            return

        rules_text = "\n".join([
            "**1.** Must be at least 13 years of age to use Bloxloot.",
            "**2.** No manipulating bot commands or webhooks.",
            "**3.** No scamming, exploiting, impersonating.",
            "**4.** Use common sense and respect at all times.",
            "**5.** Keep language and behavior clean in channels.",
            "**6.** No invite links, spam, DM advertising.",
            "**7.** Follow Discord's TOS and Guidelines.",
            "**8.** No sharing bot usernames or private servers.",
            "**9.** Bloxloot Staff may modify rules at times without notice.",
            "**10.** Items have no real-world value and are for entertainment only.",
        ])

        description = (
            "We encourage all Looters to read the rules fully before wagering.\n\n"
            f"{rules_text}\n\n"
            "Please take time to read the Terms of Service in full to understand your responsibilities, our policies, and how we keep Looters safe."
        )

        embed = discord.Embed(
            title="Bloxloot Rules & TOS",
            description=description,
            color=discord.Color.green()
        )
        if RULES_IMAGE_URL:
            embed.set_image(url=RULES_IMAGE_URL)

        embed.set_footer(text="Powered by Bloxloot  •  All violations can result in action from Bloxloot Staff.")

        panel_data = load_rules_panel()
        panel_message_id = panel_data.get("message_id")

        if panel_message_id:
            try:
                message = await channel.fetch_message(panel_message_id)
                await message.edit(embed=embed)
                print("Rules panel updated successfully")
                return
            except Exception as e:
                print(f"Failed to update existing rules panel: {e}")

        try:
            message = await channel.send(embed=embed)
            save_rules_panel({"message_id": message.id})
            print("Rules panel created successfully")
        except Exception as e:
            print(f"Failed to send rules panel: {e}")

    async def fetch_oxa_merchant_transactions(self):
        if not OXA_MERCHANT_API_KEY or not OXA_MERCHANT_ID:
            return []

        url = "https://api.oxapay.com/v1/merchant/transactions"
        headers = get_oxa_headers()

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params={"merchant_id": OXA_MERCHANT_ID}, timeout=20) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data if isinstance(data, list) else data.get("data", [])
        except Exception as e:
            print(f"Error fetching Oxa Pay transactions: {e}")
        return []

    async def background_check_crypto_deposits(self):
        await self.wait_until_ready()
        while not self.is_closed():
            try:
                deposits = load_crypto_deposits()
                pending = [d for d in deposits.values() if d.get("status") == "pending"]
                if pending:
                    transactions = await self.fetch_oxa_merchant_transactions()
                    for deposit in pending:
                        if not deposit:
                            continue
                        deposit_id = deposit["deposit_id"]
                        address = deposit["address"]
                        user_id = deposit["user_id"]
                        usd_amount = float(deposit["usd_amount"])
                        channel_id = deposit.get("channel_id")
                        message_id = deposit.get("message_id")
                        matched_tx = None

                        for tx in transactions:
                            tx_id = str(tx.get("id") or tx.get("transaction_id") or "")
                            metadata = tx.get("metadata") or {}
                            destination = str(tx.get("destination_address") or tx.get("address") or "")
                            status = str(tx.get("status") or "").lower()

                            if deposit_id == str(metadata.get("deposit_id")) or address == destination:
                                matched_tx = tx
                                if status in ("completed", "confirmed", "settled", "success"):
                                    break

                        if matched_tx:
                            status = str(matched_tx.get("status") or "").lower()
                            if status in ("completed", "confirmed", "settled", "success"):
                                update_crypto_deposit_status(deposit_id, "success")
                                add_user_balance(user_id, usd_amount)

                                try:
                                    channel = self.get_channel(channel_id)
                                    if channel and message_id:
                                        message = await channel.fetch_message(message_id)
                                        embed = discord.Embed(
                                            title="Deposit Success",
                                            color=discord.Color.green(),
                                            description=f"Your deposit of **${usd_amount:.2f} USD** has been confirmed.",
                                            timestamp=datetime.now()
                                        )
                                        embed.add_field(name="Currency", value=f"{get_crypto_currency_label(deposit['currency'])}", inline=True)
                                        embed.add_field(name="Received", value=f"**${usd_amount:.2f} USD** added to your inventory!", inline=True)
                                        embed.set_footer(text="Deposit Confirmed - use /inventory to see your balance!")
                                        await message.edit(embed=embed, view=None)
                                except Exception as e:
                                    print(f"Error updating deposit success embed: {e}")
                await asyncio.sleep(30)
            except Exception as e:
                print(f"Error checking crypto deposits: {e}")
                await asyncio.sleep(30)

    async def setup_trade_monitoring(self):
        """Setup trade monitoring by finding the MM2 trade webhook and channel."""
        await self.wait_until_ready()
        
        print("Setting up trade monitoring...")
        
                                    
        await self.setup_mm2_trade_monitoring()
                                    
        await self.setup_adm_trade_monitoring()
        
                          
        self.loop.create_task(self.monitor_mm2_trades())
        self.loop.create_task(self.monitor_adm_trades())

    
    async def setup_mm2_trade_monitoring(self):
        """Setup MM2 trade monitoring"""
        print("Setting up MM2 trade monitoring...")
        found_webhook = False
        for guild in self.guilds:
                                         
            try:
                webhooks = await guild.webhooks()
                for webhook in webhooks:
                    if webhook.name == MM2_WEBHOOK_USERNAME:
                        self.trade_webhook_id = webhook.id
                        self.trade_channel = webhook.channel
                        print(f"Found MM2 trade webhook: {webhook.name} (ID: {webhook.id}) in channel: {webhook.channel.name}")
                        found_webhook = True
                        break
            except discord.Forbidden:
                print(f"No permission to view webhooks in {guild.name}")
                continue

            if found_webhook:
                                                                       
                try:
                    if self.trade_channel and not self.last_processed_trade_id:
                        async for msg in self.trade_channel.history(limit=1):
                            self.last_processed_trade_id = msg.id
                            print(f"Set last_processed_trade_id to {self.last_processed_trade_id} (latest message on startup)")
                            break
                except Exception:
                    pass
                break

        if not found_webhook:
            print(f"WARNING: Could not find webhook with username '{MM2_WEBHOOK_USERNAME}'")
            print("Falling back to channel scanning for MM2...")

                                                
            for guild in self.guilds:
                for channel in guild.text_channels:
                    if channel.name.lower() in ['trades', 'trade-log', 'deposits', 'trade-monitor']:
                        self.trade_channel = channel
                        print(f"Found potential MM2 trade channel: {channel.name}")
                        break

                                                                                                       
        try:
            if self.trade_channel and not self.last_processed_trade_id:
                async for msg in self.trade_channel.history(limit=1):
                    self.last_processed_trade_id = msg.id
                    print(f"Set last_processed_trade_id to {self.last_processed_trade_id} (latest message on startup)")
                    break
        except Exception:
            pass
    async def setup_adm_trade_monitoring(self):
        """Setup ADM trade monitoring"""
        print("Setting up ADM trade monitoring...")
        found_webhook = False
        for guild in self.guilds:
            try:
                webhooks = await guild.webhooks()
                for webhook in webhooks:
                    if webhook.name == ADM_WEBHOOK_USERNAME:
                        self.adm_webhook_id = webhook.id
                        self.adm_channel = webhook.channel
                        print(f"Found ADM webhook: {webhook.name} (ID: {webhook.id}) in channel: {webhook.channel.name}")
                        found_webhook = True
                        break
            except discord.Forbidden:
                continue

            if found_webhook:
                                                                           
                try:
                    if self.adm_channel and not self.last_processed_adm_id:
                        async for msg in self.adm_channel.history(limit=1):
                            self.last_processed_adm_id = msg.id
                            print(f"Set last_processed_adm_id to {self.last_processed_adm_id} (latest message on startup)")
                            break
                except Exception:
                    pass
                break

        if not found_webhook:
            print(f"WARNING: Could not find webhook with username '{ADM_WEBHOOK_USERNAME}'")
                                                   
            for guild in self.guilds:
                for channel in guild.text_channels:
                    if channel.id == ADM_TRADE_MONITOR_CHANNEL_ID:
                        self.adm_channel = channel
                        print(f"Using configured ADM channel: {channel.name}")
                                                                                                        
                        try:
                            async for msg in channel.history(limit=1):
                                self.last_processed_adm_id = msg.id
                                print(f"Set last_processed_adm_id to {self.last_processed_adm_id} (latest message on startup)")
                                break
                        except Exception:
                            pass
                        return
            print("Falling back to channel scanning for ADM...")
            for guild in self.guilds:
                for channel in guild.text_channels:
                    if channel.name.lower() in ['adoptme', 'adm', 'deposits', 'trade-log']:
                        self.adm_channel = channel
                        print(f"Found potential ADM channel: {channel.name}")
                        try:
                            async for msg in channel.history(limit=1):
                                self.last_processed_adm_id = msg.id
                                print(f"Set last_processed_adm_id to {self.last_processed_adm_id} (latest message on startup)")
                                break
                        except Exception:
                            pass
                        return
    async def monitor_mm2_trades(self):
        """Monitor MM2 trades from webhook or channel"""
        await self.wait_until_ready()
        
        if not self.trade_channel:
            print("ERROR: No MM2 trade channel found! Please set MM2_TRADE_MONITOR_CHANNEL_ID or ensure webhook exists.")
            return
        
        print(f"Monitoring MM2 trades in channel: {self.trade_channel.name}")
        
        while not self.is_closed():
            try:
                                                     
                messages_found = False
                async for message in self.trade_channel.history(limit=50):
                                                                               
                    if self.last_processed_trade_id and message.id <= self.last_processed_trade_id:
                        continue

                                                                                
                    if (message.webhook_id == self.trade_webhook_id or 
                        (message.embeds and MM2_TRADE_MONITOR_CHANNEL_ID is None)):
                                                   
                        await self.process_trade_message(message, GameType.MM2)
                                                      
                        self.last_processed_trade_id = message.id
                        messages_found = True
                
                if messages_found:
                    print(f"Processed new MM2 trade messages")
                
                                            
                await asyncio.sleep(10)                          
                
            except discord.Forbidden:
                print(f"ERROR: No permission to read channel {self.trade_channel.name}")
                await asyncio.sleep(60)                                   
            except Exception as e:
                print(f"Error in MM2 trade monitoring: {e}")
                import traceback
                traceback.print_exc()
                await asyncio.sleep(30)                        
    async def monitor_adm_trades(self):
        """Monitor ADM deposits from webhook or channel"""
        await self.wait_until_ready()

        if not self.adm_channel:
            print("ERROR: No ADM channel found! Please set ADM_TRADE_MONITOR_CHANNEL_ID or ensure webhook exists.")
            return

        print(f"Monitoring ADM deposits in channel: {self.adm_channel.name}")

        while not self.is_closed():
            try:
                messages_found = False
                async for message in self.adm_channel.history(limit=50):
                    if self.last_processed_adm_id and message.id <= self.last_processed_adm_id:
                        continue

                    if (message.webhook_id == self.adm_webhook_id or (message.embeds and ADM_TRADE_MONITOR_CHANNEL_ID is None)):
                        await self.process_trade_message(message, GameType.ADM)
                        self.last_processed_adm_id = message.id
                        messages_found = True

                if messages_found:
                    print(f"Processed new ADM deposit messages")

                await asyncio.sleep(10)

            except discord.Forbidden:
                print(f"ERROR: No permission to read channel {self.adm_channel.name}")
                await asyncio.sleep(60)
            except Exception as e:
                print(f"Error in ADM trade monitoring: {e}")
                import traceback
                traceback.print_exc()
                await asyncio.sleep(30)
    async def process_trade_message(self, message: discord.Message, game_type: str):
        """Process a trade completion message from webhook or embed"""
        try:
            print(f"Processing {game_type} trade message {message.id} from {message.author}")
            
                                                
                                                                                        
            content_to_check = message.content or ''
            if message.embeds:
                emb = message.embeds[0]
                if emb.title:
                    content_to_check += '\n' + emb.title
                if emb.description:
                    content_to_check += '\n' + emb.description
                for f in emb.fields:
                    if f.name:
                        content_to_check += '\n' + str(f.name)
                    if f.value:
                        content_to_check += '\n' + str(f.value)

                                                    
            if re.search(r'\bended\b', content_to_check, re.IGNORECASE) or re.search(r'status\s*[:\-]?\s*ended', content_to_check, re.IGNORECASE):
                print(f"Skipping message {message.id} because it indicates trade ENDED")
                return

            if message.embeds:
                embed = message.embeds[0]
                await self.process_trade_embed(embed, message, game_type)
            else:
                                             
                await self.process_trade_text(message.content, message, game_type)
                
        except Exception as e:
            print(f"Error processing trade message {message.id}: {e}")
            import traceback
            traceback.print_exc()
    
    async def process_trade_embed(self, embed: discord.Embed, message: discord.Message, game_type: str):
        """Process trade data from an embed"""
                                                                 
        username = None
        items = {}
        footer_bot_username = None
        if embed.footer and embed.footer.text:
            footer_bot_username = match_deposit_server_username(embed.footer.text, game_type)

        if game_type == GameType.ADM:
                                                                                          
            if embed.title:
                username = self.extract_username_from_text(embed.title)
            if not username and embed.description:
                username = self.extract_username_from_text(embed.description)

            for field in embed.fields:
                                 
                if field.name and 'partner' in field.name.lower() and field.value:
                    maybe = self.extract_username_from_text(field.value)
                    if maybe:
                        username = maybe
                        break
                                                                 
                if field.value and 'partner:' in field.value.lower():
                    maybe = self.extract_username_from_text(field.value)
                    if maybe:
                        username = maybe
                        break

                                                                              
            for field in embed.fields:
                if field.name and 'partner gave' in field.name.lower():
                                                                                      
                    raw = field.value or ''
                    parts = re.split(r'[\n,;]+', raw)
                    for part in parts:
                        part = part.strip()
                        if not part:
                            continue
                                                                                         
                        base = re.sub(r'\s*\([^\)]*\)', '', part).strip()
                        base_clean = self.clean_item_name(base)
                        resolved = self.resolve_adm_item_name(part, base_clean)
                        key = resolved if resolved else base_clean
                        if key:
                            items[key] = items.get(key, 0) + 1
                    break

                                                                                         
            if not items and embed.description:
                                                                                        
                desc_text = re.sub(r'\*\*', '', embed.description)
                lines = [ln.strip() for ln in re.split(r'\r?\n', desc_text) if ln.strip()]
                partner_idx = None
                for idx, ln in enumerate(lines):
                    if re.search(r'partner\s+gave', ln, re.IGNORECASE):
                        partner_idx = idx
                        break

                if partner_idx is not None:
                    for ln in lines[partner_idx+1:]:
                        low = ln.lower()
                                                                                            
                        if re.search(r'bot\s+gave', low) or re.search(r'^[A-Za-z ]+:$', ln) or re.search(r'\b(status|partner):', low):
                            break
                                                     
                        ln_numb = re.sub(r'^[\d\s\.\-•>*]+', '', ln).strip()
                        if not ln_numb:
                            continue
                        base = re.sub(r'\s*\([^\)]*\)', '', ln_numb).strip()
                        base_clean = self.clean_item_name(base)
                        resolved = self.resolve_adm_item_name(ln_numb, base_clean)
                        key = resolved if resolved else base_clean
                        if key:
                            items[key] = items.get(key, 0) + 1
                else:
                    m = re.search(r'Partner Gave\s*\(?\d*\)?:\s*(.*)', embed.description, re.IGNORECASE)
                    if m:
                        raw = m.group(1)
                        parts = re.split(r'[\n,;]+', raw)
                        for part in parts:
                            part = part.strip()
                            if not part:
                                continue
                            base = re.sub(r'\s*\([^\)]*\)', '', part).strip()
                            base_clean = self.clean_item_name(base)
                            resolved = self.resolve_adm_item_name(part, base_clean)
                            key = resolved if resolved else base_clean
                            if key:
                                items[key] = items.get(key, 0) + 1

            if items:
                print(f"Found {len(items)} ADM items in embed")
                if username:
                    await self.add_items_to_user(username, items, message, game_type, bot_username=footer_bot_username)
                else:
                    await self.send_trade_error(message, items, "Could not extract username from ADM embed.")
                return

                                                     
                                                     
        if embed.title:
            username = self.extract_username_from_text(embed.title)
        if not username and embed.description:
            username = self.extract_username_from_text(embed.description)
        if not username:
            for field in embed.fields:
                if field.name and "user" in field.name.lower():
                    username = self.extract_username_from_text(field.value)
                    break
                if field.value:
                    extracted = self.extract_username_from_text(field.value)
                    if extracted and (not username or len(extracted) > len(username)):
                        username = extracted
        if not username and embed.author and embed.author.name:
            username = self.extract_username_from_text(embed.author.name)

                                                         
        items_text = ""
        if embed.description:
            items_text += embed.description + "\n"
        for field in embed.fields:
            if field.name:
                items_text += field.name + ": "
            if field.value:
                items_text += field.value + "\n"

        items = self.parse_items_from_text(items_text)

        if not items and embed.fields:
            for field in embed.fields:
                if field.value and any(char.isdigit() for char in field.value):
                    field_items = self.parse_items_from_text(field.value)
                    if field_items:
                        items.update(field_items)

        if items:
            print(f"Found {len(items)} item types from {game_type} embed")
            if username:
                await self.add_items_to_user(username, items, message, game_type, bot_username=footer_bot_username)
            else:
                print(f"Could not extract username from {game_type} embed")
                await self.send_trade_error(message, items, f"Could not extract username from {game_type} trade embed.")
        else:
            print(f"No items found in {game_type} embed")
    
    async def process_trade_text(self, text: str, message: discord.Message, game_type: str):
        """Process trade data from plain text"""
        username = self.extract_username_from_text(text)
        items = self.parse_items_from_text(text)
        
        if items:
            print(f"Found {len(items)} item types from {game_type} text")
            if username:
                await self.add_items_to_user(username, items, message, game_type)
            else:
                print(f"Could not extract username from {game_type} text")
                await self.send_trade_error(message, items, f"Could not extract username from {game_type} trade message.")
        else:
            print(f"No items found in {game_type} text")
    
    def extract_username_from_text(self, text: str) -> Optional[str]:
        """Extract username from text using multiple patterns"""
        if not text:
            return None
                                                                                                 
        cleaned = re.sub(r'\*+|`+|~+', '', text)
                                           
        patterns = [
            r'Username:\s*([\w\-_]+)',                     
            r'Partner:\s*([\w\-_]+)',                             
            r'User:\s*([\w\-_]+)',                 
            r'([\w\-_]+)\s+has deposited',                         
            r'Deposit Completed\s*([\w\-_]+)',                        
            r'Player:\s*([\w\-_]+)',                   
            r'^([\w\-_]{3,20})$',                             
            r'Deposit from ([\w\-_]+)',                        
            r'([\w\-_]+) deposited',                     
        ]
        for pattern in patterns:
            match = re.search(pattern, cleaned, re.IGNORECASE)
            if match:
                username = match.group(1).strip()
                                                          
                if 3 <= len(username) <= 20 and re.match(r'^[\w\-_]+$', username):
                    return username
        
                                                            
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
                                                          
            if 3 <= len(line) <= 20 and re.match(r'^[\w\-_]+$', line) and not any(x in line.lower() for x in ['x', 'has', 'deposit', 'trade', 'completed']):
                return line
        
        return None
    
    def parse_items_from_text(self, text: str) -> Dict[str, int]:
        """Parse items from text using multiple patterns"""
        items = {}
        
        if not text:
            return items
        
                                                
        text = re.sub(r'[*_`~\\/|]', '', text)
        text = re.sub(r'<:[^>]+>|<@[^>]+>', '', text)

                                                                                                 
        lines = [ln for ln in re.split(r'\r?\n', text)]
        bot_idx = None
        for i, ln in enumerate(lines):
            if re.search(r'\b(bot\s+gave)\b', ln, re.IGNORECASE):
                bot_idx = i
                break
        if bot_idx is not None:
            text = '\n'.join(lines[:bot_idx])
        
                                                      
        patterns = [
                                                                 
            r'(\d+)\s*x\s*([^\n\r\d]+?)(?=\s*\d*\s*x|$|\.|,)',
                                                                 
            r'([^\n\r\d]+?)\s*x\s*(\d+)(?=\s*\d*\s*x|$|\.|,)',
                                          
            r'(\d+)\s+([^\n\r\d]+?)(?=\s*\d+\s+|$|\.|,)',
                                            
            r'([^\n\r\d]+?)\s*\((\d+)\)',
        ]
        
        all_matches = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            all_matches.extend(matches)
        
        for match in all_matches:
            if len(match) == 2:
                try:
                    if match[0].isdigit():
                        quantity = int(match[0])
                        raw_item_text = match[1].strip()
                    else:
                        quantity = int(match[1])
                        raw_item_text = match[0].strip()

                                                                 
                    base_name = self.clean_item_name(raw_item_text)
                    resolved_name = self.resolve_adm_item_name(raw_item_text, base_name)
                    if resolved_name and quantity > 0:
                        items[resolved_name] = items.get(resolved_name, 0) + quantity
                        print(f"Parsed item: {quantity}x {resolved_name}")
                    elif base_name and quantity > 0 and self.is_valid_item(base_name):
                        items[base_name] = items.get(base_name, 0) + quantity
                        print(f"Parsed item: {quantity}x {base_name}")
                except ValueError:
                    continue

                                                                                                                 
        if not items:
            lines = [ln.strip() for ln in text.split('\n') if ln.strip()]
            for ln in lines:
                                             
                if re.search(r'^(status:|partner:|bot:|today at)', ln, re.IGNORECASE):
                    continue
                                                             
                ln_clean = re.sub(r'^[\d\s\.\-•>*]+', '', ln)
                ln_clean = re.sub(r'\s*\([^\)]*\)', '', ln_clean).strip()
                if not ln_clean:
                    continue
                candidate = self.clean_item_name(ln_clean)
                resolved = self.resolve_adm_item_name(ln, candidate)
                if resolved:
                    items[resolved] = items.get(resolved, 0) + 1
                    print(f"Parsed (line) item: 1x {resolved}")
                elif candidate and self.is_valid_item(candidate):
                    items[candidate] = items.get(candidate, 0) + 1
                    print(f"Parsed (line) item: 1x {candidate}")
        
                                                 
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
                                                   
            if line.startswith(('•', '-', '*', '>')) or 'x' in line.lower():
                                     
                line = re.sub(r'^[•\-\*>]\s*', '', line)
                
                                                        
                if 'x' in line:
                                                                 
                    parts = re.split(r'\s+x\s+', line, flags=re.IGNORECASE)
                    if len(parts) == 2:
                        left = parts[0].strip()
                        right = parts[1].strip()
                        
                        try:
                                                     
                            if left.isdigit():
                                quantity = int(left)
                                raw_item = right
                                item_name = self.clean_item_name(right)
                            elif right.isdigit():
                                quantity = int(right)
                                raw_item = left
                                item_name = self.clean_item_name(left)
                            else:
                                                                 
                                num_match = re.search(r'(\d+)', left)
                                if num_match:
                                    quantity = int(num_match.group(1))
                                    raw_item = right
                                    item_name = self.clean_item_name(right)
                                else:
                                    continue

                                                  
                            resolved = self.resolve_adm_item_name(raw_item, item_name)
                            if resolved and quantity > 0:
                                items[resolved] = items.get(resolved, 0) + quantity
                            elif item_name and quantity > 0 and self.is_valid_item(item_name):
                                items[item_name] = items.get(item_name, 0) + quantity
                        except ValueError:
                            continue
        
                                                                                 
                                                                                 
                                  
        final_items = {}
        lines_all = [ln.strip() for ln in text.split('\n') if ln.strip()]
                                                                                 
                                                                  
        for base_name, total_qty in list(items.items()):
            matched_qty = 0
            base_lower = base_name.lower()
            for ln in lines_all:
                if re.search(rf'\b{re.escape(base_name)}\b', ln, re.IGNORECASE):
                                                                            
                    qty = None
                                                                                            
                    m = re.search(rf'(\d+)\s*x\s*.*\b{re.escape(base_name)}\b', ln, re.IGNORECASE)
                    if not m:
                                                                                          
                        m = re.search(rf'\b{re.escape(base_name)}\b\s*\(\s*(\d+)\s*\)\s*$', ln, re.IGNORECASE)
                    if m:
                        try:
                            qty = int(m.group(1))
                        except ValueError:
                            qty = 1
                    else:
                        qty = 1

                                                            
                    resolved = self.resolve_adm_item_name(ln, base_name)
                    key = resolved if resolved else base_name
                    final_items[key] = final_items.get(key, 0) + qty
                    matched_qty += qty

                                                                                            
            if matched_qty == 0:
                resolved = self.resolve_adm_item_name(text, base_name)
                key = resolved if resolved else base_name
                final_items[key] = final_items.get(key, 0) + total_qty

                                                                  
        if final_items:
            return final_items
        return items
    
    def clean_item_name(self, item_name: str) -> str:
        """Clean up item name by removing special characters and formatting"""
                                                                 
        item_name = re.sub(r'[*_`~\\/|]', '', item_name)
        
                                    
        item_name = re.sub(r'<:[^>]+>|<@[^>]+>', '', item_name)
        
                                                    
        item_name = re.sub(r'\s*\(\d+\)', '', item_name)
        
                                 
        item_name = ' '.join(item_name.split())
        
                                                                                  
        item_name = item_name.rstrip('.,;:!?')
        
                                                              
        item_name = ' '.join(word.capitalize() for word in item_name.split())
        
        return item_name.strip()
    
    def is_valid_item(self, item_name: str) -> bool:
        """Check if an item exists in items.json"""
        items = load_items()
                                 
        if item_name in items:
            return True
        
                                      
        for item in items.keys():
            if item.lower() == item_name.lower():
                return True
        
        return False
    
    def get_correct_item_name(self, item_name: str) -> Optional[str]:
        """Get the correct item name (case-sensitive) from items.json"""
        items = load_items()
                                 
        if item_name in items:
            return item_name
        
                                      
        for item in items.keys():
            if item.lower() == item_name.lower():
                return item
        
        return None

    def resolve_adm_item_name(self, raw_text: str, base_name: str) -> Optional[str]:
        """Resolve ADM pet variants by detecting words like MEGA/NEON/FLY/RIDE in raw_text
        and returning the correct item key from items.json (e.g., 'MFR California Condor').
        """
        items = load_items()
                                           
        flags = {
            'M': bool(re.search(r'\bmega\b', raw_text, re.IGNORECASE)),
            'N': bool(re.search(r'\bneon\b', raw_text, re.IGNORECASE)),
            'F': bool(re.search(r'\bfly\b', raw_text, re.IGNORECASE)),
            'R': bool(re.search(r'\bride\b', raw_text, re.IGNORECASE)),
        }

                                                                              
        if flags.get('M') and flags.get('N'):
            flags['N'] = False

                                          
        prefix = ''.join([k for k in ['M', 'N', 'F', 'R'] if flags.get(k)])

                                                               
        if prefix:
                                                         
            candidate = f"{prefix} {base_name}"
            correct = self.get_correct_item_name(candidate)
            if correct:
                return correct

                                                                                   
                                                             
            subs = []
            seq = [k for k in ['M', 'N', 'F', 'R'] if flags.get(k)]
            for i in range(len(seq), 0, -1):
                subs.append(''.join(seq[:i]))

            for p in subs:
                candidate = f"{p} {base_name}"
                correct = self.get_correct_item_name(candidate)
                if correct:
                    return correct

                                                        
            for k in ['M', 'N', 'F', 'R']:
                candidate = f"{k} {base_name}"
                correct = self.get_correct_item_name(candidate)
                if correct:
                    return correct

                                                       
        correct_base = self.get_correct_item_name(base_name)
        if correct_base:
            return correct_base

                                                 
        for k in ['M', 'N', 'F', 'R']:
            candidate = f"{base_name} {k}"
            correct = self.get_correct_item_name(candidate)
            if correct:
                return correct

        return None
    
    async def send_trade_error(self, message: discord.Message, items: Dict[str, int], error_msg: str):
        """Send error message for trade processing"""
        try:
            embed = discord.Embed(
                title="Trade Processing Failed",
                description=error_msg,
                color=discord.Color.red(),
                timestamp=datetime.now()
            )
            
            if items:
                items_list = "\n".join([f"• {quantity}x {item_name}" for item_name, quantity in items.items()])
                embed.add_field(
                    name="Items Detected",
                    value=items_list,
                    inline=False
                )
            
            embed.add_field(
                name="How to Fix",
                value="Make sure the trade message includes:\n1. A clear Roblox username\n2. Items in format like '13x Candy Swirl' or 'Candy Swirl x13'\n3. Username should be at the beginning or marked with 'Username:'",
                inline=False
            )
            
            await message.reply(embed=embed)
        except Exception as e:
            print(f"Error sending trade error: {e}")
    
    async def add_items_to_user(self, roblox_username: str, items: Dict[str, int], message: discord.Message, game_type: str, bot_username: Optional[str] = None):
        """Add items to user's inventory based on Roblox username"""
        try:
                                
            roblox_username = roblox_username.strip()
            
                                                          
            registrations = load_registrations()
            discord_user_id = None
            discord_user_data = None
            
            print(f"Looking for Roblox username in registrations: {roblox_username}")
            print(f"Total registrations: {len(registrations)}")
            
            for user_id_str, user_data in registrations.items():
                registered_name = user_data.get('roblox_username', '').strip()
                registered_display = user_data.get('roblox_display_name', '').strip()
                
                print(f"Checking: {registered_name} (username) and {registered_display} (display)")
                
                if registered_name.lower() == roblox_username.lower():
                    discord_user_id = int(user_id_str)
                    discord_user_data = user_data
                    print(f"Found match by username: {roblox_username} -> {discord_user_id}")
                    break
                elif registered_display.lower() == roblox_username.lower():
                    discord_user_id = int(user_id_str)
                    discord_user_data = user_data
                    print(f"Found match by display name: {roblox_username} -> {discord_user_id}")
                    break
            
            if not discord_user_id:
                print(f"No registered Discord user found for Roblox username: {roblox_username}")
                                                  
                await self.send_user_not_found_error(message, roblox_username, items)
                return
            
                                                                 
            
                                                                                     
            corrected_items = {}
            for item_name, quantity in items.items():
                correct_name = self.get_correct_item_name(item_name)
                                                                                
                if not correct_name and str(game_type).upper() == 'ADM':
                    resolved = self.resolve_adm_item_name(item_name, self.clean_item_name(item_name))
                    if resolved:
                        correct_name = resolved

                if correct_name:
                                                                           
                    item_type = get_item_type(correct_name)
                    if item_type == game_type:
                        corrected_items[correct_name] = corrected_items.get(correct_name, 0) + quantity
                    else:
                        print(f"Skipping item {correct_name} - expected {game_type} but got {item_type}")
                else:
                    print(f"Invalid item skipped: {item_name}")
            
            if not corrected_items:
                await self.send_trade_error(message, items, f"None of the detected items are valid {game_type} items in the system.")
                return
            
                                           
            items_to_add = []
            total_items_added = 0
            total_value_added = 0
            
            for item_name, quantity in corrected_items.items():
                for _ in range(quantity):
                    items_to_add.append(item_name)
                total_items_added += quantity
                item_value = get_item_value(item_name)
                total_value_added += item_value * quantity
            
                                   
            add_items_to_inventory(str(discord_user_id), items_to_add)
            
                                     
            discord_user = await self.fetch_user(discord_user_id)
            
                                  
            embed = discord.Embed(
                title="Trade Processed Successfully!",
                description=f"Items have been added to **{roblox_username}**'s inventory.",
                color=discord.Color.green(),
                timestamp=datetime.now()
            )
            
                                                   
            roblox_avatar = discord_user_data.get('roblox_avatar')
            if roblox_avatar:
                embed.set_thumbnail(url=roblox_avatar)
            
                                      
            embed.add_field(
                name="Discord User",
                value=f"{discord_user.mention}",
                inline=True
            )
            
                                 
            embed.add_field(
                name="Roblox Account",
                value=f"**{roblox_username}**",
                inline=True
            )
            
                                       
            embed.add_field(
                name="Total Value",
                value=f"{VALUE_EMOJI} **{format_value_with_commas(total_value_added)}**",
                inline=True
            )
            
                              
            items_list = ""
            for item_name, quantity in list(corrected_items.items())[:10]:                       
                item_value = get_item_value(item_name)
                item_emoji = get_item_emoji(item_name)
                items_list += f"{item_emoji} **{item_name}** x{quantity} ({VALUE_EMOJI} {format_value_with_commas(item_value)} each)\n"
            
            if len(corrected_items) > 10:
                items_list += f"\n*...and {len(corrected_items) - 10} more item types*"
            
            embed.add_field(
                name="Items Added",
                value=items_list or "No items",
                inline=False
            )
            
            embed.set_footer(text=f"Trade ID: {message.id} • Processed by Bloxloot")
            
                                        
            await message.reply(embed=embed)

                                                      
            processed_trades = load_processed_trades()
            if not any(isinstance(rec, dict) and rec.get("message_id") == message.id for rec in processed_trades):
                bot_name = normalize_bot_username(bot_username) or normalize_bot_username(message.author.name if getattr(message, 'author', None) else None)
                processed_trades.append({
                    "message_id": message.id,
                    "game_type": game_type,
                    "roblox_username": roblox_username,
                    "bot_username": bot_name,
                    "items": corrected_items,
                    "total_value": float(total_value_added),
                    "processed_at": datetime.now().isoformat()
                })
                save_processed_trades(processed_trades)
            
            print(f"Added {total_items_added} {game_type} items worth {VALUE_EMOJI} {format_value_with_commas(total_value_added)} to {roblox_username}'s inventory")
            
                                                         
                
        except Exception as e:
            print(f"Error adding items to user: {e}")
            import traceback
            traceback.print_exc()
            await self.send_trade_error(message, items, f"An error occurred: {str(e)}")
    
    async def send_user_not_found_error(self, message: discord.Message, roblox_username: str, items: Dict[str, int]):
        """Send error when user is not found"""
        embed = discord.Embed(
            title="Trade Processing Failed",
            description=f"User **{roblox_username}** is not registered with Bloxloot!",
            color=discord.Color.red(),
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="How to Register",
            value=f"**{roblox_username}** needs to:\n1. Use `/register` command\n2. Verify their Roblox account\n3. Then trade items will be added automatically",
            inline=False
        )
        
        if items:
            items_list = "\n".join([f"• {quantity}x {item_name}" for item_name, quantity in items.items()])
            embed.add_field(
                name="Items Not Added",
                value=items_list,
                inline=False
            )
        
        await message.reply(embed=embed)

                     
bot = BloxlootBot()


@bot.event
async def on_guild_channel_delete(channel: discord.abc.GuildChannel):
    if not isinstance(channel, discord.TextChannel):
        return

    active_race_channels = get_active_race_channels()
    if channel.id not in active_race_channels:
        return

    remove_active_race_channel(channel.id)
    await update_event_panel_embed()

    embed, _ = build_race_panel_embed()
    for view in list(ACTIVE_RACE_PANEL_VIEWS):
        if getattr(view, 'message', None) is None:
            ACTIVE_RACE_PANEL_VIEWS.remove(view)
            continue
        try:
            await view.message.edit(embed=embed, view=view)
        except Exception:
            try:
                ACTIVE_RACE_PANEL_VIEWS.remove(view)
            except ValueError:
                pass


async def staff_reset_loop():
    """Background task to reset staff uses daily at local midnight."""
    await bot.wait_until_ready()
    while True:
        now = datetime.now()
                             
        next_reset = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        delta = (next_reset - now).total_seconds()
        try:
            await asyncio.sleep(delta)
        except asyncio.CancelledError:
            return
        try:
            reset_staff_uses()
            await update_tax_panel_embed()
            print("Staff uses reset to 0 for the new day.")
        except Exception as e:
            print(f"Failed to reset staff uses: {e}")

                  
try:
    bot.loop.create_task(staff_reset_loop())
except Exception:
    pass

                                
@bot.tree.command(name="list", description="List items from your inventory!")
async def list_items(interaction: discord.Interaction):
    if not is_user_registered(interaction.user.id):
        await interaction.response.send_message(
            "You need to register first! Use `/register` to get started.",
            ephemeral=True
        )
        return
    
                      
    user_items = get_user_all_items(str(interaction.user.id))
    
    if not user_items:
        await interaction.response.send_message(
            "You don't have any items to list!",
            ephemeral=True
        )
        return
    
                                               
    listings = load_listings()
    active_listings = sum(1 for listing in listings.values() if listing['seller_id'] == interaction.user.id and listing['status'] == 'active')
    
    if active_listings >= 3:
        await interaction.response.send_message(
            "You can only have 3 active listings at a time! Please cancel some of your existing listings.",
            ephemeral=True
        )
        return
    
                              
    embed = discord.Embed(
        title="List Items for Sale",
        description="Select items from your inventory to list for sale in USD.",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="How It Works",
        value="1. Select items from your inventory\n2. Set a USD price\n3. Listing appears in marketplace\n4. Buyers purchase instantly using USD balance\n5. Items are removed while listed",
        inline=False
    )
    
    embed.add_field(
        name="Listing Rules",
        value="• Max 3 active listings per user!\n• Items are removed from inventory while listed.\n• Purchases are automated and instant using USD balance.\n• You can cancel listings anytime!",
        inline=False
    )
    
    view = ListingItemSelectionView(user_items)
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="withdraw", description="Withdraw items from your inventory!")
async def withdraw(interaction: discord.Interaction):
    if not is_user_registered(interaction.user.id):
        await interaction.response.send_message(
            "You need to register first! Use `/register` to get started.",
            ephemeral=True
        )
        return
    
                                            
    
                                                  
    withdrawals = load_withdrawals()
    pending = any(
        w['user_id'] == interaction.user.id and w['status'] == 'pending'
        for w in withdrawals.values()
    )
    
    if pending:
        await interaction.response.send_message(
            "You already have a pending withdrawal request! Please wait for it to be processed or cancel it.",
            ephemeral=True
        )
        return
    
                      
    user_items = get_user_all_items(str(interaction.user.id))
    
    if not user_items:
        await interaction.response.send_message(
            "You don't have any items to withdraw!",
            ephemeral=True
        )
        return
    
                              
    embed = discord.Embed(
        title="Withdraw Items",
        description="Select items from your inventory to withdraw.",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="How It Works",
        value="1. Select items to withdraw\n2. A ticket channel will be created\n3. Support team will review your request\n4. Once approved, items are removed from bot\n5. You can cancel anytime using the button",
        inline=False
    )
    
    embed.add_field(
        name="Important Notes",
        value="• Items are removed from your inventory immediately\n• They will be held until approved or cancelled\n• Make sure the items are correct before confirming",
        inline=False
    )
    
    embed.add_field(
        name="Your Inventory Value",
        value=f"{VALUE_EMOJI} **{format_value_with_commas(calculate_inventory_value(str(interaction.user.id)))}**",
        inline=False
    )
    
    view = WithdrawalItemSelectionView(user_items)
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="blackjack", description="Start a Blackjack PVP game!")
async def blackjack(interaction: discord.Interaction):
    if not is_user_registered(interaction.user.id):
        await interaction.response.send_message(
            f"You need to register your Roblox account first! Use `/register` to get started.", 
            ephemeral=True
        )
        return
    
    embed = discord.Embed(
        title="BLACKJACK PVP",
        description="Challenge someone to a game of Blackjack! Closest to 21 without busting wins.",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="HOW IT WORKS",
        value="1. Create a game with your bet\n2. Opponent joins with matching bet\n3. Both players get 2 cards\n4. Take turns: HIT or STAND\n5. Closest to 21 without going over wins\n6. **House tax applied** (current rate shown in game)",
        inline=False
    )
    
    embed.add_field(
        name="GAME RULES",
        value="• Aces count as 1 or 11\n• Face cards (J,Q,K) = 10\n• Number cards = face value\n• Bust = over 21 = automatic loss\n• Both bust = push (bets returned)\n• Tie score = push",
        inline=False
    )
    
    embed.add_field(
        name="MINIMUM BET",
        value=f"{VALUE_EMOJI} **{format_value_with_commas(BLACKJACK_MIN_BET)}**",
        inline=True
    )
    
    embed.add_field(
        name="MAXIMUM BET",
        value=f"{VALUE_EMOJI} **{format_value_with_commas(BLACKJACK_MAX_BET)}**",
        inline=True
    )
    
    class BlackjackStartView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
        
        @discord.ui.button(label="CREATE GAME", style=discord.ButtonStyle.secondary, row=0)
        async def create_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                              
            user_items = get_user_all_items(str(interaction.user.id))
            
            if not user_items:
                await interaction.response.send_message(
                    "You don't have any items to bet!",
                    ephemeral=True
                )
                return
            
            embed = discord.Embed(
                title="Select Items to Bet",
                description=f"Select items worth at least {VALUE_EMOJI} **{format_value_with_commas(BLACKJACK_MIN_BET)}** and at most {VALUE_EMOJI} **{format_value_with_commas(BLACKJACK_MAX_BET)}**.",
                color=discord.Color.green()
            )
            
            embed.add_field(
                name="Instructions",
                value="1. Select items from the dropdown\n2. You can select multiple items\n3. Total value must be between 0 and 1,000,000\n4. Click 'Confirm Selection' when done",
                inline=False
            )
            
            view = ItemSelectionView(user_items, BLACKJACK_MAX_BET, creating=True, is_blackjack=True)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    view = BlackjackStartView()
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="mines", description="Start a Mines PVP game!")
async def mines(interaction: discord.Interaction):
    if not is_user_registered(interaction.user.id):
        await interaction.response.send_message(
            f"You need to register your Roblox account first! Use `/register` to get started.", 
            ephemeral=True
        )
        return
    
    embed = discord.Embed(
        title="MINES PVP GAME",
        description="Create a 1v1 Mines game on a 5x5 board! First player to click a mine loses.",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="HOW IT WORKS",
        value="1. Choose number of mines (1-10)\n2. Select items to bet\n3. Create game with hidden mines\n4. Opponent joins your game\n5. Game starts automatically\n6. Take turns clicking cells (1-25)\n7. First player to hit a mine loses\n8. **House tax applied** (current rate shown in game)\n9. **WILD MODE - REVERSED OUTCOME!**",
        inline=False
    )
    
    embed.add_field(
        name="GAME RULES",
        value=f"• {MINES_SAFE_EMOJI} Safe cell - game continues\n• {MINES_HIT_EMOJI} Mine - player loses immediately\n• Random starting player\n• Winner takes the entire pot\n• **5x5 board** with customizable mines\n• If all safe cells are revealed, the last player wins!",
        inline=False
    )
    
    embed.add_field(
        name="WILD MODE EFFECTS",
        value=f"• **Extra Mine:** +1 additional mine!\n• **Outcome Reversal:** Hitting a mine makes you WIN!\n• **1% chance** for wild mode in every game",
        inline=False
    )
    
    embed.add_field(
        name="MINIMUM BET",
        value=f"{VALUE_EMOJI} - **0**",
        inline=True
    )
    
    embed.add_field(
        name="MAXIMUM BET",
        value=f"{VALUE_EMOJI} - **1,000,000**",
        inline=True
    )
    
    class MinesStartView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
        
        @discord.ui.button(label="CREATE", style=discord.ButtonStyle.secondary, row=0)
        async def create_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            modal = MinesCreationModal()
            await interaction.response.send_modal(modal)
    
    view = MinesStartView()
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="towers", description="Start a Towers PVP game!")
async def towers(interaction: discord.Interaction):
    if not is_user_registered(interaction.user.id):
        await interaction.response.send_message(
            f"You need to register your Roblox account first! Use `/register` to get started.", 
            ephemeral=True
        )
        return
    
    embed = discord.Embed(
        title="TOWERS PVP GAME",
        description="Create a 1v1 Towers game on a 3x7 board! First player to click the bomb loses.",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="GAME RULES",
        value=f"• {MINES_SAFE_EMOJI} Safe cell - game continues\n• {WILD_MODE_EMOJI} Bomb - player loses immediately\n• Random starting player\n• Winner takes the entire pot\n• If all safe cells are revealed, the last player wins!",
        inline=False
    )
    
    embed.add_field(
        name="MINIMUM BET",
        value=f"{VALUE_EMOJI} - **0**",
        inline=True
    )
    
    embed.add_field(
        name="MAXIMUM BET",
        value=f"{VALUE_EMOJI} - **1,000,000**",
        inline=True
    )
    
    class TowersStartView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
        
        @discord.ui.button(label="CREATE", style=discord.ButtonStyle.secondary, row=0)
        async def create_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                              
            user_items = get_user_all_items(str(interaction.user.id))
            
            if not user_items:
                await interaction.response.send_message(
                    "You don't have any items to bet!",
                    ephemeral=True
                )
                return
            
            embed = discord.Embed(
                title="Select Items to Bet",
                description=f"Select items worth at least {VALUE_EMOJI} **{format_value_with_commas(MIN_BET_VALUE)}** and at most {VALUE_EMOJI} **{format_value_with_commas(MAX_BET_VALUE)}**.\n\nTowers: 3 wide × 7 tall with 5 bombs",
                color=discord.Color.green()
            )
            
            embed.add_field(
                name="Instructions",
                value="1. Select items from the dropdown\n2. You can select multiple items\n3. Total value must be between 0 and 1,000,000\n4. Click 'Confirm Selection' when done",
                inline=False
            )
            
                                        
            view = ItemSelectionView(user_items, MAX_BET_VALUE, creating=True, is_towers=True)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    view = TowersStartView()
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

                                        
class RobloxUsernameInputModal(discord.ui.Modal, title="Enter Your Roblox Username"):
    roblox_username = discord.ui.TextInput(
        label="Roblox Username",
        placeholder="Enter your exact Roblox username (case sensitive)",
        required=True,
        max_length=50
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)

        username_input = self.roblox_username.value.strip()


        try:
            async with aiohttp.ClientSession() as session:
                headers = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'}

                async with session.post(
                    "https://users.roblox.com/v1/usernames/users",
                    headers=headers,
                    json={"usernames": [username_input], "excludeBannedUsers": True}
                ) as resp:
                    if resp.status != 200:
                        await interaction.followup.send(
                            "Could not find that Roblox username. Please check it and try again.",
                            ephemeral=True
                        )
                        return
                    data = await resp.json()
                    if not data.get('data'):
                        await interaction.followup.send(
                            "Could not find that Roblox username. Please check it and try again.",
                            ephemeral=True
                        )
                        return
                    user_info = data['data'][0]
                    roblox_id = str(user_info['id'])
                    roblox_username = user_info['name']
                    roblox_display_name = user_info.get('displayName', roblox_username)


                avatar_url = f"https://www.roblox.com/headshot-thumbnail/image?userId={roblox_id}&width=420&height=420&format=png"
                try:
                    async with session.get(
                        f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={roblox_id}&size=420x420&format=Png&isCircular=false",
                        headers=headers
                    ) as avatar_resp:
                        if avatar_resp.status == 200:
                            avatar_data = await avatar_resp.json()
                            if avatar_data.get('data') and len(avatar_data['data']) > 0:
                                avatar_url = avatar_data['data'][0]['imageUrl']
                except Exception:
                    pass

        except Exception as e:
            print(f"Error fetching Roblox user info during registration: {e}")
            await interaction.followup.send(
                "An error occurred while looking up your Roblox account. Please try again.",
                ephemeral=True
            )
            return


        verification_code = get_verification_code(interaction.user.id, interaction.user.name)
        registrations = load_registrations()
        uid = str(interaction.user.id)
        registrations[uid]['discord_username'] = interaction.user.name
        registrations[uid]['pending_roblox_username'] = roblox_username
        registrations[uid]['pending_roblox_display_name'] = roblox_display_name
        registrations[uid]['pending_roblox_id'] = roblox_id
        registrations[uid]['pending_roblox_avatar'] = avatar_url
        save_json(REGISTRATIONS_FILE, registrations)

        def build_pending_embed(verification_code: str, roblox_username: str,
                                roblox_display_name: str, avatar_url: str) -> discord.Embed:
            embed = discord.Embed(
                title="Bloxloot Registration",
                color=discord.Color.green(),
                description=(
                    f"Welcome, **{roblox_display_name}** (`{roblox_username}`)!\n\n"
                    "Copy the code below and paste it into your **Roblox bio**.\n"
                )
            )
            if avatar_url:
                embed.set_thumbnail(url=avatar_url)
            embed.add_field(
                name="",
                value=f"```\n{verification_code}\n```",
                inline=False
            )
            embed.set_footer(text="Checking your bio.. | Need help? Contact the Bloxloot Team!")
            return embed

        class CopyCodeView(discord.ui.View):
            def __init__(self, code: str):
                super().__init__(timeout=None) 
                self.code = code

            @discord.ui.button(label="COPY CODE", style=discord.ButtonStyle.secondary)
            async def copy_button(self, btn_interaction: discord.Interaction, button: discord.ui.Button):
                await btn_interaction.response.send_message(
                    content=f"```\n{self.code}\n```",
                    ephemeral=True
                )

        pending_embed = build_pending_embed(
            verification_code, roblox_username, roblox_display_name, avatar_url
        )
        view = CopyCodeView(verification_code)


        pending_message = await interaction.followup.send(
            embed=pending_embed,
            view=view,
            ephemeral=True,
            wait=True
        )

        asyncio.create_task(
            _poll_roblox_bio_for_verification(
                discord_user_id=interaction.user.id,
                roblox_username=roblox_username,
                roblox_display_name=roblox_display_name,
                roblox_id=roblox_id,
                avatar_url=avatar_url,
                verification_code=verification_code,
                interaction=interaction,
                pending_message=pending_message,
                copy_view=view,
            )
        )


async def _poll_roblox_bio_for_verification(
    discord_user_id: int,
    roblox_username: str,
    roblox_display_name: str,
    roblox_id: str,
    avatar_url: str,
    verification_code: str,
    interaction: discord.Interaction,
    pending_message,                                                                          
    copy_view: discord.ui.View,
    max_attempts: int = 60,                                  
    interval: int = 10
):
    """Poll Roblox bio every `interval` seconds and edit the ephemeral message on success/timeout."""
    headers = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'}

    for attempt in range(max_attempts):
        await asyncio.sleep(interval)

                                                  
        registrations = load_registrations()
        uid = str(discord_user_id)
        if registrations.get(uid, {}).get('verified', False):
            print(f"[AUTO-VERIFY] {roblox_username} already verified, stopping poll.")
            return

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://users.roblox.com/v1/users/{roblox_id}",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as profile_resp:
                    if profile_resp.status != 200:
                        continue
                    profile_data = await profile_resp.json()
                    description = profile_data.get("description", "")

                    if verification_code.strip() not in description.strip():
                        continue

                                                      
                    print(f"[AUTO-VERIFY] Code found in {roblox_username}'s bio!")
                    registrations = load_registrations()
                    existing_registration = registrations.get(uid, {})
                    registrations[uid]['discord_username'] = existing_registration.get('discord_username', str(discord_user_id))
                    registrations[uid]['verified'] = True
                    registrations[uid]['roblox_username'] = roblox_username
                    registrations[uid]['roblox_display_name'] = roblox_display_name
                    registrations[uid]['roblox_id'] = roblox_id
                    registrations[uid]['roblox_avatar'] = avatar_url
                    registrations[uid]['verified_at'] = datetime.now().isoformat()
                    for k in ['pending_roblox_username', 'pending_roblox_display_name',
                              'pending_roblox_id', 'pending_roblox_avatar']:
                        registrations[uid].pop(k, None)

                    roblox_emoji_mention = await ensure_registration_emoji(discord_user_id, roblox_username, avatar_url)
                    if roblox_emoji_mention:
                        registrations[uid]['roblox_emoji'] = roblox_emoji_mention

                    save_json(REGISTRATIONS_FILE, registrations)

                    await bot.update_presence()

                    if avatar_url:
                        success_embed.set_thumbnail(url=avatar_url)
                    success_embed.add_field(
                        name="GET STARTED",
                        value=(
                            "• `/inventory` — view your items\n"
                            "• `/coinflip` — Play Coinflip PvP\n"
                            "• `/mines` — Play Mines PVP\n"
                            "• `/blackjack` — Play Blackjack PvP"
                        ),
                        inline=False
                    )
                    success_embed.set_footer(text="Welcome to Bloxloot!")

                    try:
                        await pending_message.edit(embed=success_embed, view=copy_view)
                    except discord.NotFound:
                                                                                 
                        print(f"[AUTO-VERIFY] Could not edit ephemeral message for {discord_user_id} — token expired.")
                    except Exception as edit_err:
                        print(f"[AUTO-VERIFY] Edit error for {discord_user_id}: {edit_err}")

                    return        

        except Exception as e:
            print(f"[AUTO-VERIFY] Poll attempt {attempt + 1} failed for {roblox_username}: {e}")
            continue

                                                   
    print(f"[AUTO-VERIFY] Timed out for {roblox_username}.")
    timeout_embed = discord.Embed(
        title="Registration Timed Out",
        color=discord.Color.red(),
        description=(
            f"We couldn't detect the verification code in **{roblox_username}**'s bio after 10 minutes.\n\n"
            "Please use `/register` again and make sure the code is saved to your bio exactly as shown."
        )
    )
    if avatar_url:
        timeout_embed.set_thumbnail(url=avatar_url)
    timeout_embed.set_footer(text="Use /register to try again.")

    for child in copy_view.children:
        child.disabled = True

    try:
        await pending_message.edit(embed=timeout_embed, view=copy_view)
    except Exception:
        pass


@bot.tree.command(name="register", description="Register your Roblox account to use Bloxloot!")
async def register(interaction: discord.Interaction):
                       
    if is_user_registered(interaction.user.id):
        registrations = load_registrations()
        user_info = registrations.get(str(interaction.user.id), {})
        embed = discord.Embed(
            title="Already Registered",
            color=discord.Color.green(),
            description=(
                f"You are already registered!\n"
                f"**Roblox Username:** {user_info.get('roblox_username', 'Not set')}\n"
                f"**Roblox Display Name:** {user_info.get('roblox_display_name', 'Not set')}\n"
                f"**Registered:** {datetime.fromisoformat(user_info['registered_at']).strftime('%Y-%m-%d %H:%M')}"
            )
        )
        roblox_avatar = user_info.get('roblox_avatar')
        if roblox_avatar:
            embed.set_thumbnail(url=roblox_avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

                                                              
    await interaction.response.send_modal(RobloxUsernameInputModal())

@bot.tree.command(name="inventory", description="View your inventory!")
async def inventory(interaction: discord.Interaction):
    
    if not is_user_registered(interaction.user.id):
        await interaction.response.send_message(
            "You need to register first! Use `/register` to get started.", 
            ephemeral=True
        )
        return
    
                                  
    registrations = load_registrations()
    user_data = registrations.get(str(interaction.user.id), {})
    
                                      
    user_items = get_user_items_with_values(str(interaction.user.id))
    total_value = calculate_inventory_value(str(interaction.user.id))
    usd_balance = get_user_balance(str(interaction.user.id))
    
                  
    embed = discord.Embed(
        title="",
        color=discord.Color.green()
    )
    
                                                              
    roblox_avatar = user_data.get('roblox_avatar')
    if roblox_avatar:
        embed.set_thumbnail(url=roblox_avatar)
    
                                      
    roblox_username = user_data.get('roblox_username')
    if roblox_username:
        embed.set_author(
            name=f"",
        )
    
    embed.add_field(
        name="Inventory Value",
        value=f"{VALUE_EMOJI} **{format_value_with_commas(total_value)}**",
        inline=True
    )
    embed.add_field(
        name="USD Balance",
        value=f"**${usd_balance:.2f} **",
        inline=True
    )
    
    if user_items:
        items_text = ""
        total_items_count = 0
        
                             
        for item_name, item_value, item_details, count in user_items:
            total_items_count += count
            item_emoji = get_item_emoji(item_name)
            items_text += f"{item_emoji} **`{item_name}`** x{count} ({VALUE_EMOJI} {format_value_with_commas(item_value)} each)\n"
        
        embed.add_field(
            name=f"Items ({total_items_count} total)",
            value=items_text or "No items",
            inline=False
        )
    else:
        embed.add_field(
            name="No Items",
            value="Your inventory is empty. Deposit items to start playing!",
            inline=False
        )
    
                                  
    embed.set_footer(
        text=f"ID: {interaction.user.id} • Use /list to sell your items!"
    )
    
                     
    embed.timestamp = datetime.now()
    
    await interaction.response.send_message(embed=embed, ephemeral=True)


class DepositAmountModal(discord.ui.Modal, title="Enter USD Amount"):
    def __init__(self, user_id: int, currency: str, message_id: int, channel_id: int):
        super().__init__()
        self.user_id = user_id
        self.currency = currency
        self.message_id = message_id
        self.channel_id = channel_id

    usd_amount = discord.ui.TextInput(
        label="USD Amount",
        placeholder="Enter how much USD you want to deposit",
        required=True,
        max_length=12
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            usd_amount = float(self.usd_amount.value)
            if usd_amount <= 0:
                await interaction.response.send_message(
                    "Please enter a USD amount greater than 0.",
                    ephemeral=True
                )
                return

            deposit_id = f"deposit_{self.user_id}_{int(datetime.now().timestamp())}"
            invoice = await request_oxa_static_address(
                CRYPTO_CURRENCIES[self.currency]["code"],
                deposit_id
            )

            if not invoice or (not invoice.get("address") and not invoice.get("payment_url")):
                await interaction.response.send_message(
                    "Unable to generate a deposit address or payment link from Oxa Pay at this time. Please try again later.",
                    ephemeral=True
                )
                return

            address = invoice.get("address")
            payment_url = invoice.get("payment_url")
            crypto_amount = float(invoice.get("crypto_amount") or calculate_crypto_amount(usd_amount, self.currency))
            qr_url = invoice.get("qr_code_url") or (get_qr_code_url(address) if address else None)

            deposit_record = create_crypto_deposit_record(
                str(self.user_id),
                self.currency,
                usd_amount,
                crypto_amount,
                address,
                self.channel_id,
                self.message_id or 0,
                deposit_id=deposit_id,
                oxa_invoice_id=invoice.get("invoice_id"),
                payment_url=payment_url
            )

            embed = discord.Embed(
                title="Bloxloot Deposit Created",
                description=(
                    f"You have chosen {get_crypto_currency_label(self.currency)}.\n"
                    "Use the link or address below to complete your deposit.\n"
                ),
                color=0x2ecc71,
                timestamp=datetime.now()
            )
            embed.add_field(name="USD Amount", value=f"**${usd_amount:.2f} USD**", inline=True)
            embed.add_field(name="Crypto Amount", value=f"**{crypto_amount:.8f} {CRYPTO_CURRENCIES[self.currency]['code']}**", inline=True)
            if address:
                embed.add_field(name="Deposit Address", value=f"`{address}`", inline=False)
            if payment_url:
                embed.add_field(name="Deposit Payment Page", value=payment_url, inline=False)
            if qr_url:
                embed.set_thumbnail(url=qr_url)
            embed.set_footer(text="Deposit created. Monitor this message for further confirmation.")

            await interaction.response.send_message(embed=embed, ephemeral=True)
        except ValueError:
            await interaction.response.send_message(
                "Please enter a valid number for the USD amount.",
                ephemeral=True
            )
        except Exception as e:
            print(f"Error generating deposit details: {e}")
            await interaction.response.send_message(
                "There was an error creating your deposit details. Please try again.",
                ephemeral=True
            )


class DepositCryptoSelectView(discord.ui.View):
    def __init__(self, owner_id: int = None, timeout: int = None):
        super().__init__(timeout=timeout)
        self.owner_id = owner_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.owner_id and interaction.user.id != self.owner_id:
            await interaction.response.send_message(
                "This deposit panel was created for another user.",
                ephemeral=True
            )
            return False
        return True

    @discord.ui.select(
        placeholder="Deposit with Cryptocurrencys..",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label="Bitcoin", value="Bitcoin", emoji=CRYPTO_CURRENCIES["Bitcoin"]["emoji"]),
            discord.SelectOption(label="Litecoin", value="Litecoin", emoji=CRYPTO_CURRENCIES["Litecoin"]["emoji"]),
            discord.SelectOption(label="Ethereum", value="Ethereum", emoji=CRYPTO_CURRENCIES["Ethereum"]["emoji"]),
            discord.SelectOption(label="Solana", value="Solana", emoji=CRYPTO_CURRENCIES["Solana"]["emoji"]),
            discord.SelectOption(label="Tether", value="Tether", emoji=CRYPTO_CURRENCIES["Tether"]["emoji"])
        ],
        custom_id="deposit_crypto_select"
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        currency = select.values[0]
        await interaction.response.send_modal(
            DepositAmountModal(
                interaction.user.id,
                currency,
                interaction.message.id if interaction.message else 0,
                interaction.channel.id if interaction.channel else DEPOSIT_CHANNEL_ID
            )
        )


class WithdrawCryptoModal(discord.ui.Modal, title="Crypto Withdrawal"):
    def __init__(self, user_id: int, currency: str, message_id: int, channel_id: int):
        super().__init__()
        self.user_id = user_id
        self.currency = currency
        self.message_id = message_id
        self.channel_id = channel_id

    usd_amount = discord.ui.TextInput(
        label="USD Amount",
        placeholder="Enter how much USD you want to withdraw",
        required=True,
        max_length=12
    )

    address = discord.ui.TextInput(
        label="Your Address",
        placeholder="Enter your crypto wallet address",
        required=True,
        max_length=128
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            usd_amount = float(self.usd_amount.value)
            address_value = self.address.value.strip()

            if usd_amount <= 0:
                await interaction.response.send_message(
                    "Please enter a USD amount greater than 0.",
                    ephemeral=True
                )
                return

            user_id_str = str(self.user_id)
            current_balance = get_user_balance(user_id_str)
            if usd_amount > current_balance:
                await interaction.response.send_message(
                    f"Insufficient USD balance. You have **${current_balance:.2f}** available.",
                    ephemeral=True
                )
                return

            if not validate_crypto_address(address_value, self.currency):
                await interaction.response.send_message(
                    "Please enter a valid destination address for the selected currency.",
                    ephemeral=True
                )
                return

            if not subtract_user_balance(user_id_str, usd_amount):
                await interaction.response.send_message(
                    "Unable to reserve that USD amount. Please try again with a lower amount.",
                    ephemeral=True
                )
                return

            try:
                withdrawal_record = create_crypto_withdrawal_record(
                    user_id_str,
                    self.currency,
                    usd_amount,
                    address_value,
                    self.channel_id,
                    self.message_id or 0
                )
            except Exception:
                add_user_balance(user_id_str, usd_amount)
                raise


            crypto_amount = withdrawal_record["crypto_amount"]

            embed = discord.Embed(
                title="Bloxloot Withdrawal Created",
                description=(
                    f"You have chosen {get_crypto_currency_label(self.currency)}.\n"
                ),
                color=0x2ecc71,
                timestamp=datetime.now()
            )
            embed.add_field(name="USD Amount", value=f"**${usd_amount:.2f}**", inline=True)
            embed.add_field(name="Crypto Amount", value=f"**{crypto_amount:.8f} {CRYPTO_CURRENCIES[self.currency]['code']}**", inline=True)
            embed.add_field(name="Your Address", value=f"`{address_value}`", inline=False)
            embed.add_field(name="Status", value="Pending", inline=True)
            embed.set_footer(text="Withdrawal created. Support will process the payout.")

            await interaction.response.send_message(embed=embed, ephemeral=True)
        except ValueError:
            await interaction.response.send_message(
                "Please enter a valid number for the USD amount.",
                ephemeral=True
            )
        except Exception as e:
            print(f"Error generating withdrawal details: {e}")
            await interaction.response.send_message(
                "There was an error creating your withdrawal. Please try again.",
                ephemeral=True
            )


class CryptoWithdrawSelectView(discord.ui.View):
    def __init__(self, owner_id: int = None, timeout: int = None):
        super().__init__(timeout=timeout)
        self.owner_id = owner_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.owner_id and interaction.user.id != self.owner_id:
            await interaction.response.send_message(
                "This withdrawal panel was created for another user.",
                ephemeral=True
            )
            return False
        return True

    @discord.ui.select(
        placeholder="Withdraw with Cryptocurrencys..",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label="Bitcoin", value="Bitcoin", emoji=CRYPTO_CURRENCIES["Bitcoin"]["emoji"]),
            discord.SelectOption(label="Litecoin", value="Litecoin", emoji=CRYPTO_CURRENCIES["Litecoin"]["emoji"]),
            discord.SelectOption(label="Ethereum", value="Ethereum", emoji=CRYPTO_CURRENCIES["Ethereum"]["emoji"]),
            discord.SelectOption(label="Solana", value="Solana", emoji=CRYPTO_CURRENCIES["Solana"]["emoji"]),
            discord.SelectOption(label="Tether", value="Tether", emoji=CRYPTO_CURRENCIES["Tether"]["emoji"])
        ],
        custom_id="withdraw_crypto_select"
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        currency = select.values[0]
        await interaction.response.send_modal(
            WithdrawCryptoModal(
                interaction.user.id,
                currency,
                interaction.message.id if interaction.message else 0,
                interaction.channel.id if interaction.channel else WITHDRAW_CHANNEL_ID
            )
        )


@bot.tree.command(name="values", description="View the Bloxloot Value List!")
async def values(interaction: discord.Interaction):
    """View the value list for MM2 or ADM! Defaults to MM2 with a toggle button for ADM."""
    selected_type = GameType.MM2

    embed, view = build_values_response(selected_type)
    if not embed or not view:
        await interaction.response.send_message(
            f"No {selected_type} items found in the database.",
            ephemeral=True
        )
        return
    
                                           
    if hasattr(view, 'game_type'):
        view.game_type = selected_type

    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
                                                                                                    
                                                                              
class CaseSelectionDropdown(discord.ui.Select):
    def __init__(self):
        options = []
        for i in range(1, len(collections) + 1):
            section = collections[str(i)]
            options.append(
                discord.SelectOption(
                    label=f"{section['name']}",
                    value=str(i),
                    emoji=section['emoji'],
                    description=section['description'][:50]
                )
            )
        super().__init__(
            placeholder="Select case sections...",
            min_values=1,
            max_values=len(collections),
            options=options,
            custom_id="case_selection_dropdown"
        )

    async def callback(self, interaction: discord.Interaction):
        self.view.selected_cases = self.values
        await interaction.response.send_message(
            f"Selected {len(self.values)} case section(s). Proceed with game creation.",
            ephemeral=True
        )


class CaseSelectionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.selected_cases = []
        self.add_item(CaseSelectionDropdown())


class CaseBattleJoinView(discord.ui.View):
    def __init__(self, game_id, creator_id, bet_amount, value_price, rounds, case_section, selected_cases=None, crazy_mode=False):
        super().__init__(timeout=None)
        self.game_id = game_id
        self.creator_id = creator_id
        self.bet_amount = bet_amount
        self.value_price = value_price
        self.rounds = rounds
        self.case_section = case_section
        self.selected_cases = selected_cases or [str(case_section)]
        self.joined_players = [creator_id]
        self.game_started = False
        self.crazy_mode = crazy_mode

    @discord.ui.button(label="JOIN", style=discord.ButtonStyle.secondary, row=0)
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                                               
        if not is_user_registered(interaction.user.id):
            await interaction.response.send_message(
                "You need to register first! Use `/register` to get started.",
                ephemeral=True
            )
            return

        if self.game_started:
            await interaction.response.send_message("Game has already started!", ephemeral=True)
            return

        if interaction.user.id in self.joined_players:
            await interaction.response.send_message("You can't join your own game!", ephemeral=True)
            return

                                                   
        required_value = self.bet_amount
        min_allowed = int(required_value * 0.9)
        max_allowed = int(required_value * 1.1)
        
        user_items = get_user_all_items(str(interaction.user.id))
        if not user_items:
            await interaction.response.send_message("You don't have any items to bet!", ephemeral=True)
            return

        user_total_value = calculate_inventory_value(str(interaction.user.id))
        if user_total_value < min_allowed:
            await interaction.response.send_message(
                f"You need at least {VALUE_EMOJI} **{format_value_with_commas(min_allowed)}** in items to join this game!\n"
                f"Your current inventory value: {VALUE_EMOJI} **{format_value_with_commas(user_total_value)}**",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="CASE BATTLE JOIN",
            description=f"Select items worth between {VALUE_EMOJI} **{format_value_with_commas(min_allowed)}** and {VALUE_EMOJI} **{format_value_with_commas(max_allowed)}** to join this game.",
            color=discord.Color.green()
        )
        embed.add_field(name="Instructions", value=f"Select items within 10% of {VALUE_EMOJI} **{format_value_with_commas(required_value)}**.", inline=False)

        view = ItemSelectionView(user_items, required_value, self.game_id, allow_range=True)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @discord.ui.button(label="CANCEL", style=discord.ButtonStyle.danger, row=0)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.creator_id:
            await interaction.response.send_message("Only the game creator can cancel the game!", ephemeral=True)
            return

                               
        if self.game_id in active_case_battles:
            game = active_case_battles[self.game_id]
            for player_id in self.joined_players:
                if not game.get('game_started', False):
                                                 
                    items = game.get('creator_items', []) if player_id == self.creator_id else game.get('joiner_items', [])
                    if items:
                        add_items_to_inventory(str(player_id), items)
            del active_case_battles[self.game_id]

        for child in self.children:
            child.disabled = True

        embed = discord.Embed(title="CASE BATTLE GAME CANCELLED", color=discord.Color.red())
        embed.add_field(name="Items Returned", value=f"All items have been returned to <@{self.creator_id}>", inline=False)
        await interaction.response.edit_message(embed=embed, view=self)
        await interaction.followup.send("Case Battle has been cancelled and bets refunded.", ephemeral=True)


def build_casebattle_eos_block(game_id: str, creator_id: int, joiner_id: Optional[int], base_seed: Optional[str] = None) -> dict:
    """Create a deterministic EOS-block-like payload for case battle fairness."""
    timestamp = int(datetime.now().timestamp())
    base_seed = base_seed or generate_server_seed("casebattle", game_id, creator_id, joiner_id or 0, timestamp)
    block_height = timestamp % 10_000_000
    block_hash = hashlib.sha256(f"{game_id}:{creator_id}:{joiner_id}:{base_seed}:{block_height}".encode("utf-8")).hexdigest()
    return {
        "height": block_height,
        "id": block_hash[:16],
        "hash": block_hash,
        "timestamp": timestamp,
    }


async def update_casebattle_status(game_id: str, status_text: str, eos_block: Optional[dict] = None):
    """Update the case battle message embed with the current status text."""
    game = active_case_battles.get(game_id)
    if not game:
        return

    channel = bot.get_channel(game.get('channel_id')) if game.get('channel_id') else None
    if not channel or not game.get('message_id'):
        return

    try:
        message = await channel.fetch_message(game['message_id'])
        if not message.embeds:
            return

        embed = message.embeds[0]
        for idx, field in enumerate(embed.fields):
            if field.name == "STATUS":
                value = f"**{status_text}**"
                if eos_block:
                    value += f"\n\n**EOS Block:** #{eos_block['height']} | `{eos_block['id']}`"
                embed.set_field_at(idx, name="STATUS", value=value, inline=False)
                break
        await message.edit(embed=embed)
    except Exception:
        pass


async def play_casebattle(game_id: str):
    """Automate all rounds for a case battle and resolve winner by total value."""
    await asyncio.sleep(1)
    game = active_case_battles.get(game_id)
    if not game:
        return

    channel = bot.get_channel(game.get('channel_id')) if game.get('channel_id') else None
                  
    creator_id = game.get('creator')
    joiner_id = [p for p in game.get('joined_players', []) if p != game.get('creator')]
    joiner_id = joiner_id[0] if joiner_id else None

                                     
    creator = None
    joiner = None
    try:
        creator = await bot.fetch_user(int(creator_id)) if creator_id else None
    except Exception:
        pass
    try:
        joiner = await bot.fetch_user(int(joiner_id)) if joiner_id else None
    except Exception:
        pass

    rounds = game.get('rounds', 3)
    selected_cases = list(game.get('selected_cases', [str(game.get('case_section'))]))
    crazy = game.get('crazy_mode', False)
    game_type = game.get('game_type', 'Unknown')

    creator_id = int(creator_id) if creator_id is not None else None
    joiner_id = int(joiner_id) if joiner_id is not None else None

    if not game.get('eos_block'):
        eos_block = build_casebattle_eos_block(game_id, creator_id, joiner_id, game.get('server_seed'))
        game['eos_block'] = eos_block
        game['server_seed'] = generate_server_seed('casebattle', game_id, creator_id, joiner_id, eos_block['height'], eos_block['id'])
        game['server_seed_hash'] = get_server_seed_hash(game['server_seed'])
        active_case_battles[game_id] = game

    await update_casebattle_status(game_id, "Fetching EOS Block..", game.get('eos_block'))
    await asyncio.sleep(1)
    await update_casebattle_status(game_id, "Playing rounds...", game.get('eos_block'))

    creator_score = 0
    joiner_score = 0

                                                                                           
    pool = selected_cases.copy()
    pool = deterministic_shuffle(game.get('server_seed', generate_server_seed('casebattle', game_id)), pool, 'casebattle')
    for r in range(1, rounds + 1):
        if game_id not in active_case_battles:
            return
                                                                       
        if not pool:
            pool = selected_cases.copy()
            pool = deterministic_shuffle(game.get('server_seed', generate_server_seed('casebattle', game_id)), pool, f'casebattle_round_{r}')
        key = pool.pop(0)
        case_section = CASE_SECTIONS[str(key)]
        Value = case_section['Value']

        def pick_item(Value):
            return deterministic_weighted_choice(Value, game.get('server_seed', generate_server_seed('casebattle', game_id)), 'casebattle', r)

        creator_Item = pick_item(Value)
        joiner_Item = pick_item(Value)

        if crazy:
            creator_Item['value'] = int(creator_Item['value'] * 2)
            joiner_Item['value'] = int(joiner_Item['value'] * 2)

        creator_score += creator_Item['value']
        joiner_score += joiner_Item['value']

                      
        game['round_history'].append({
            'round': r,
            'case_section': case_section['name'],
            'creator_Item': creator_Item,
            'joiner_Item': joiner_Item,
            'winner': 'creator' if creator_Item['value'] > joiner_Item['value'] else ('joiner' if joiner_Item['value'] > creator_Item['value'] else 'tie')
        })

                                                   
        try:
            if channel and game.get('message_id'):
                message = await channel.fetch_message(game['message_id'])
                embed = discord.Embed(title=f"ROUND {r} RESULTS", color=discord.Color.green())
                if crazy:
                    embed.add_field(name=f"{WILD_MODE_EMOJI} CRAZY MODE", value="**Values doubled!**", inline=False)
                embed.add_field(name="CASES", value=f"{case_section['emoji']} **{case_section['name']}**", inline=False)
                embed.add_field(name=f"{creator.mention if creator else f'<@{creator_id}>'}'s Item", value=f"{creator_Item['emoji']} **{creator_Item['name']}**\n{VALUE_EMOJI} **{format_value_with_commas(creator_Item['value'])}**", inline=True)
                embed.add_field(name=f"{joiner.mention if joiner else f'<@{joiner_id}>'}'s Item", value=f"{joiner_Item['emoji']} **{joiner_Item['name']}**\n{VALUE_EMOJI} **{format_value_with_commas(joiner_Item['value'])}**", inline=True)
                embed.add_field(name="CURRENT SCORES", value=f"**{creator.mention if creator else f'<@{creator_id}>'}:** {VALUE_EMOJI} **{format_value_with_commas(creator_score)}**\n**{joiner.mention if joiner else f'<@{joiner_id}>'}:** {VALUE_EMOJI} **{format_value_with_commas(joiner_score)}**", inline=False)
                await message.edit(embed=embed)
        except Exception:
            pass

        await asyncio.sleep(2)

                                    
    total_pot = game['bet_amount'] * 2
    tax_amount = calculate_tax(total_pot)
    net_winnings = calculate_net_winnings(total_pot)
    
    if creator_score > joiner_score:
        winner_id = str(creator_id)
        loser_id = str(joiner_id) if joiner_id else None
    elif joiner_score > creator_score:
        winner_id = str(joiner_id) if joiner_id else None
        loser_id = str(creator_id)
    else:
        winner_id = None
                          
    creator_items = game.get('creator_items', [])
    joiner_items = game.get('joiner_items', [])
    all_items = creator_items + joiner_items

    if winner_id:
                               
        remaining_items, taxed_items = deduct_tax_from_items(all_items, tax_amount)
        
                         
        await log_taxed_items(
            source_game="Case Battle",
            winner_id=int(winner_id),
            loser_id=int(loser_id) if loser_id else 0,
            tax_amount=tax_amount,
            items=taxed_items,
            pot_value=total_pot
        )
        
        add_items_to_inventory(winner_id, remaining_items)
        result_text = f"Winner: {creator.mention if creator_id == int(winner_id) and creator else joiner.mention if joiner_id == int(winner_id) and joiner else f'<@{winner_id}>'} — awarded {len(remaining_items)} items."
    else:
                                    
        add_items_to_inventory(str(creator_id), creator_items)
        if joiner_id:
            add_items_to_inventory(str(joiner_id), joiner_items)
        result_text = "Game ended in a tie — bets returned to both players."
        tax_amount = 0

                 
    try:
        if channel and game.get('message_id'):
            message = await channel.fetch_message(game['message_id'])
            final_embed = discord.Embed(title="CASE BATTLE - RESULTS", color=discord.Color.green())
            final_embed.add_field(name="Result", value=result_text, inline=False)
            final_embed.add_field(name="Final Scores", value=f"{creator.mention if creator else f'<@{creator_id}>'}:  {VALUE_EMOJI} **{format_value_with_commas(creator_score)}**\n{joiner.mention if joiner else f'<@{joiner_id}>'}:  {VALUE_EMOJI} **{format_value_with_commas(joiner_score)}**", inline=False)
                                       
            if winner_id:
                item_counts = {}
                for it in remaining_items:
                                                              
                    item_name = it.get('name') if isinstance(it, dict) else it
                    item_counts[item_name] = item_counts.get(item_name, 0) + 1
                summary = ""
                for name, cnt in sorted(list(item_counts.items()), key=lambda x: x[1], reverse=True)[:10]:
                    summary += f"• {get_item_emoji(name)} `{name}` x{cnt}\n"
                if len(item_counts) > 10:
                    summary += f"...and {len(item_counts)-10} more types"
                final_embed.add_field(name="Items Won", value=summary if summary else "No items", inline=False)
            await message.edit(embed=final_embed, view=None)
    except Exception:
        pass

              
                                                         
    try:
        creator_items = game.get('creator_items', [])
        joiner_items = game.get('joiner_items', [])
                                                                        
        try:
            creator_wager = sum(int(it.get('value', 0)) if isinstance(it, dict) else int(get_item_value(it)) for it in creator_items) if creator_items else int(game.get('bet_amount', 0))
        except Exception:
            creator_wager = int(game.get('bet_amount', 0))
        try:
            joiner_wager = sum(int(it.get('value', 0)) if isinstance(it, dict) else int(get_item_value(it)) for it in joiner_items) if joiner_items else int(game.get('bet_amount', 0))
        except Exception:
            joiner_wager = int(game.get('bet_amount', 0))

                                                                             
        gtype = game.get('game_type') or None
        try:
            ok, detected_type, _ = validate_items_same_type((creator_items or []) + (joiner_items or []))
            if ok and detected_type:
                gtype = detected_type
        except Exception:
            pass

                                                                        
        try:
            if gtype in (GameType.MM2, GameType.ADM):
                try:
                    add_user_wager(int(game.get('creator')), gtype, int(creator_wager))
                except Exception:
                    pass
                try:
                    if joiner_id:
                        add_user_wager(int(joiner_id), gtype, int(joiner_wager))
                except Exception:
                    pass
        except Exception:
            pass

                                             
        try:
            record_completed_game({
                "game_id": game_id,
                "game_type": gtype or "CaseBattle",
                "participants": [int(game.get('creator'))] + ([int(joiner_id)] if joiner_id else []),
                "per_player": {
                    str(game.get('creator')): int(creator_wager),
                    str(joiner_id) if joiner_id else "": int(joiner_wager)
                },
                "total_pot": int(total_pot),
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            print(f"Error recording completed case battle: {e}")
    except Exception:
        pass

    if game_id in active_case_battles:
        del active_case_battles[game_id]

@bot.tree.command(name="casebattle", description="Start a Case Battle PVP game!")
async def casebattle(interaction: discord.Interaction):
    if not is_user_registered(interaction.user.id):
        await interaction.response.send_message(
            f"You need to register your Roblox account first! Use `/register` to get started.", 
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title="CASE BATTLE PVP GAME",
        description="Create a 1v1 Case Battle game! Open cases with rare Value and highest total value wins!",
        color=discord.Color.green()
    )

    embed.add_field(
        name="HOW IT WORKS",
        value="1. Select case sections from dropdown\n2. Set bet amount per player\n3. Choose number of rounds (3-10)\n4. Opponent joins your game\n5. Game starts automatically when both players join\n6. Each round, both players open a case\n7. Highest total value after all rounds wins!",
        inline=False
    )

    sections_text = ""
    for i in range(1, len(collections) + 1):
        section = collections[str(i)]
        sections_text += f"{section['emoji']} **{section['name']}** - {section['description']}\n"

    embed.add_field(name="AVAILABLE CASES", value=sections_text, inline=False)

    class CaseBattleStartView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=60)

        @discord.ui.button(label="CREATE", style=discord.ButtonStyle.secondary)
        async def create_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            selection_view = CaseSelectionView()

            async def on_confirm_button(confirm_interaction: discord.Interaction):
                if not selection_view.selected_cases:
                    await confirm_interaction.response.send_message(
                        "Please select at least one case section!",
                        ephemeral=True
                    )
                    return
                                                                                        
                try:
                    case_section_num = selection_view.selected_cases[0] if selection_view.selected_cases else "1"
                    selected_case_names = [collections[str(case)]["name"] for case in selection_view.selected_cases] if selection_view.selected_cases else [collections["1"]["name"]]
                                                                                     
                    rounds_num = len(selection_view.selected_cases) if selection_view.selected_cases else 1
                    crazy_mode_chance = random.random() < 0.01

                    case_meta = {
                        'case_section': case_section_num,
                        'selected_cases': selection_view.selected_cases,
                        'rounds': rounds_num,
                        'crazy_mode': crazy_mode_chance
                    }

                    user_items = get_user_all_items(str(confirm_interaction.user.id))
                    if not user_items:
                        await confirm_interaction.response.send_message("You don't have any items to bet!", ephemeral=True)
                        return

                    view = ItemSelectionView(user_items, MAX_BET_VALUE, creating=True, is_casebattle=True, case_meta=case_meta)
                    item_embed = discord.Embed(
                        title="Select Items to Bet",
                        description=f"Select the items you want to bet for this Case Battle.",
                        color=discord.Color.green()
                    )
                                                     
                    try:
                        if crazy_mode_chance:
                            item_embed.add_field(name="Crazy Mode", value="Activated (values doubled)", inline=True)
                    except Exception:
                        pass
                    item_embed.add_field(name="Instructions", value="1. Select items from the dropdown\n2. You can select multiple items\n3. Click 'Confirm Selection' when done", inline=False)

                    await confirm_interaction.response.send_message(embed=item_embed, view=view, ephemeral=True)
                except Exception as e:
                    await confirm_interaction.response.send_message(f"Error creating case battle: {e}", ephemeral=True)

            confirm_button = discord.ui.Button(label="CONFIRM SELECTION", style=discord.ButtonStyle.secondary)
            confirm_button.callback = on_confirm_button
            selection_view.add_item(confirm_button)

            select_embed = discord.Embed(
                title="Select Cases",
                description="Choose cases for your game. Click 'Confirm Selection' when done.",
                color=discord.Color.green()
            )

            await interaction.response.send_message(embed=select_embed, view=selection_view, ephemeral=True)

    view = CaseBattleStartView()
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

                                   
@bot.tree.command(name="tip", description="Send items to another user!")
@app_commands.describe(
    user="The user to send items to",
    item_name="Name of the item to send",
    quantity="Number of items to send (default: 1)"
)
async def tip(interaction: discord.Interaction, user: discord.User, item_name: str, quantity: int = 1):
                                   
    if not is_user_registered(interaction.user.id):
        await interaction.response.send_message(
            "You need to register first! Use `/register` to get started.",
            ephemeral=True
        )
        return
    
                                      
    if not is_user_registered(user.id):
        await interaction.response.send_message(
            f"{user.mention} is not registered! They need to use `/register` first.",
            ephemeral=True
        )
        return
    
                                     
    if interaction.user.id == user.id:
        await interaction.response.send_message(
            "You cannot tip yourself!",
            ephemeral=True
        )
        return
    
                       
    if quantity <= 0:
        await interaction.response.send_message(
            "Quantity must be a positive number!",
            ephemeral=True
        )
        return
    
    if quantity > 100:
        await interaction.response.send_message(
            "Maximum quantity per tip is 100!",
            ephemeral=True
        )
        return
    
                              
    items = load_items()
    if item_name not in items:
                                                      
        sender_items = get_user_all_items(str(interaction.user.id))
        sender_item_names = set(item[0] for item in sender_items)
        
        if sender_item_names:
            available_items = "\n".join([f"• `{item}`" for item in sender_item_names][:10])
            if len(sender_item_names) > 10:
                available_items += f"\n• ...and {len(sender_item_names)-10} more"
        else:
            available_items = "No items in your inventory"
        
        embed = discord.Embed(
            title="Item Not Found",
            description=f"Item `{item_name}` does not exist in the items database.",
            color=discord.Color.red()
        )
        embed.add_field(
            name="Your Available Items",
            value=available_items,
            inline=False
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
                                             
    sender_inventory = get_user_inventory(str(interaction.user.id))
    sender_item_count = sum(1 for item in sender_inventory if item.get('name') == item_name)
    
    if sender_item_count < quantity:
        await interaction.response.send_message(
            f"You only have **{sender_item_count}** `{item_name}` in your inventory!\n"
            f"You tried to send **{quantity}**.",
            ephemeral=True
        )
        return
    
                                  
    item_details = items[item_name]
    item_value = item_details.get('value', 0)
    item_emoji = item_details.get('emoji', VALUE_EMOJI)
    item_type = item_details.get('type', 'Unknown')
    total_value = item_value * quantity
    
                    
    items_to_transfer = [item_name] * quantity
    transfer_items(str(interaction.user.id), str(user.id), items_to_transfer)
    
                                  
    sender_new_value = calculate_inventory_value(str(interaction.user.id))
    recipient_new_value = calculate_inventory_value(str(user.id))
    
                          
    embed = discord.Embed(
        title="Tip Sent Successfully!",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="From",
        value=f"{interaction.user.mention}",
        inline=True
    )
    
    embed.add_field(
        name="To",
        value=f"{user.mention}",
        inline=True
    )

    embed.add_field(
        name="Value",
        value=f"**{VALUE_EMOJI} {format_value_with_commas(total_value)}**",
        inline=True
    )
    
    item_sent_text = f"{item_emoji} `{item_name}` x{quantity}"
    if item_value:
        item_sent_text += f" ({VALUE_EMOJI} {format_value_with_commas(item_value)} each)"
    
    embed.add_field(
        name="Item Sent",
        value=item_sent_text,
        inline=False
    )
    
    embed.timestamp = datetime.now()
    embed.set_footer(text=f"Tip ID: {interaction.id}")
    
    await interaction.response.send_message(embed=embed)
    
                                                      

@tip.autocomplete('item_name')
async def tip_item_name_autocomplete(
    interaction: discord.Interaction,
    current: str
) -> List[app_commands.Choice[str]]:
    """Autocomplete for items in the sender's inventory"""
                                   
    if not is_user_registered(interaction.user.id):
        return []
    
                                    
    sender_items = get_user_items_with_values(str(interaction.user.id))
    choices = []
    
    for item_name, item_value, item_details, count in sender_items:
        if current.lower() in item_name.lower():
            item_emoji = item_details.get('emoji', VALUE_EMOJI)
            total_value = item_value * count
            item_type = item_details.get('type', 'Unknown')
            
            choices.append(
                app_commands.Choice(
                    name=f"{item_emoji} {item_name} x{count} ({item_type}) - {VALUE_EMOJI} {format_value_with_commas(total_value)}",
                    value=item_name
                )
            )

            
                                                          
    choices.sort(key=lambda x: x.name)
    return choices[:25]    

                                   
if __name__ == "__main__":
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("ERROR: Please replace BOT_TOKEN with your actual bot token!")
        print("Get your token from: https://discord.com/developers/applications")
    else:
        bot.run(BOT_TOKEN)
