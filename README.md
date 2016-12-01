# Telegram Extractor

Few Python 3 scripts to help analyse the data stored in the official [Telegram Android app](https://github.com/DrKLO/Telegram).

## Message extractor

Extracts messages from the bytes stored in messages.data sqlite column of Telegram.

### Usage

`python message-extractor.py <path>`

- `<path>` path to the byte file you need to extract manually from Telegram's sqlite database

### Example

`python message-extractor.py examples/regular-message-1.dat`


## License

Copyright 2016 Tomas Susanka

Licensed under the MIT license.

