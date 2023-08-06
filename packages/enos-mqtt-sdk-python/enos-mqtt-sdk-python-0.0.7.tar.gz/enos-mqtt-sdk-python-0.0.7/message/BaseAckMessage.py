from abc import ABCMeta
from message.AckMessageBody import AckMessageBody
from core.msg.IMqttAck import IMqttAck

class BaseAckMessage(AckMessageBody, IMqttAck):
    __metaclass__ = ABCMeta

    pass