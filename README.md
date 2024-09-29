# 🍭 LFI Finder

![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg) ![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg) ![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg) ![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)

LFI Finder is a Python package designed to help identify Local File Inclusion (LFI) vulnerabilities in web applications.

## Features

- Scans web applications for potential LFI vulnerabilities
- Multi-threaded for fast scanning
- Supports scanning multiple URLs from a file
- Customizable scan parameters

## Installation

To install LFI Finder, run the following command:

```bash
pip install https://github.com/vffuunnyy/lfi-finder/archive/main.zip
```

```bash
pipx install git+https://github.com/vffuunnyy/lfi-finder.git
```

## Usage

```bash
vfny@archlinux ~ > lfinder --help
usage: lfinder [-h] [-u URL] [-o OUTPUT] [-l LIST] [-t THREADS] [-s SLEEPTIME]

LFI Finder Tool

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     Target URL
  -o OUTPUT, --output OUTPUT
                        Output file to save vulnerable endpoints
  -l LIST, --list LIST  File containing target URLs
  -t THREADS, --threads THREADS
                        Number of threads (default: 5)
  -s SLEEPTIME, --sleeptime SLEEPTIME
                        Sleep time between requests (default: 1.5 seconds)
```

To use LFI Finder, simply run the following command:

```bash
lfinder -u http://example.com?page= -t 10 -s 0
```

## LFI List

LFI Finder uses a list of common LFI payloads to scan for potential vulnerabilities. The list can be found in the [lfi_list.txt](lfi_finder/lfi_list.txt) file. The LFI payloads were sourced from [capture0x/LFI-FINDER](https://github.com/capture0x/LFI-FINDER).


## Contributing

We welcome contributions! If you would like to contribute to LFI Finder, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contact

For any questions or suggestions, please open an issue or contact us at [telegram](https://t.me/vffuunnyy).