#!/bin/python
import binascii
import pprint
import click
import hashlib


def hexToStr(byte):
	return binascii.hexlify(byte).decode()


def printByte(label, byte):
	print(label + hexToStr(byte))


@click.command()
@click.argument('path')
def fingerprint(path):
	with open(path, 'rb') as f:
		authKey = f.read(256)
		hash = hashlib.sha1(authKey)
		fingerprint = hash.digest()[-8:]
		printByte("0x", fingerprint)
		x = (fingerprint[7] << 56) + ((fingerprint[6] & 0xFF) << 48) + ((fingerprint[5] & 0xFF) << 40) + ((fingerprint[4] & 0xFF) << 32) + ((fingerprint[3] & 0xFF) << 24) + ((fingerprint[2] & 0xFF) << 16) + ((fingerprint[1] & 0xFF) << 8) + (fingerprint[0] & 0xFF)
		print(hex(x))


if __name__ == '__main__':
    fingerprint()
