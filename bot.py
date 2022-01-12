TOKEN = "ENTER YOUR TOKEN HERE" # << bot token here :)

import os
try:
  import discord
  from discord import mentions
  from discord.message import Message
except ModuleNotFoundError:
  os.system("pip install discord")
  import discord
  from discord import mentions
  from discord.message import Message
import requests, json, time, discord, datetime, asyncio, random



# FUNCTIONS

def convert_int_in_list(lst):
    new=[]
    for x in lst:
        new.append(int(x))
    return new


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))


def rgb_to_decimal(value):
    return (value[0] * 256 * 256) + (value[1] * 256) + value[2]

def hex_to_decimal(value):
    return rgb_to_decimal(hex_to_rgb(value))

client=discord.Client()

commands = {
  "bot_info":{"Prefix":'"."',"Creator":"TwetyDev#1636","Creator ID":"865505304962662410"},
  "understanding":{"Usage of vocabulary:":"|","c":"means 'channel' or 'create'","cat":"means 'catagory'","rem":"means 'remove'","del":"means 'delete'","w":"means 'webhook'","r":"means 'role'"},
  "channel":{"cc (name|catagory_name[OPTIONAL] or name,another name)":"Creates 1 or more text channels","ccat (name)":"Creates 1 or more catagories","delc (name,another)":"Deletes 1 or more channels","delcat (name)":"Deletes 1 or more catagories"},
  "server_config":{"cr (name)|(admin=true,false)|(color[rgb,decimal,hex])":"Creates a role","dr (name)":"Deletes specified role name","cw (name)":"Creates webhook and returns link"},
  "mass_edit":{"remcfromcat (name)":"Removes all channels in catagory","delallw":"Deletes all webhooks"},
  "destruction":{"$delall":"Deletes all channels & catagories","$delallc":"Delete all channels only","$delallcat":"Deleteall catagories only"}
}

helpcmd = ""

BTOKEN = "Bot " + TOKEN
headers={"authorization":BTOKEN,"content-type":"application/json"}


for command in commands:
    helpcmd += "\n\n"+command.replace("_"," ")+":\n"
    for x in commands[command]:
        helpcmd += ''.join((x," - ",commands[command][x]+"\n"))

@client.event
async def on_ready():
    print(f"Your invite link >> https://discord.com/oauth2/authorize?client_id={client.user.id}&scope=bot&permissions=8")
    print(client.user, "is online.")
    await client.change_presence(activity=discord.Game('".help" for server builders.'))

