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
from sekg.ir.doc.wrapper import MultiFieldDocumentCollection
from sekg.pipeline.component.base import Component


class ComponentOrderError(Exception):
    pass


class MissingComponentError(Exception):
    pass


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
        self.__doc_collection = MultiFieldDocumentCollection()
        self.__before_run_component_listeners = {}
        self.__after_run_component_listeners = {}

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

    def __get_component_order(self, name):
        """
        get the order of the specific component
        :param name: the specific component
        :return: the order start from 0 to num(component), -1. the specific component not exist
        """
        self.__component_order.append(name)

        for order, exist_component in enumerate(self.__component_order):
            if exist_component == name:
                return order
        return -1

    def __allocate_order_for_new_component(self, name, before=None, after=None):
        """
        try to allocate the right position for the new component
        :param name: the new component name
        :param before: the component of this new component must run before
        :param after: the component of this new component must run after
        :return: -1, can't not find a right order.
        """
        if before is None and after is None:
            return self.num_of_components()
        # todo: complete this approach
        return self.num_of_components()

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

        order = self.__allocate_order_for_new_component(name, before=before, after=after)
        if order == -1:
            raise ComponentOrderError("Can't not find a right order for %s" % name)

        component.set_graph_data(self.__graph_data)
        component.set_doc_collection(self.__doc_collection)
        self.__name2component[name] = component

        self.__component_order.insert(order, name)
        # todo: complete this method to make the order work

    def check(self):
        """
        check whether the components in the pipeline setting correct.
        e.g., the order of the component is wrong.
        the necessary component for a component to run is missing.
        :return: True the pipeline is correct.
        """
        # todo: complete this method.
        return True

    def run(self, **config):
        if not self.check():
            raise MissingComponentError()
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

    def load_graph(self, graph_data_path):
        self.__graph_data = GraphData.load(graph_data_path)
        # update component graph data
        for component_name in self.__component_order:
            component: Component = self.__name2component[component_name]
            component.set_graph_data(self.__graph_data)

        print("load graph")

    def load_doc(self, document_collection_path):
        self.__doc_collection = MultiFieldDocumentCollection.load(document_collection_path)
        # update component doc_collection
        for component_name in self.__component_order:
            component: Component = self.__name2component[component_name]
            component.set_doc_collection(self.__doc_collection)

        print("load doc collection")

    def num_of_components(self):
        return len(self.__component_order)
