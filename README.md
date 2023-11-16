# XOR cracker with NLP

## Description

This function attempts to decrypt a ciphertext that has been encrypted using the XOR cipher. It operates under the assumption that the key used for encryption is of a specific length and comprises printable ASCII characters. The function iteratively generates all possible keys of the given length and applies each one to decrypt the ciphertext, returning the first readable decrypted text it finds (if any).

Feature:

- uses NLP for filtering meaningful guesses
- will try to guess secret key lengths
- brute forces all possible keys
- can also securely generate an XOR ciphertext
- supports UNIX pipe

## Parameters

```
usage: xornlp [-h] [-d DOWNLOAD_DIR] [-s] [-v | -vv | -q] [-x EXACT_KEY_LENGTH] [-l MIN_KEY_LENGTH] [-u MAX_KEY_LENGTH] [-f OUTPUT_FILE] [{crack,gen}]

positional arguments:
  {crack,gen}

options:
  -h, --help            show this help message and exit
  -d DOWNLOAD_DIR, --download-dir DOWNLOAD_DIR
                        set location to store NLP data downloaded
  -s, --skip-download   skip the NLP data downloaded (assumes data was downloaded already)
  -v, --verbose         set logging level to INFO
  -vv, --debug          set logging level to DEBUG
  -q, --no-logging      disable logging (except for results)
  -x EXACT_KEY_LENGTH, --exact-key-len EXACT_KEY_LENGTH
                        set a known key length, this will be ignored if not provided and a length will be derived from --upper-key-len and --lower-key-len
  -l MIN_KEY_LENGTH, --lower-key-len MIN_KEY_LENGTH
                        set a minimum key length to start cracking from
  -u MAX_KEY_LENGTH, --upper-key-len MAX_KEY_LENGTH
                        set a max key length to stop trying to derive the secret key
  -f OUTPUT_FILE, --dump-enc-file OUTPUT_FILE
                        when using the generate action, set the filename to output the generated ciphertext value (default: stdout)
```

## Basic Usage

**Generate**

Use `xornlp gen -f flag.enc This is a flag` which will prompt for a secret key (e.g. `ctf`), then produce a ciphertext in file `flag.enc`

**Crack**

Use `xornlp crack -v -x 3 flag.enc` to read from ciphertext in file `flag.enc` and set the key length to 3 (for testing) and brute force attack it - to output the flag `This is a flag` and secret key `ctf`.
