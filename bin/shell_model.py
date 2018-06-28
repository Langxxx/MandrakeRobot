from datetime import datetime, timedelta
from subprocess import SubprocessError
from bin.common import exec_cmd
from common import production


_shell_model = ()
_max_seconds = 3*60


@production
def run(consumer):
    global _shell_model
    _, _, is_first = _shell_model
    if is_first:
        consumer.send('Enable shell model successful. In the next {seconds} seconds,\
        you can run any shell command'.format(seconds=_max_seconds))
    else:
        consumer.send('Enable shell model failure, maybe had enable')
    _shell_model = _shell_model[0], _shell_model[1], False


def setup_shell_model(uid):
    global _shell_model
    if in_shell_model(uid):
        return
    now = datetime.now()
    valid_time = timedelta(seconds=_max_seconds)
    _shell_model = (uid, now+valid_time, True)


def in_shell_model(uid):
    global _shell_model
    if not _shell_model:
        return False

    _uid, valid_time, _ = _shell_model
    now = datetime.now()
    return valid_time > now and _uid == uid


@production
def exec(consumer, message):
    if in_shell_model(message['uid']):
        try:
            consumer.send(exec_cmd(message['text']))
        except SubprocessError as e:
            consumer.send(str(e))
    else:
        consumer.send('Error: shell model was completed')


