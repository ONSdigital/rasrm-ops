import csv
import json
import os
import sys
import uuid

import jinja2
import pika
import redis



from flask import current_app as app

try:
    config_info = getattr(config, os.environ['APP_SETTINGS'])
except (AttributeError, KeyError) as e:
    config_info = config.DevelopmentConfig

# get rabbitmq env vars

rabbitmq_host = app.config['RABBITMQ_SERVICE_HOST']
rabbitmq_port = app.config['RABBITMQ_SERVICE_PORT']
rabbitmq_vhost = app.config['RABBITMQ_VHOST']
rabbitmq_queue = app.config['RABBITMQ_QUEUE']
rabbitmq_exchange = app.config['RABBITMQ_EXCHANGE']
rabbitmq_user = app.config['RABBITMQ_USER']
rabbitmq_password = app.config['RABBITMQ_PASSWORD']

# rabbit global vars
rabbitmq_credentials = None
rabbitmq_connection = None
rabbitmq_channel = None

# # get redis env vars
redis_host = app.config['REDIS_SERVICE_HOST']
redis_port = app.config['REDIS_SERVICE_PORT']
redis_db = app.config['REDIS_DB']

# globally load sampleunit message template
env = jinja2.Environment(loader=jinja2.FileSystemLoader(["./"]))
jinja_template = env.get_template("app/scripts/message_template.xml")


def sample_reader(file_obj, ce_uuid, ap_uuid, ci_uuid):
    init_rabbit()
    sampleunits = {}
    reader = csv.DictReader(file_obj, delimiter=',')
    count = 0
    for sampleunit in reader:
        sample_id = uuid.uuid4()
        sampleunits.update({"sampleunit:" + str(sample_id): create_json(sample_id, sampleunit)})
        publish_sampleunit(
            jinja_template.render(sample=sampleunit, uuid=sample_id, ce_uuid=ce_uuid, ap_uuid=ap_uuid, ci_uuid=ci_uuid))
        count += 1
        if count % 5000 == 0:
            sys.stdout.write("\r" + str(count) + " samples loaded")
            sys.stdout.flush()

    print('\nAll Sample Units have been added to the queue ' + rabbitmq_queue)
    rabbitmq_connection.close()
    write_sampleunits_to_redis(sampleunits)


def create_json(sample_id, sampleunit):
    sampleunit = {"id": str(sample_id), "attributes": sampleunit}

    return json.dumps(sampleunit)


def publish_sampleunit(message):
    rabbitmq_channel.basic_publish(exchange=rabbitmq_exchange,
                                   routing_key=rabbitmq_queue,
                                   body=str(message),
                                   properties=pika.BasicProperties(content_type='text/xml'))


def init_rabbit():
    global rabbitmq_credentials, rabbitmq_connection, rabbitmq_channel
    rabbitmq_credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    rabbitmq_connection = pika.BlockingConnection(
        pika.ConnectionParameters(rabbitmq_host,
                                  rabbitmq_port,
                                  rabbitmq_vhost,
                                  rabbitmq_credentials))
    rabbitmq_channel = rabbitmq_connection.channel()

    if rabbitmq_queue == 'localtest':
        rabbitmq_channel.queue_declare(queue=rabbitmq_queue)


def write_sampleunits_to_redis(sampleunits):
    redis_connection = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

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


def load_sample(sample_file, collection_exercise_id, action_plan_id, collection_instrument_id):
    init_rabbit()
    # with open('/tmp/'+sample_file) as f_obj:
    sample_reader(sample_file, collection_exercise_id, action_plan_id, collection_instrument_id)

# ------------------------------------------------------------------------------------------------------------------
# Usage python loadSample.py <SAMPLE.csv> <COLLECTION_EXERCISE_UUID> <ACTIONPLAN_UUID> <COLLECTION_INSTRUMENT_UUID>
# ------------------------------------------------------------------------------------------------------------------

# if __name__ == "__main__":
#     if len(sys.argv) < 4:
#         print(
#             'Usage python loadSample.py sample.csv <COLLECTION_EXERCISE_UUID> <ACTIONPLAN_UUID> <COLLECTION_INSTRUMENT_UUID>')
#     else:
#         init_rabbit()
#         with open(sys.argv[1]) as f_obj:
#             sample_reader(f_obj, sys.argv[2], sys.argv[3], sys.argv[4])
