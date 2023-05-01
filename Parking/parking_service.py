from datetime import datetime


class ParkingService:
    def __init__(self):
        self.ticket_id = 0
        self.parking_lots = {}

    def inc_id(self):
        self.ticket_id = self.ticket_id + 1

    def get_and_inc_ticket_id(self):
        self.inc_id()
        return self.ticket_id

    def is_vehicle_plate_already_parked(self, vehicle_plate) -> bool:
        for ticket_id, ticket_data in self.parking_lots.items():
            if ticket_data['vehicle_plate'] == vehicle_plate:
                return True

    def insert_vehicle_to_parking_lot(self, parking_lot: str, vehicle_plate: str) -> int or None:
        if self.is_vehicle_plate_already_parked(vehicle_plate):
            return None
        current_ticket_id = self.get_and_inc_ticket_id()
        self.parking_lots[current_ticket_id] = {'start_time': datetime.now(),
                                                "parking_lot": parking_lot,
                                                "vehicle_plate": vehicle_plate}

        return current_ticket_id

    def exit_from_parking_lot(self, ticket_id: str) -> dict or None:
        ticket_id = int(ticket_id)
        vehicle_data = self.parking_lots.get(ticket_id)
        if not vehicle_data:
            return None
        total_pay = ParkingService.calculate_total_pay(vehicle_data.get("start_time"))
        del self.parking_lots[ticket_id]
        del vehicle_data["start_time"]
        vehicle_data["total_pay"] = total_pay
        return vehicle_data

    @classmethod
    def calculate_total_pay(cls, start_time: datetime) -> float:
        time_diff = (datetime.now() - start_time)
        time_diff_in_minutes = (time_diff.total_seconds() / 60)/15
        total_pay = time_diff_in_minutes * 2.5
        return total_pay



