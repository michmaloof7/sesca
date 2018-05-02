import discord
from discord.ext import commands
import asyncio
import gspread
from oauth2client.service_account import ServiceAccountCredentials

Client = discord.Client()
client = commands.Bot(command_prefix="Sesca, ")


def triangle(attack,defend):
    return "advantage" if (attack == "Sword" and defend == "Axe") else\
           "advantage" if (attack == "Axe" and defend == "Lance") else\
           "advantage" if (attack == "Lance" and defend == "Sword") else\
           "advantage" if (attack == "Light" and defend == "Dark") else\
           "advantage" if (attack == "Dark" and defend == "Fire") else \
           "advantage" if (attack == "Dark" and defend == "Wind") else \
           "advantage" if (attack == "Dark" and defend == "Thunder") else\
           "advantage" if (attack == "Fire" and defend == "Wind") else \
           "advantage" if (attack == "Wind" and defend == "Thunder") else \
           "advantage" if (attack == "Thunder" and defend == "Fire") else\
           "advantage" if (attack == "Fire" and defend == "Light") else\
           "advantage" if (attack == "Wind" and defend == "Light") else\
           "advantage" if (attack == "Thunder" and defend == "Light") else\
           "disadvantage" if (attack == "Sword" and defend == "Lance") else\
           "disadvantage" if (attack == "Lance" and defend == "Axe") else\
           "disadvantage" if (attack == "Axe" and defend == "Sword") else\
           "disadvantage" if (attack == "Light" and defend == "Fire") else\
           "disadvantage" if (attack == "Light" and defend == "Thunder") else\
           "disadvantage" if (attack == "Light" and defend == "Wind") else\
           "disadvantage" if (attack == "Wind" and defend == "Fire") else\
           "disadvantage" if (attack == "Fire" and defend == "Thunder") else\
           "disadvantage" if (attack == "Thunder" and defend == "Wind") else\
           "disadvantage" if (attack == "Wind" and defend == "Dark") else\
           "disadvantage" if (attack == "Fire" and defend == "Dark") else\
           "disadvantage" if (attack == "Thunder" and defend == "Dark") else\
           "disadvantage" if (attack == "Dark" and defend == "Light") else\
           "none"


@client.event
async def on_ready():
    print("Bot is ready!")


