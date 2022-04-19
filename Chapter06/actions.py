import json
import os

from typing import Any, Dict, List, Text

from rasa_sdk import Tracker, Action
from rasa_sdk.events import AllSlotsReset, Restarted
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase

SLOT_MENTION = "mention"
SLOT_OBJECT_TYPE = "object_type"
SLOT_ATTRIBUTE = "attribute"
SLOT_LISTED_OBJECTS = "knowledge_base_listed_objects"
SLOT_LAST_OBJECT = "knowledge_base_last_object"
SLOT_LAST_OBJECT_TYPE = "knowledge_base_last_object_type"

USE_NEO4J = bool(os.getenv("USE_NEO4J", False))

if USE_NEO4J:
    from neo4j_knowledge_base import Neo4jKnowledgeBase


def return_gbk(s):
    try:
        if isinstance(s, str):
            return s.encode('gbk').decode()
        if isinstance(s, (int, float, complex)):
            return str(s).encode('gbk').decode()
        return s.encode('gbk').decode()
    except TypeError:
        try:
            return str(s).encode('gbk').decode()
        except AttributeError:
            return s
    except AttributeError:
        return s
    except UnicodeDecodeError:
        return s


class EnToZh:
    def __init__(self, data_file):
        with open(data_file) as fd:
            self.data = json.load(fd)

    def __call__(self, key):
        returnString = self.data.get(key, key)
        print("EnToZh ==>%s gbk(%s)" % (returnString, return_gbk(returnString)))
        return return_gbk(returnString)


class MyKnowledgeBaseAction(ActionQueryKnowledgeBase):
    def name(self) -> Text:
        return "action_response_query"

    def __init__(self):
        if USE_NEO4J:
            print("using Neo4jKnowledgeBase")
            knowledge_base = Neo4jKnowledgeBase("bolt://localhost:7687", "neo4j", "43215678")
        else:
            print("using InMemoryKnowledgeBase")
            knowledge_base = InMemoryKnowledgeBase("data.json")

        super().__init__(knowledge_base)

        self.en_to_zh = EnToZh("en_to_zh.json")

    async def utter_objects(
            self,
            dispatcher: CollectingDispatcher,
            object_type: Text,
            objects: List[Dict[Text, Any]],
    ) -> None:
        """
        Utters a response to the user that lists all found objects.
        Args:
            dispatcher: the dispatcher
            object_type: the object type
            objects: the list of objects
        """
        print("utter_objects enter %s,list=%s" % (object_type, objects))
        print(objects)
        print("-----------------------")

        if objects:
            dispatcher.utter_message(text="找到下列{}:".format(self.en_to_zh(object_type)))

            repr_function = await self.knowledge_base.get_representation_function_of_object(
                object_type
            )

            for i, obj in enumerate(objects, 1):
                dispatcher.utter_message(text=f"{i}: {repr_function(obj)}")
        else:
            textTips = "我没找到任何{}.".format(self.en_to_zh(object_type))
            print(textTips)
            dispatcher.utter_message(
                text=textTips
            )

    def utter_attribute_value(
            self,
            dispatcher: CollectingDispatcher,
            object_name: Text,
            attribute_name: Text,
            attribute_value: Text,
    ) -> None:
        """
        Utters a response that informs the user about the attribute value of the
        attribute of interest.
        Args:
            dispatcher: the dispatcher
            object_name: the name of the object
            attribute_name: the name of the attribute
            attribute_value: the value of the attribute
        """

        print("utter_attribute_value object_name:%s,attribute_name:%s,attribute_value:%s"
              % (object_name, attribute_name, attribute_value))

        if attribute_value:
            dispatcher.utter_message(
                text="{}的{}是{}。".format(
                    self.en_to_zh(object_name),
                    self.en_to_zh(attribute_name),
                    self.en_to_zh(attribute_value),
                )
            )
        else:
            dispatcher.utter_message(
                text="没有找到{}的{}。".format(
                    self.en_to_zh(object_name), self.en_to_zh(attribute_name)
                )
            )

    async def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict]:

        print(
            "\nMyKnowledgeBaseAction"
            "---------------------------------------------------------------------------------------------------------")

        currentSlots = tracker.current_slot_values()
        for slot in currentSlots:
            print("run slot:\t\t%s=%s" % (slot, currentSlots[slot]))

        object_type = tracker.get_slot(SLOT_OBJECT_TYPE)
        last_object_type = tracker.get_slot(SLOT_LAST_OBJECT_TYPE)
        attribute = tracker.get_slot(SLOT_ATTRIBUTE)
        restartConversation = tracker.get_slot("restart_conversation")

        new_request = object_type != last_object_type
        result = []

        if restartConversation is not None:
            print("AllSlotsReset()")
            return [AllSlotsReset()]

        # self.use_last_object_mention = True
        if attribute is not None:
            if not object_type:
                if attribute == "album" or attribute == "style":
                    print("run 强制设置object_type=song")
                    object_type = "song"
                else:
                    print("run 强制设置object_type=singer")
                    object_type = "singer"
                tracker.slots[SLOT_OBJECT_TYPE] = object_type

            # self.use_last_object_mention = False
            result = await super()._query_attribute(
                dispatcher, object_type, attribute, tracker
            )
            # print("append AllSlotsReset()")
            # result.append(AllSlotsReset())
            return result

        if not object_type:
            # object type always needs to be set as this is needed to query the
            # knowledge base
            print("utter_message utter_ask_rephrase")
            dispatcher.utter_message(response="utter_ask_rephrase")
            return []

        if not attribute or new_request:
            return await self._query_objects(dispatcher, object_type, tracker)

        dispatcher.utter_message(response="utter_ask_rephrase")

        return result

    class ActionRestartConversation(Action):
        def name(self) -> Text:
            return "action_restart_conversation"

        def __init__(self):
            super().__init__()

        def run(
                self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
        ) -> List[Dict]:
            print('\n ActionRestartConversation-------------')
            currentSlots = tracker.current_slot_values()
            for slot in currentSlots:
                print("run slot:\t\t%s=%s" % (slot, currentSlots[slot]))

            dispatcher.utter_message(response="utter_greet")
            print('Restarted()')
            return [Restarted()]

    class ActionAllSlotsReset(Action):
        def name(self) -> Text:
            return "action_reset_slots"

        def __init__(self):
            super().__init__()

        def run(
                self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
        ) -> List[Dict]:
            print('\n ActionAllSlotsReset-------------')
            currentSlots = tracker.current_slot_values()
            for slot in currentSlots:
                print("run slot:\t\t%s=%s" % (slot, currentSlots[slot]))

            dispatcher.utter_message(response="utter_greet")
            print('AllSlotsReset()')
            return [AllSlotsReset()]