@client.event
async def on_message(message):
    msg = message.content
    cmd = msg[1:] if msg.startswith(".") else None
    guild = message.guild.id


    # COMMAND RESPONSE
    if cmd!=None:
        c=cmd.lower()
        try:
            fc = cmd.split(" ",1)[1]
        except IndexError:
            pass
        print(cmd)
        if c.startswith("cc "):
            if "," in fc and "|" not in fc:
                for b in fc.split(","):
                    fc = b
                    requests.post(f"https://discord.com/api/guilds/{guild}/channels",headers=headers,data=json.dumps({"type":0,"name":fc,"permission_overwrites":[]}))



            elif "," in fc and "|" in fc:
                parentid = fc.split("|")[1]
                for b in fc.split("|")[0].split(","):
                    fc = b
                    for x in json.loads(requests.get(f"https://discord.com/api/guilds/{guild}/channels",headers=headers).text):
                        if str(x['type'])=="4":
                            if parentid.lower() in x['name'].lower() or parentid.lower()==str(x['id']):
                                r=requests.post(f"https://discord.com/api/guilds/{guild}/channels",headers=headers,data=json.dumps({"type":0,"name":fc.split('|',1)[0],"permission_overwrites":[],"parent_id":str(x['id'])}))
                                break




            else:
                if "|" in fc:
                    for x in json.loads(requests.get(f"https://discord.com/api/guilds/{guild}/channels",headers=headers).text):
                        if str(x['type'])=="4":
                            if fc.split("|",1)[1].lower() in x['name'].lower() or fc.split("|",1)[1].lower()==str(x['id']):
                                requests.post(f"https://discord.com/api/guilds/{guild}/channels",headers=headers,data=json.dumps({"type":0,"name":fc.split('|',1)[0],"permission_overwrites":[],"parent_id":str(x['id'])}))
                                break
                else:
                    requests.post(f"https://discord.com/api/guilds/{guild}/channels",headers=headers,data=json.dumps({"type":0,"name":fc,"permission_overwrites":[]}))
        elif c.startswith("ccat "):
            requests.post(f"https://discord.com/api/guilds/{guild}/channels",headers=headers,data=json.dumps({"type":4,"name":fc,"permission_overwrites":[]}))
        elif c.startswith("delc "):
            for x in json.loads(requests.get(f"https://discord.com/api/guilds/{guild}/channels",headers=headers).text):
                if "," in fc:
                    for b in fc.split(","):
                        if str(x['type'])=="0":
                            if b.lower() in x['name'] or b.lower()==x['id']:
                                requests.delete(f"https://discord.com/api/v9/channels/{x['id']}",headers=headers)
                else:
                    if str(x['type'])=="0":
                        if fc.lower() in x['name'] or fc.lower()==x['id']:
                            requests.delete(f"https://discord.com/api/v9/channels/{x['id']}",headers=headers)
        elif c.startswith("delcat "):
            for x in json.loads(requests.get(f"https://discord.com/api/guilds/{guild}/channels",headers=headers).text):
                if str(x['type'])=="4":
                    if fc.lower() in x['name'] or fc.lower()==x['id']:
                        requests.delete(f"https://discord.com/api/v9/channels/{x['id']}",headers=headers)
        elif c.startswith("cr "):
            name,admin,color=fc.split("|")
            admin = admin.lower()
            if admin == "true":
                admin=True
            else:
                admin=False
            color = color.replace(" ","")
            if "," in color:
                color = rgb_to_decimal(convert_int_in_list(color.split(",")))
            elif "#" in color:
                color = hex_to_decimal(color)
            data = {"name":name,"permissions":"1071698660929" if admin==False else "1071698660937","color":int(color),"hoist":False,"mentionable":False}
            r=requests.post(f"https://discord.com/api/v9/guilds/{guild}/roles",headers=headers,data=json.dumps(data))
        elif c.startswith("dr "):
            for x in json.loads(requests.get(f"https://discord.com/api/guilds/{guild}/roles",headers=headers).text):
                if x['name']!="@everyone":
                    if fc.lower() in x['name'] or fc.lower()==x['id']:
                        requests.delete(f"https://discord.com/api/guilds/{guild}/roles/{x['id']}",headers=headers)

                        
        elif c.startswith("cw "):
            try:
                r=json.loads(requests.post(f"https://discord.com/api/v9/channels/{message.channel.id}/webhooks",headers=headers,data=json.dumps({"name":fc})).text)
                await message.reply("||https://discord.com/api/webhooks/"+r["id"]+"/"+r["token"]+"||")
            except:
                pass
        elif c.startswith("remcfromcat "):
            for x in json.loads(requests.get(f"https://discord.com/api/guilds/{guild}/channels",headers=headers).text):
                if x['parent_id']==fc:
                    requests.delete(f"https://discord.com/api/v9/channels/{x['id']}",headers=headers)
        elif c.startswith("delallw"):
            for x in json.loads(requests.get(f"https://discord.com/api/guilds/{guild}/webhooks",headers=headers).text):
                requests.delete(f"https://discord.com/api/v9/webhooks/{x['id']}",headers=headers)
        elif c=="$delall":
            for x in json.loads(requests.get(f"https://discord.com/api/guilds/{guild}/channels",headers=headers).text):
                requests.delete(f"https://discord.com/api/v9/channels/{x['id']}",headers=headers)
                

        elif c=="$delallc":
            for x in json.loads(requests.get(f"https://discord.com/api/guilds/{guild}/channels",headers=headers).text):
                if str(x['type'])=="0":
                    requests.delete(f"https://discord.com/api/v9/channels/{x['id']}",headers=headers)
        elif c=="$delallcat":
            for x in json.loads(requests.get(f"https://discord.com/api/guilds/{guild}/channels",headers=headers).text):
                if str(x['type'])=="4":
                    requests.delete(f"https://discord.com/api/v9/channels/{x['id']}",headers=headers)






        elif c=="help":
            await message.channel.send("```"+helpcmd+"```")
client.run(TOKEN)
