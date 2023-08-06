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
    mq.loop_start()
    mq.on_log = log

    collector = StatsCollector()
    while(True):
        for device in config.get_devices():
            data = collector.collect(device['device'])
            data['device'] = device['device']
            data['device_alias'] = device['device_alias']
            data['cache_read_hits_percentage'] = _calculate_percentage(int(data['cache_read_hits']), (int(data['cache_read_hits']) + int(data['cache_read_misses']))) 
            data['cache_write_hits_percentage'] = _calculate_percentage(int(data['cache_write_hits']), (int(data['cache_write_hits']) + int(data['cache_write_misses'])))
            print(data)
            mq.publish(device['target_topic'], json.dumps(data))
        
        time.sleep(30)

def _calculate_percentage(fraction, total):
    if total != 0:
        return fraction / total * 100
    
    return 0

def log(self, client, userdata, level, buf):
    if level >= client.MQTT_LOG_INFO:
        print(buf)

if __name__ == '__main__':
    main()
