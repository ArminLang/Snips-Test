#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    current_session_id = intentMessage.session_id
    mqtt_client.publish("lgtv/set/toast","YES")
    hermes.publish_end_session(current_session_id, "Hello World")


if __name__ == "__main__":
    mqtt_client = mqtt.Client()
 #   mqtt_client.message_callback_add('hermes/intent/#', on_message_intent)
    mqtt_client.connect("localhost", 1883)
#    mqtt_client.subscribe('hermes/intent/#')
    mqtt_client.loop_forever()
    
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("arminlang:sonosInvade", subscribe_intent_callback) \
         .start()
