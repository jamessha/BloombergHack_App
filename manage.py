#!/usr/bin/env python
import os
import sys
import threading


import time
import phone_messenger as msg

SLEEP_TIME = 60 # seconds

def query_cycle():
	counter = 0
	while(True):
		counter += 1
		print "call from: ", os.getpid()
		current_time = time.asctime( time.localtime(time.time()) )
		message = "testing texting: " + str(counter) + " sent at: " + str(current_time)
		print ">>>>> Begin call to to send_text...: ", message
		msg.send_text('5103886932', 'att', message)
		print ">>>>> Finished called to send_text \n"
		time.sleep(SLEEP_TIME)

if __name__ == "__main__":
	if ('runloop' in sys.argv):
		query_cycle()
	else:
		os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BloombergHack_App.settings")
		from django.core.management import execute_from_command_line
		execute_from_command_line(sys.argv)