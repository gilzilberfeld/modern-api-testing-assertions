import time
from flask import Blueprint, jsonify, request
import state

mod_bp = Blueprint("moderation", __name__)


@mod_bp.route("/moderate", methods=["POST"])
def moderate():
    if state.mode == "reject":
        return jsonify({"approved": False, "reason": state.reject_reason}), 200
    if state.mode == "error":
        return jsonify({"error": "Internal moderation error"}), 500
    if state.mode == "delay":
        time.sleep(state.delay_seconds)
    return jsonify({"approved": True}), 200


@mod_bp.route("/admin/configure", methods=["POST"])
def configure():
    data = request.get_json(silent=True) or {}
    if "mode" in data:
        state.mode = data["mode"]
    if "delay_seconds" in data:
        state.delay_seconds = data["delay_seconds"]
    if "reject_reason" in data:
        state.reject_reason = data["reject_reason"]
    return jsonify({"status": "ok"}), 200


@mod_bp.route("/admin/reset", methods=["POST"])
def reset():
    state.mode = "approve"
    state.delay_seconds = 0
    state.reject_reason = "Content not appropriate"
    return jsonify({"status": "ok"}), 200
