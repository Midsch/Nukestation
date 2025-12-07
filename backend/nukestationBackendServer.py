from flask import Flask, request
import flask
import json
from flask_cors import CORS
import subprocess

import getBlockdeviceInfo
import commandInterface
import logfileParser
import unmountBlockdevice

app = Flask(__name__)
CORS(app)


@app.route('/getBlockdeviceInfo', methods=["GET"])
def route_get_blockdevice_info():
    try:
        devices = getBlockdeviceInfo.getBlockdeviceInfo()
        print("getBlockdeviceInfo() returned:", devices, flush=True)
        return flask.jsonify(devices)
    except Exception as e:
        print("ERROR in /getBlockdeviceInfo:", repr(e), flush=True)
        return flask.jsonify({"error": str(e)}), 500

@app.route('/unmount', methods=['POST'])
def unmount():
    requestData = request.get_json()
    print(requestData)
    if 'blockdeviceName' in requestData:
        print('Blockdevice name found!')
        tmp = requestData['blockdeviceName']
        answer = unmountBlockdevice.unmountBlockdevice(tmp)
        print(answer)
    return 'answer'

@app.route('/', methods=['POST'])
def json_example():
    requestData = request.get_json()
    print(requestData)
    if 'command' in requestData:
        print('command found!')
        tmp = requestData['command']
        nwipePID = commandInterface.executeCommand(tmp)
        print(nwipePID)
    return {'nwipe pid' : nwipePID}

@app.route('/sendWipeCommand', methods=["POST"])
def route_send_wipe_command():
    data = flask.request.get_json()
    command_string = data.get("command")

    if not command_string:
        return flask.jsonify({"error": "missing command"}), 400

    try:
        pid = commandInterface.executeCommand(command_string)
        return flask.jsonify({"pid": pid})
    except Exception as e:
        print("ERROR in /sendWipeCommand:", repr(e), flush=True)
        return flask.jsonify({"error": str(e)}), 500

@app.route('/kill', methods=['POST'])
def killCommand():
    requestData = request.get_json()
    print(requestData)
    if 'command' in requestData:
        print('command found!')
        
        #pid = int(requestData['command'])
        blockdeviceName = requestData['command']
        #print(pid)
        #print(type(pid))
        print(blockdeviceName)
        #success = commandInterface.executeKill(pid)
        success = commandInterface.executeKill(blockdeviceName)
        print(success)
    return {'message' : 'process killed'}

@app.route('/progress', methods=["POST"])
def progress():
    requestData = request.get_json()
    print(requestData)
    if 'logfileName' in requestData:
        print('logfile name found!')
        logfileDir = requestData['logfileDir']
        logfileName = requestData['logfileName']
        blockdeviceName = requestData['blockdeviceName']
        print(logfileDir + logfileName + ' - ' + blockdeviceName)
        progress = logfileParser.accessFileByLine(logfileDir, logfileName, blockdeviceName)
        print(progress)
    return {'progress' : progress}
    #currentInfo = commandInterface.getInfoFromLogfile()
    
    #data = [{
    #    "progress": currentInfo,
    #}]
    
    #data = [currentInfo]
    #return flask.jsonify(data)
    return 1



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6969, debug=False)
