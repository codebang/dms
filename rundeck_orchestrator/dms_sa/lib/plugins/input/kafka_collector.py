from lib.base.inputbase import InputBase
from lib.services.servicecontext import ServiceContext
import avro.io
import avro.schema
import io
from lib.events import EventFactory
import json
import traceback
import logging
from lib.utils import Logger
from kafka import KafkaConsumer

class KafkaCollector(InputBase,Logger):

    def getPluginName(self):
        return "kafka_collector"

    def run(self):
        ctx = ServiceContext()
        queue = ctx.getQueueService()
        self._initializeschema()
        self._initializeconsumer()
        for msg in self.consumer:

            value = bytearray(msg.value)
            topic = msg.topic
            bytes_reader = io.BytesIO(value[5:])
            decoder = avro.io.BinaryDecoder(bytes_reader)
            reader = avro.io.DatumReader(self.schema)
            kafkamsg = reader.read(decoder)
            try:
                jsondata = json.loads(kafkamsg['rawdata'])
                eventType = jsondata["eventName"]
                jsondata['topic'] = topic
                print EventFactory.getEvent(eventType,jsondata)
                queue.put(EventFactory.getEvent(eventType,jsondata))
            except:
                self.error("has excetpion when resovle kafka message.")
                #logging.log(logging.DEBUG,traceback.print_exc())


    def _initializeschema(self):
        avro_schema = """
            {"namespace": "com.dadycloud.sa",
            "type": "record",
            "name": "event",
            "fields": [
                 {"name": "timestamp", "type": "long"},
                 {"name": "src",       "type": "string"},
                 {"name": "host_ip",   "type": "string"},
                 {"name": "rawdata",   "type": "bytes"}
            ]
            }
         """
        self.schema = avro.schema.parse(avro_schema)

    def _initializeconsumer(self):
        constructor="KafkaConsumer(%s,group_id=%s,bootstrap_servers=%s)"
        topics = self.kafka_topics
        group_id = self.kafka_groupid
        bootstrap_server = self.kafka_broker
        str = constructor % (topics,group_id,bootstrap_server)
        self.consumer = eval(str)

    def _decodemsg(self,msg):
        value = bytearray(msg.value)
        bytes_reader = io.BytesIO(value[5:])
        decoder = avro.io.BinaryDecoder(bytes_reader)
        reader = avro.io.DatumReader(self.schema)
        message = reader.read(decoder)
        return message

