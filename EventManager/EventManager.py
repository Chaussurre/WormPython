class EventManager:
    def __init__(self):
        self.listeners = {}

    def addListener(self, event, callBack):
        if event not in self.listeners.keys():
            self.listeners[event] = []
        self.listeners[event].append(callBack)

    def removeListener(self, event, callBack):
        if event not in self.listeners.keys():
            return
        self.listeners[event].remove(callBack)

    def triggerEvent(self, event, *args):
        print("event trigger:", event)
        if event in self.listeners.keys():
            for cb in self.listeners[event]:
                cb(*args)

eventManager = EventManager()
