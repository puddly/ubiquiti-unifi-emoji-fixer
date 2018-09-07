#!/usr/bin/env python3

import sys
import subprocess


def mutf8_to_utf8(mutf8_bytes):
    return mutf8_bytes.decode('utf-8', 'surrogatepass') \
                      .encode('utf-16', 'surrogatepass') \
                      .decode('utf-16') \
                      .encode('utf-8')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'usage: {__file__} [ssh_arguments]')
        sys.exit(1)

    # Pass all the remaining arguments to SSH
    ssh = ['ssh'] + sys.argv[1:]

    # We need to fix both config files
    for filename in ['/etc/aaa1.cfg', '/tmp/system.cfg']:
        print(f'Fixing {filename}...')

        print(' * Reading contents...')
        broken_file = subprocess.check_output(ssh + [f'cat {filename}'])
        fixed_file = mutf8_to_utf8(broken_file)

        if fixed_file == broken_file:
            print(f' * File is already OK!')
            continue

        print(f' * Writing fixed contents...')
        with subprocess.Popen(ssh + [f'cat > {filename}'], stdin=subprocess.PIPE) as process:
            process.stdin.write(fixed_file)

    print('Saving config...')
    subprocess.check_output(ssh + ['/usr/bin/syswrapper.sh save-config'])

    # No need to reboot
    print('Reloading hostapd...')
    subprocess.check_output(ssh + ['pkill -HUP hostapd'])
