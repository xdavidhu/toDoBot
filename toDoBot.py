import discord
import asyncio

toDoDB = []

def newToDo(desc):
    status = True
    tempTodo = [desc, status]
    toDoDB.append(tempTodo)

def doneToDo(id):
    i = 0
    success = False
    for todo in toDoDB:
        i += 1
        if i == id:
            success = True
            i -= 1
            toDoDB.remove(toDoDB[i])
    return success

def listToDo():
    id = 0
    returnList = []
    for todo in toDoDB:
        temptodo = []
        for i in todo:
            temptodo.append(i)
        id += 1
        temptodo.insert(0, id)
        returnList.append(temptodo)
    return returnList

def commandHandler(command):
    if command.startswith("add "):
        command = command.replace("add ", "")
        newToDo(command)
        print("[+] ToDo '" + command + "' added.")

    elif command == "list":
        list = listToDo()
        printline = ""
        for todo in list:
            printline = printline + "[" + str(todo[0]) + "] - " + str(todo[1]) + "\n"
        print("\n" + printline)

    elif command.startswith("done "):
        command = command.replace("done ", "")
        try:
            command = int(command)
        except:
            print("[!] ID needs to be a number!")
            return
        doneToDo(command)
        print("[+] ToDo deleted")

    else:
        print("Command not found...")

# header = "toDoList $> "
# while True:
#     commandHandler(input(header))

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):

    command = str(message.content)

    if command.startswith("/add "):
        command = command.replace("/add ", "")
        if command == "":
            await client.send_message(message.channel, "**[-]** No ToDo entered.")
            print("[-] No ToDo entered.")
        newToDo(command)
        await client.send_message(message.channel, "**[+]** ToDo `" + command + "` added.")
        print("[+] ToDo '" + command + "' added.")
    elif command == "/add":
        await client.send_message(message.channel, "**[-]** Usage: `/add [TODO]`")
        print("**[-]** Usage: `/add [TODO]`")

    elif command == "/todo":
        list = listToDo()
        printline = ""
        for todo in list:
            printline = printline + "**[" + str(todo[0]) + "]** - " + str(todo[1]) + "\n"
        if printline == "":
            printline = "**No ToDo's!**"
        else:
            printline = "**ToDo's:**\n\n" + printline
        await client.send_message(message.channel, printline)
        print(printline)

    elif command.startswith("/done "):
        command = command.replace("/done ", "")
        try:
            command = int(command)
        except:
            await client.send_message(message.channel, '**[!]** ID needs to be a number!')
            print("[!] ID needs to be a number!")
            return
        success = doneToDo(command)
        if success:
            await client.send_message(message.channel, '**[+]** ToDo done.')
            print("[+] ToDo deleted")
        else:
            await client.send_message(message.channel, '**[-]** No ToDo with ID **' + str(command) + '**')
            print('**[-]** No ToDo with ID **' + str(command) + '**')
    elif command == "/done":
        await client.send_message(message.channel, "**[-]** Usage: `/done [ID]`")
        print("**[-]** Usage: `/done [ID]`")

    elif command == "/help":
        printline = "'/todo' - Show the current todo list.\n'/add [TODO]' - Add a new todo.\n'/done [ID]' - Mark a todo done (delete).\n'/help' - Show this menu."
        printline = "**Help menu:**\n" + "```" + printline + "```"
        await client.send_message(message.channel, printline)
        print(printline)

    elif command.startswith("/"):
        printline = "**[-]** Command `" + command + "` not found. Type `/help` for the help menu."
        await client.send_message(message.channel, printline)
        print(printline)

    # else:
    #     await client.send_message(message.channel, '[-] Command not found...')
    #     print("[-] Command not found...")

client.run('token')
