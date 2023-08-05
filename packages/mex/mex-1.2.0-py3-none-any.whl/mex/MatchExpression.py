# -*- coding: utf-8 -*-

import nwae.utils.Log as lg
from inspect import getframeinfo, currentframe
import re
import nwae.utils.StringUtils as su
import mex.MexBuiltInTypes as mexbuiltin
import pandas as pd


#
# A Layer of Abstraction above Regular Expressions
#
# Human Level Description of extracting parameters from sentence
# WITHOUT technical regular expression syntax.
#
# Higher Level Abstraction to re.match() to extract parameters
# Never allow user to specify their own regex, this is the idea of this
# abstraction or simplification - always keep it simple, support a new
# var type if need.
#
# Language
#   var_1;var_2;var_3;..
# where
#   var_x = <var_name>, <var_type>, <expression_1> / <expression_2> / ..., <direction>
#
# In human level, the above says, "Please extract variable x using <var_name>
# (e.g. email, date, and this variable is of type <var_type> (e.g. float, email,
# time") and expect a person to type words "<expression_1>" or "<expression_2>"...
# when presenting this parameter". Preferred direction is <direction> (left or right),
# default is left.
#
# <var_name> can be anything but must be unique among the variables
# <var_type> can be
#    - int
#    - float
#    - number (string instead of integer and will not remove leading 0's)
#    - time (12:30:55, 23:59)
#    - datetime (20190322 23:59:11, 2019-03-22 23:59, 2019-03-22)
#    - email
#    - str-en (any Latin string)
#    - str-zh-cn (any simplified Chinese string)
#    - str-ko (any Hangul string)
#    - str-th (any Thai string)
#    - str-vi (any Vietnamese string)
# <expression_x> is the word you expect to see before/after the parameter
#
class MatchExpression:
    MEX_OBJECT_VARS_TYPE = 'type'
    MEX_OBJECT_VARS_EXPRESIONS_FOR_LEFT_MATCHING = 'expressions_for_left_matching'
    # This might come with postfixes (e.g. 'is') attached to expressions
    MEX_OBJECT_VARS_EXPRESIONS_FOR_RIGHT_MATCHING = 'expressions_for_right_matching'
    MEX_OBJECT_VARS_PREFERRED_DIRECTION = 'preferred_direction'

    # Separates the different variables definition. e.g. 'm,float,mass&m;c,float,light&speed'
    MEX_VAR_DEFINITION_SEPARATOR = ';'
    # Separates the description of the same variable. e.g. 'm,float,mass&m'
    MEX_VAR_DESCRIPTION_SEPARATOR = ','
    # Separates the names of a variable. e.g. 'mass / m'. Accept either '/' or '&'
    MEX_VAR_EXPRESSIONS_SEPARATORS = ['/','&']

    TERM_LEFT = mexbuiltin.MexBuiltInTypes.TERM_LEFT
    TERM_RIGHT = mexbuiltin.MexBuiltInTypes.TERM_RIGHT

    def __init__(
            self,
            pattern,
            map_vartype_to_regex = None,
            case_sensitive       = False,
            lang                 = None
    ):
        self.pattern = pattern
        self.case_sensitive = case_sensitive
        self.lang = lang
        self.map_vartype_to_regex = map_vartype_to_regex
        if self.map_vartype_to_regex is None:
            self.map_vartype_to_regex = mexbuiltin.MexBuiltInTypes.get_mex_built_in_types()
            lg.Log.debug(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Using default mex built-in types'
            )
        lg.Log.debug(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno) \
            + ': Pattern "' + str(self.pattern) + '", case sensitive = ' + str(self.case_sensitive)
            + ', lang = ' + str(self.lang) + '.'
        )
        #
        # Decode the model variables
        #
        self.mex_obj_vars = self.decode_match_expression_pattern(
            lang = self.lang
        )
        lg.Log.info(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno) \
            + ': Model Object vars: ' + str(self.mex_obj_vars)
        )
        return

    #
    # Extract from string encoding 'm,float,mass&m;c,float,light&speed' into something like:
    #   {
    #      'm': {
    #         'type': 'float',
    #         'names': ['mass', 'm']
    #      },
    #      'c': {
    #         'type': 'float',
    #         'names': ['speed', 'light']
    #      }
    #   }
    #
    def decode_match_expression_pattern(
            self,
            lang
    ):
        try:
            var_encoding = {}

            # Use our own split function that will ignore escaped built-in separator
            # Here we split "m,float,mass&m;c,float,light&speed" into ['m,float,mass&m', 'c,float,light&speed']
            str_encoding = su.StringUtils.split(
                string     = self.pattern,
                split_word = MatchExpression.MEX_VAR_DEFINITION_SEPARATOR
            )
            for unit_mex_pattern in str_encoding:
                unit_mex_pattern = su.StringUtils.trim(unit_mex_pattern)
                if unit_mex_pattern == '':
                    continue
                # Use our own split function that will ignore escaped built-in separator
                # Here we split 'm,float,mass&m' into ['m','float','mass&m']
                var_desc = su.StringUtils.split(
                    string     = unit_mex_pattern,
                    split_word = MatchExpression.MEX_VAR_DESCRIPTION_SEPARATOR
                )

                if len(var_desc) < 3:
                    raise Exception(
                        'Mex pattern must have at least 3 parts, got only ' + str(len(unit_mex_pattern))
                        + ' for unit mex pattern "' + str(unit_mex_pattern)
                        + '" from mex pattern "' + str(self.pattern)
                    )

                part_var_id = su.StringUtils.trim(var_desc[0])
                part_var_type = su.StringUtils.trim(var_desc[1])
                part_var_expressions = su.StringUtils.trim(var_desc[2])
                part_var_preferred_direction = MatchExpression.TERM_LEFT
                if len(var_desc) >= 4:
                    part_var_preferred_direction = su.StringUtils.trim(var_desc[3]).lower()

                expressions_arr_for_left_matching = \
                    MatchExpression.process_expressions_for_var(
                        mex_expressions = part_var_expressions,
                        for_left_or_right_matching = MatchExpression.TERM_LEFT,
                        lang = lang
                    )
                # For right matching, we add common postfixes to expressions
                expressions_arr_for_right_matching = \
                    MatchExpression.process_expressions_for_var(
                        mex_expressions = part_var_expressions,
                        for_left_or_right_matching = MatchExpression.TERM_RIGHT,
                        lang = lang
                    )

                var_encoding[part_var_id] = {
                    # Extract 'float' from ['m','float','mass / m','left']
                    MatchExpression.MEX_OBJECT_VARS_TYPE: part_var_type,
                    # Extract ['mass','m'] from 'mass / m'
                    MatchExpression.MEX_OBJECT_VARS_EXPRESIONS_FOR_LEFT_MATCHING: expressions_arr_for_left_matching,
                    MatchExpression.MEX_OBJECT_VARS_EXPRESIONS_FOR_RIGHT_MATCHING: expressions_arr_for_right_matching,
                    # Extract 'left'
                    MatchExpression.MEX_OBJECT_VARS_PREFERRED_DIRECTION: part_var_preferred_direction
                }
                lg.Log.info(
                    str(MatchExpression.__name__) + ' ' + str(getframeinfo(currentframe()).lineno) \
                    + ': Successfully decoded vars object item "'
                    + str(part_var_id) + '": ' + str(var_encoding[var_desc[0]])
                )
            return var_encoding
        except Exception as ex:
            errmsg = str(MatchExpression.__name__) + ' ' + str(getframeinfo(currentframe()).lineno) \
                     + ': Failed to get var encoding for mex pattern "' \
                     + str(self.pattern) + '". Exception ' + str(ex) + '.'
            lg.Log.error(errmsg)
            raise Exception(errmsg)

    @staticmethod
    def process_expressions_for_var(
            mex_expressions,
            for_left_or_right_matching,
            lang
    ):
        # We try to split by several separators for backward compatibility
        expressions_arr_raw_no_postfix = None
        for exp_sep in MatchExpression.MEX_VAR_EXPRESSIONS_SEPARATORS:
            expressions_arr_raw_no_postfix = su.StringUtils.split(
                string     = mex_expressions,
                split_word = exp_sep
            )
            # TODO Remove this code when we don't need backward compatibility
            #  to support both '&' and '/'. '&' will be removed.
            if len(expressions_arr_raw_no_postfix) > 1:
                break

        expressions_arr_raw = expressions_arr_raw_no_postfix.copy()
        #
        # For right matching, we add common postfixes to expressions
        #
        if for_left_or_right_matching == MatchExpression.TERM_RIGHT:
            postfix_list_for_right_matching = mexbuiltin.MexBuiltInTypes.ALL_EXPRESSION_POSTFIXES
            if lang in mexbuiltin.MexBuiltInTypes.COMMON_EXPRESSION_POSTFIXES.keys():
                postfix_list_for_right_matching = mexbuiltin.MexBuiltInTypes.COMMON_EXPRESSION_POSTFIXES[lang]
            for expr in expressions_arr_raw_no_postfix:
                for postfix in postfix_list_for_right_matching:
                    expressions_arr_raw.append(expr + postfix)

        len_expressions_arr_raw = []
        for i in range(len(expressions_arr_raw)):
            len_expressions_arr_raw.append(len(expressions_arr_raw[i]))

        lg.Log.debug(
            str(MatchExpression.__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Raw Expressions for ' + str(for_left_or_right_matching) + ' matching: '
            + str(expressions_arr_raw)
        )

        #
        # Now we need to sort by longest to shortest.
        # Longer names come first
        # If we had put instead "이름 / 이름은", instead of detecting "김미소", it would return "은" instead
        # 'mex': 'kotext, str-ko, 이름은 / 이름   ;'
        #
        expressions_arr = expressions_arr_raw
        if len(expressions_arr_raw) > 1:
            try:
                df_expressions = pd.DataFrame({
                    'expression': expressions_arr_raw,
                    'len': len_expressions_arr_raw
                })
                df_expressions = df_expressions.sort_values(by=['len'], ascending=False)
                expressions_arr = df_expressions['expression'].tolist()
                lg.Log.debug(
                    str(MatchExpression.__name__) + ' ' + str(getframeinfo(currentframe()).lineno) \
                    + ': Sorted ' + str(expressions_arr_raw) + ' to ' + str(expressions_arr)
                )
            except Exception as ex_sort:
                lg.Log.error(
                    str(MatchExpression.__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
                    + ': Failed to sort ' + str(expressions_arr_raw) + ', len arr ' + str(len_expressions_arr_raw)
                    + '. Exception ' + str(ex_sort) + '.'
                )
                expressions_arr = expressions_arr_raw

        corrected_expressions_arr = []
        # Bracket characters that are common regex key characters,
        # as they are inserted into regex later on
        for expression in expressions_arr:
            expression = su.StringUtils.trim(expression)
            corrected_expression = ''
            #
            # We now need to escape common characters found in regex patterns
            # if found in the expression. So that when inserted into regex patterns,
            # the expression will retain itself.
            #
            for i in range(len(expression)):
                if expression[i] in mexbuiltin.MexBuiltInTypes.COMMON_REGEX_CHARS:
                    corrected_expression = corrected_expression + '[' + expression[i] + ']'
                else:
                    corrected_expression = corrected_expression + expression[i]
            corrected_expressions_arr.append(corrected_expression)

        return corrected_expressions_arr

    #
    # Extract variables from string
    #
    def extract_variable_values(
            self,
            sentence
    ):
        lg.Log.debug(
            str(MatchExpression.__name__) + ' ' + str(getframeinfo(currentframe()).lineno) \
            + ': Extracting vars from "' + str(sentence) + '", using mex encoding ' + str(self.mex_obj_vars)
        )

        var_values = {}

        # Look one by one
        for var in self.mex_obj_vars.keys():
            # Left and right values
            var_values[var] = (None, None)
            # Get the names and join them using '|' for matching regex
            var_expressions_for_left_matching = \
                '|'.join(self.mex_obj_vars[var][MatchExpression.MEX_OBJECT_VARS_EXPRESIONS_FOR_LEFT_MATCHING])
            var_expressions_for_right_matching = \
                '|'.join(self.mex_obj_vars[var][MatchExpression.MEX_OBJECT_VARS_EXPRESIONS_FOR_RIGHT_MATCHING])

            data_type = self.mex_obj_vars[var][MatchExpression.MEX_OBJECT_VARS_TYPE]

            #
            # Default to search the front value first
            # TODO Make this more intelligent
            #
            value_left = self.get_var_value(
                sentence        = sentence,
                var_name        = var,
                var_expressions = var_expressions_for_left_matching,
                data_type       = data_type,
                left_or_right   = MatchExpression.TERM_LEFT
            )
            value_right = self.get_var_value(
                sentence        = sentence,
                var_name        = var,
                var_expressions = var_expressions_for_right_matching,
                data_type       = data_type,
                left_or_right   = MatchExpression.TERM_RIGHT
            )

            if value_left or value_right:
                lg.Log.debug(
                    str(MatchExpression.__name__) + ' ' + str(getframeinfo(currentframe()).lineno) \
                    + ': For var "' + str(var) + '" found values ' + str([value_left, value_right])
                )
                try:
                    if data_type not in self.map_vartype_to_regex.keys():
                        raise Exception('Unrecognized type "' + str(data_type) + '".')
                    elif data_type == mexbuiltin.MexBuiltInTypes.MEX_TYPE_INT:
                        if value_left:
                            value_left = int(value_left)
                        if value_right:
                            value_right = int(value_right)
                        var_values[var] = (value_left, value_right)
                    elif data_type == mexbuiltin.MexBuiltInTypes.MEX_TYPE_FLOAT:
                        if value_left:
                            value_left = float(value_left)
                        if value_right:
                            value_right = float(value_right)
                        var_values[var] = (value_left, value_right)
                    else:
                        if value_left:
                            value_left = str(value_left)
                        if value_right:
                            value_right = str(value_right)
                        var_values[var] = (value_left, value_right)
                except Exception as ex_int_conv:
                    errmsg = str(MatchExpression.__name__) + ' ' + str(getframeinfo(currentframe()).lineno) \
                             + ': Failed to extract variable "' + str(var) \
                             + '" from sentence "' + str(sentence) \
                             + '". Exception ' + str(ex_int_conv) + '.'
                    lg.Log.warning(errmsg)

        lg.Log.debug(
            str(MatchExpression.__name__) + ' ' + str(getframeinfo(currentframe()).lineno) \
            + ': For sentence "' + str(sentence) + '" var values ' + str(var_values)
        )

        return var_values

    def get_var_value_regex(
            self,
            sentence,
            patterns_list,
            var_name
    ):
        lg.Log.debug(
            str(MatchExpression.__name__) + ' ' + str(getframeinfo(currentframe()).lineno) \
            + ': For var "' + str(var_name)
            + '" using match patterns list ' + str(patterns_list)
        )
        if patterns_list is None:
            lg.Log.error(
                str(MatchExpression.__name__) + ' ' + str(getframeinfo(currentframe()).lineno) \
                + ': No patterns list provided for string "' + str(sentence)
                + '", var name "' + str(var_name) + '".'
            )
            return None

        for pattern in patterns_list:
            m = re.match(pattern=pattern, string=sentence)
            if m:
                lg.Log.debug(
                    str(MatchExpression.__name__) + ' ' + str(getframeinfo(currentframe()).lineno) \
                    + ': For var "' + str(var_name) + '" using pattern "' + str(pattern)
                    + '", found groups ' + str(m.groups())
                )
                return m
        return None

    def get_pattern_list(
            self,
            data_type,
            var_expressions,
            left_or_right
    ):
        if not self.case_sensitive:
            var_expressions = var_expressions.lower()

        patterns_list = []
        try:
            fix_list = self.map_vartype_to_regex[data_type][left_or_right]
            for pat in fix_list:
                if left_or_right == MatchExpression.TERM_LEFT:
                    patterns_list.append(
                        pat + '[ ]*(' + str(var_expressions) + ').*'
                    )
                else:
                    patterns_list.append(
                        '.*(' + var_expressions + ')[ ]*' + pat
                    )
            return patterns_list
        except Exception as ex:
            errmsg = str(MatchExpression.__class__) + ' ' + str(getframeinfo(currentframe()).lineno) \
                     + ': Exception "' + str(ex) \
                     + '" getting ' + str(left_or_right) + ' pattern list for var expressions "' \
                     + str(var_expressions) + '", data type "' + str(data_type) + '".'
            lg.Log.error(errmsg)
            raise Exception(errmsg)

    def get_var_value(
            self,
            sentence,
            var_name,
            var_expressions,
            data_type,
            left_or_right
    ):
        var_expressions = var_expressions.lower()

        #
        # If no expressions are specified, then there is no need to match
        # the right side, as we are only looking for the regex, and this is
        # handled correctly on the left side but not on the right side.
        # For example if we are looking for an email 'email@gmail.com', the
        # right side will return only 'l@gmail.com'
        #
        if left_or_right == MatchExpression.TERM_RIGHT:
            if var_expressions == '':
                return None

        try:
            patterns_list = self.get_pattern_list(
                data_type       = data_type,
                var_expressions = var_expressions,
                left_or_right   = left_or_right
            )
        except Exception as ex:
            errmsg = str(MatchExpression.__class__) + ' ' + str(getframeinfo(currentframe()).lineno) \
                     + ': Exception "' + str(ex) \
                     + '" getting ' + str(left_or_right) + ' pattern list for var name "' + str(var_name) \
                     + '", sentence "' + str(sentence) + '", var expressions "' + str(var_expressions) \
                     + '", data type "' + str(data_type) + '".'
            lg.Log.error(errmsg)
            return None

        m = self.get_var_value_regex(
            sentence      = sentence,
            patterns_list = patterns_list,
            var_name      = var_name
        )

        group_position = 1
        if left_or_right == MatchExpression.TERM_RIGHT:
            group_position = 2

        if m:
            if len(m.groups()) >= group_position:
                return m.group(group_position)
            else:
                warn_msg = \
                    str(MatchExpression.__class__) + ' ' + str(getframeinfo(currentframe()).lineno) \
                    + ': For ' + str(left_or_right) + ' match, expected at least ' + str(group_position) \
                    + ' match groups for var name "' + str(var_name) \
                    + '", string "' + str(sentence) + '", var expressions "' + str(var_expressions) \
                    + '", data type "' + str(data_type) + '" but got groups ' + str(m.groups()) + '.'
                lg.Log.warning(warn_msg)
        return None

    def get_params(
            self,
            sentence,
            return_one_value = True
    ):
        if not self.case_sensitive:
            sentence = str(sentence).lower()

        #
        # Extract variables from question
        #
        params_dict = self.extract_variable_values(
            sentence = sentence
        )

        if return_one_value:
            for var in params_dict.keys():
                values = params_dict[var]
                preferred_direction = self.mex_obj_vars[var][MatchExpression.MEX_OBJECT_VARS_PREFERRED_DIRECTION]

                index_priority_order = (0, 1)
                if preferred_direction == MatchExpression.TERM_RIGHT:
                    index_priority_order = (1, 0)
                if values[index_priority_order[0]] is not None:
                    params_dict[var] = values[index_priority_order[0]]
                elif values[index_priority_order[1]] is not None:
                    params_dict[var] = values[index_priority_order[1]]
                else:
                    params_dict[var] = None

        return params_dict


if __name__ == '__main__':
    # cf_obj = cf.Config.get_cmdline_params_and_init_config_singleton(
    #     Derived_Class = cf.Config
    # )
    lg.Log.DEBUG_PRINT_ALL_TO_SCREEN = True
    lg.Log.LOGLEVEL = lg.Log.LOG_LEVEL_IMPORTANT

    tests = [
        {
            # We also use the words 'test&escape' and ';' (clashes with var separator
            # but works because we escape the word using '\\;')
            # to detect diameter.
            # Need to escape special mex characters like ; if used as expression
            'mex': 'r, float, radius & r  ;'
                   + 'd, float, diameter / d / test\\/escape / \\; / + / * /\\/   ;   ',
            'sentences': [
                'What is the volume of a sphere of radius 5.88?',
                'What is the volume of a sphere of radius 5.88 and 4.9 diameter?',
                'What is the volume of a sphere of radius 5.88 and 33.88 test&escape?',
                'What is the volume of a sphere of radius 5.88, 33.88;?',
                # When stupid user uses '+' to detect a param, should also work, but not recommended
                'What is the volume of a sphere of radius 5.88, +33.88?',
                # Using '*' to detect diameter
                'What is the volume of a sphere of radius 5.88, 33.88*?',
                # Using '&' to detect diameter
                'What is the volume of a sphere of radius 5.88, 33.88&?',
                # Should not detect diameter because we say to look for 'd', not any word ending 'd'
                # But because we have to handle languages like Chinese/Thai where there is no word
                # separator, we allow this and the diameter will be detected
                'What is the volume of a sphere of radius 5.88 and 33.88?',
                # Should not be able to detect now diameter
                'What is the volume of a sphere of radius 5.88 / 33.88?'
            ]
        },
        {
            'mex': 'dt,datetime,   ;   email,email,   ;   inc, float, inc / inch / inches',
            'sentences': [
                'What is -2.6 inches? 20190322 05:15 send to me@abc.com.',
                'What is +1.2 inches? 2019-03-22 05:15 you@email.ua ?',
                '2019-03-22: u_ser-name.me@gmail.com is my email',
                '이멜은u_ser-name.me@gmail.com',
                'u_ser-name.me@gmail.invalid is my email'
            ]
        },
        {
            'mex': 'dt, datetime,   ;   acc, number, 계정 / 번호   ;   '
                   + 'm, int, 월   ;   d, int, 일   ;   t, time, 에   ;'
                   + 'amt, float, 원   ;   bal, float, 잔액   ;'
                   + 'name, str-zh-cn, 】 ',
            'sentences': [
                '2020-01-01: 번호 0011 계정은 9 월 23 일 10:12 에 1305.67 원, 잔액 9999.77.',
                '20200101 xxx: 번호 0011 계정은 8 월 24 일 10:12 에 원 1305.67, 9999.77 잔액.',
                'AAA 2020-01-01 11:52:22: 번호 0022 계정은 7 월 25 일 10:15:55 에 1405.78 원, 잔액 8888.77.',
                '2020-01-01: 번호 0033 계정은 6 월 26 일 完成23:24 에 1505.89 원, 잔액 7777.77.',
                '2020-01-01: 번호 0044 계정은 5 월 27 일 完成23:24:55 에 5501.99 원, 잔액 6666.77.',
                '2020-01-01: 번호0055계정은4월28일11:37에1111.22원，잔액5555.77.',
                '2020-01-01: 번호0066계정은3월29일11:37:55에2222.33원，잔액4444.77',
                '2020-01-01: 번호0777계정은30일 完成11:38:55에3333.44원',
                '【은행】 陈豪贤于.',
                'xxx 陈豪贤 】 于.',
                '陈豪贤 】 于.',
            ]
        },
        {
            # Longer names come first
            # If we had put instead "이름 / 이름은", instead of detecting "김미소", it would return "은" instead
            # But because we do internal sorting already, this won't happen
            'mex': 'kotext, str-ko, 이름 / 이름은   ;'
                   + 'thtext, str-th, ชื่อ   ;'
                   + 'vitext, str-vi, tên   ;'
                   + 'cntext, str-zh-cn, 名字 / 名 / 叫 / 我叫, right',
            'sentences': [
                '이름은 김미소 ชื่อ กุ้ง tên yêu ... 我叫是习近平。'
            ],
            'priority_direction': [
                'right'
            ]
        }
    ]

    import nwae.utils.Profiling as prf

    for test in tests:
        pattern = test['mex']
        sentences = test['sentences']
        return_value_priorities = [MatchExpression.TERM_LEFT]*len(sentences)
        if 'priority_direction' in test.keys():
            return_value_priority = test['priority_direction']

        for i in range(len(sentences)):
            sent = sentences[i]

            a = prf.Profiling.start()
            cmobj = MatchExpression(
                pattern = pattern,
                lang    = 'zh-cn'
            )
            #a = prf.Profiling.start()
            params = cmobj.get_params(
                sentence         = sent,
                return_one_value = True
            )
            print(params)
            #print('Took ' + str(prf.Profiling.get_time_dif_str(start=a, stop=prf.Profiling.stop(), decimals=5)))

    exit(0)
    lg.Log.LOGLEVEL = lg.Log.LOG_LEVEL_DEBUG_2
    print(MatchExpression(
        pattern = 'mth,int,月;day,int,日;t,time,完成;amt, float, 民币;bal,float,金额/余额'
    ).get_params(
        sentence = '【中国农业银行】您尾号0579账户10月17日09:27完成代付交易人民币2309.95，余额2932.80。',
        return_one_value = True
    ))
