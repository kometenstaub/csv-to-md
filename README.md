# CSV to Markdown converter

This script converts every row of all CSV files in the working directory and subdirectories into markdown files according to the formatting settings you choose.

This will ***not*** create a Markdown table.

>It is still in early alpha, so please have backups!
>**The encoding with which the files will be opened is UTF-8. Make sure that your CSV files are in that encoding, otherwise they might get screwed up. Again, please have backups**.

I have tested it with Python 3.9.4. (Because I use typing the Python version needs to be at least 3.5, I haven't checked for the other imported packages.)

## Usage

Clone this repo and put the CSV files you want to convert in the same directory.

Run `csv_to_md-file.py` in the terminal.

It will prompt you for your choices.

The outputted Markdown files will appear in the `./data/` subdirectory. (No need to create it, the program takes care of it.)

## Options

You can:

- add everything as YAML frontmatter
- choose the delimiter of your CSV files
- the maximum file name length
- from which column the file name should be generated
- choose the markdown formatting for each column
- write the chosen settings to `saved_settings.py`
- or read settings you set before.

## How it works

It will let you choose the settings for the first file in the list of CSV files, so all the CSV files you run it on have to have
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