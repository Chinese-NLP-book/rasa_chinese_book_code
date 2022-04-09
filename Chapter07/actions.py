from typing import Any, Text, Dict, List

from rasa_sdk import Tracker, Action
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted
from rasa_sdk.executor import CollectingDispatcher
from rasa.core.actions.forms import FormAction, REQUESTED_SLOT
from rasa_sdk.types import DomainDict


class ActionGoodbye(Action):
    def name(self) -> Text:
        return 'action_goodbye'

    def __init__(self):
        super().__init__()

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> List[Dict[Text, Any]]:

        print('\n ActionGoodbye-------------')
        currentSlots = tracker.current_slot_values()
        for slot in currentSlots:
            print('run slot:\t\t%s=%s' % (slot, currentSlots[slot]))

        dispatcher.utter_message(response="utter_goodbye", **tracker.slots)

        print('Restarted()')
        return [Restarted()]


class ActionTicketForm(Action):
    def name(self) -> Text:
        return "action_ticket_form_submit"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
            ) -> List[Dict]:
        dispatcher.utter_message(response='utter_ask_confirm', **tracker.slots)
        return []


class TicketFormAction(FormAction):
    def name(self) -> Text:
        return "ticket_form"

    def required_slots(self, tracker: Tracker) -> List[Text]:
        return ["city_depart", "city_arrive", "date"]

    def extract_other_slots(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
        if not slot_to_fill:
            return super().extract_other_slots(dispatcher, tracker, domain)
        else:
            return {}

    def slot_mappings(self):
        return {
            "city_depart": [
                self.from_entity(entity="city", role="departure"),
                self.from_entity(entity="city", intent="info_city")
            ],
            "city_arrive": [
                self.from_entity(entity="city", role="destination"),
                self.from_entity(entity="city", intent="info_city")
            ],
        }


class ActionBuyTicket(Action):
    def name(self) -> Text:
        return "action_buy_ticket"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        arrive = tracker.get_slot("city_arrive")
        api_succeed = arrive == "北京"
        return [SlotSet("api_succeed", api_succeed)]


class ActionAskConfirmThenNo(Action):
    def name(self) -> Text:
        return 'action_ask_confirm_then_no'

    def __init__(self):
        super().__init__()

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> List[Dict[Text, Any]]:

        print('\n ActionAskConfirmThenNo-------------')
        currentSlots = tracker.current_slot_values()
        for slot in currentSlots:
            print('run slot:\t\t%s=%s' % (slot, currentSlots[slot]))

        dispatcher.utter_message(response="utter_ask_confirm_then_no", **tracker.slots)
        print('Restarted()')
        return [Restarted()]


class ActionApiSucceedTrue(Action):
    def name(self) -> Text:
        return 'action_api_succeed_true'

    def __init__(self):
        super().__init__()

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        print('\n ActionApiSucceedTrue-------------')
        currentSlots = tracker.current_slot_values()
        for slot in currentSlots:
            print('run slot:\t\t%s=%s' % (slot, currentSlots[slot]))

        dispatcher.utter_message(response="utter_api_succeed_true", **tracker.slots)

        print('Restarted()')
        return [Restarted()]


class ActionApiSucceedFalse(Action):
    def name(self) -> Text:
        return 'action_api_succeed_false'

    def __init__(self):
        super().__init__()

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        print('\n ActionApiSucceedFalse-------------')
        currentSlots = tracker.current_slot_values()
        for slot in currentSlots:
            print('run slot:\t\t%s=%s' % (slot, currentSlots[slot]))

        dispatcher.utter_message(response="utter_api_succeed_false", **tracker.slots)
        print('Restarted()')
        return [Restarted()]
        
    class RestartConversationAction(Action):
        def name(self) -> Text:
            return "action_restart_conversation"

        def __init__(self):
            super().__init__()

        def run(
                self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
        ) -> List[Dict]:

            print('\n RestartConversationAction-------------')
            currentSlots = tracker.current_slot_values()
            for slot in currentSlots:
                print("run slot:\t\t%s=%s" % (slot, currentSlots[slot]))

            print('Restarted()')
            return [Restarted()]
