from datetime import datetime, timedelta
from types import NoneType
import discord
from bs4 import BeautifulSoup
from urllib.request import urlopen
from random import randrange
import asyncio
from private.config import Token
from copy import copy

def find_tags(tag : BeautifulSoup):
    return tag.has_attr("data-id") and tag.has_attr("id")

def Get_Slurs():
    page = urlopen("http://www.rsdb.org/full")

    html = page.read().decode(encoding="iso-8859-1")

    soup = BeautifulSoup(html, "html.parser")

    output = soup.find_all(find_tags)
    slurlist = []
    for outputv in output:
        index = 0
        slur = Slur()
        for td in outputv.find_all("td"):
            out = td.string if type(td.string) != NoneType else ""
            if index == 0:
                slur.Slur = out
            elif index == 1:
                slur.Race = out
            elif index == 2:
                slur.Reason = out
            index += 1
        slurlist.append(slur)
    return slurlist

class Slur:

    def __init__(self, Slur="", Race="", Reason="") -> None:
        self.Slur = Slur
        self.Race = Race
        self.Reason = Reason
    
    def __str__(self) -> str:
        return self.Slur + '\n' + self.Race + '\n' + self.Reason
    
    def copy(self):
        return Slur(self.Slur, self.Race, self.Reason)


def copy_list(list : list) -> list:
    cp = []
    for slur in list:
        cp.append(slur.copy())
    return cp

class Client(discord.Client):

    def __init__(self):
        self.slurlist = Get_Slurs()
        intents = discord.Intents.all()
        super().__init__(intents=intents)
        self.Hentais_ID = 500171309641236480
        self.lock = asyncio.Lock()
    
    async def on_ready(self):
        print("We have logged in as {0}".format(self.user))
        await self.Timer()

    async def on_message(self, message):
        if message.content == "$slur":
            channel = message.channel
            slurs = Get_Slurs()
            rand = randrange(len(slurs))
            slurlist = self.SetIndexes(slurs.copy())
            await channel.send(slurlist[rand])
            await self.SetDurgunName(Get_Slurs()[rand])
        elif message.content.startswith("$slur_b"):
            channel = message.channel
            slurlist = self.GetBlackSlurs()
            slurlist = self.SetIndexes(slurlist.copy())
            rand = randrange(len(slurlist))
            string = slurlist[rand].__str__()
            await channel.send(string)
            await self.SetDurgunName(self.GetBlackSlurs()[rand])
        elif message.content == "$slur_n":
            channel = message.channel
            slurlist = self.GetNigSlurs()
            slurlist = self.SetIndexes(slurlist.copy())
            rand = randrange(len(slurlist))
            string = slurlist[rand].__str__()
            await channel.send(string)
        elif message.content == "$slur_nn":
            channel = message.channel
            slurlist = self.GetNigSlurs()
            slurlist = self.SetIndexes(slurlist.copy())
            rand = randrange(len(slurlist))
            string = slurlist[rand].__str__()
            await channel.send(string)
            await self.SetDurgunName(self.GetNigSlurs()[rand])
        elif message.content == "$checktime":
            channel = message.channel
            counter = 0
            async with self.lock:
                counter = copy(self.counter)
            await channel.send(str(counter) + " seconds")
        elif message.content.startswith("$settime"):
            channel = message.channel
            lenth = len("$settime ")
            coppy = 0
            async with self.lock:
                self.timercounter = int(message.content[lenth:])
                coppy = copy(self.timercounter)
            await channel.send("Timer set to " + str(coppy) + " seconds")
    def GetBlackSlurs(self) -> list:
        black = []
        for slur in Get_Slurs():
            if slur.Race == "Blacks":
                black.append(slur)
        return black
    
    def GetNigSlurs(self) -> list:
        nig = []
        for slur in Get_Slurs():
            if ("nig" in slur.Slur.lower()) and (slur.Slur != "Midnight"):
                nig.append(slur)
        return nig
    
    def SetIndexes(self, list1):
        list2 = []
        for slur in list1:
            slur.Slur = "Slur: " + slur.Slur
            slur.Race = "Race: " + slur.Race
            slur.Reason = "Reason: " + slur.Reason
            list2.append(slur)
        return list2
    
    async def SetDurgunName(self, slur : Slur):
        guild = self.get_guild(self.Hentais_ID)
        user = guild.get_member(278335245915389953)
        string = slur.Slur
        await user.edit(nick=string)

    async def Timer(self):
        slurs = self.GetNigSlurs()
        self.timercounter = 43200
        while True:
            self.counter = 0
            while True:
                await asyncio.sleep(1)
                async with self.lock:
                    self.counter += 1
                    if self.counter >= self.timercounter:
                        break
            rand = randrange(len(slurs))
            await self.SetDurgunName(slurs[rand])
            channel = self.get_channel(797367069070983189)
            cp = copy_list(slurs)
            await channel.send(self.SetIndexes(cp)[rand])
            if len(slurs) > 2:
                slurs.pop(rand)
            else:
                slurs = self.GetNigSlurs()


def main():
    client = Client()
    client.run(Token)
if __name__ == "__main__":
    main()