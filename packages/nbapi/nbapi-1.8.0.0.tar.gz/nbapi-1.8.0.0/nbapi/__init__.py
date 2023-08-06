import asyncio,requests,json
from random import randint

#Note: Using this API you are going to be using a API that MAY (unlikely) But MAY send NSFW results.
#If that happens, DM my owner (LazyNeko#5644), or join the Neko Support Server from the website.

#Nothing much yet :3

#                   #-------------------------------------------------#
#                       To join: Copy the below link.  
#                       https://discord.gg/RauzUYK
#                   #--------------------------------------------------#

#You may edit this code to your needs. I dont mind ;3
#TODO: make requests smaller (DONE)
#TODO: make "hug"&"pat" animated&static endpoint! (STARTED STATIC, WILL START ON ANIMATED SOON!)
class api():
    def locked(key,str(api_type)):
        
        url="http://api.neko-bot.net/api/locked/{api_type}"
        headers={"TagKey":f"{key}"}
        r=requests.get(url=url,headers=headers)
        if "403" not in r.status_code:
            return r.text
        if "403" in r.status_code:
            print(f"Invalid token ({key}) was supplied.")
        
class random():
    def anime(source=False):
        if source == False:
            return f"http://neko-bot.net/anime/anime{str(randint(int(1),int(str(requests.get('http://neko-bot.net/info/totalanime.txt').text))))}.png"
        if source == True:
            total=requests.get('http://neko-bot.net/info/totalanime.txt').text
            sources=json.loads(requests.get('http://neko-bot.net/info/anime.json').text)
            animeNum=str(randint(0,int(total)))
            output=[animeNum,sources[f"{animeNum}"]]
            return output
            
            
            
    def neko(source=False):

        if source==False:    
            return f"http://neko-bot.net/nekos/neko{str(randint(int(1),int(str(requests.get('http://neko-bot.net/info/totalnekos.txt').text))))}.png"
        if source==True:
            total=requests.get('http://neko-bot.net/info/totalnekos.txt').text
            sources=json.loads(requests.get('http://neko-bot.net/info/nekos.json').text)
    class pat():
        def static():
            return f"http://neko-bot.net/pats/static/{str(randint(int(1),int(str(requests.get('http://neko-bot.net/info/totalpats.txt').text))))}.png"
        def animated():
            return f"This endpoint is not finished!"
    class hug():
        def animated():
            return "This endpoint is not finished!"
        def static():
            return "This endpoint is not finished!"
class search():
    def neko(num):
        return 'http://neko-bot.net/nekos/neko'+str(num)+'.png'
    def anime(num):
        return 'http://neko-bot.net/posts/post'+str(num)+'.png'
#print(random.pat.static() + random.neko() + random.anime())   #DEBUG
def version():
    return str(open("version.txt","r").read())


