# -*- coding: UTF-8 -*-

import os
import sys
import json
# import git
import zipfile
import re
import shutil


try:
    from log import logger
    from tools import *
except:
    from yoctools.log import logger
    from yoctools.tools import *

class Variables:
    def __init__(self):
        self.vars = {}
        pass

    def set(self, k, v):
        self.vars[k] =  v


    def get(self, var):
        if var in self.vars:
            return self.vars[var]

    def convert(self, var):
        v = var.split('?')
        if len(v) > 1:
            x = re.search('<(.+?)>', v[1], re.M | re.I)
            if x:
                x = self.get(x.group(1))
                if x in ['n', 'no', 'f', 'false', '0']:
                    return None
                var = v[0].strip()

        x = re.findall('<(.+?)>', var)
        for key in x:
            value = self.get(key)
            if value != None:
                var = var.replace('<'+key+'>', self.vars[key])
            else:
                print('not found variable:', var)

        return var

    def items(self):
        return self.vars.items()

class Solution:
    def __init__(self):
        self.variables = Variables()
        self.solution_component = None       # 当前 solution 组件
        self.board_component = None          # 当前开发板组件
        self.chip_component = None           # 当前芯片组件
        self.components = []
        self.global_includes = []
        self.libs = []
        self.libpath = []
        self.depend_libs = []
        self.defines = {}
        self.ASFLAGS   = []
        self.CCFLAGS   = []
        self.CXXFLAGS  = []
        self.LINKFLAGS = []
        self.ld_script = ''
        self.cpu_name = ''

    def set_solution(self, all_components):
        # find current solution & board component
        for _, component in all_components.items():
            if component.path == current_pwd() and component.type == 'solution':
                self.solution_component = component

                self.board_component = all_components.get(self.solution_component.solution.board_name)
                if self.board_component:
                    self.chip_component = all_components.get(self.board_component.board.chip_name)

                save_yoc_config({}, 'app/include/yoc_config.h')
                save_csi_config({}, 'app/include/csi_config.h')
                break

        if not self.solution_component:
            logger.error('No define solution component, please set a solution component')

        if not self.board_component:
            logger.error('No define board component, please set a board component')

        if not self.chip_component:
            logger.error('No define chip component, please set a chip component')

        if not (self.solution_component and self.board_component and self.chip_component):
            exit(-1)

        for component in [self.chip_component, self.board_component, self.solution_component]:
            for c in component.build_config.cflag.split():
                self.CCFLAGS.append(c)
            for c in component.build_config.asmflag.split():
                self.ASFLAGS.append(c)
            for c in component.build_config.cxxflag.split():
                self.CXXFLAGS.append(c)
            for c in component.build_config.ldflag.split():
                self.LINKFLAGS.append(c)


        def cpu_set_variable(cpu):
            self.cpu_name = cpu
            self.variables.set('CPU', cpu)
            self.variables.set('cpu', cpu.lower())
            if cpu.lower() == 'rv32emc':
                self.variables.set('cpu_num', 'rv32')
                self.variables.set('arch', 'riscv')
            else:
                self.variables.set('cpu_num', cpu_id(cpu))
                self.variables.set('arch', 'csky')


        if self.chip_component.chip.cpu_name:
            cpu_set_variable(self.chip_component.chip.cpu_name)

        self.variables.set('VENDOR', self.chip_component.chip.vendor_name)
        self.variables.set('vendor', self.chip_component.chip.vendor_name.lower())
        self.variables.set('CHIP', self.chip_component.name)
        self.variables.set('chip', self.chip_component.name.lower())

        self.variables.set('BOARD', self.board_component.name)
        self.variables.set('board', self.board_component.name.lower())
        self.variables.set('BOARD_PATH', self.board_component.path)

        self.variables.set('SOLUTION_PATH', self.solution_component.path)
        self.yoc_path = os.path.join(self.solution_component.path, 'yoc_sdk')
        self.lib_path = os.path.join(self.yoc_path, 'lib')
        self.libpath.append(self.lib_path)

        self.components = self.solution_component.getDependList(all_components)
        self.components.append(self.solution_component)
        for component in self.components:
            # defines
            for k, v in component.defconfig.items():
                self.variables.set(k, v)
                self.defines[k] = v
                if k == 'CONFIG_CPU':
                    cpu_set_variable(v)


        for component in self.components:
            if len(component.source_file) > 0 and component.type != 'solution' and component.name not in self.libs:
                self.libs.append(component.name)
                self.depend_libs.append(os.path.join(self.lib_path, 'lib' + component.name + '.a'))

            component.variable_convert(self.variables)

            # include
            for path in component.build_config.include:
                if path not in self.global_includes:
                    self.global_includes.append(path)

            # libpath
            for path in component.build_config.libpath:
                if path not in self.libpath:
                    self.libpath.append(path)

            # libs
            for lib in component.build_config.libs:
                if lib not in self.libs:
                    self.libs.append(lib)

        if self.solution_component.solution.ld_script:
            self.ld_script = self.solution_component.solution.ld_script
        elif self.board_component.board.ld_script:
            self.ld_script = self.board_component.board.ld_script
        elif self.chip_component.chip.ld_script:
            self.ld_script = self.chip_component.chip.ld_script
        else:
            logger.error("not found LD script file, please set ld_script")
            exit(-1)

    def install(self):
        for component in self.components:
            component.install(self.yoc_path)

    def show(self):
        print("[component]")
        for c in self.components:
            c.show(4)

        print("solution:", self.solution_component.name)
        print("board   :", self.board_component.name)
        print("chip    :", self.chip_component.name)

        print("[libs]")
        for v in self.libs:
            print('    ', v)

        print("[libpath]")
        for v in self.libpath:
            print('    ', v)

        print("[global_includes]")
        for v in self.global_includes:
            print('    ', v)

        print("[defines]")
        for k, v in self.defines.items():
            print('    ', k, '=', v)

        print("[variables]")
        for k, v in self.variables.items():
            print('    ', k, '=', v)

        print("ASFLAGS  :", self.ASFLAGS)
        print("CCFLAGS  :", self.CCFLAGS)
        print("CXXFLAGS :", self.CXXFLAGS)
        print("LINKFLAGS:", self.LINKFLAGS)

def cpu_id(s):
    ids = ''
    for c in s:
        if ord(c) >= ord('0') and ord(c) <= ord('9'):
            ids += c
        elif ids:
            return ids


if __name__ == "__main__":
    v = Variables()
    v.set('aaa', '111')
    v.set('bbb', '222')
    v.set('DEBUG', 'no')

    s = v.convert('<aaa>/xxx/bbb ? <DEBUG>')
    print(s)