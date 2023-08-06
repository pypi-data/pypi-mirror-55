#!/usr/bin/env python

# -*- coding: UTF-8 -*-

import json
import shutil
import glob

try:
    from tools import *
    from log import logger
except:
    from yoctools.tools import *
    from yoctools.log import logger

def obj_dict(d):
    top = type('Config', (object,), d)
    seqs = tuple, list, set, frozenset
    for i, j in d.items():
    	if isinstance(j, dict):
    	    setattr(top, i, obj_dict(j))
    	elif isinstance(j, seqs):
    	    setattr(top, i,
    		    type(j)(obj_dict(sj) if isinstance(sj, dict) else sj for sj in j))
    	else:
    	    setattr(top, i, j)
    return top


class solution:
    def __init__(self, dic):
        self.board_name = ''
        self.ld_script = ''
        for k, v in dic.items():
            if v:
                self.__dict__[k] = v
    def __str__(self):
        return "board_name: %s, ld_script: %s" % (self.board_name, self.ld_script)


class board:
    def __init__(self, dic):
        self.chip_name = ''
        self.ld_script = ''
        for k, v in dic.items():
            if v:
                self.__dict__[k] = v

        if not self.chip_name:
            logger.warning('Component `board.chip_name` cannot be empty!')

    def __str__(self):
        return "chip: %s, ld_script: %s" % (self.chip_name, self.ld_script)

class chip:
    def __init__(self, dic):
        self.vendor_name = ''
        self.cpu_name = ''
        self.ld_script = ''
        for k, v in dic.items():
            if v:
                self.__dict__[k] = v

        if not self.vendor_name:
            logger.error('Component `board.vendor_name` cannot be empty!')

        # if not self.cpu_name:
        #     logger.warning('Component `board.cpu_name` cannot be empty!')

    def __str__(self):
        return "vendor: %s, cpu: %s, ld_script: %s" % (self.vendor_name,self.cpu_name, self.ld_script)


class build_config:
    def __init__(self, dic):
        self.include = []
        self.internal_include = []
        self.libs = []
        self.libpath = []
        self.cflag = ''
        self.cxxflag = ''
        self.asmflag = ''
        self.ldflag = ''
        self.define = ''

        for k, v in dic.items():
            if v:
                self.__dict__[k] = v

class Package(object):
    def __init__(self, filename):
        self.name = ''
        self.description = ''
        self.type = ''
        self.keywords = {}
        self.author = ''
        self.license = ''
        self.homepage = ''
        self.yoc_version = ''
        self.depends = {}
        self.build_config = build_config({})
        self.defconfig = {}
        self.source_file = []
        self.install = []
        self.board = None

        self.load(filename)

    def load(self, filename):
        conf = yaml_load(filename)

        for k, v in conf.items():
            if v:
                if k == 'build_config':
                    v = build_config(v)
                if k not in ['board', 'chip', 'solution']:
                    self.__dict__[k] = v
                if k == 'lib':
                    self.__dict__['libs'] = v

        if self.type in ['board', 'chip', 'solution']:
            if self.type not in conf:
                logger.error('%s component must set `%s` field' % (filename, self.type))
                exit(-1)

        if self.type == 'board':
            self.__dict__['board'] = board(conf['board'])
        elif self.type == 'chip':
            self.__dict__['chip'] = chip(conf['chip'])
        elif self.type == 'solution':
            self.__dict__['solution'] = solution(conf['solution'])

        if not self.name:
            logger.error('%s `name` cannot be empty!' % filename)
            exit(-1)

        if self.type not in ['solution', 'common', 'board', 'chip']:
            logger.error('%s `type` must be "solution" or "common" or "board" or "chip".' % filename)
            exit(-1)

    def show(self):
        for k, v in self.__dict__.items():
            if not v:
                continue
            if k in ['build_config']:
                print(k)
                for kk, vv, in v.__dict__.items():
                    print("  ", kk, ":", vv)
            elif k in ['defconfig']:
                print(k)
                for k1, v1 in v.items():
                    print("  ", k1, ":", v1)
            else:
                print(k, str(v))


def package_test():
    p = Package('../solutions/helloworld/package.yaml')
    # p = Package('../solutions/chip_test_hobbit4_e902/package.yaml')
    # p = Package('../components/chip-hobbit4_e902/package.yaml')
    p = Package('../components/aos/package.yaml')
    # p = Package('package.yaml')
    p.show()


if __name__ == "__main__":
    package_test()
