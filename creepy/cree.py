import discord
import aiohttp
from io import BytesIO
import random
import re
from itertools import islice, cycle

client = discord.Client()

ownerid = "229280523472732160"
prefix = """<<"""
tags = {
"""65wat""" : """http://i.imgur.com/8mK6GsV.png """
,"""Spew""" : """https://cdn.discordapp.com/attachments/190969917216915456/211236395308679169/SPEW.gif """
,"""ohno""" : """https://www.youtube.com/watch?v=kkDMz2ml0gw """
,"""sed""" : """http://stream1.gifsoup.com/view4/20160325/5303059/sr-pelo-crying-o.gif """
,"""El""" : """{if:{args}|=|Papiro|then:<text>|else:⛔ Tag "El {args}" could not be found} """
,"""brony""" : """niggers """
,"""PureJoy""" : """http://vignette2.wikia.nocookie.net/monsterhunter/images/5/52/MHRoC-Savage_Deviljho_Art_001.jpg """
,"""begel""" : """https://cdn.discordapp.com/attachments/155839865240420352/210877656172855297/unknown.png """
,"""JOHNCENA""" : """http://cdn.makeagif.com/media/9-29-2015/ehBR19.gif """
,"""RelicArmorSkinChart""" : """http://i.imgur.com/x5qPipoh.jpg """
,"""mh4uchat""" : """http://s2.quickmeme.com/img/dc/dcfa356e294726a8674f93336fff4ec31d4b8ba9612ef75bdcaf4dd180f9bf66.jpg """
}

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    clientid = (await client.application_info()).id
    print("Invite url")
    print("https://discordapp.com/oauth2/authorize?&client_id={}&scope=bot".format(clientid))


