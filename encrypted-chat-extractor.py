#!/bin/python
# Describes enc_chats.data
import binascii
import pprint
import click


def hexToStr(byte):
    return binascii.hexlify(byte).decode()


def printByte(label, byte):
    print(label + ': ' + hexToStr(byte))


@click.command()
@click.argument('path')
def extract(path):
    with open(path, 'rb') as f:
        labels = [
            ('constructor', 4),
            ('id', 4),
            ('access_hash', 8),
            ('date', 4),
            ('admin_id', 4),
            ('participant_id', 4),
            ('g_a lengh', 4),
            ('g_a_or_b', 256),
            ('key_fingerprint', 8)
        ]

        for label, count in labels:
            byte = f.read(count)
            printByte(label, byte)


if __name__ == '__main__':
    extract()
