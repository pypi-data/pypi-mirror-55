# UQtie

Utilities for Qt

A small set of features to make it easier to use PyQt5. Implements
a repetive pattern for quickly building throwaway or small
Qt applications.

## Getting Started

### Prerequisites

* [PyQt5](https://pypi.org/project/PyQt5/) is obviously required.

The **uqtie** distribution package does not name *PyQt5* as a dependency
because you may have already installed it in some custom way, and
you don't want the **uqtie** installation process to create a redundant
*PyQt5* installation.

If you don't already have it, you can install **PyQt5** by doing this:

```bash
pip install pyqt5
```

Be aware that the appropriate installation procedure for a package can
vary depending on your OS and other factors.

### Installing uqtie

Install the package:

```bash
pip install uqtie
```

Or clone from GitHub:

```bash
git clone https://github.com/langrind/uqtie.git
```

and then run the setup script:

```bash
python setup.py
```

To show **uqtie** in action, run this script (provide relative path of script
in repo for info purposes):

```bash
#!/usr/bin/env python

import argparse, sys

from   uqtie           import UqtWin
from   PyQt5.QtWidgets import QApplication

class TestAppMainWindow(UqtWin.MainWindow):

    def __init__(self, parsedArgs, **kwargs ):
        super(TestAppMainWindow, self).__init__(parsedArgs, **kwargs)
        self.show()

parser = argparse.ArgumentParser()
parser.add_argument('-x', '--test', help='Test Argument placeholder', default='Test')
parsedArgs,unparsedArgs = parser.parse_known_args()

# Pass unparsed args to Qt, might have some X Windows args, like --display
qtArgs = sys.argv[:1] + unparsedArgs
app = QApplication(qtArgs)

mainw = TestAppMainWindow(parsedArgs, app=app, organizationName='Craton', appName='UqtTest')

sys.exit(app.exec_())
```

## Tests

There are no tests yet.

## Deployment

TBS: details about usage in different OS environments

## Contributing

This project is *ad hoc* in nature, so I don't foresee contributions. Nevertheless,
feel free to make a pull request.

## Versioning

Versions are assigned in accordance with [Semantic Versioning](http://semver.org/).
For the versions available, see the [tags on this repository](https://github.com/langrind/uqtie/tags).

## Pronunciation

* "**uqtie**" is pronounced *You Cutie* :heart_eyes:
* "**Uqt**", used as a prefix in the code, rhymes with "duct" 

## Authors

* **[Nik Langrind](https://github.com/langrind)** - *Sole author*

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* I used the **PurpleBooth** [README template](https://github.com/PurpleBooth/a-good-readme-template)
