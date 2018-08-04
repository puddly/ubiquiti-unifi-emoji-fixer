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

    print('Reading config...')
    broken_config = subprocess.check_output(ssh + ['cat /tmp/system.cfg'])
    fixed_config = mutf8_to_utf8(broken_config)

    if fixed_config == broken_config:
        print('Configuration is already OK!')
        sys.exit(0)

    print('Installing new configuration...')
    with subprocess.Popen(ssh + ['cat > /tmp/system.cfg && /usr/bin/syswrapper.sh save-config && reboot'], stdin=subprocess.PIPE) as process:
        process.stdin.write(fixed_config)
