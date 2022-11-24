import subprocess


def ping_web(*ping_and_resource):
    subproc_ping = subprocess.Popen(ping_and_resource, stdout=subprocess.PIPE)
    for line in subproc_ping.stdout:
        line = line.decode('cp866').encode('utf-8')
        print(line.decode('utf-8'))


ping_web('ping', 'yandex.ru')
ping_web('ping', 'youtube.com')
