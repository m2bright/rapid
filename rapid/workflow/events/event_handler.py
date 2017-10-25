"""
Copyright (c) 2015 Michael Bright and Bamboo HR LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import re
from abc import abstractmethod, ABCMeta

import pkgutil
from simpleeval import simple_eval


class EventHandlerFactory(object):

    @staticmethod
    def get_event_handler(type):
        """
        :param type:
        :type type: lib.Constants.EventTypes
        :return:
        :rtype: EventHandler
        """
        import rapid.workflow.events.handlers as handlers
        for importer, modname, ispkg in pkgutil.iter_modules(handlers.__path__):
            try:
                name = "{}.{}".format(handlers.__name__, modname)
                tmp = getattr(__import__(name, fromlist=[modname]), modname)
                if tmp.get_event_type() == type:
                    return tmp()
            except Exception as exception:
                pass
        return None


class EventHandler(object):
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def get_event_type():
        yield

    @abstractmethod
    def handle_event(self, pipeline_instance, action_instance, event):
        """
        :param pipeline_instance:
        :type pipeline_instance: rapid.workflow.data.models.PipelineInstance
        :param action_instance:
        :type action_instance: rapid.workflow.data.models.ActionInstance
        :param event:
        :type event: rapid.workflow.data.models.PipelineEvent
        :return:
        :rtype:
        """
        yield

    def passes_conditional(self, pipeline_instance, action_instance, conditional):
        """
        :param pipeline_instance:
        :type pipeline_instance: workflow.data.models.PipelineInstance
        :param conditional:
        :type conditional: str
        :return:
        :rtype:
        """
        if conditional is None or conditional == '':
            return True

        new_conditional = self._prepare_conditional(conditional, pipeline_instance, action_instance)
        return self._evaluate_condition(new_conditional)

    def _prepare_conditional(self, conditional, pipeline_instance, action_instance):
        """
        :param conditional:
        :type conditional: str
        :param parameters:
        :type parameters: dict
        :return:
        :rtype:
        """
        new_conditional = conditional
        for parameter, value in pipeline_instance.get_parameters_dict().items():
            if "{{{}}}".format(parameter) in new_conditional:
                new_conditional = new_conditional.replace("{{{}}}".format(parameter), str(value))

        if 'pipelineInstance.' in new_conditional:
            copy = new_conditional
            for term in re.findall('(pipelineInstance\.[^\s]{0,})', copy):
                replaced_term = term.replace('pipelineInstance.', '', 1)
                new_conditional = new_conditional.replace(term, str(self._get_attribute_trait(pipeline_instance, replaced_term)))

        if 'actionInstance.' in new_conditional:
            copy = new_conditional
            for term in re.findall('(actionInstance\.[^\s]{0,})', copy):
                replaced_term = term.replace('actionInstance.', '', 1)
                new_conditional = new_conditional.replace(term, str(self._get_attribute_trait(action_instance, replaced_term)))

        return new_conditional

    def _evaluate_condition(self, condition):
        try:
            return simple_eval(condition)
        except:
            return False

    def _get_attribute_trait(self, obj, trait):
        if '.' in trait:
            sp_obj = trait.split('.', 2)
            new_obj = getattr(obj, sp_obj[0])

            if len(sp_obj) > 1:
                return self._get_attribute_trait(new_obj, sp_obj[1])
            else:
                return new_obj
        else:
            return getattr(obj, trait)