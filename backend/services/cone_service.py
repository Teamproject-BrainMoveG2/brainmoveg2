from datetime import datetime
import logging

from fastapi.encoders import jsonable_encoder
import socketio
from models.models import Cone, ConeStatusDTO, ConeWithStatus

colors = ['red', 'blue', 'green', 'yellow']
cones = [Cone(cone_id=1, color="red", battery_percentage=None, last_status=None),
         Cone(cone_id=2, color="blue", battery_percentage=None, last_status=None),
         Cone(cone_id=3, color="green", battery_percentage=None, last_status=None),
         Cone(cone_id=4, color="yellow", battery_percentage=None, last_status=None)]

class ConeService:
    def __init__(self):
        self.logger = logging.getLogger(__name__) 
        self.logger.info("ConeService initialized.")

    async def register_cone(self, coneStatus: ConeStatusDTO, sio: socketio.AsyncServer) -> None:
        for c in cones:
            if c.cone_id == coneStatus.cone_id:
                c.battery_percentage = coneStatus.battery_percentage
                c.last_status = datetime.now()
                self.logger.info(f"Cone updated: {c}")
                await sio.emit('cone_update', jsonable_encoder(self.get_cones()))
                break
    def get_cones(self) -> list[ConeWithStatus]:
        conesWithStatus = []
        for c in cones:
            if c.battery_percentage is not None and c.last_status is not None:
                conesWithStatus.append(ConeWithStatus(
                    cone_id=c.cone_id,
                    color=c.color,
                    battery_percentage=c.battery_percentage,
                    connected=(datetime.now() - c.last_status).total_seconds() < 60
                ))
            else:
                conesWithStatus.append(ConeWithStatus(
                    cone_id=c.cone_id,
                    color=c.color,
                    battery_percentage=0,
                    connected=False
                ))
        return conesWithStatus

    def get_active_cones(self, max_cones: int = None):
        active_cones = [c for c in cones if c.battery_percentage is not None and (datetime.now() - c.last_status).total_seconds() < 60]
        if max_cones is not None:
            active_cones = active_cones[:max_cones]
        self.logger.debug(f"{datetime.now()} - Active cones retrieved: {active_cones}")
        self.logger.debug(f"{datetime.now()} - Total cones: {cones}")
        return active_cones