@client.event
async def on_message(message):
    if message.content.upper().startswith("SESCA, ARE YOU THERE?"):
        user_id = message.author.id
        await client.send_message(message.channel, "<@%s>, you know it! :point_right: :point_right:" % user_id)
        
    if message.content.upper().startswith("S!SAY"):
        args = message.content.split(" ")
        await client.send_message(message.channel, "%s" % (" ".join(args[1:])))

    if message.content.upper().startswith("S!SHEET"):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        sheet_credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        google_client = gspread.authorize(sheet_credentials)
        args = message.content.split(" ")
        name = " ".join(args[1:])
        sheet = google_client.open("SESCA Database").sheet1
        name_list = sheet.row_values(1)
        counter = 1
        full_message = "Who is " + name + "? They aren't in my database..."
        for i in name_list:
            if i == name:
                full_message = ""
                labels = sheet.col_values(1)
                stats = sheet.col_values(counter)
                for j in range(0, len(labels)):
                    full_message += "**" + labels[j] + ":** " + stats[j] + "\n"
                break
            counter = counter + 1
        await client.send_message(message.channel, "%s" % full_message)

    if message.content.upper().startswith("S!STATS"):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        sheet_credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        google_client = gspread.authorize(sheet_credentials)
        args = message.content.split(" ")
        name = " ".join(args[1:])
        sheet = google_client.open("SESCA Database").sheet1
        name_list = sheet.row_values(1)
        counter = 1
        full_message = "Who is " + name + "? They aren't in my database..."
        for i in name_list:
            if i == name:
                full_message = ""
                labels = sheet.col_values(1)
                stats = sheet.col_values(counter)
                for j in [0, 1, 5, 6, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]:
                    full_message += "**" + labels[j] + ":** " + stats[j] + "\n"
                full_message += "**Items:** "
                oxford = False
                for k in [31, 32, 33, 34, 35]:
                    if stats[k] != "":
                        if not oxford:
                            full_message += stats[k]
                            oxford = True
                        else:
                            full_message += ", " + stats[k]
                full_message += "\n**Skills:** "
                oxford = False
                for l in [36, 37, 38, 39, 40, 41, 42, 43, 44]:
                    if stats[l] != "":
                        if not oxford:
                            full_message += stats[l]
                            oxford = True
                        else:
                            full_message += ", " + stats[l]
                full_message += "\n"
                break
            counter = counter + 1
        await client.send_message(message.channel, "%s" % full_message)

    if message.content.upper().startswith("S!BATTLE"):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        sheet_credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        google_client = gspread.authorize(sheet_credentials)
        args = message.content.split(" ")
        sheet = google_client.open("SESCA Database")
        datasheet = sheet.get_worksheet(0)
        weaponsheet = sheet.get_worksheet(1)
        name_list = datasheet.row_values(1)
        weapon_list = weaponsheet.row_values(1)
        full_message = ""
        attacker = args[1]
        defender = args[2]
        attacker_stats = None
        defender_stats = None
        attacker_weapon = ["0"]
        defender_weapon = ["0"]
        counter = 0
        for i in name_list:
            counter = counter + 1
            if i == attacker:
                attacker_stats = datasheet.col_values(counter)
                continue
            if i == defender:
                defender_stats = datasheet.col_values(counter)
                continue
            if attacker_stats is not None and defender_stats is not None:
                break
        if attacker_stats is None:
            full_message = "Who is " + attacker + "? They aren't in my database..."
        if defender_stats is None:
            full_message = "Who is " + defender + "? They aren't in my database..."
        if attacker_stats is not None and defender_stats is not None:
            for w in range(0, len(weapon_list)):
                if weapon_list[w] == attacker_stats[31]:
                    attacker_weapon = weaponsheet.col_values(w+1)
                if weapon_list[w] == defender_stats[31]:
                    defender_weapon = weaponsheet.col_values(w+1)
                if attacker_weapon != ["0"] and defender_weapon != ["0"]:
                    break
            if attacker_weapon != ["0"]:
                if int(attacker_stats[20]) - int(attacker_weapon[4]) < 0:
                    eff_spd_atk = int(attacker_stats[16]) + (int(attacker_stats[20]) - int(attacker_weapon[4]))
                else:
                    eff_spd_atk = int(attacker_stats[16])
                if defender_weapon != ["0"]:
                    if int(defender_stats[20]) - int(defender_weapon[4]) < 0:
                        eff_spd_def = int(defender_stats[16]) + (int(defender_stats[20]) - int(attacker_weapon[4]))
                    else:
                        eff_spd_def = int(defender_stats[16])
                else:
                    eff_spd_def = int(defender_stats[16])
                if attacker_weapon[1] == "Sword" or attacker_weapon[1] == "Lance" or attacker_weapon[1] == "Axe" or \
                   attacker_weapon[1] == "Bow" or attacker_weapon[1] == "Dagger":
                    atk = int(attacker_stats[13]) + int(attacker_weapon[2]) - int(defender_stats[18])
                else:
                    atk = int(attacker_stats[14]) + int(attacker_weapon[2]) - int(defender_stats[19])
                hit = ((int(attacker_stats[15]) * 2) + (int(attacker_stats[17]) / 2) + int(attacker_weapon[3])) - \
                      ((eff_spd_def * 2) + int(defender_stats[17]))
                crit = (int(attacker_stats[15]) / 2) - int(defender_stats[17])
                if defender_weapon != ["0"]:
                    if triangle(attacker_weapon[1], defender_weapon[1]) == "advantage":
                        atk = atk + 1
                        hit = hit + 20
                    elif triangle(attacker_weapon[1], defender_weapon[1]) == "disadvantage":
                        atk = atk - 1
                        hit = hit - 20
                if atk < 0:
                    atk = 0
                if hit < 0:
                    hit = 0
                if crit < 0:
                    crit = 0
                if hit > 100:
                    hit = 100
                if crit > 100:
                    crit = 100
                full_message = "__**Battle Forecast for " + attacker + " vs " + defender + "**__"
                full_message += "\n\n**" + attacker + " initiates with " + attacker_weapon[0] + "**"
                full_message += "\n**Damage Dealt:** " + str(atk)
                full_message += "\n**Chance to Hit:** " + str(int(hit)) + "%"
                full_message += "\n**Chance to Critically Strike:** " + str(int(crit)) + "%"
                if eff_spd_atk - eff_spd_def >= 5:
                    full_message += "\n" + attacker + " has enough speed to attack twice"
                if defender_weapon != ["0"]:
                    full_message += "\n\n**" + defender + " counters with " + defender_weapon[0] + \
                                    " (if within range)**"
                    if defender_weapon[1] == "Sword" or defender_weapon[1] == "Lance" or defender_weapon[1] == "Axe" \
                            or defender_weapon[1] == "Bow" or defender_weapon[1] == "Dagger":
                        atk = int(defender_stats[13]) + int(defender_weapon[2]) - int(attacker_stats[18])
                    else:
                        atk = int(defender_stats[14]) + int(defender_weapon[2]) - int(attacker_stats[19])
                    hit = ((int(defender_stats[15]) * 2) + (int(defender_stats[17]) / 2) + int(defender_weapon[3])) - \
                          ((eff_spd_atk * 2) + int(attacker_stats[17]))
                    crit = (int(defender_stats[15]) / 2) - int(attacker_stats[17])
                    if triangle(defender_weapon[1], attacker_weapon[1]) == "advantage":
                        atk = atk + 1
                        hit = hit + 20
                    elif triangle(defender_weapon[1], attacker_weapon[1]) == "disadvantage":
                        atk = atk - 1
                        hit = hit - 20
                    if atk < 0:
                        atk = 0
                    if hit < 0:
                        hit = 0
                    if crit < 0:
                        crit = 0
                    if hit > 100:
                        hit = 100
                    if crit > 100:
                        crit = 100
                    full_message += "\n**Damage Dealt:** " + str(atk)
                    full_message += "\n**Chance to Hit:** " + str(int(hit)) + "%"
                    full_message += "\n**Chance to Critically Strike:** " + str(int(crit)) + "%"
                    if eff_spd_def - eff_spd_atk >= 5:
                        full_message += "\n" + defender + " has enough speed to attack twice"
            else:
                full_message = attacker + " doesn't seem to have a weapon equipped..."
        await client.send_message(message.channel, "%s" % full_message)

    if message.content.upper().startswith("S!EQUIP"):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        sheet_credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        google_client = gspread.authorize(sheet_credentials)
        args = message.content.split(" ")
        name = args[1]
        weapon = " ".join(args[2:])
        sheet = google_client.open("SESCA Database")
        datasheet = sheet.get_worksheet(0)
        weaponsheet = sheet.get_worksheet(1)
        name_list = datasheet.row_values(1)
        weapon_list = weaponsheet.row_values(1)
        counter = 1
        full_message = "Who is " + name + "? They aren't in my database..."
        for i in name_list:
            if i == name:
                stats = datasheet.col_values(counter)
                for j in weapon_list:
                    if j == weapon:
                        if stats[31] == weapon:
                            full_message = name + " already has their " + weapon + " equipped..."
                            break
                        else:
                            for k in range(32,35):
                                if stats[k] == weapon:
                                    datasheet.update_cell(k+1, counter, stats[31])
                                    datasheet.update_cell(32, counter, weapon)
                                    full_message = name + " now has their " + weapon + " equipped!"
                                    break
                                else:
                                    full_message = name + " doesn't have that in their inventory..."
                        break
                    else:
                        full_message = weapon + " doesn't seem to be a weapon in my database..."
                break
            counter = counter + 1
        await client.send_message(message.channel, "%s" % full_message)


client.run("NDI2MTM1NjM5Mjk4NDA4NDUw.DZWGJg.WbYOBpinNIJpqRM2HFgN2L_KdTE")
