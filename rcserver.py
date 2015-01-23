#!/usr/bin/env python
### BEGIN INIT INFO
# Provides:          RCServer
# Required-Start:    $syslog
# Required-Stop:     $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO
import sys, time
from daemon import Daemon
from subprocess import call
import json, os, bottle

class MyDaemon(Daemon):
    
    @bottle.hook("after_request")
    def setup_response():
        bottle.response.headers["Access-Control-Allow-Origin"] = "*"
        bottle.response.content_type="application/json"
        
    @bottle.route('/blyss/<key:re:[0-9A-F]{6}>/<channel:re:[0-5]>/<status:re:on|off>')
    def blyss(key,channel,status):
        call(["sudo", "/home/pi/BlyssController/send", str(key), str(channel), ("1" if status == 'on' else "0")])
        return json.dumps({'data':"ok"})
    
    @bottle.route('/x10/<device:re:[A-Pa-p]>/<unit:re:[1-16]>/<status:re:on|off>')
    def x10rf(device,unit,status):
        call(["sudo", "/home/pi/X10RF-raspberry/send", str(device), str(unit), ("1" if status == 'on' else "0")])
        return json.dumps({'data':"ok"})

    @bottle.route('/tristate/<state:re:[01F]{12}>')
    def tristate(state):
        call(["sudo", "/home/pi/rcswitch-pi/tristate", str(state)])
        return json.dumps({'data':"ok"})

    @bottle.route('/switch/<device:re:[0-1]{5}>/<unit:re:[1-5]>/<status:re:on|off>')
    def rcswitch(device,unit,status):
        call(["sudo", "/home/pi/rcswitch-pi/send", str(device), str(unit), ("1" if status == 'on' else "0")])
        return json.dumps({'data':"ok"})
    
    @bottle.error(404)
    def error404(error):
        bottle.setup_response()
        return json.dumps({'error':"404"})
    
    def run(self):
        bottle.run(host="0.0.0.0", port=int(os.environ.get("PORT", 80)))

if __name__ == "__main__":
	daemon = MyDaemon('/tmp/rcserver.pid') #, stderr="/dev/pts/0")
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		elif 'debug' == sys.argv[1]:
			daemon.run()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
