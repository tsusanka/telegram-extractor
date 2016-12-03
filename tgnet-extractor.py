#!/bin/python
import binascii
import pprint
import click


def hexToStr(byte):
    return binascii.hexlify(byte).decode()


def printByte(indentSize, label, byte):
    print('\t' * indentSize + label + ':\t' + hexToStr(byte))


def indentPrint(indentSize, string):
    print('\t' * indentSize + string)


# Prints the first general headers
def frontHeaders(f):
    labels = [
        ('?', 4),
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
        printByte(0, label, byte)


def parseIPBytes(f):
    numOfIPs = int.from_bytes(f.read(4), 'little') # usually 1
    for i in range(0, numOfIPs):
        IPlength = int.from_bytes(f.read(1), 'little')
        indentPrint(2, 'IP: ')
        if IPlength % 2 == 0: # ? needs to be odd?
            IPlength += 1
        byte = f.read(IPlength)
        indentPrint(3, 'bytes: ' + hexToStr(byte))
        indentPrint(3, 'ascii: ' + byte.decode('utf-8'))
        byte = f.read(4)
        # strange bug, datacenter4 contains two zeros before port for unclear reason
        if (byte == b'\x00\x00\xbb\x01'):
            f.read(2)
            byte = b'\xbb\x01\x00\x00'
        indentPrint(2, 'port: ')
        indentPrint(3, 'bytes: ' + hexToStr(byte))
        indentPrint(3, 'num: ' + str(int.from_bytes(byte, 'little')))


# Prints info about all the datacenters
def datacenters(file, numOfDatacenters):
    for i in range(0, numOfDatacenters):
        print('\nDATACENTER ' + str(i))

        printByte(1, 'configVersion', file.read(4))
        printByte(1, 'dataCenterId', file.read(4))
        printByte(1, 'lastInitVer', file.read(4))

        for ipLabel in ['IPv4', 'IPv6', 'download IPv4', 'download IPv6']:
            print('\taddress ' + ipLabel + ':')
            parseIPBytes(file)

        readAuth(file)
        printByte(1, 'authorized', file.read(4))
        salts(file)


def readAuth(f):
    length = int.from_bytes(f.read(4), 'little') # should be 256
    indentPrint(1, 'auth_key: \t' + hexToStr(f.read(length)))
    indentPrint(1, 'auth_key_id: \t' + hexToStr(f.read(8)))


def salts(f):
    numOfSalts = int.from_bytes(f.read(4), 'little') # usually 1
    indentPrint(1, 'server salts:')
    for i in range(0, numOfSalts):
        printByte(2, 'validSince', f.read(4))
        printByte(2, 'validUntil', f.read(4))
        printByte(2, 'serverSalt', f.read(8))


@click.command()
@click.argument('path')
def extract(path):

    with open(path, 'rb') as file:
        frontHeaders(file)
        numOfDatacenters = int.from_bytes(file.read(4), 'little')
        print('Datacenters ' + '(' + str(numOfDatacenters) + '):')
        datacenters(file, numOfDatacenters)


if __name__ == '__main__':
    extract()
