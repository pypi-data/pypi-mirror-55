# -*- coding: utf-8 -*-

import nwae.utils.Log as lg
from inspect import getframeinfo, currentframe


class MexBuiltInTypes:

    MEX_TYPE_FLOAT = 'float'
    MEX_TYPE_INT = 'int'
    # String format and will not remove leading 0's
    MEX_TYPE_NUMBER = 'number'
    # e.g. 10:12:36, 12:15
    MEX_TYPE_TIME = 'time'
    MEX_TYPE_DATETIME = 'datetime'
    # e.g. me@gmail.com
    MEX_TYPE_EMAIL = 'email'
    # Any Latin string
    MEX_TYPE_STR_EN = 'str-en'
    # Any Chinese string
    MEX_TYPE_STR_CN = 'str-zh-cn'

    #
    # Regex Constants
    #
    USERNAME_CHARS = 'a-zA-Z0-9_.-'
    # These characters need to be bracketed if found in mex expressions
    COMMON_REGEX_CHARS = ('*', '+', '[', ']', '{', '}', '|')

    TERM_LEFT = 'left'
    TERM_RIGHT = 'right'

    @staticmethod
    def get_mex_built_in_types():
        #
        # Mapping of regular expressions to data type, you may pass in your custom one at constructor
        #
        return {
            MexBuiltInTypes.MEX_TYPE_FLOAT: {
                MexBuiltInTypes.TERM_LEFT: [
                    # Left of variable expression
                    '.*[^0-9\-]+([+\-]*[0-9]+[.][0-9]*)',
                    # Left of variable expression at the start of sentence
                    '^([+\-]*[0-9]+[.][0-9]*)'
                ],
                MexBuiltInTypes.TERM_RIGHT: [
                    # Right of variable expression
                    '([+\-]*[0-9]+[.][0-9]*).*'
                ]
            },
            MexBuiltInTypes.MEX_TYPE_INT: {
                MexBuiltInTypes.TERM_LEFT: [
                    # Left of variable expression
                    '.*[^0-9\-]+([+\-]*[0-9]+)',
                    # Left of variable expression at the start of sentence
                    '^([+\-]*[0-9]+)'
                ],
                MexBuiltInTypes.TERM_RIGHT: [
                    # Right of variable expression
                    '([+\-]*[0-9]+).*'
                ]
            },
            MexBuiltInTypes.MEX_TYPE_NUMBER: {
                MexBuiltInTypes.TERM_LEFT: [
                    # Left of variable expression
                    '.*[^0-9\-]+([+\-]*[0-9]+)',
                    # Left of variable expression at the start of sentence
                    '^([+\-]*[0-9]+)'
                ],
                MexBuiltInTypes.TERM_RIGHT: [
                    # Right of variable expression
                    '([+\-]*[0-9]+).*'
                ]
            },
            MexBuiltInTypes.MEX_TYPE_TIME: {
                MexBuiltInTypes.TERM_LEFT: [
                    # HHMMSS. Check this first
                    # HHMMSS. Left of variable expression
                    '.*[^0-9]+([0-9]+[:][0-9]+[:][0-9]+)',
                    # HHMMSS. Left of variable expression at the start of sentence
                    '^([0-9]+[:][0-9]+[:][0-9]+)',
                    # HHMM. Check this only after checking HHMMSS
                    # HHMM. Left of variable expression
                    '.*[^0-9]+([0-9]+[:][0-9]+)',
                    # HHMM. Left of variable expression at the start of sentence
                    '^([0-9]+[:][0-9]+)',
                ],
                MexBuiltInTypes.TERM_RIGHT: [
                    # HHMMSS. Right of variable expression
                    '([0-9]+[:][0-9]+[:][0-9]+).*',
                    # HHMM. Right of variable expression
                    '([0-9]+[:][0-9]+).*'
                ]
            },
            MexBuiltInTypes.MEX_TYPE_DATETIME: {
                MexBuiltInTypes.TERM_LEFT: [
                    # "yyyymmdd HHMMSS". Check this first
                    # HHMMSS. Left of variable expression
                    '.*[^0-9]+([0-9]{4}[-]*[0-1][0-9][-*][0-3][0-9][ ]+[0-9]+[:][0-9]+[:][0-9]+)',
                    # "yyyymmdd HHMMSS". Left of variable expression at the start of sentence
                    '^([0-9]{4}[-]*[0-1][0-9][-]*[0-3][0-9][ ]+[0-9]+[:][0-9]+[:][0-9]+)',
                    # "yyyymmdd HHMM". Check this only after checking "yyyymmdd HHMMSS"
                    # "yyyymmdd HHMM". Left of variable expression
                    '.*[^0-9]+([0-9]{4}[-]*[0-1][0-9][-]*[0-3][0-9][ ]+[0-9]+[:][0-9]+)',
                    # "yyyymmdd HHMM". Left of variable expression at the start of sentence
                    '^([0-9]{4}[-]*[0-1][0-9][-]*[0-3][0-9][ ]+[0-9]+[:][0-9]+)',
                    # "yyyymmdd". Left of variable expression
                    '.*[^0-9]+([0-9]{4}[-]*[0-1][0-9][-]*[0-3][0-9])',
                    # "yyyymmdd". Left of variable expression at the start of sentence
                    '^([0-9]{4}[-]*[0-1][0-9][-]*[0-3][0-9])',
                ],
                MexBuiltInTypes.TERM_RIGHT: [
                    # "yyyymmdd HHMMSS". Right of variable expression
                    '([0-9]{4}[-]*[0-1][0-9][-*][0-3][0-9][ ]+[0-9]+[:][0-9]+[:][0-9]+).*',
                    # "yyyymmdd HHMM". Right of variable expression
                    '([0-9]{4}[-]*[0-1][0-9][-*][0-3][0-9][ ]+[0-9]+[:][0-9]+).*',
                    # "yyyymmdd"". Right of variable expression
                    '([0-9]{4}[-]*[0-1][0-9][-*][0-3][0-9]).*',
                ]
            },
            MexBuiltInTypes.MEX_TYPE_EMAIL: {
                MexBuiltInTypes.TERM_LEFT: [
                    # Left of variable expression
                    '.*[^' + MexBuiltInTypes.USERNAME_CHARS + ']+' + '([' + MexBuiltInTypes.USERNAME_CHARS + ']+' + '[@][a-zA-Z0-9]+[.][a-zA-Z]+)',
                    # Left of variable expression at the start of sentence
                    '^([' + MexBuiltInTypes.USERNAME_CHARS + ']+' + '[@][a-zA-Z0-9]+[.][a-zA-Z]+)'
                ],
                MexBuiltInTypes.TERM_RIGHT: [
                    # Right of variable expression
                    # Note that if given math expressions are nothing or '', then
                    # 'email@x.com' will be returned correctly on the left side but
                    # the right side will return 'l@x.com'.
                    # The user needs to choose the right one
                    '([' + MexBuiltInTypes.USERNAME_CHARS + ']+' + '[@][a-zA-Z0-9]+[.][a-zA-Z]+).*'
                ]
            },
            MexBuiltInTypes.MEX_TYPE_STR_EN: {
                MexBuiltInTypes.TERM_LEFT: [
                    # Left of variable expression
                    '.*[^a-zA-Z]+([a-zA-Z]+)',
                    # Left of variable expression at the start of sentence
                    '^([a-zA-Z]+)'
                ],
                MexBuiltInTypes.TERM_RIGHT: [
                    # Right of variable expression
                    '([a-zA-Z]+).*'
                ]
            },
            MexBuiltInTypes.MEX_TYPE_STR_CN: {
                MexBuiltInTypes.TERM_LEFT: [
                    # Left of variable expression
                    '.*[^\u4e00-\u9fff]+([\u4e00-\u9fff]+)',
                    # Left of variable expression at the start of sentence
                    '^([\u4e00-\u9fff]+)'
                ],
                MexBuiltInTypes.TERM_RIGHT: [
                    # Right of variable expression
                    '([\u4e00-\u9fff]+).*'
                ]
            }
        }

    def __init__(self):
        return

