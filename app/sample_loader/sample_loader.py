import csv
import json
import sys
import uuid

import jinja2
import pika
import redis

from flask import current_app


class SampleLoader:

    def __init__(self):
        # get rabbitmq env vars
        self.rabbitmq_host = current_app.config['RABBITMQ_HOST']
        self.rabbitmq_port = current_app.config['RABBITMQ_PORT']
        self.rabbitmq_vhost = current_app.config['RABBITMQ_VHOST']
        self.rabbitmq_queue = current_app.config['RABBITMQ_QUEUE']
        self.rabbitmq_exchange = current_app.config['RABBITMQ_EXCHANGE']
        self.rabbitmq_user = current_app.config['RABBITMQ_USER']
        self.rabbitmq_password = current_app.config['RABBITMQ_PASSWORD']

        # rabbit vars
        self.rabbitmq_connection = None
        self.rabbitmq_channel = None

        # # get redis env vars
        self.redis_host = current_app.config['REDIS_HOST']
        self.redis_port = current_app.config['REDIS_PORT']
        self.redis_db = current_app.config['REDIS_DB']

        # load sampleunit message template
        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(["./"]))
        self.jinja_template = self.env.get_template("app/sample_loader/message_template.xml")

    def sample_reader(self, file_obj, ce_uuid, ap_uuid, ci_uuid):
        sampleunits = {}
        reader = csv.DictReader(file_obj, delimiter=',')
        count = 0
        for sampleunit in reader:
            sample_id = uuid.uuid4()
            sampleunits.update({"sampleunit:" + str(sample_id): self.create_json(sample_id, sampleunit)})
            self.publish_sampleunit(
                self.jinja_template.render(sample=sampleunit, uuid=sample_id, ce_uuid=ce_uuid, ap_uuid=ap_uuid,
                                           ci_uuid=ci_uuid))
            count += 1
            if count % 5000 == 0:
                sys.stdout.write("\r" + str(count) + " samples loaded")
                sys.stdout.flush()

        print('\nAll Sample Units have been added to the queue ' + self.rabbitmq_queue)
        self.write_sampleunits_to_redis(sampleunits)

    def create_json(self, sample_id, sampleunit):
        sampleunit = {"id": str(sample_id), "attributes": sampleunit}

        return json.dumps(sampleunit)

    def publish_sampleunit(self, message):
        self.rabbitmq_channel.basic_publish(exchange=self.rabbitmq_exchange,
                                            routing_key=self.rabbitmq_queue,
                                            body=str(message),
                                            properties=pika.BasicProperties(content_type='text/xml'))

    def init_rabbit(self):
        rabbitmq_credentials = pika.PlainCredentials(self.rabbitmq_user, self.rabbitmq_password)
        self.rabbitmq_connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.rabbitmq_host,
                                      self.rabbitmq_port,
                                      self.rabbitmq_vhost,
                                      rabbitmq_credentials))
        self.rabbitmq_channel = self.rabbitmq_connection.channel()

        if self.rabbitmq_queue == 'localtest':
            self.rabbitmq_channel.queue_declare(queue=self.rabbitmq_queue)

    def write_sampleunits_to_redis(self, sampleunits):
        redis_connection = redis.StrictRedis(host=self.redis_host, port=self.redis_port, db=self.redis_db)

        print("Writing sampleunits to Redis")
        count = 0
        redis_pipeline = redis_connection.pipeline()
        for key, attributes in sampleunits.items():
            redis_connection.set(key, attributes)
            count += 1
            if count % 5000 == 0:
                sys.stdout.write("\r" + str(count) + " samples loaded")
                sys.stdout.flush()

        redis_pipeline.execute()
        print("Sample Units written to Redis")

    def load_sample(self, sample_file, collection_exercise_id, action_plan_id, collection_instrument_id):
        self.init_rabbit()
        self.sample_reader(sample_file, collection_exercise_id, action_plan_id, collection_instrument_id)
        self.rabbitmq_connection.close()
