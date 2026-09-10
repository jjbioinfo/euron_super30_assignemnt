# File Organiser Python Package

This package organizes the immediate files in a folder by extension. It uses
separate modules for detection, movement, logging, exceptions, and workflow
coordination.

## Structure

```text
file_organiser/
├── __init__.py
├── exceptions.py
├── file_detector.py
├── file_mover.py
├── logging_config.py
├── organizer.py
├── main.py
└── test_file_organiser.py
```

## Default categories

- `Images`: JPG, JPEG, PNG, GIF, BMP, SVG, WEBP
- `Text`: TXT, MD, RTF, LOG
- `Documents`: PDF, DOC, DOCX, PPT, PPTX
- `Data`: CSV, TSV, JSON, XML, XLS, XLSX

Unsupported files remain in the source folder. Missing category folders are
created by default. Duplicate filenames are renamed safely (`photo_1.jpg`,
`photo_2.jpg`) rather than overwritten.

Logging starts at `DEBUG` level and records attempted operations, successful
results, and validation warnings. A complete traceback is recorded once where a
failure is handled. Records are written to the terminal and a rotating log file.

## Run the safe demonstration

From `assignment/week4`:

```bash
python -m file_organiser.main
```

The demo uses a temporary folder and does not modify personal files.

## Organize a real folder

```bash
python -m file_organiser.main /path/to/inbox
```

Optional arguments:

```bash
python -m file_organiser.main /path/to/inbox \
  --output /path/to/organized \
  --duplicate-policy rename \
  --log-file /path/to/file_organiser.log
```

## Run tests

```bash
python -m file_organiser.test_file_organiser
```

The tests cover normal moves, missing sources and destinations, duplicate
policies, unsupported types, mixed-case extensions, permission errors, logging,
and the complete organization workflow.

## Submission links

- GitHub Link: ______________________________
- YouTube Video: ____________________________
