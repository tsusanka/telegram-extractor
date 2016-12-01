#!/bin/python
# Describes enc_chats.data
import binascii
import pprint
import click


def hexToStr(byte):
	return binascii.hexlify(byte).decode()


def printByte(label, byte):
	print(label + ':\t' + hexToStr(byte))

# Prints the first general headers
def frontHeaders(f):
	labels = [
		('??', 4),
		('configVersion', 4),
		('testBackend', 4),
		('currentDataCenter', 4),
		('currentDataCenterId', 4),
		('timeDifference', 4),
		('lastDcUpdateTime', 4),
		('pushSessionId', 8),
		('regForInternalPush', 4),
		('sessionSize', 4),
		('session', 8),
	]

	for label, count in labels:
		byte = f.read(count)
		printByte(label, byte)


def readIP(f):
	numOfIPs = int.from_bytes(f.read(4), 'little') # usually 1
	for i in range(0, numOfIPs):
		print('\t\tIP: ')
		IPlength = int.from_bytes(f.read(1), 'little')
		if IPlength % 2 == 0: # ??? needs to be odd?
			IPlength += 1
		byte = f.read(IPlength)
		print('\t\t\tbytes: ' + hexToStr(byte))
		print('\t\t\tascii: ' + byte.decode('utf-8'))
		byte = f.read(4)
		print('\t\tport: ')
		print('\t\t\tbytes: ' + hexToStr(byte))
		print('\t\t\tnum: ' + str(int.from_bytes(byte, 'little')))


def readAuth(f):
	length = int.from_bytes(f.read(4), 'little') # should be 256
	print('\n\tauth_key: \t' + hexToStr(f.read(length)))
	print('\tauth_key_id: \t' + hexToStr(f.read(8)))


def salts(f):
	numOfSalts = int.from_bytes(f.read(4), 'little') # usually 1
	print('\n\tserver salts:')
	for i in range(0, numOfSalts):
		printByte('\t\tvalidSince', f.read(4))
		printByte('\t\tvalidUntil', f.read(4))
		printByte('\t\tserverSalt', f.read(8))


# Prints info about all the datacenters
def datacenters(f, numOfDatacenters):
	for i in range(0, numOfDatacenters):
		print('DATACENTER ' + str(i))

		printByte('\tconfigVersion', f.read(4))
		printByte('\tdataCenterId', f.read(4))
		printByte('\tlastInitVer', f.read(4))

		print('\taddress ipv4:')
		readIP(f)
		print('\taddress ipv6:')
		readIP(f)
		print('\taddress-download ipv4:')
		readIP(f)
		print('\taddress-download ipv6:')
		readIP(f)

		readAuth(f)

		printByte('\n\tauthorized', f.read(4))

		salts(f)


@click.command()
@click.argument('path')
def extract(path):
	print("0xb5757299 TRUE")
	print("0x379779bc FALSE")
	print("---------------")
	with open(path, 'rb') as f:

		frontHeaders(f)

		numOfDatacenters = int.from_bytes(f.read(4), 'little')
		print('\nDatacenters ' + '(' + str(numOfDatacenters) + '):')
		datacenters(f, numOfDatacenters)


if __name__ == '__main__':
	extract()
