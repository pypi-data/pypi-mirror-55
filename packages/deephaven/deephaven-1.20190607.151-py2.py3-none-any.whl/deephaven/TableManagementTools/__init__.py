#
# Copyright (c) 2016-2019 Deephaven Data Labs and Patent Pending
#

##############################################################################
#               This code is auto generated. DO NOT EDIT FILE!
# Run generatePythonIntegrationStaticMethods or
# "./gradlew :Generators:generatePythonIntegrationStaticMethods" to generate
##############################################################################


import sys
import jpy
import wrapt
from ..conversion_utils import _isJavaType, _isStr

_java_type_ = None  # None until the first defineSymbols() call
_java_file_type_ = None
_iris_config_ = None


def defineSymbols():
    """
    Defines appropriate java symbol, which requires that the jvm has been initialized through the :class:`jpy` module,
    for use throughout the module AT RUNTIME. This is versus static definition upon first import, which would lead to an
    exception if the jvm wasn't initialized BEFORE importing the module.
    """

    if not jpy.has_jvm():
        raise SystemError("No java functionality can be used until the JVM has been initialized through the jpy module")

    global _java_type_, _java_file_type_, _iris_config_
    if _java_type_ is None:
        # This will raise an exception if the desired object is not the classpath
        _java_type_ = jpy.get_type("com.illumon.iris.db.tables.utils.TableManagementTools")
        _java_file_type_ = jpy.get_type("java.io.File")
        _iris_config_ = jpy.get_type("com.fishlib.configuration.Configuration")


# every module method should be decorated with @_passThrough
@wrapt.decorator
def _passThrough(wrapped, instance, args, kwargs):
    """
    For decoration of module methods, to define necessary symbols at runtime

    :param wrapped: the method to be decorated
    :param instance: the object to which the wrapped function was bound when it was called
    :param args: the argument list for `wrapped`
    :param kwargs: the keyword argument dictionary for `wrapped`
    :return: the decorated version of the method
    """

    defineSymbols()
    return wrapped(*args, **kwargs)


@_passThrough
def getFileObject(input):
    """
    Helper function for easily creating a java file object from a path string
    :param input: path string, or list of path strings
    :return: java File object, or java array of File objects
    """

    if _isJavaType(input):
        return input
    elif _isStr(input):
        return _java_file_type_(input)
    elif isinstance(input, list):
        # NB: map() returns an iterator in python 3, so list comprehension is appropriate here
        return jpy.array("java.io.File", [_java_file_type_(el) for el in input])
    else:
        raise ValueError("Method accepts only a java type, string, or list of strings as input. Got {}".format(type(input)))


@_passThrough
def getWorkspaceRoot():
    """
    Helper function for extracting the root directory for the workspace configuration
    """

    return _iris_config_.getInstance().getWorkspacePath()


def _custom_addColumns(*args):
    return _java_type_.addColumns(args[0], getFileObject(args[1]), *args[2:])


def _custom_addGroupingMetadata(*args):
    if len(args) == 1:
        return _java_type_.addGroupingMetadata(getFileObject(args[0]))
    else:
        return _java_type_.addGroupingMetadata(getFileObject(args[0]), *args[1:])


def _custom_deleteTable(path):
    return _java_type_.deleteTable(getFileObject(path))


def _custom_dropColumns(*args):
    return _java_type_.dropColumns(args[0], getFileObject(args[1]), *args[2:])


def _custom_getAllDbDirs(tableName, rootDir, levelsDepth):
    return [el.getAbsolutePath() for el in _java_type_.getAllDbDirs(tableName, getFileObject(rootDir), levelsDepth).toArray()]


def _custom_readTable(*args):
    if len(args) == 1:
        return _java_type_.readTable(getFileObject(args[0]))
    else:
        return _java_type_.readTable(getFileObject(args[0]), *args[1:])


def _custom_renameColumns(*args):
    return _java_type_.renameColumns(args[0], getFileObject(args[1]), *args[2:])


def _custom_updateColumns(currentDefinition, rootDir, levels, *updates):
    return _java_type_.updateColumns(currentDefinition, getFileObject(rootDir), levels, *updates)


def _custom_writeTables(sources, tableDefinition, destinations):
    return _java_type_.writeTables(sources, tableDefinition, getFileObject(destinations))


# Define all of our functionality, if currently possible
try:
    defineSymbols()
except Exception as e:
    pass


@_passThrough
def addColumns(*args):
    return _custom_addColumns(*args)


@_passThrough
def addGroupingMetadata(*args):
    return _custom_addGroupingMetadata(*args)


@_passThrough
def appendToTable(tableToAppend, destDir):
    return _java_type_.appendToTable(tableToAppend, destDir)


@_passThrough
def appendToTables(definitionToAppend, tablesToAppend, destinationDirectoryNames):
    return _java_type_.appendToTables(definitionToAppend, tablesToAppend, destinationDirectoryNames)


@_passThrough
def deleteTable(path):
    return _custom_deleteTable(path)


@_passThrough
def dropColumns(*args):
    return _custom_dropColumns(*args)


@_passThrough
def flushColumnData():
    return _java_type_.flushColumnData()


@_passThrough
def getAllDbDirs(tableName, rootDir, levelsDepth):
    return _custom_getAllDbDirs(tableName, rootDir, levelsDepth)


@_passThrough
def readTable(*args):
    return _custom_readTable(*args)


@_passThrough
def renameColumns(*args):
    return _custom_renameColumns(*args)


@_passThrough
def updateColumns(currentDefinition, rootDir, levels, *updates):
    return _custom_updateColumns(currentDefinition, rootDir, levels, *updates)


@_passThrough
def writeColumn(sourceTable, destinationTable, pendingCount, columnDefinition, currentMapping, currentSize):
    return _java_type_.writeColumn(sourceTable, destinationTable, pendingCount, columnDefinition, currentMapping, currentSize)


@_passThrough
def writeTable(sourceTable, destDir):
    return _java_type_.writeTable(sourceTable, destDir)


@_passThrough
def writeTables(sources, tableDefinition, destinations):
    return _custom_writeTables(sources, tableDefinition, destinations)
