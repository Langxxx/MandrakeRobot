import time
import re
from bearychat import RTMClient
from rtm_loop import RTMLoop
from bin import beta, bump_version, ls, shell_model, nanfang
from common import cfg


def handle_message(message):
    """parse message

    :message: rmt message
    :returns: TODO

    """
    text = message['text']
    cmd = re.sub('@<=(=[A-Za-z0-9]+)=>', '', text).strip()
    if cmd == 'beta':
        return beta.run
    elif cmd == 'bump_version':
        return bump_version.run
    elif cmd == 'ls':
        return ls.run
    elif cmd == 'nanfang':
        return nanfang.run
    elif cmd == 'shell_model':
        uid = message['uid']
        shell_model.setup_shell_model(uid)
        return shell_model.run


def main():
    # init the rtm client
    client = RTMClient(cfg.get('main', 'rtm_token'), "https://rtm.bearychat.com")

    resp = client.start()  # get rtm user and ws_host
    user = resp["user"]
    ws_host = resp["ws_host"]

    loop = RTMLoop(ws_host)  # init the loop
    loop.start()
    time.sleep(2)

    def message_consumer(message):
        r = ''
        while True:
            text = yield r
            if not text:
                return
            reply = message.refer(text)
            try:
                loop.send(reply)
            except Exception:
                continue

    while True:
        error = loop.get_error()

        if error:
            print(error)
            continue

        message = loop.get_message(True, 5)

        try:
            print("rtm loop received {0} from {1}".format(message["text"],
                                                          message["uid"]))
        except Exception:
            continue

        if message.is_mention_user(user):
            message_produce = handle_message(message)
            message_produce(message_consumer(message))
        elif shell_model.in_shell_model(message['uid']):
            shell_model.exec(message_consumer(message), message)


if __name__ == '__main__':
    main()
