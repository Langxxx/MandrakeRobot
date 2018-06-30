from bin.common import exec_cmd
from common import production
from subprocess import SubprocessError


@production
def run(consumer):
    try:
        rebase_nanfang_cmd = 'git reset --hard && git pull --rebase origin nanfang'
        consumer.send(rebase_nanfang_cmd)
        exec_cmd(rebase_nanfang_cmd)


        update_local_pods = "make update-local-pods"
        consumer.send(update_local_pods)
        consumer.send(exec_cmd(update_local_pods))

        update_bcnetwork = 'cd ../BCNetwork && git checkout nanfang && git pull --rebase origin nanfang'
        consumer.send(update_bcnetwork)
        consumer.send(exec_cmd(update_bcnetwork))

        pod_install_cmd = 'pod install'
        consumer.send(pod_install_cmd)
        consumer.send(exec_cmd(pod_install_cmd))

        beta_enterprise = 'fastlane beta_enterprise'
        consumer.send(beta_enterprise)
        consumer.send(exec_cmd(beta_enterprise, True))

    except SubprocessError as e:
        consumer.send(str(e))
