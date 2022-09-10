from enum import Enum
from BotEvent import BotEvent
from Plugin import Plugin
from datetime import datetime

SLEEP_SECONDS = 10


class Echo(Plugin):
    """
    自动复读`echoList`中的内容
    ```python
    self.echoList = ['？','?','好好好','111']
    ```
    以及自动+1
    """

    def __init__(self) -> None:
        super().__init__()
        self.echoList = ["？", "?", "好好好", "111"]
        # self.state = True
        self.last_msg_datetime = 0
        self.__temp__ = "114514"
        self.count = 0

    def run(self):
        while True:
            event = self.eventBox.get(block=True)
            if (
                self.state
                and event["post_type"] == "message"
            ):
                if (event["raw_message"] in self.echoList):
                    now_datetime = datetime.now().timestamp()
                    seconds_elapsed = now_datetime - self.last_msg_datetime
                    if seconds_elapsed < SLEEP_SECONDS:
                        continue
                    self.last_msg_datetime = now_datetime
                    self.PutEvent2Bot(
                        BotEvent(
                            "group", event["group_id"], event["raw_message"])
                    )
                else:
                    if (self.__temp__ == event["raw_message"]):
                        self.count += 1
                    else:
                        self.__temp__ = event["raw_message"]
                        self.count = 0
            if (self.count == 1):
                self.PutEvent2Bot(
                    BotEvent("group", event["group_id"], self.__temp__)
                )
            else:
                self.TrySwitchState(event, "echo")
