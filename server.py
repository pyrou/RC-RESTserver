from bottle import *
from subprocess import call
import json, os

@hook("after_request")
def setup_response():
	response.headers["Access-Control-Allow-Origin"] = "*"
	response.content_type="application/json"

@route('/blyss/<key:re:[0-9A-F]{6}>/<channel:re:[0-5]>/<status:re:on|off>')
def blyss(key,channel,status):
        call(["sudo", "./BlyssController-raspberry/send", str(key), str(channel), ("1" if status == 'on' else "0")])
        return json.dumps({'data':"ok"})

@route('/x10/<device:re:[A-Pa-p]>/<unit:re:[1-16]>/<status:re:on|off>')
def x10rf(device,unit,status):
	call(["sudo", "./X10RF-raspberry/send", str(device), str(unit), ("1" if status == 'on' else "0")])
	return json.dumps({'data':"ok"})

@route('/switch/<device:re:[0-1]{5}>/<unit:re:[1-5]>/<status:re:on|off>')
def rcswitch(device,unit,status):
	call(["sudo", "./rcswitch-pi/send", str(device), str(unit), ("1" if status == 'on' else "0")])
	return json.dumps({'data':"ok"})
	redirect('/')

@error(404)
def error404(error):
	setup_response()
	return json.dumps({'error':"404"})

run(host="0.0.0.0", port=int(os.environ.get("PORT", 80)))
