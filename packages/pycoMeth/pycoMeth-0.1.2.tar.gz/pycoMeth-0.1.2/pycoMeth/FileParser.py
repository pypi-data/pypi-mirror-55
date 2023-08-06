# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~IMPORTS~~~~~~~~~~~~~~#
# Standard library imports
import os
from collections import *

# Local imports
from pycoMeth.common import *

#~~~~~~~~~~~~~~CLASS~~~~~~~~~~~~~~#

class FileParser ():
    def __init__ (self,
        fn,
        colnames=False,
        first_line_header=True,
        sep="\t",
        auto_numeric=False,
        include_byte_offset=False,
        dtypes={},
        force_dtypes=False,
        **kwargs):
        """
        Open a parser ++ for field delimited file
        * fn
            Path to a field delimited file
        * colnames
            List of column names to use if not in first file line
        * sep
            field separator
        * auto_numeric
            Try to automatically cast fields values in int or float
        * include_byte_offset
            Add byte offset corresponding to the beginning of each line in the file
        * dtypes
            Dict corresponding to fields (based on colnames) to cast in a given python type
        * force_dtypes
            Raise an error if type casting fails
        * kwargs
            Allow to pass extra options such as verbose, quiet and progress
        """

        # Init logger
        self.log = get_logger (
            name = "pycoMeth_FileParser",
            verbose = kwargs.get("verbose", False),
            quiet = kwargs.get("quiet", False))

        # Save self variables
        self.fn = fn
        self.sep = sep
        self.first_line_header= first_line_header
        self.include_byte_offset = include_byte_offset
        self.auto_numeric = auto_numeric
        self.force_dtypes = force_dtypes

        # Open file
        self.log.debug ("\tOpening file:{}".format(self.fn))
        self.fp = open(fn, "r")
        self.is_open = True
        self.is_closed = False

        # Init extra variables
        self.byte_offset=0
        self.counter = Counter()
        self._current = None
        self._previous = None

        # Define colname depending on options
        if colnames and type(colnames) in (list, tuple):
            self.colnames=colnames
        elif first_line_header:
            self.colnames= self._get_first_line_header()
        else:
            raise ValueError("Invalid column name option")

        # Define custom nammed tuple
        if include_byte_offset:
            self.lt = namedtuple("lt", self.colnames+["byte_offset"])
        else:
            self.lt = namedtuple("lt", self.colnames)

        # Set types to try to cast data in
        self.dtypes_index = self._set_types(dtypes)

    #~~~~~~~~~~~~~~MAGIC AND PROPERTY METHODS~~~~~~~~~~~~~~#

    def __len__ (self):
        return int(os.path.getsize(self.fn))

    def __enter__ (self):
        return self

    def close (self):
        try:
            self.fp.close()
            self.is_open = False
            self.is_closed = True
            self.log.debug ("\tClosing file:{}".format(self.fn))
        except Exception as E:
            print (E)

    def __exit__(self, exception_type, exception_val, trace):
        try:
            self.close()
        except Exception as E:
            print (E)

    def __iter__ (self):
        for line in self.fp:
            self.counter["Lines Parsed"]+=1
            try:
                line = self._parse_line(line)
                self._previous = self._current
                self._current = line
                yield line
            except FileParserError:
                self.counter["Malformed or Invalid Lines"]+=1

    #~~~~~~~~~~~~~~PUBLIC METHODS~~~~~~~~~~~~~~#

    def current_line (self):
        return self._current

    def previous_line (self):
        return self._previous

    def next_line (self):
        if self.byte_offset >= len(self):
            raise StopIteration

        line = self.fp.readline()
        line = self._parse_line(line)
        self._previous = self._current
        self._current = line
        return line

    def get_line (self, byte_offset):
        if byte_offset < 0 or byte_offset >= len(self):
            raise FileParserError("Byte offset is out of valid range [0-{}]".format(len(self)))
        else:
            self.fp.seek(byte_offset, 0)
            self.byte_offset=byte_offset
            return self.next_line()

    def get_lines (self, byte_offset_list):
        ll = []
        for b in byte_offset_list:
            try:
                lt = self.get_line(b)
                ll.append (lt)
            except FileParserError:
                pass
        return ll

    #~~~~~~~~~~~~~~PRIVATE METHODS~~~~~~~~~~~~~~#

    def _get_first_line_header (self):
        header_line = self.fp.readline()
        self.byte_offset+=len(header_line)
        return header_line.rstrip().split(self.sep)

    def _parse_line (self, line):
        line_len = len(line)
        line = line.rstrip().split(self.sep)

        # Return None if the length of the line is inconsistent with the header
        if len(line) != len(self.colnames):
            self.byte_offset+=line_len
            raise FileParserError("Invalid Number of fields found")

        # Try to autocast in int or float
        if self.auto_numeric:
            for i in range(len(line)):
                val = line[i]
                try:
                    line[i] = int(val)
                except ValueError:
                    try:
                        line[i] = float(val)
                    except ValueError:
                        pass

        # Cast values according to provided types
        elif self.dtypes_index:
            for i, dtype in self.dtypes_index.items():
                try:
                    line[i] = dtype(line[i])
                except Exception:
                    if self.force_dtypes:
                        raise FileParserError("Cannot cast field in required type")

        if self.include_byte_offset:
            line.append(self.byte_offset)

        self.byte_offset+=line_len

        # Return nametuple
        return self.lt(*line)

    def _set_types (self, dtypes):
        """"""
        dtypes_index = OrderedDict()
        if dtypes:
            for i, name in enumerate(self.colnames):
                if name in dtypes:
                    dtypes_index[i] = dtypes[name]
        return dtypes_index

class FileParserError (Exception):
    """ Basic exception class for FileParserError """
    pass
