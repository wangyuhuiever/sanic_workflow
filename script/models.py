# -*- coding: utf-8 -*-

from tools.decorators import collect


@collect("测试模型")
class StringProcess(object):

    async def function_test(self, st):
        """测试方法"""
        new_st = st + "测试"
        return new_st


@collect("测试模型2")
class StringProcess2(object):

    async def function_test(self, st):
        """测试方法2"""
        print(st)
        new_st = "......" + st
        # return new_st