@client.event
async def on_message(message):
    def findUserseverywhere(self, query):
        mentionregex = "<@!?(\d+)>"
        userid = ''
        discrim = None
        if bool(re.search(mentionregex, query)):
            userid = re.findall(mentionregex, query)[0]
            user = discord.utils.get(client.get_all_members(), id=userid)
            return [user]
        elif bool(re.search(r"^.*#\d{4}$", query)):
            discrim = query[-4:]
            query = query[:-5]
        exact = set()
        wrongcase = set()
        startswith = set()
        contains = set()
        lowerquery = query.lower()
        for u in client.get_all_members():
            if discrim is not None and u.discriminator != discrim:
                continue
            if u.name == query:
                exact.add(u)
            elif not exact and u.name.lower() == lowerquery:
                wrongcase.add(u)
            elif not wrongcase and u.name.lower().startswith(lowerquery):
                startswith.add(u)
            elif not startswith and lowerquery in u.name.lower():
                contains.add(u)
        if exact:
            return list(exact)
        if wrongcase:
            return list(wrongcase)
        if startswith:
            return list(startswith)
        return list(contains)


    def findUsers(self, query, server):
        mentionregex = "<@!?(\d+)>"
        userid = ''
        discrim = None
        if bool(re.search(mentionregex, query)):
            userid = re.findall(mentionregex, query)[0]
            user = discord.utils.get(server.members, id=userid)
            return [user]
        elif bool(re.search(r"^.*#\d{4}$", query)):
            discrim = query[-4:]
            query = query[:-5]
        exact = set()
        wrongcase = set()
        startswith = set()
        contains = set()
        lowerquery = query.lower()
        for u in server.members:
            nick = u.display_name
            if discrim is not None and u.discriminator != discrim:
                continue
            if u.name == query or nick == query:
                exact.add(u)
            elif not exact and (u.name.lower() == lowerquery or nick.lower() == lowerquery):
                wrongcase.add(u)
            elif not wrongcase and (u.name.lower().startswith(lowerquery) or nick.lower().startswith(lowerquery)):
                startswith.add(u)
            elif not startswith and (lowerquery in u.name.lower() or lowerquery in nick.lower()):
                contains.add(u)
        if exact:
            return list(exact)
        if wrongcase:
            return list(wrongcase)
        if startswith:
            return list(startswith)
        return list(contains)

    def jagtagparser(content, args):
        def evaluateStatement(statement):
            index = statement.find('|=|')
            if index == -1:
                index = statement.find('|<|')
            if index == -1:
                index = statement.find('|>|')
            if index == -1:
                index = statement.find('|~|')
            if index == -1:
                index = statement.find('|?|')
            if index == -1:
                return False
            s1 = statement[0:index]
            s2 = statement[index + 3:]
            try:
                i1 = float(s1)
                i2 = float(s2)
                if statement[index:index + 3] == "|=|":
                    return i1 == i2
                elif statement[index:index + 3] == "|~|":
                    return i1 * 100 == i2 * 100
                elif statement[index:index + 3] == "|>|":
                    return i1 > i2
                elif statement[index:index + 3] == "|<|":
                    return i1 < i2
            except ValueError:
                if statement[index:index + 3] == "|=|":
                    return s1 == s2
                elif statement[index:index + 3] == "|~|":
                    return s1.lower() == s2.lower()
                elif statement[index:index + 3] == "|>|":
                    return s1 > s2
                elif statement[index:index + 3] == "|<|":
                    return s1 < s2
                elif statement[index:index + 3] == "|?|":
                    return bool(re.search(s2, s1))

        def evaluateMath(statement):
            index = statement.find('|+|')
            if index == -1:
                index = statement.find('|-|')
            if index == -1:
                index = statement.find('|*|')
            if index == -1:
                index = statement.find('|%|')
            if index == -1:
                index = statement.find('|/|')
            if index == -1:
                return statement
            s1 = evaluateMath(statement[0:index])
            s2 = evaluateMath(statement[index + 3:])
            try:
                i1 = float(s1)
                i2 = float(s2)
                if statement[index:index + 3] == "|+|":
                    return str(i1 + i2)
                elif statement[index:index + 3] == "|-|":
                    return str(i1 - i2)
                elif statement[index:index + 3] == "|*|":
                    return str(i1 * i2)
                elif statement[index:index + 3] == "|%|":
                    return str(i1 % i2)
                elif statement[index:index + 3] == "|/|":
                    return str(i1 / i2)
            except ValueError:
                if statement[index:index + 3] == "|+|":
                    return s1 + s2
                elif statement[index:index + 3] == "|-|":
                    loc = s1.find(s2)
                    if loc != -1:
                        return s1[0:loc] + (s1[loc + len(s2)] if loc + len(s2) < len(s1) else "")
                    else:
                        return s1 + '-' + s2
                elif statement[index:index + 3] == "|*|":
                    return s1 + '*' + s2
                elif statement[index:index + 3] == "|%|":
                    return s1 + '%' + s2
                elif statement[index:index + 3] == "|/|":
                    return s1 + '/' + s2

        content = content.replace("{user}", message.author.name).replace("{userid}", message.author.id).replace("{nick}", message.author.display_name).replace("{discrim}", str(message.author.discriminator)).replace("{server}", message.server.name if message.server is not None else "Direct Message").replace("{serverid}", message.server.id if message.server is not None else "0").replace("{servercount}", str(len(message.server.members)) if message.server is not None else "1").replace("{channel}", message.channel.name if message.server is not None else "Direct Message").replace(
            "{channelid}", message.channel.id if message.server is not None else "0").replace("{randuser}", random.choice(list(message.server.members)).display_name if message.server is not None else message.author.display_name).replace("{randonline}", random.choice([m for m in message.server.members if m.status is discord.Status.online]).display_name if message.server is not None else message.author.display_name).replace("{randchannel}", random.choice(list(message.server.channels)).name if message.server is not None else "Direct Message").replace("{args}", " ".join(args)).replace("{argslen}", str(len(args))).replace('{avatar}', message.author.avatar_url)
        output = content
        toEval = ""
        iterations = 0
        lastoutput = ""
        variables = {}
        while lastoutput != output and iterations < 200:
            lastoutput = output
            iterations += 1
            i1 = output.find("}")
            i2 = -1 if i1 == -1 else output.rfind("{", 0, i1)
            if i1 != -1 and i2 != -1:
                toEval = output[i2 + 1:i1]
                if toEval.startswith('length:'):
                    toEval = str(len(toEval[7:]))

                elif toEval.startswith('arg:'):
                    try:
                        argget = int(toEval[4:])
                        if not args:
                            toEval = ""
                        else:
                            toEval = next(
                                islice(cycle(args), argget, argget + 1))
                    except ValueError:
                        pass

                elif toEval.startswith("choose:"):
                    choices = toEval[7:]
                    choices = choices.split('|')
                    toEval = random.choice(choices)

                elif toEval.startswith("if:"):
                    index1 = toEval.find('|then:')
                    index2 = toEval.find('|else:', index1)
                    if index1 != -1 and index2 != -1:
                        statement = toEval[3:index1]
                        sthen = toEval[index1 + 6:index2]
                        selse = toEval[index2 + 6:]
                        if evaluateStatement(statement):
                            toEval = sthen
                        else:
                            toEval = selse

                elif toEval.startswith('range:'):
                    evalrange = toEval[6:]
                    int1, int2 = evalrange.split('|', 1)
                    if int1.isdigit() and int2.isdigit():
                        toEval = str(random.randint(int(int1), int(int2)))

                elif toEval.startswith('upper:'):
                    toEval = toEval[6:]
                    toEval = toEval.upper()

                elif toEval.startswith('lower:'):
                    toEval = toEval[6:]
                    toEval = toEval.lower()

                elif toEval.startswith('replaceregex:'):
                    index1 = toEval.find('|with:')
                    index2 = toEval.find('|in:', index1)

                    if index1 != -1 and index2 != -1:
                        rep = toEval[13:index1]
                        rwith = toEval[index1 + 6:index2]
                        rin = toEval[index2 + 4:]
                        if len(rep) > 0:
                            toEval = re.sub(rep.replace("\u0013", "{").replace(
                                "\u0014", "}"), re.sub("\$(\d+)", "\\\1", rwith), rin)

                elif toEval.startswith('replace:'):
                    index1 = toEval.find('|with:')
                    index2 = toEval.find('|in:', index1)
                    if index1 != -1 and index2 != -1:
                        rep = toEval[8:index1]
                        rwith = toEval[index1 + 6:index2]
                        rin = toEval[index2 + 4:]
                        if len(rep) > 0:
                            toEval = rin.replace(rep, rwith)

                elif toEval.startswith('set:'):
                    variable, stuff = toEval[4:].split('|', 1)
                    variables[variable] = stuff
                    toEval = ''

                elif toEval.startswith('get:'):
                    variable = toEval[4:]
                    toEval = variables.get(variable, '')

                elif toEval.startswith('user:'):
                    query = toEval[5:]
                    if not query:
                        toEval = ""
                    else:
                        users = None
                        if message.server is not None:
                            users = findUsers(
                                query, message.server)
                        if users is None or not users:
                            users = findUserseverywhere(query)
                        if not users:
                            return '⚠ No users found matching "{}"'.format(query)
                        elif len(users) > 1:
                            out = '⚠ Multiple users found matching "{}":'.format(
                                query)
                            for u in users[:6]:
                                out += "\n - {}".format(str(u))
                            if len(users) > 6:
                                out += "\n And {} more...".format(
                                    str(len(users) - 6))
                            return out

                        toEval = users[0].name

                elif toEval.startswith('nick:'):
                    query = toEval[5:]
                    if not query:
                        toEval = ""
                    else:
                        users = None
                        if message.server is not None:
                            users = findUsers(
                                query, message.server)
                        if users is None or not users:
                            users = findUserseverywhere(query)
                        if not users:
                            return '⚠ No users found matching "{}"'.format(query)
                        elif len(users) > 1:
                            out = '⚠ Multiple users found matching "{}":'.format(
                                query)
                            for u in users[:6]:
                                out += "\n - {}".format(str(u))
                            if len(users) > 6:
                                out += "\n And {} more...".format(
                                    str(len(users) - 6))
                            return out

                        toEval = users[0].display_name

                elif toEval.startswith('url:'):
                    toEval = toEval[4:].replace(
                        '-', '--').replace('_', "__").replace('%', '~p').replace('?', '~q').replace(" ", "_")

                elif toEval.startswith('math:'):
                    toEval = evaluateMath(toEval[5:])

                elif toEval.startswith('note:'):
                    toEval = ''

                else:
                    toEval = "\u0013" + toEval + "\u0014"

                output = output[0:i2] + toEval + output[i1 + 1:]
        return output.replace("\u0013", "{").replace("\u0014", "}")

    if message.content.startswith(prefix+'help'):
        fmt = "**{}** commands:\nPrefix: `{}`\n\n".format(client.user.name, prefix) + " ".join('`'+tagname+'`' for tagname in tags)
        if message.author.id == ownerid:
            fmt += "\n\nOwner commands: `setavatar` `setusername` `setgame`"
        await client.send_message(message.channel, fmt)

    elif message.content.startswith(prefix+'setavatar') and message.author.id == ownerid:
        if message.attachments == []:
            url = message.content[len(prefix)+10:]
        else:
            attachment = message.attachments[0]
            url = attachment['url']
        async with aiohttp.get(url) as r:
            await client.edit_profile(avatar=await r.read())
        await client.send_message(message.channel, "Successfully changed avatar!")

    elif message.content.startswith(prefix+'setusername ') and message.author.id == ownerid:
        newname = message.content[len(prefix)+12:]
        await client.edit_profile(username=newname)
        await client.send_message(message.channel, "Successfully changed username!")

    elif message.content.startswith(prefix+'setgame ') and message.author.id == ownerid:
        newgame = message.content[len(prefix)+8:]
        await client.change_status(game=discord.Game(name=newgame))
        await client.send_message(message.channel, "Successfully changed game!")

    elif message.content.startswith(prefix+'about'):
        await client.send_message(message.channel, """This bot was created using **Spectra**'s `makebot` command. It is written in python for the discord.py library.
The template was written by Floretta#7311
The internal command parser utilizes JagTag™ parsing; documentation here: <https://github.com/jagrosh/Spectra/wiki/JagTag>
This parser was designed by jagrosh#4824 and implemented in python by Floretta#7311
Commands are supplied by Spectra's tag database

This bot's owner is: {}""".format(str(discord.utils.get(client.get_all_members(), id=ownerid))))

    elif message.content.startswith(prefix):
        args = message.content[len(prefix):].split()
        for tagname in tags:
            if args[0].lower() == tagname.lower():
                await client.send_message(message.channel, jagtagparser(tags[tagname], args[1:]))




client.run('TOKEN')
