#!/bin/python
# Extracts messages.data into headers and the actual message

import binascii
import pprint
import click


def hexToStr(byte):
	return binascii.hexlify(byte).decode()


def printByte(label, byte):
	print(label + ':\t' + hexToStr(byte))


@click.command()
@click.argument('path')
def extractMessage(path):
	with open(path, 'rb') as f:
		firstLabels = ['constr', 'flags', 'id', 'ttl?', 'from', 'to', 'date?', '??']
		for label in firstLabels:
			byte = f.read(4)
			printByte(label, byte)

		byte = f.read(1)
		messageLength = int.from_bytes(byte, 'little')
		print('length:\t' + hexToStr(byte) + ' (' + str(messageLength) + ')')

		print('message: ')
		byte = f.read(messageLength)
		print('\tbytes: ' + hexToStr(byte))
		print('\tascii: ' + byte.decode('utf-8'))

		finalLabels = ['media', 'magic?', '?', '?']
		for label in finalLabels:
			byte = f.read(4)
			printByte(label, byte)


if __name__ == '__main__':
    extractMessage()
