import random
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator,IBurpExtender
from java.util import List, ArrayList
import os
import sys

class Extender(IBurpExtender,IIntruderPayloadGeneratorFactory):
    def registerExtenderCallbacks(self, callback):
        self._callback = callback
        self._helpers = callback.getHelpers()
        callback.registerIntruderPayloadGeneratorFactory(self)
        return
    def getGename(self):
        return "Payload Gen"
    def createins(self,attack):
        return burpfuzzer(self,attack)

class Burpfuzzer(IIntruderPayloadGenerator):
    def __init__(self,extender,attack):
        self._extender = extender
        self._helper = extender._helpers
        self._attack = attack
        self.max_payload = 10
        self.num_iter = 0

    def getnextpayload(self,current_payload):
        payload = "".join(chr(i) for i in current_payload)
        payload = self.mutate_payload(payload)
        self.num_iter = self.num_iter+1
        return payload

    def reset(self):
        self.num_iter = 0
        return

    def morepl(self):
        if self.num_iter == self.max_payload:
            return 0
        else:
            return 1

    def mutate_payload(self,origin_payload):
        i = random.randint(1,3)
        offset = random.randint(0,len(origin_payload)-1)
        payload = origin_payload[:offset]

        if i == 1:
            payload = payload + "' OR 1=1#"

        elif i == 2:
            payload = payload + "<script>alert('XSS!')</script>"

        elif i == 3:
            length = random.randint(len(payload[0offset:]), len(payload)-1)

        for x in range(random.randint(1,10)):
            payload = payload + origin_payload[offset:offset+length]


        payload = payload + origin_payload[offset:]

        return payload
        