from typing import Any, Text, Dict, List

from rasa_sdk import Tracker, Action
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa.core.actions.forms import FormAction
from rasa_sdk.forms import REQUESTED_SLOT


class TicketFormAction(FormAction):
    def name(self) -> Text:
        return "ticket_form"

    def required_slots(self, tracker: Tracker) -> List[Text]:
        return ["city_depart", "city_arrive", "date"]

    def extract_other_slots(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
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
                self.from_entity(entity="city", intent="info_city"),
            ],
            "city_arrive": [
                self.from_entity(entity="city", role="destination"),
                self.from_entity(entity="city", intent="info_city"),
            ],
        }

    def submit(
        self, dispatch: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict]:
        # don't using template alone,
        # since the system tracker is not updated yet when render the template,
        # using current tracker instead
        dispatch.utter_message(template="utter_ask_confirm", **tracker.slots)
        return []


class ActionBuyTicket(Action):
    def name(self) -> Text:
        return "action_buy_ticket"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        city_arrive = tracker.get_slot("city_arrive")
        city_depart = tracker.get_slot("city_depart")
        date = tracker.get_slot("date")


        dispatcher.utter_message(f"BOT 动作：购买「{date}」从「{city_depart}」出发到「{city_arrive}」的车票")

        return []
