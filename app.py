from threading import Thread
from botHandlers import client as bot
from userBotHandlers import client as user
from functions import save_and_send_all_history


def main():
    save_and_send_all_history(user)
    print("Message Aggregator started...")
    for thread in [Thread(target=bot.run()), Thread(target=user.run())]:
        thread.daemon = True
        thread.start()


main()
