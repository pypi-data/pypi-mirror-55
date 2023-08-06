#!python
import time
import argparse
import os.path
from tezos_python.tools import constants, paths, utils
from tezos_python.launchers.sandbox import Sandbox


def scenario(contract, storage, time_between_blocks):
    if contract:
        assert os.path.isfile(contract), f'{contract} is not a file'
    if storage is None:
        storage = 'unit'
    with Sandbox(paths.TEZOS_HOME,
                 constants.IDENTITIES,
                 constants.GENESIS_PK) as sandbox:
        parameters = dict(constants.PARAMETERS)
        parameters["time_between_blocks"] = [str(time_between_blocks), "0"]

        sandbox.add_node(1)
        utils.activate_alpha(sandbox.client(1))
        sandbox.add_baker(1, 'bootstrap5', proto=constants.ALPHA_DEAMON)
        client = sandbox.client(1)
        if contract:
            args = ['--init', storage, '--burn-cap', '10.0']
            sender = 'bootstrap2'
            amount = 0
            client.originate('my_contract', sender, amount, sender,
                             contract, args)
        while 1:
            client.get_head()
            time.sleep(time_between_blocks)


def main():
    # TODO add port parameter
    description = 'run node/baker in sandbox mode (port 18731)'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--time-between-blocks', dest='time_between_blocks',
                        metavar='TIME',
                        help='time between blocks (seconds), default=2',
                        required=False, default='2')
    parser.add_argument('--contract', dest='contract', metavar='CONTRACT',
                        help='path to the contract', required=False)
    parser.add_argument('--storage', dest='storage', metavar='STORAGE',
                        help='initial storage for contract',
                        required=False
                        )
    args = parser.parse_args()
    scenario(args.contract, args.storage, int(args.time_between_blocks))


if __name__ == "__main__":
    main()
