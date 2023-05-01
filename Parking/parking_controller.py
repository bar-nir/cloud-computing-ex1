from flask import Blueprint, request, jsonify
from Parking.parking_service import ParkingService


parking_controller = Blueprint('parking_controller', __name__)
parking_service = ParkingService()


@parking_controller.route('/entry', methods=['POST'])
def create_ticket():
    plate = request.args.get('plate')
    parking_lot = request.args.get('parkingLot')
    ticket_id = parking_service.insert_vehicle_to_parking_lot(parking_lot, plate)
    if not ticket_id:
        return jsonify({'error': f'vehicle with plate: {plate} already parked,'
                                 ' please pay before trying to enter another parkinglot'}), 400
    return jsonify({'ticketId': ticket_id}), 201


@parking_controller.route('/exit', methods=['POST'])
def close_ticket():
    ticket_id = request.args.get('ticketId')
    vehicle_data = parking_service.exit_from_parking_lot(ticket_id)
    if vehicle_data is None:
        return jsonify({'error': 'Invalid ticket ID'}), 500

    return jsonify(vehicle_data), 200
