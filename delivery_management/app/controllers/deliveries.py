''' controller and routes for deliveries '''
import os
import logger
import json
from flask import request, jsonify
from bson import json_util
from app import app, mongo


@app.route('/delivery', methods=['GET', 'POST', 'DELETE'])
def delivery():
    ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
    LOG = logger.get_root_logger(os.environ.get('ROOT_LOGGER', 'root'), filename=os.path.join(ROOT_PATH, 'deliveries-output.log'))
    if request.method == 'GET':
        LOG.info(f'on GET delivery query args are : {query}')
        query = request.args
        data = mongo.db.deliveries.find_one(query)
        return json.loads(json_util.dumps(data))

    data = request.get_json()
    if request.method == 'POST':
        if data.get('transport', None) is not None and data.get('quantity', None) is not None:
            response = mongo.db.deliveries.insert_one(data)
            #inserted_id = str(response.inserted_id)
            # return jsonify({'ok': True, 'message': 'Delivery created successfully with id:'+inserted_id+'!'}), 200
            return jsonify({'ok': True, 'message': 'Delivery created successfully!'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    if request.method == 'DELETE':
        if data.get('transport', None) is not None:
            db_response = mongo.db.deliveries.delete_one(
                {'transport': data['transport']})
            if db_response.deleted_count == 1:
                response = {'ok': True, 'message': 'record deleted'}
            else:
                response = {'ok': True, 'message': 'no record found'}
            return jsonify(response), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
