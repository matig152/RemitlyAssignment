from flask import Blueprint, request, jsonify
import pymongo
import json
from bson import json_util


swift_codes_blueprint = Blueprint('swift_codes', __name__)

myclient = pymongo.MongoClient("mongodb://localhost:27017")
database = myclient['swift_codes_db']


@swift_codes_blueprint.route("/")
def hello_world():
    return 'Hello, World!'


# ENDPOINT 1: DETAILS OF SINGLE SWIFT CODE
@swift_codes_blueprint.route("/v1/swift-codes/<swift_code>")
def endpoint1(swift_code):

    if (swift_code.endswith('XXX')): # HEADQUARTERS
        pipeline = [
        { 
            "$match": { "swiftCode": swift_code } 
        },
        { 
            "$addFields": {
                "isHeadquarter": {
                    "$cond": {
                        "if": { "$regexMatch": { "input": "$swiftCode", "regex": "XXX$" }},
                        "then": True,  
                        "else": False 
                    }
                }
            }
        },
        {
            "$lookup": {
                "from": "banks",   # <-- the collection name (self-join)
                "let": { "prefix": { "$substr": ["$swiftCode", 0, 8] } },  # define a variable
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$eq": [
                                    { "$substr": ["$swiftCode", 0, 8] },
                                    "$$prefix"
                                ]
                            }
                        }
                    },
                    {
                        "$addFields": {
                            "isHeadquarter": {
                                "$cond": [
                                    { "$regexMatch": { "input": "$swiftCode", "regex": "XXX$" } },
                                    True,
                                    False
                                ]
                            }
                        }
                    },
                    {
                        "$project": {
                            "_id": 0,
                            "address": 1,
                            "bankName": 1,
                            "countryISO2": 1,
                            "countryName": 1,
                            "isHeadquarter": 1,
                            "swiftCode": 1
                        }
                    }
                ],
                "as": "branches"
            }
        },
        { 
            "$project": {
                '_id': 0,
                'address': 1,
                'bankName': 1,
                'countryISO2': 1,
                'countryName': 1,
                'isHeadquarter': 1,
                'swiftCode': 1,
                'branches': 1 
            }
        }
        ]
        result = database['banks'].aggregate(pipeline)
        return jsonify(json.loads(json_util.dumps(result)))

    else:
        pipeline = [
        { 
            "$match": { "swiftCode": swift_code } 
        },
        { 
            "$addFields": {
                "isHeadquarter": {
                    "$cond": {
                        "if": { "$regexMatch": { "input": "$swiftCode", "regex": "XXX$" }},
                        "then": True,  
                        "else": False 
                    }
                }
            }
        },
        { 
            "$project": {
                '_id': 0,
                'address': 1,
                'bankName': 1,
                'countryISO2': 1,
                'countryName': 1,
                'isHeadquarter': 1,
                'swiftCode': 1,
            }
        }
        ]
        result = database['banks'].aggregate(pipeline)
        return jsonify(json.loads(json_util.dumps(result)))

# ENDPOINT 2: RETURN ALL SWIFT CODES WITH DETAILS FOR SPECIFIC COUNTRY
@swift_codes_blueprint.route("/v1/swift-codes/country/<countryISO2code>")
def endpoint2(countryISO2code):
    pipeline = [
        {
            "$match": { "countryISO2": countryISO2code }  # Match documents for the specific country
        },
        {
            "$group": {
                "_id": "$countryISO2", 
                "countryName": { "$first": "$countryName" },
                "swiftCodes": {
                    "$push": { 
                        "address": "$address",
                        "bankName": "$bankName",
                        "countryISO2": "$countryISO2",
                        "isHeadquarter": {
                            "$eq": [
                                { "$substrCP": ["$swiftCode", { "$subtract": [{ "$strLenCP": "$swiftCode" }, 3] }, 3] },
                                "XXX"
                            ]
                        },
                        "swiftCode": "$swiftCode"
                    }
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "countryISO2": "$_id", 
                "countryName": 1,
                "swiftCodes": 1
            }
        }
    ]
        
    result = database['banks'].aggregate(pipeline)
    return jsonify(json.loads(json_util.dumps(result))[0])

# ENDPOINT 3: ADD NEW SWIFT CODE TO DATABASE
@swift_codes_blueprint.route("/v1/swift-codes", methods=['POST'])
def endpoint3():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        required_fields = ['address', 'bankName', 'countryISO2', 'countryName', 'isHeadquarter', 'swiftCode']
            
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400

        if 'isHeadquarter' in data:
            del data['isHeadquarter']

        result = database['banks'].insert_one(data)

        return jsonify({'message': 'Swift code added succesfully.'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ENDPOINT 4: DELETE BANK WITH SPECIFIED SWIFT CODE
@swift_codes_blueprint.route('/v1/swift-codes/<swift_code>', methods=['DELETE'])
def endpoint4(swift_code):
    try:
        if not swift_code:
            return jsonify({'error': 'swiftCode is required'}), 400
        result = collection.delete_one({'swiftCode': swift_code})
        if result.deleted_count == 0:
            return jsonify({'error': 'No document found with the provided swiftCode'}), 404
        return jsonify({'message': f'Document with swiftCode {swift_code} deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500