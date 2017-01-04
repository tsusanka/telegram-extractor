# Telegram Extractor

Few scripts to help to analyse the data stored in the official [Telegram Android app](https://github.com/DrKLO/Telegram). Written in Python 3.



## tgnet.dat extractor

Extracts the `files/tgnet.dat` file that contains datacenter's IP addresses, master secrets and other. This script parses the file and prints all the values to standard output.

#### Usage

`python tgnet-extractor.py <path>`

- `<path>` path to the `tgnet.dat` file you need to extract from a mobile phone manually, for example by using _adb_: `adb pull /data/data/org.telegram.messenger.beta`

#### Example

`python tgnet-extractor.py examples/tgnet.dat`



## Message extractor

Extracts messages from the bytes stored in messages.data sqlite column of Telegram.

#### Usage

`python message-extractor.py <path>`

- `<path>` path to the byte file you need to extract manually from the Telegram's sqlite database

#### Example

`python message-extractor.py examples/regular-message-1.dat`



## Encrypted chat info extractor

Extracts info from the bytes stored in enc_chats.data sqlite column of Telegram which contains the secret chat's main auth_key secret and other.

#### Usage

`python encrypted-chat-extractor.py <path>`

- `<path>` path to the byte file you need to extract manually from the Telegram's sqlite database

#### Example

`python encrypted-chat-extractor.py examples/encrypted-chat-info.dat`



## License

Copyright 2016 Tomas Susanka

Licensed under the MIT license.

