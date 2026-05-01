# unix-converter

Simple Python tool to convert Unix timestamps in bulk into human-readable format with timezone support.

Built for quick conversion during log analysis and investigations.

## What it does
- Reads a file containing Unix timestamps (one per line)
- Automatically detects format: seconds, milliseconds, microseconds
- Lets you select a timezone
- Converts each timestamp into readable format
- Preserves input order by default
- Optional chronological sorting (--sort)
- Marks invalid lines as ERROR

## Requirements
- Python 3.9+
- No external dependencies (uses built-in zoneinfo)

## Input File
Plain text file with one timestamp per line.

Example:
1715213600
1715213665000
1715213728000000

Invalid lines will be marked as ERROR.
## Usage
```
python3 unix_converter.py -f <input_file>
```

Example:
```
python3 unix_converter.py -f Unix_time.txt
```

Optional sorting:
```
python3 unix_converter.py -f Unix_time.txt --sort
```
## Output
```
RAW                      | FORMAT       | TIMEZONE           | CONVERTED
----------------------------------------------------------------------------------------------------
1715213632.754            | seconds      | Sydney (AEST/AEDT)   | 2024-05-09T10:13:52.754+10:00

1715213633.147            | seconds      | Sydney (AEST/AEDT)   | 2024-05-09T10:13:53.147+10:00
```
## Example output (Default - Preserves Input Order)

<img width="917" height="500" alt="image" src="https://github.com/user-attachments/assets/1bdc5c7a-44ec-4d17-8a29-e29b44803d80" />

## Example output (--sort Enabled - Chronological Order)

<img width="911" height="515" alt="image" src="https://github.com/user-attachments/assets/07d4a663-4186-45a1-bae5-05237c4ae252" />

## Notes
- Default behaviour preserves input order
- --sort enables chronological ordering
- Original values are not modified
- Designed for bulk conversion only (no log parsing)

## Use Case
- Log analysis
- Incident investigation
- Converting large sets of epoch timestamps quickly
