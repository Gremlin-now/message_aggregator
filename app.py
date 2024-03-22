from threading import Thread
from botHandlers import client as bot
from userBotHandlers import client as user, targets

archive = []


def get_all_history():
    user.start()
    for target in targets:
        for message in user.get_chat_history(target):
            archive.append(message)
    user.stop()
    print(len(archive))

def main():
    get_all_history()
    for thread in [Thread(target=bot.run()), Thread(target=user.run())]:
        thread.daemon = True
        thread.start()


main()
