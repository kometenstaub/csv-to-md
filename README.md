# CSV to Markdown converter

This script converts all CSV files in the working directory and subdirectories into markdown files.

## Usage

Clone this repo and put the CSV files you want to convert in the same directory.

Run `csv_to_md-file.py`.

It will prompt you for your choices.

The outputted Markdown files will appear in the ./data/ subdirectory. (No need to create it, the program takes care of it.)

## Options

You can:

- add everything as YAML frontmatter
- choose the delimiter of your CSV files
- the maximum file name length
- from which column the file name should be generated
- write the chosen settings to saved_settings.py
- or read settings you set before.

## How it works

It will let you choose the settings for the first file in the list of CSV files, so all the CSV files you run it on have have
the same columns if you want the settings to be applied consistently/if you want it not to fail.

`saved_settings.py` is not yet created, but will be. All subsequent saved settings will be appended to the file.

## Example settings

```python
save2 = {'addYAML': 'n',
 'column': {0: ['h1'],
            1: ['st'],
            2: ['ma'],
            3: ['ta', 'y', ','],
            4: ['oc'],
            5: ['ml'],
            6: ['ut'],
            7: ['ct'],
            8: ['cb']},
 'delimiter': ',',
 'fileNameCol': 0,
 'fileNameLength': 10}
```

You can create them manually as well, just make sure that all keys shown in the example settings are present.