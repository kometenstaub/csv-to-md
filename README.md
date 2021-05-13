# CSV to Markdown converter

This script converts every row of all CSV files in the working directory and subdirectories into markdown files according to the formatting settings you choose per column.

This will ***not*** create a Markdown table.

**It is still in early alpha, so please have backups!** At this stage I may still introduce features that will break existing saved settings. When you update, you may need to update them/do the configuration again.

**The encoding with which the files will be opened is UTF-8. Make sure that your CSV files are in that encoding, otherwise they might get screwed up. Again, please have backups**.

I have tested it with Python 3.9.4. (Because I use typing the Python version needs to be at least 3.5, I haven't checked for the other imported packages.)

The Markdown syntax is supposed to support the full range of Markdown formatting which is available within Obsidian. Therefore, it supports some non-standard formatting, which may not work with every Markdown editor.

## Usage

Clone this repo and put the CSV files you want to convert in the same directory.

Run `csv_to_md-file.py` in the terminal *from the directory in which these files are located*.

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

It will let you choose the settings for the first file in the list of CSV files the program creates, so all the CSV files you run it on have to have
the same columns if you want the settings to be applied consistently/if you want it not to fail. (This means that you should only run the script on CSV files with the same number of rows/formatting at once and choose different settings for the next batch.)

`saved_settings.py` is not yet created, but will be. That way your settings won't be overwritten when you `pull` to update. All subsequent saved settings will be appended to this file.

## Example settings

Breaking change 2021/05/13: If you have existing settings from before this version, you will need to surround the corresponding value of 'fileNameCol' with square brackets.

```python
dndnew = {'addYAML': 'y',
 'column': {0: ['h1'],
            1: ['cb'],
            2: ['hl'],
            3: ['ta', 'y', ','],
            4: ['bq'],
            5: ['ml'],
            6: ['st'],
            7: ['mb'],
            8: ['ut']},
 'delimiter': ',',
 'fileNameCol': [0, 1],
 'fileNameColSeparator': ' -- ',
 'fileNameLength': 30}
```

You can create them manually as well, just make sure that all keys shown in the example settings are present. 'fileNameColSeparator' is not needed, if there is only one element in 'fileNameCol'.