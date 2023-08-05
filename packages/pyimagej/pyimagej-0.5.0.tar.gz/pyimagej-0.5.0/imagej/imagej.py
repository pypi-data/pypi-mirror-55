"""
wrapper for imagej and python integration using ImgLyb

"""

# TODO: Unify version declaration to one place.
# https://www.python.org/dev/peps/pep-0396/#deriving
__version__ = '0.5.0'
__author__ = 'Curtis Rueden, Yang Liu, Michael Pinkert'

import os, re
import logging
import scyjava_config
import jnius_config
from pathlib import Path
import numpy

_logger = logging.getLogger(__name__)

# Enable debug logging if DEBUG environment variable is set.
try:
    debug = os.environ['DEBUG']
    if debug:
        _logger.setLevel(logging.DEBUG)
except KeyError as e:
    pass


def _dump_exception(exc):
    if _logger.isEnabledFor(logging.DEBUG) and hasattr(exc, 'stacktrace'):
        _logger.debug("\n\tat ".join([str(e) for e in exc.stacktrace]))


def search_for_jars(ij_dir, subfolder):
    """
    Search and add .jars ile to a list
    :param ij_dir: System path for Fiji.app
    :param subfolder: the folder needs to be searched
    :return: a list of jar files
    """
    jars = []
    for root, dirs, files in os.walk(ij_dir + subfolder):
        for f in files:
            if f.endswith('.jar'):
                path = root + '/' + f
                jars.append(path)
                _logger.debug('Added %s', path)
    return jars


def set_ij_env(ij_dir):
    """
    Create a list of required jars and add to the java classpath

    :param ij_dir: System path for Fiji.app
    :return: num_jar(int): number of jars added
    """
    jars = []
    # search jars directory
    jars.extend(search_for_jars(ij_dir, '/jars'))
    # search plugins directory
    jars.extend(search_for_jars(ij_dir, '/plugins'))
    # add to classpath
    scyjava_config.add_classpath(os.pathsep.join(jars))
    return len(jars)


