# Excel Postprocessor ![image info](./pictures/excel_processor.png) 

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Coverage Status](./.github/badges/coverage-badge.svg?dummy=8484744)
![Last Commit Date](./.github/badges/last-commit-badge.svg?dummy=8484744)

---

**Documentation**: [https://github.com/DBMI/ExcelPostprocessor](https://github.com/DBMI/ExcelPostprocessor)

**Source Code**: [https://github.com/DBMI/ExcelPostprocessor](https://github.com/DBMI/ExcelPostprocessor)

---

`Excel Postprocessor`applies Regular Expressions to an existing Excel workbook, extracting data
        into new columns. You must provide an XML configuration file that lists:
1. Name of the Excel workbook to process
2. Sheet(s) and column(s) to be processed
3. Regular Expression to use and the new column(s) to be created.

## Execution
Run the app with:

            excel_postprocess.exe --config <name of config file.xml>
If the config file name is not specified, the app will look for the default file `excel_postprocess.xml`.
The app creates a new Excel workbook for each worksheet to be processed.

## Configuration
### Basic
 Here's an example configuration file:

        <workbook>
            <name>test_data.xlsx</name>
            <sheet>
                <name>Patients</name>
                <source_column>
                    <name>Report</name>
                    <extract>
                        <pattern>Date of Exam:\s?(\d{1,2}/\d{1,2}/\d{4})</pattern>
                        <new_column>Date of Exam</new_column>
                    </extract>
                    <extract>
                        <pattern>LV EF MOD BP:\s?(\d+\.?\d*\s?)%</pattern>
                        <new_column>LV EF %</new_column>
                    </extract>
                </source_column>
            </sheet>
        </workbook>
### Cleaning
To handle errors in text, you can add`<cleaning>`statements to define a regex`replace`statement:

    <workbook>
            <name>test_data.xlsx</name>
            <sheet>
                <name>Patients</name>
                <source_column>
                    <name>Report</name>
                    <cleaning>
                        <pattern>\(MAL</pattern>
                        <replace>\(MLA</replace>
                    </cleaning>
                    <extract>....

Using `<cleaning>`statements can help simplify the matching patterns, since the patterns won't have to accommodate misspelled words.
These`<cleaning>`statements will be executed on the specified column before the`<extract>`statements,
but the _original_ column&mdash;not the modified column&mdash;will be shown in the Excel file that is created. 
### Multiple Patterns
To accommodate multiple styles in free text, you can define several regex patterns for the same source column. This allows several patterns to all result in the same new column. Here's an example:

        <extract>
            <pattern>[D|d]istal to mid stent:?[^\d\.:]{0,50}(Atherosclerosis|atherosclerosis|Concentric|concentric|Eccentric|eccentric|Mild|mild|Scant|scant|Short arc|short arc)[^\d\.:]{0,50}(?:intimal thickening|IT)[^\d\.:]{0,50}\d*\.?\d* *mm</pattern>
            <pattern>[D|d]istal to mid stent:?[^\d\.:]{0,50}(Atherosclerosis|atherosclerosis|Concentric|concentric|Eccentric|eccentric|Mild|mild|Scant|scant|Short arc|short arc)[^\d\.:]{0,50}[^\d\.:]{0,50}\d*\.?\d* *mm(?:intimal thickening|IT)</pattern>
            <pattern>[D|d]istal to mid stent:?[^\d\.:]{0,50}(?:intimal thickening|IT)[^\d\.:]{0,50}(Atherosclerosis|atherosclerosis|Concentric|concentric|Eccentric|eccentric|Mild|mild|Scant|scant|Short arc|short arc)[^\d\.:]{0,50}\d*\.?\d* *mm</pattern>
            <pattern>[D|d]istal to mid stent:?[^\d\.:]{0,50}(Atherosclerosis|atherosclerosis|Concentric|concentric|Eccentric|eccentric|Mild|mild|Scant|scant|Short arc|short arc) (?:LAD|left anterior descending):?[^\d\.:]{0,50}\d*\.?\d* *mm[^\d\.:]{0,50}(?:intimal thickening|IT)</pattern>
            <pattern>(Atherosclerosis|atherosclerosis|Concentric|concentric|Eccentric|eccentric|Mild|mild|Scant|scant|Short arc|short arc)[^\d\.:]{0,50}(?:intimal thickening|IT)[^\d\.:]{0,50}[D|d]istal to mid stent:?[^\d\.:]{0,50}(?:LAD|left anterior descending):?[^\d\.:]{0,50}\d*\.?\d* *mm</pattern>
            <new_column>Distal to mid stent: qualifier</new_column>
        </extract>
This is easier than trying to write a single regex that can allow for keywords to appear in different orders. 
And, instead of writing a separate `<extract>` block for each possible ordering&mdash;each creating its own new column&mdash;
all these variations will be inserted into the same new column. When defining multiple `<pattern>` rules, 
the first one that matches a particular spreadsheet row will be used.
## Installation
To allow its use in secure environments in which `pip install` is unavailable, the app has been compiled into `.exe` form.
Copy `dist/excel_postprocess.zip` to the directory with the target Excel spreadsheet and unpack into the executable file 
`excel_postprocess.exe` and a sample configuration file `excel_postprocess.xml`.
Customize the configuration file `excel_postprocess.xml` to specify the workbook, worksheets and
columns you want to process.

## Development

* Clone this repository
* Requirements:
  * [Poetry](https://python-poetry.org/)
  * Python 3.7+
* Create a virtual environment and install the dependencies

```sh
poetry install
```

* Activate the virtual environment

```sh
poetry shell
```

### Testing

```sh
pytest
```

### Documentation

The documentation is automatically generated from the content of the [docs directory](./docs) and from the docstrings
 of the public signatures of the source code. The documentation is updated and published as a [Github project page
 ](https://pages.github.com/) automatically as part each release.

### Releasing

Trigger the [Draft release workflow](https://github.com/DBMI/ExcelPostprocessor/actions/workflows/draft_release.yml)
(press _Run workflow_). This will update the changelog & version and create a GitHub release which is in _Draft_ state.

Find the draft release from the
[GitHub releases](https://github.com/DBMI/ExcelPostprocessor/releases) and publish it. When
 a release is published, it'll trigger [release](https://github.com/DBMI/ExcelPostprocessor/blob/master/.github/workflows/release.yml) workflow which creates PyPI
 release and deploys updated documentation.

### Pre-commit

Pre-commit hooks run all the auto-formatters (e.g. `black`, `isort`), linters (e.g. `mypy`, `flake8`), and other quality
 checks to make sure the changeset is in good shape before a commit/push happens.

You can install the hooks with (runs for each commit):

```sh
pre-commit install
```

Or if you want them to run only for each push:

```sh
pre-commit install -t pre-push
```

Or if you want e.g. want to run all checks manually for all files:

```sh
pre-commit run --all-files
```

---

This project was generated using the [python-package-cookiecutter](https://github.com/DBMI/python-package-cookiecutter) template, modeled on the [wolt-python-package-cookiecutter](https://github.com/woltapp/wolt-python-package-cookiecutter) template.
