import logging
from typing import Optional
from services.mqtt_service import MQTTService
from models.models import ConeWithStatus

logger = logging.getLogger(__name__)

class BuzzerService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("BuzzerService initialized.")
    
    def trigger_buzzer(self, cone_id: int, cone_color: str, 
                      buzzer_pattern: str = "single", 
                      duration_ms: int = 100, mqtt_service: Optional[MQTTService] = None) -> bool:
        """
        Trigger buzzer on a specific cone via MQTT
        
        Args:
            cone_id: ID of the cone to trigger
            cone_color: Color of the cone (red, blue, green, yellow)
            buzzer_pattern: Pattern type - "single", "double", "triple", "long"
            duration_ms: Duration of buzzer tone in milliseconds
        
        Returns:
            bool: Success status
        """
        if not mqtt_service:
            self.logger.warning("MQTT service not available")
            return False
        
        topic = f"brainmove/cones/{cone_id}/buzzer"
        payload = {
            "cone_id": cone_id,
            "action": "beep",
            "pattern": buzzer_pattern,
            "duration_ms": duration_ms
        }
        
        success = mqtt_service.publish(topic, payload)
        if success:
            self.logger.info(f"Buzzer triggered for cone {cone_id} ({cone_color}): {buzzer_pattern}")
        return success
    
    def trigger_buzzer_for_round_start(self, cone: ConeWithStatus, mqtt_service: Optional[MQTTService] = None) -> bool:
        """Trigger buzzer when a round starts (player should hit this cone)"""
        return self.trigger_buzzer(
            cone_id=cone.cone_id,
            cone_color=cone.color,
            buzzer_pattern="long",
            duration_ms=150,
            mqtt_service=mqtt_service
        )
    