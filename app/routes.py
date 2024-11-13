from flask import Blueprint, jsonify, request

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return jsonify({"message": "Welcome to the Royal Enfield Auction Hub!"})