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
@Description: The definition of the base KG Build Pipeline
"""
from abc import abstractmethod

from sekg.graph.exporter.graph_data import GraphData
from sekg.pipeline.component.base import Component


class PipelineListener:

    @abstractmethod
    def on_before_run_component(self, component_name, kg_build_pipeline, **config):
        print("hook before pipeline run component %r" % component_name)

    @abstractmethod
    def on_after_run_component(self, component_name, kg_build_pipeline, **config):
        print("hook after pipeline run component %r" % component_name)


class KGBuildPipeline:
    def __init__(self):
        self.__name2component = {}
        self.__component_order = []
        self.__graph_data = GraphData()
        self.__before_run_component_listeners = {}
        self.__after_run_component_listeners = {}

    # todo: add listener for each component before running and after running.
    #  In this way, we could save graph for each version.
    def __repr__(self):
        return str(self.__component_order)

    def add_before_listener(self, component_name, listener: PipelineListener):
        if component_name not in self.__before_run_component_listeners:
            self.__before_run_component_listeners[component_name] = []
        self.__before_run_component_listeners[component_name].append(listener)

    def add_after_listener(self, component_name, listener: PipelineListener):
        if component_name not in self.__after_run_component_listeners:
            self.__after_run_component_listeners[component_name] = []
        self.__after_run_component_listeners[component_name].append(listener)

    def add_component(self, name, component: Component, before=None, after=None, **config):
        """
        add a new component to this pipeline with given name. In a pipeline, the component name must be unique.
        :param after: the component name the this new component must run after
        :param before: the component name the this new component must run after
        :param name: the name of this new component
        :param component: the component instance
        :param config: the other config, save for update
        :return:
        """
        component.set_graph_data(self.__graph_data)
        self.__name2component[name] = component
        self.__component_order.append(name)

        # todo: complete this method to make the order work

    def run(self, **config):
        print("start running the pipeline")
        for component_name in self.__component_order:
            component: Component = self.__name2component[component_name]
            self.before_run_component(component_name, **config)
            component.before_run()
            component.run()
            component.after_run()
            self.after_run_component(component_name, **config)

        print("finish running the pipeline")

    def before_run_component(self, component_name, **config):
        print("start running with name=%r in the pipeline" % component_name)
        for listener in self.__before_run_component_listeners.get(component_name, []):
            listener.on_before_run_component(component_name, self, **config)

    def after_run_component(self, component_name, **config):
        print("finish running with name=%r in the pipeline\n" % component_name)
        for listener in self.__after_run_component_listeners.get(component_name, []):
            listener.on_after_run_component(component_name, self, **config)

    def save(self, path):
        """
        save the graph data object after all the building of all component
        :param path:
        :return:
        """
        self.__graph_data.save(path)
