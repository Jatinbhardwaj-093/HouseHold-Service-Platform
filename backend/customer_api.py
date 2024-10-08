from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS
from app import app


@app.route('/api/v1/service', methods=['POST'])
def service():
    return jsonify({"hello": "world"})