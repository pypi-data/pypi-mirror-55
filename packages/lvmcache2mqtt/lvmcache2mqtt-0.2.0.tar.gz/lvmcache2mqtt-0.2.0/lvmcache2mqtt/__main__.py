import json
import time

import paho.mqtt.client as mqtt

from . import Config, StatsCollector

def main():
    config_file = 'config.yml'
    config = Config(config_file)


    mqtt_config = config.get_mqtt()
    mq = mqtt.Client()
    mq.connect(mqtt_config['host'])
    mq.on_log = log

    collector = StatsCollector()
    while(True):
        for device in config.get_devices():
            data = collector.collect(device['device'])
            data['device'] = device['device']
            data['device_alias'] = device['device_alias']
            data['cache_read_hits_percentage'] = data['cache_read_hits'] / (data['cache_read_hits'] + data['cache_read_misses']) * 100
            data['cache_write_hits_percentage'] = data['cache_write_hits'] / (data['cache_write_hits'] + data['cache_write_misses']) * 100
            print(data)
            mq.publish(device['target_topic'], json.dumps(data))
        
        time.sleep(30)

    
def log(self, client, userdata, level, buf):
    if level >= MQTT_LOG_INFO:
        print(buf)


if __name__ == '__main__':
    main()
