from flask import Blueprint, request, jsonify
from app.routes.auth_routes import verify_token
from app.services.tree_service import (
    generate_tree_info,
    identify_tree,
    get_all_trees,
    delete_tree
)

tree_bp = Blueprint("tree", __name__)


def get_current_user():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    token = auth_header[7:]
    return verify_token(token)


@tree_bp.route("/trees", methods=["GET"])
def get_all():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)
    type_filter = request.args.get("type", default=None, type=str)

    data = get_all_trees(page=page, per_page=per_page, type_filter=type_filter)
    return jsonify(data)


@tree_bp.route("/trees/generate", methods=["POST"])
def generate():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"error": "Nama pohon wajib diisi"}), 400

    try:
        result = generate_tree_info(name)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@tree_bp.route("/trees/identify", methods=["POST"])
def identify():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    characteristics = data.get("characteristics")

    if not characteristics:
        return jsonify({"error": "Ciri-ciri pohon wajib diisi"}), 400

    try:
        result = identify_tree(characteristics)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@tree_bp.route("/trees/<int:tree_id>", methods=["DELETE"])
def delete(tree_id):
    user = get_current_user()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        success = delete_tree(tree_id)
        if success:
            return jsonify({"message": "Pohon berhasil dihapus"})
        else:
            return jsonify({"error": "Data tidak ditemukan"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
