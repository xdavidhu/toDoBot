import discord
import asyncio

toDoDB = []

def channelDBManager(channel):
    channelExists = False
    for db in toDoDB:
        if db[0] == channel:
            channelExists = True
            currentDB = db[1]

    if not channelExists:
        toDoDB.append([channel, []])
        for db in toDoDB:
            if db[0] == channel:
                currentDB = db[1]
    try:
        return currentDB
    except:
        print("channeldbmanager fatal fail - exiting")
        exit()

def newToDo(desc, channel):
    db = channelDBManager(channel)
    status = True
    tempTodo = [desc, status]
    db.append(tempTodo)

def doneToDo(id, channel):
    db = channelDBManager(channel)
    i = 0
    success = False
    for todo in db:
        i += 1
        if i == id:
            success = True
            db.remove(db[i])
    return success

def listToDo(channel):
    db = channelDBManager(channel)
    id = 0
    returnList = []
    for todo in db:
        temptodo = []
        for i in todo:
            temptodo.append(i)
        id += 1
        temptodo.insert(0, id)
        returnList.append(temptodo)
    return returnList

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):

    channel = str(message.channel.id)

    command = str(message.content)

    if command.startswith("/"):

        print(toDoDB)

        if command.startswith("/add "):
            command = command.replace("/add ", "")
            if command == "":
                await client.send_message(message.channel, ":x: No ToDo entered.")
                print(":x: No ToDo entered.")
            newToDo(command, channel)
            await client.send_message(message.channel, ":white_check_mark: ToDo `" + command + "` added.")
            print(":white_check_mark: ToDo '" + command + "' added.")
        elif command == "/add":
            await client.send_message(message.channel, ":x: Usage: `/add [TODO]`")
            print(":x: Usage: `/add [TODO]`")

        elif command == "/todo":
            list = listToDo(channel)
            printline = ""
            for todo in list:
                printline = printline + "**[" + str(todo[0]) + "]** - " + str(todo[1]) + "\n"
            if printline == "":
                printline = ":metal: **No ToDo's!** :metal:"
            else:
                printline = ":pencil: **ToDo's:** :pencil:\n\n" + printline
            await client.send_message(message.channel, printline)
            print(printline)

        elif command.startswith("/done "):
            command = command.replace("/done ", "")
            try:
                command = int(command)
            except:
                await client.send_message(message.channel, ':x: ID needs to be a number!')
                print(":x: ID needs to be a number!")
                return
            success = doneToDo(command, channel)
            if success:
                await client.send_message(message.channel, ':white_check_mark: ToDo done.')
                print(":white_check_mark: ToDo deleted")
            else:
                await client.send_message(message.channel, ':x: No ToDo with ID **' + str(command) + '**')
                print(':x: No ToDo with ID **' + str(command) + '**')
        elif command == "/done":
            await client.send_message(message.channel, ":x: Usage: `/done [ID]`")
            print(":x: Usage: `/done [ID]`")

        elif command == "/help":
            printline = "'/todo' - Show the current todo list.\n'/add [TODO]' - Add a new todo.\n'/done [ID]' - Mark a todo done (delete).\n'/help' - Show this menu.\nv1.0 by @xdavidhu"
            printline = ":question: **Help menu:** :question:\n" + "```" + printline + "```"
            await client.send_message(message.channel, printline)
            print(printline)

        elif command.startswith("/"):
            printline = ":x: Command `" + command + "` not found. Type `/help` for the help menu."
            await client.send_message(message.channel, printline)
            print(printline)

client.run('YOUR-TOKEN-HERE')
