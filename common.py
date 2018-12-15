# -*- coding: utf-8 -*-

import sys
import logging
import argparse


class Constants:
    TRAINING = "Train"
    VALIDATION = "Valid"
    EVALUATION = "Test"
    EMPTY = "__empty__"
    UNK = '<unk>'
    BOS = '<s>'
    EOS = '</s>'


class ExitCode:
    NO_DATA = 0
    NOT_SUPPORTED = 1
    INVALID_OPTION = 11
    INVALID_CONVERSION = 12
    INVALID_NAME = 13
    INVALID_NAME_OF_CONFIGURATION_FILE = 14
    INVALID_FILE_PATH = 15
    INVALID_DICTIONARY = 16


class Logger:
    """
    !!Usage: please create a logger with one line as shown in the example below.
      logger = Logger(name="word2vec", level=Logger.DEBUG).logger

    This logger print out logging messages similar to the logging message of tensorflow.
    2018-07-01 19:35:33.945120: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1406]
    2018-07-20 16:23:08.000295: I kmlm_common.py:94] Configuration lists:

    TO-DO:
    verbose level
    """
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET
    INFO = logging.INFO
    WARN = logging.WARN
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
# l.logger.debug('debug message')
# l.logger.info('info message')
# l.logger.warn('warn message')
# l.logger.error('error message')
# l.logger.critical('critical message')

    def __init__(self, name="__default__", level=logging.NOTSET):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        h = logging.StreamHandler()
        h.setLevel(level)
        formatter = logging.Formatter('%(asctime)s: %(levelname).1s %(filename)s:%(lineno)d] %(message)s')
        formatter.default_msec_format = '%s.%06d'
        h.setFormatter(formatter)
        self.logger.addHandler(h)


class ParseOption:
    """
    it merges options from both an option file and command line into python option
    """
    def __init__(self, argv, logger):
        self._logger = logger

        _parser, _blist = self._build_parser_4_eswd()

        if len(argv) > 1:
            # args from command line
            command_args = _parser.parse_args(argv[1:])

            # Handling boolean
            command_dict = vars(command_args)
            for arg in command_dict:
                if arg in _blist:
                    command_dict[arg] = (str(command_dict[arg]) == "True")

            # rate
            if float(command_dict["eswd_min_sentence_levenshtein_distance_rate"]) > 1.0:
                command_dict["eswd_min_sentence_levenshtein_distance_rate"] = 1.0
                self._logger.warn("eswd_min_sentence_levenshtein_distance_rate should be within [0.0, 1.0]")
            elif float(command_dict["eswd_min_sentence_levenshtein_distance_rate"]) < 0.0:
                command_dict["eswd_min_sentence_levenshtein_distance_rate"] = 0.0
                self._logger.warn("eswd_min_sentence_levenshtein_distance_rate should be within [0.0, 1.0]")
            args = argparse.Namespace(**command_dict)

            self.print_args(args)
            self._args = args
        else:
            self._logger.critical("No options..")
            sys.exit(ExitCode.INVALID_OPTION)

    @property
    def args(self):
        return self._args

    def print_args(self, args):
        self._logger.info("/******************************************")
        self._logger.info("                Settings")
        self._logger.info("*******************************************")
        sorted_args = sorted(vars(args))
        pre_name = ""
        for arg in sorted_args:
            name = arg.split("_")[0]
            if name != pre_name:
                self._logger.info(". %s" % name.upper())
                pre_name = name

            self._logger.info("- %s=%s" % (arg, getattr(args, arg)))
        self._logger.info("*******************************************/")

    @staticmethod
    def _build_parser_4_eswd():
        # create parser
        blist = list()
        parser = argparse.ArgumentParser(
            description="A script for expanding text corpus to phonetically similar corpus.",
            fromfile_prefix_chars='@')

        prep_group = parser.add_argument_group(title="eswd", description="required options")
        prep_group.add_argument( '--eswd-sid-start', '--start', type=int, default=1, help="start of sentence index.")
        prep_group.add_argument( '--eswd-sid-end', '--end', type=int, defulat=-1, help="end of sentence index.")
        prep_group.add_argument('--eswd-lex', '--lex', help="lexicon.", required=True)
        prep_group.add_argument('--eswd-text', '--text', help="text corpus to be expanded.", required=True)
        prep_group.add_argument('--eswd-save-sid-corpus', '--sid-corpus', default=True,
                                help="Whether saving text corpus including sequential id  or not.")
        prep_group.add_argument('--eswd-max-expanded-sentence', '--max-n', type=int, default=100,
                                help="The maximum number of expanded sentences for each sentence.")

        prep_group.add_argument('--eswd-min-sentence-levenshtein-distance-rate', '--min-lev-rate', type=float,
                                default=0.0,
                                help="min levenshtein distance between reference sentence and expanded sentences.")
        prep_group.add_argument('--eswd-min-sentence-levenshtein-distance', '--min-lev', type=int, default=5,
                                help="min levenshtein distance between reference sentence and expanded sentences.")
        blist.append("save_sid_corpus")

        return parser, blist