def init(ij_dir_or_version_or_endpoint=None, headless=True, new_instance=False):
    """
    Initialize the ImageJ environment.

    :param ij_dir_or_version_or_endpoint:
        Path to a local ImageJ installation (e.g. /Applications/Fiji.app),
        OR version of net.imagej:imagej artifact to launch (e.g. 2.0.0-rc-67),
        OR endpoint of another artifact (e.g. sc.fiji:fiji) that uses imagej.
    :param headless: Whether to start the JVM in headless or gui mode.
    :param new_instance: If JVM is already running, setting this parameter to
        True will create a new ImageJ instance.
    :return: an instance of the net.imagej.ImageJ gateway
    """

    global ij

    if jnius_config.vm_running and not new_instance:
        _logger.warning('The JVM is already running.')
        return ij

    if not jnius_config.vm_running:

        if headless:
            scyjava_config.add_options('-Djava.awt.headless=true')

        if ij_dir_or_version_or_endpoint is None:
            # Use latest release of ImageJ.
            _logger.debug('Using newest ImageJ release')
            scyjava_config.add_endpoints('net.imagej:imagej')

        elif os.path.isdir(ij_dir_or_version_or_endpoint):
            # Assume path to local ImageJ installation.
            path = ij_dir_or_version_or_endpoint
            _logger.debug('Local path to ImageJ installation given: %s', path)
            num_jars = set_ij_env(path)
            _logger.info("Added " + str(num_jars + 1) + " JARs to the Java classpath.")
            plugins_dir = str(Path(path, 'plugins'))
            scyjava_config.add_options('-Dplugins.dir=' + plugins_dir)

        elif re.match('^(/|[A-Za-z]:)', ij_dir_or_version_or_endpoint):
            # Looks like a file path was intended, but it's not a folder.
            path = ij_dir_or_version_or_endpoint
            _logger.error('Local path given is not a directory: %s', path)
            return False

        elif ':' in ij_dir_or_version_or_endpoint:
            # Assume endpoint of an artifact.
            endpoint = ij_dir_or_version_or_endpoint
            _logger.debug('Maven coordinate given: %s', endpoint)
            scyjava_config.add_endpoints(endpoint)

        else:
            # Assume version of net.imagej:imagej.
            version = ij_dir_or_version_or_endpoint
            _logger.debug('ImageJ version given: %s', version)
            scyjava_config.add_endpoints('net.imagej:imagej:' + version)

    # Must import imglyb (not scyjava) to spin up the JVM now.
    import imglyb
    from jnius import autoclass

    # Initialize ImageJ.
    ImageJ = autoclass('net.imagej.ImageJ')
    ij = ImageJ()

    # Append some useful utility functions to the ImageJ gateway.

    from scyjava import jclass, isjava, to_java, to_python

    Dataset                  = autoclass('net.imagej.Dataset')
    RandomAccessibleInterval = autoclass('net.imglib2.RandomAccessibleInterval')

    class ImageJPython:
        def __init__(self, ij):
            self._ij = ij

        def dims(self, image):
            """
            Return the dimensions of the equivalent numpy array for the image.  Reverse dimension order from Java.
            """
            if self._is_arraylike(image):
                return image.shape
            if not isjava(image):
                raise TypeError('Unsupported type: ' + str(type(image)))
            if jclass('net.imglib2.Dimensions').isInstance(image):
                return [image.dimension(d) for d in range(image.numDimensions() -1, -1, -1)]
            if jclass('ij.ImagePlus').isInstance(image):
                dims = image.getDimensions()
                dims.reverse()
                dims = [dim for dim in dims if dim > 1]
                return dims
            raise TypeError('Unsupported Java type: ' + str(jclass(image).getName()))

        def new_numpy_image(self, image):
            """
            Creates a numpy image (NOT a Java image)
            dimensioned the same as the given image.
            """
            return numpy.zeros(self.dims(image))

        def rai_to_numpy(self, rai):
            """
            Convert a RandomAccessibleInterval into a numpy array
            """
            result = self.new_numpy_image(rai)
            self._ij.op().run("copy.rai", self.to_java(result), rai)
            return result

        def run_plugin(self, plugin, args=None, ij1_style=True):
            """
            Run an ImageJ plugin
            :param plugin: The string name for the plugin command
            :param args: A dict of macro arguments in key/value pairs
            :param ij1_style: Whether to use implicit booleans in IJ1 style or explicit booleans in IJ2 style
            :return: The plugin output
            """
            macro = self._assemble_plugin_macro(plugin, args=args, ij1_style=ij1_style)
            return self.run_macro(macro)

        def run_macro(self, macro, args=None):
            """
            Run an ImageJ1 style macro script
            :param macro: The macro code
            :param args: Arguments for the script as a dictionary of key/value pairs
            :return:
            """
            try:
                if args is None:
                    return self._ij.script().run("macro.ijm", macro, True).get()
                else:
                    return self._ij.script().run("macro.ijm", macro, True, to_java(args)).get()
            except Exception as exc:
                _dump_exception(exc)
                raise exc

        def run_script(self, language, script, args=None):
            """
            Run a script in an IJ scripting language
            :param language: The file extension for the scripting language
            :param script: A string containing the script code
            :param args: Arguments for the script as a dictionary of key/value pairs
            :return:
            """
            script_lang = self._ij.script().getLanguageByName(language)
            if script_lang is None:
                script_lang = self._ij.script().getLanguageByExtension(language)
            if script_lang is None:
                raise ValueError("Unknown script language: " + language)
            exts = script_lang.getExtensions()
            if exts.isEmpty():
                raise ValueError("Script language '" + script_lang.getLanguageName() + "' has no extensions")
            ext = exts.get(0)
            try:
                if args is None:
                    return self._ij.script().run("script." + ext, script, True).get()
                return self._ij.script().run("script." + ext, script, True, to_java(args)).get()
            except Exception as exc:
                _dump_exception(exc)
                raise exc

        def to_java(self, data):
            """
            Converts the data into a java equivalent.  For numpy arrays, the java image points to the python array
            """
            if self._is_memoryarraylike(data):
                return imglyb.to_imglib(data)
            return to_java(data)

        def to_dataset(self, data):
            """
            Converts the data into a ImageJ Dataset
            """
            try:
                if self._ij.convert().supports(data, Dataset):
                    return self._ij.convert().convert(data, Dataset)
            except Exception as exc:
                _dump_exception(exc)
                raise exc
            raise TypeError('Cannot convert to dataset: ' + str(type(data)))

        def from_java(self, data):
            """
            Converts the data into a python equivalent
            """
            if not isjava(data): return data
            try:
                if self._ij.convert().supports(data, Dataset):
                    # HACK: Converter exists for ImagePlus -> Dataset, but not ImagePlus -> RAI.
                    data = self._ij.convert().convert(data, Dataset)
                if (self._ij.convert().supports(data, RandomAccessibleInterval)):
                    rai = self._ij.convert().convert(data, RandomAccessibleInterval)
                    return self.rai_to_numpy(rai)
            except Exception as exc:
                _dump_exception(exc)
                raise exc
            return to_python(data)

        def show(self, image, cmap=None):
            """
            Display a java or python 2D image.
            :param image: A java or python image that can be converted to a numpy array
            :param cmap: The colormap of the image, if it is not RGB
            :return:
            """
            if image is None:
                raise TypeError('Image must not be None')

            # NB: Import this only here on demand, rather than above.
            # Otherwise, some headless systems may experience errors
            # like "ImportError: Failed to import any qt binding".
            from matplotlib import pyplot

            pyplot.imshow(self.from_java(image), interpolation='nearest', cmap=cmap)
            pyplot.show()

        def _is_arraylike(self, arr):
            return hasattr(arr, 'shape') and \
                hasattr(arr, 'dtype') and \
                hasattr(arr, '__array__') and \
                hasattr(arr, 'ndim')

        def _is_memoryarraylike(self, arr):
            return self._is_arraylike(arr) and \
                hasattr(arr, 'data') and \
                type(arr.data).__name__ == 'memoryview'

        def _assemble_plugin_macro(self, plugin: str, args=None, ij1_style=True):
            """
            Assemble an ImageJ macro string given a plugin to run and optional arguments in a dict
            :param plugin: The string call for the function to run
            :param args: A dict of macro arguments in key/value pairs
            :param ij1_style: Whether to use implicit booleans in IJ1 style or explicit booleans in IJ2 style
            :return: A string version of the macro run
            """
            if args is None:
                    macro = "run(\"{}\");".format(plugin)
                    return macro
            macro = """run("{0}", \"""".format(plugin)
            for key, value in args.items():
                    argument = self._format_argument(key, value, ij1_style)
                    if argument is not None:
                            macro = macro + ' {}'.format(argument)
            macro = macro + """\");"""
            return macro

        def _format_argument(self, key, value, ij1_style):
            if value is True:
                    argument = '{}'.format(key)
                    if not ij1_style:
                            argument = argument + '=true'
            elif value is False:
                    argument = None
                    if not ij1_style:
                            argument = '{0}=false'.format(key)
            elif value is None:
                    raise NotImplementedError('Conversion for None is not yet implemented')
            else:
                    val_str = self._format_value(value)
                    argument = '{0}={1}'.format(key, val_str)
            return argument

        def _format_value(self, value):
            temp_value = str(value).replace('\\', '/')
            if temp_value.startswith('[') and temp_value.endswith(']'):
                    return temp_value
            final_value = '[' + temp_value + ']'
            return final_value

    ij.py = ImageJPython(ij)
    return ij


def imagej_main():
    import sys
    args = []
    for i in range(1, len(sys.argv)):
        args.append(sys.argv[i])
    ij = init(headless='--headless' in args)
    # TODO: Investigate why ij.launch(args) doesn't work.
    ij.ui().showUI()


def help():
    """
    print the instruction for using imagej module

    :return:
    """

    print(("Please set the environment variables first:\n"
           "Fiji.app:   ij_dir = 'your local fiji.app path'\n"
           "Then call init(ij_dir)"))
