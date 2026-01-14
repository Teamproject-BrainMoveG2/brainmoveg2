from datetime import datetime
import logging
from models.models import Cone, ConeStatusDTO

colors = ['red', 'blue', 'green', 'yellow']
cones = [Cone(cone_id=1, color="red", battery_percentage=None, last_status=None),
         Cone(cone_id=2, color="blue", battery_percentage=None, last_status=None),
         Cone(cone_id=3, color="green", battery_percentage=None, last_status=None),
         Cone(cone_id=4, color="yellow", battery_percentage=None, last_status=None)]

class ConeService:
    def __init__(self):
        self.logger = logging.getLogger(__name__) 
        self.logger.info("ConeService initialized.")

    def register_cone(self, coneStatus: ConeStatusDTO) -> None:
        for c in cones:
            if c.cone_id == coneStatus.cone_id:
                c.battery_percentage = coneStatus.battery_percentage
                c.last_status = datetime.now()
                self.logger.info(f"Cone updated: {c}")
                break
    def get_cones(self):
        return cones

    def get_active_cones(self):
        active_cones = [c for c in cones if c.battery_percentage is not None and (datetime.now() - c.last_status).total_seconds() < 60]
        return active_cones