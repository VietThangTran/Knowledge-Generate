from .agent import Agent
from typing import List, Union, Optional


class KnowledgeAgent(Agent):
    def __init__(self):
        super().__init__(prompt_dir="Prompt/KnowledgePrompt")

    def extract_topic(
            self,
            topic: Union[List[str] | str],
            previous_context: Union[List[str] | str] = None
    ) -> Union[List[List[str]], List[str]]:
        if isinstance(topic, str):
            prompt = self.prompts["EXTRACT_TOPIC"].replace("[INPUT]", topic)
            if previous_context:
                prompt = prompt.replace("[PREVIOUS_CONTEXT]", "with the Context of the Topic is: \n" + previous_context)
            else:
                prompt = prompt.replace("[PREVIOUS_CONTEXT]", "")
            response = self.generate(prompt=prompt, response_type="json")['topics']
            return [topic.title() for topic in response]
        else:
            if previous_context is None:
                previous_context = len(topic) * [None]
            return [
                self.extract_topic(single_topic, single_previous_context)
                for single_topic, single_previous_context in zip(topic, previous_context)
            ]

    def create_knowledge(
            self,
            topic: Union[List[str] | str],
            sub_topics: Union[List[List[str]] | List[str]],
            previous_context: Union[List[str] | str] = None,
            final: bool = False
    ) -> Union[List[List[str]], List[str]]:
        if isinstance(topic, str):
            if final:
                prompt = (self.prompts["CREATE_KNOWLEDGE_FINAL"]
                          .replace("[INPUT]", topic))
            else:
                prompt = (self.prompts["CREATE_KNOWLEDGE"]
                          .replace("[INPUT]", topic)
                          .replace("[SUB_TOPICS]", '- ' + '\n- '.join(sub_topics))
                          )
            if previous_context:
                prompt = prompt.replace("[PREVIOUS_CONTEXT]", "with the Context of the Topic is: \n" + previous_context)
            else:
                prompt = prompt.replace("[PREVIOUS_CONTEXT]", "")
            response = self.generate(prompt=prompt, response_type="text")
            response = '\n'.join(response.split("\n")[1:-1])
            return response
        else:
            if previous_context is None:
                previous_context = len(topic) * [None]
            return [
                self.create_knowledge(single_topic, single_sub_topics, single_previous_context)
                for single_topic, single_sub_topics, single_previous_context in zip(topic, sub_topics, previous_context)
            ]
