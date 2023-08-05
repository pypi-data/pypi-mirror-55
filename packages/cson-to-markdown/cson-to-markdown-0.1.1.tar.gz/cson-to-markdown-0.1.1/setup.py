# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cson_to_markdown']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.2.1,<0.3.0', 'pyyaml>=5.1,<6.0', 'smart-getenv>=1.1,<2.0']

entry_points = \
{'console_scripts': ['cson_to_markdown = cson_to_markdown:main']}

setup_kwargs = {
    'name': 'cson-to-markdown',
    'version': '0.1.1',
    'description': 'Extracts the markdown section from .cson files.',
    'long_description': '# Cson To Markdown\n\n## What\nRecursively scans given folder for `.cson` files, extracts the metadata and markdown,\nand writes a `.md` file and a `meta/.yml` file.\nWritten specifically for use with [Boostnote](https://github.com/BoostIO/Boostnote).\n\n## Why?\nI write everything in Markdown format because I like the formatting, and my favourite markdown editor so far is Boostnote.\nEverything is stored in a dedicated git repository and pushed whenever changes occur.\nThis works great!\n\n*The problem* though, is that Boostnote stores the file in a `cson` format, without subfolders  and without legible note-titles.\nI wrote something that extracts this information without disturbing the original files, and writes both the markdown and the metadata somewhere else.\nThey\'re created in the subfolder to which they belong in the application, with the note title as filename.\n\n**Caution:** A new version is in the works and will be announced which might completely break this tool.\n\n## How to install\n1. Install the module with `pip`\n`pip install cson-to-markdown`\n\n## How to use\n\n### CLI\nThere\'s 3 arguments that can be provided;\n\n1. The folder with the `.cson` files that need to be converted (looks recursive  in this path for all compatible files).\n1. **Optional** target folder for markdown file output. If no value is provided, they will be stored in the same folder as the `.cson` files.\n1. **Optional** folder containing the `boostnote.json` file. This contains the key-name pairs of the folders defined in the Boostnote aplication itself.\n\n```bash\npython -m cson_to_markdown ~/my/folder/with/cson/files ~/target/folder/optional\n```\n\n### Python:\n```python\nfrom cson_to_markdown import FileConverter\n\n\nconverter = FileConverter("folder/with/cson", "optional/target/folder", "optional/boostnote/settings/dir")\nconverter.convert()\n```\n\n## How to configure\nThere are a few settings that can be configured through environment variables, defined in `cson_to_markdown/config.py`.\nWe will by default first look at an appropriately named environemnt variable, and fall back to the defaults if none were found.\n\nThese are the current settings, which work for the Boostnote use-case specifically.\n```python\n    _config = {\n        "MARKDOWN_START": "content: \'\'\'",\n        "MARKDOWN_END": "\'\'\'",\n        "TITLE_INDICATOR": \'title: "\',\n        "FOLDER_INDICATOR": \'folder: "\',\n        "YAML_STRING_INDICATOR": \'"\',\n        "CSON_EXTENSION": ".cson",\n        "MARKDOWN_EXTENSION": ".md",\n        "METADATA_EXTENSION": ".yml",\n        "METADATA_FOLDER": "meta",\n        "BNOTE_SETTINGS_FILE": "boostnote.json",\n    }\n```\n\nTo overwrite, simply set a new environment variable in your terminal, or add it to your `.bashrc` file:\n`export MARKDOWN_START="new start delimiter"`\n',
    'author': 'Bram Vereertbrugghen',
    'author_email': 'bramvereertbrugghen@live.be',
    'url': 'https://github.com/BramVer/cson-to-markdown',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
