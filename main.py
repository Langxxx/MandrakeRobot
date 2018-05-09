import time
from bearychat import RTMClient

from rtm_loop import RTMLoop

from build_carthage import move_to_production

def main():
    # init the rtm client
    client = RTMClient("a499bab800daeccfe4099bf0b58f9cf1", "https://rtm.bearychat.com")

    resp = client.start()  # get rtm user and ws_host
    user = resp["user"]
    ws_host = resp["ws_host"]

    loop = RTMLoop(ws_host)  # init the loop
    loop.start()
    time.sleep(2)

    while True:
        error = loop.get_error()

        if error:
            print(error)
            continue

        message = loop.get_message(True, 5)

        if not message or not message.is_chat_message():
            continue
        try:
            print("rtm loop received {0} from {1}".format(message["text"],
                                                          message["uid"]))
        except Exception:
            continue

        if message.is_from(user):
            continue
        try:
            loop.send(message.refer("Pardon?"))
        except Exception:
            continue


if __name__ == '__main__':
    main()
