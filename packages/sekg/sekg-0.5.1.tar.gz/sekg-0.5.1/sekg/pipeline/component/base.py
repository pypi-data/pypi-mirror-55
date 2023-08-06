#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: isky
@Email: 19110240019@fudan.edu.cn
@Created: 2019/10/28
------------------------------------------
@Modify: 2019/10/28
------------------------------------------
@Description:
"""
from abc import abstractmethod


class ComponentListener:

    @abstractmethod
    def on_before(self, component,**config):
        print("hook before component running")

    @abstractmethod
    def on_after(self,component, **config):
        print("hook after component running")


class Component:
    def __init__(self, graph_data=None):
        self.graph_data = graph_data
        self.__before_run_listeners = []
        self.__after_run_listeners = []

    def set_graph_data(self, graph_data):
        self.graph_data = graph_data

    def type(self):
        return str(self.__class__.__name__)

    @abstractmethod
    def run(self, **config):
        print("running component %r" % (self.type()))

    def add_before_listener(self, listener: ComponentListener):
        self.__before_run_listeners.append(listener)

    def add_after_listener(self, listener: ComponentListener):
        self.__after_run_listeners.append(listener)

    def before_run(self, **config):
        print("before running component %r" % (self.type()))
        for listener in self.__before_run_listeners:
            listener.on_before(self,**config)

    def after_run(self, **config):
        print("after running component %r" % (self.type()))
        for listener in self.__after_run_listeners:
            listener.on_after(self,**config)
