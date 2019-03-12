"""Loading and executing functions from R packages.

This module defines the interface between R and Python using subprocess.
At the initialization, the toolbox checks if R is available and sets
``cdt.SETTINGS.r_is_available`` to ``True`` if the R framework is detected.
Else, this module is deactivated.

Next, each time an R function is called, the availability of the R package is
tested using the ``DefaultRPackages.check_R_package`` function. The number of
available packages is limited and the list is defined in ``DefaultRPackages``.

If the package is available, the ``launch_R_script`` proceeds to the execution
of the function, by:

1. Copying the R script template and modifying it with the given arguments
2. Copying all the data to a temporary folder in /tmp
3. Launching a R subprocess using the modified template and the data, and
   the script saves the results in a folder in /tmp
4. Retrieving all the results in the Python process and cleaning up all the
   temporary files.

.. MIT License
..
.. Copyright (c) 2018 Diviyan Kalainathan
..
.. Permission is hereby granted, free of charge, to any person obtaining a copy
.. of this software and associated documentation files (the "Software"), to deal
.. in the Software without restriction, including without limitation the rights
.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
.. copies of the Software, and to permit persons to whom the Software is
.. furnished to do so, subject to the following conditions:
..
.. The above copyright notice and this permission notice shall be included in all
.. copies or substantial portions of the Software.
..
.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
.. SOFTWARE.
"""

import os
import warnings
import fileinput
import subprocess
import uuid
from shutil import copy, rmtree


def message_warning(msg, *a, **kwargs):
    """Ignore everything except the message."""
    return str(msg) + '\n'


warnings.formatwarning = message_warning
init = True


class DefaultRPackages(object):
    """Define the R packages that can be imported and checks their availability.

    The attributes define all the R packages that can be imported. Their value
    is initialized to ``None`` ; and as their are called, their availability
    will be checked and their value will be set to either `True` or `False`
    depending on the results. A package already tested (which value is not
    `None`) will not be tested again.

    Attributes:
        pcalg (bool): Availability of the `pcalg` R package
        kpcalg (bool): Availability of the `kpcalg` R package
        bnlearn (bool): Availability of the `bnlearn` R package
        D2C (bool): Availability of the `D2C` R package
        SID (bool): Availability of the `SID` R package
        CAM (bool): Availability of the `CAM` R package
        RCIT (bool): Availability of the `RCIT` R package

    .. warning ::
       The RCIT package is not the original one (github.com/ericstrobl/RCIT)
       but an adaptation made to fit in the PC algorithm, available at:
       https://github.com/Diviyan-Kalainathan/RCIT
    """

    __slots__ = ("init",
                 "pcalg",
                 "kpcalg",
                 "bnlearn",
                 "sparsebn",
                 "D2C",
                 "SID",
                 "CAM",
                 "RCIT",
                 "GENIE3")

    def __init__(self):
        """Init the values of the packages."""
        self.init = True
        self.pcalg = None
        self.kpcalg = None
        self.bnlearn = None
        self.sparsebn = None
        self.D2C = None
        self.SID = None
        self.CAM = None
        self.RCIT = None
        self.GENIE3 = None
        self.init = False

    def __repr__(self):
        """Representation."""
        return str(["{}: {}".format(i, getattr(self, i)) for i in self.__slots__])

    def __str__(self):
        """For print purposes."""
        return str(["{}: {}".format(i, getattr(self, i)) for i in self.__slots__])

    def __getattribute__(self, name):
        """Test if libraries are available on the fly."""
        out = object.__getattribute__(self, name)
        if out is None and not object.__getattribute__(self, 'init'):
            availability = self.check_R_package(name)
            setattr(self, name, availability)
            return availability
        return out

    def check_R_package(self, package):
        """Execute a subprocess to check the package's availability.

        Args:
            package (str): Name of the package to be tested.

        Returns:
            bool: `True` if the package is available, `False` otherwise
        """
        test_package = not bool(launch_R_script("{}/R_templates/test_import.R".format(os.path.dirname(os.path.realpath(__file__))),                                      {"{package}": package}, verbose=True))
        return test_package


def launch_R_script(template, arguments, output_function=None, verbose=True):
    """Launch an R script, starting from a template and replacing text in file
    before execution.

    Args:
        template (str): path to the template of the R script
        arguments (dict): Arguments that modify the template's placeholders
            with arguments
        output_function (function): Function to execute **after** the execution
            of the R script, and its output is returned by this function. Used
            traditionally as a function to retrieve the results of the
            execution.
        verbose (bool): Sets the verbosity of the R subprocess.

    Return:
        Returns the output of the ``output_function`` if not `None`
        else `True` or `False` depending on whether the execution was
        successful.
    """
    id = str(uuid.uuid4())
    os.makedirs('/tmp/cdt_R_script_' + id + '/')
    try:
        scriptpath = '/tmp/cdt_R_script_' + id + '/instance_{}'.format(os.path.basename(template))
        copy(template, scriptpath)

        with fileinput.FileInput(scriptpath, inplace=True) as file:
            for line in file:
                mline = line
                for elt in arguments:
                    mline = mline.replace(elt, arguments[elt])
                print(mline, end='')

        if output_function is None:
            output = subprocess.call("Rscript --vanilla {}".format(scriptpath), shell=True,
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            if verbose:
                process = subprocess.Popen("Rscript --vanilla {}".format(scriptpath), shell=True)
            else:
                process = subprocess.Popen("Rscript --vanilla {}".format(scriptpath), shell=True,
                                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            process.wait()
            output = output_function()

    # Cleaning up
    except Exception as e:
        rmtree('/tmp/cdt_R_script_' + id + '/')
        raise e
    except KeyboardInterrupt:
        rmtree('/tmp/cdt_R_script_' + id + '/')
        raise KeyboardInterrupt
    rmtree('/tmp/cdt_R_script_' + id + '/')
    return output


RPackages = DefaultRPackages()
init = False
