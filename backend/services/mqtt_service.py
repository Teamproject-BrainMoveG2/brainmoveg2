import paho.mqtt.client as mqtt
import json
import logging
import threading
import time
from typing import Callable, Optional

logger = logging.getLogger(__name__)

class MQTTService:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, broker_host: str = "localhost", broker_port: int = 1883, 
                username: Optional[str] = None, password: Optional[str] = None):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(MQTTService, cls).__new__(cls)
                    cls._instance._initialize(broker_host, broker_port, username, password)
        return cls._instance
    
    def _initialize(self, broker_host: str, broker_port: int, 
                   username: Optional[str], password: Optional[str]):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.username = username
        self.password = password
        self.client = None
        self.connected = False
        self._callbacks = {}
        self._lock_conn = threading.Lock()
    
    def connect(self):
        """Connect to MQTT broker"""
        with self._lock_conn:
            if self.connected:
                return
            
            try:
                self.client = mqtt.Client()
                self.client.on_connect = self._on_connect
                self.client.on_disconnect = self._on_disconnect
                self.client.on_message = self._on_message
                
                if self.username and self.password:
                    self.client.username_pw_set(self.username, self.password)
                
                self.client.connect(self.broker_host, self.broker_port, keepalive=60)
                self.client.loop_start()
                logger.info(f"Connecting to MQTT broker at {self.broker_host}:{self.broker_port}")
                
                # Wait for connection
                timeout = 10
                start_time = time.time()
                while not self.connected and (time.time() - start_time) < timeout:
                    time.sleep(0.1)
                
                if self.connected:
                    logger.info("Successfully connected to MQTT broker")
                else:
                    logger.warning("MQTT connection timeout")
                    
            except Exception as e:
                logger.error(f"Failed to connect to MQTT broker: {e}")
    
    def disconnect(self):
        """Disconnect from MQTT broker"""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            self.connected = False
            logger.info("Disconnected from MQTT broker")
    
    def publish(self, topic: str, payload: dict) -> bool:
        """Publish message to MQTT topic"""
        if not self.client:
            logger.warning(f"MQTT not connected. Cannot publish to {topic}")
            return False
        
        try:
            message = json.dumps(payload)
            msg_info = self.client.publish(topic, message, qos=1)
            if msg_info.rc != mqtt.MQTT_ERR_SUCCESS:
                logger.error(f"MQTT: Failed to queue message to {topic}, rc={msg_info.rc}")
                return False
            logger.info(f"Published to {topic}: {message}")
            return True
        except Exception as e:
            logger.error(f"Failed to publish to {topic}: {e}")
            return False
    
    def subscribe(self, topic: str, callback: Callable) -> bool:
        """Subscribe to MQTT topic with callback"""
        if not self.connected:
            logger.warning(f"MQTT not connected. Cannot subscribe to {topic}")
            return False
        
        try:
            self._callbacks[topic] = callback
            self.client.subscribe(topic, qos=1)
            logger.info(f"Subscribed to {topic}")
            return True
        except Exception as e:
            logger.error(f"Failed to subscribe to {topic}: {e}")
            return False
    
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            logger.info("MQTT: Connected successfully")
            for topic in self._callbacks:
                try:
                    self.client.subscribe(topic, qos=1)
                    logger.info(f"MQTT: Resubscribed to {topic} after connect")
                except Exception as e:
                    logger.error(f"MQTT: Failed to resubscribe to {topic}: {e}")
        else:
            logger.error(f"MQTT: Connection failed with code {rc}")
    
    def _on_disconnect(self, client, userdata, rc):
        self.connected = False
        if rc != 0:
            logger.warning(f"MQTT: Unexpected disconnection with code {rc}")
    
    def _on_message(self, client, userdata, msg):
        topic = msg.topic
        if topic in self._callbacks:
            try:
                payload = json.loads(msg.payload.decode())
                self._callbacks[topic](payload)
            except Exception as e:
                logger.error(f"Error processing message from {topic}: {e}")