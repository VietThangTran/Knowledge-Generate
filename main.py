from dotenv import load_dotenv
load_dotenv('.env')

from AI.knowledge_agent import KnowledgeAgent
from Convert.convert import create_folder, create_file
from typing import List

knowledge_agent = KnowledgeAgent()

def generate_knowledge(topic: str, deep: int, previous_context: str = None, memory: List = None):
    if memory is None:
        memory = []

    if deep == 0:
        return None
    sub_topics = knowledge_agent.extract_topic(
        topic=topic,
        previous_context=previous_context
    )
    sub_topics = [sub_topic.replace('/','-') for sub_topic in sub_topics if sub_topic not in memory]
    memory += sub_topics

    md_file = knowledge_agent.create_knowledge(
        topic=topic,
        sub_topics=sub_topics,
        previous_context=previous_context,
        final=deep == 1
    )
    if previous_context is None:
        previous_context = topic

    create_file(parent_dir='Content', file_name=topic, text=md_file)

    links = [
        generate_knowledge(sub_topic, deep - 1, previous_context=previous_context + ' -> ' + sub_topic, memory=memory)
        for sub_topic in sub_topics
    ]

    return {
        'topic': topic,
        'md_file': md_file,
        'links': links
    }

if __name__ == "__main__":
    create_folder('Content')
    knowledge = generate_knowledge(topic="English Grammar", deep=4)
    print(1)
