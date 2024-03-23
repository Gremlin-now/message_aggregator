import re
from threading import Thread
from botHandlers import client as bot
from userBotHandlers import client as user, targets


def get_all_history():
    user.start()
    with open("data.jsonline", "a+") as json_file:
        json_file.seek(0)
        file_text = json_file.read()
        for target in targets:
            for msg in user.get_chat_history(target):
                msg_id = str(msg.chat.id) + ":" + str(msg.id)
                if not re.findall(msg_id, file_text):
                    print(msg_id, " - добавлен")
                    json_file.write("\n{\"id\": " + msg_id + "}")
    user.stop()



def main():
    get_all_history()
    print("Message Aggregator started...")
    for thread in [Thread(target=bot.run()), Thread(target=user.run())]:
        thread.daemon = True
        thread.start()


main()
