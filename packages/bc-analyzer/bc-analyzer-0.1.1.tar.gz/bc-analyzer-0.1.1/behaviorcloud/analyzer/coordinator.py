import argparse
import datetime
import sys
import threading
import time
from sentry_sdk import capture_exception, init

from . import api
from . import data
from .globals import set_config
from .analyzer import Analyzer

def flush_print(line):
	print(datetime.datetime.now().isoformat(), line)
	sys.stdout.flush()

def flush_write(message):
	sys.stdout.write(message)
	sys.stdout.flush()

class Coordinator:
	def __init__(self, converter):
		self.analyzers = {}
		self.converter = converter
		self.running = False
		self.parser = argparse.ArgumentParser(description='Create a Centroid Ambulation analysis for the BehaviorCloud platform.')
		self.parser.add_argument('--host', nargs='?', required=True, help='The hostname of the BehaviorCloud api server. Typically, this is api.behaviorcloud.com.')
		self.parser.add_argument('--token', nargs='?', required=True, help='The JWT token provided by the BehaviorCloud platform.')
		self.parser.add_argument('--id', nargs='?', help='The queued analysis id.')
		self.parser.add_argument('--daemon', action='store_true', help='Will run this analyzer is a daemonized mode, watching for new jobs.')

	def analyze(self, queued_analysis_id):
		if queued_analysis_id in self.analyzers:
			return
		analyzer = Analyzer(queued_analysis_id, self.converter)
		self.analyzers[queued_analysis_id] = analyzer

		flush_print('Starting Converting Queued Analysis: %s' % (queued_analysis_id))
		try:
			analyzer.start()
			flush_print('Finished Converting Queued Analysis: %s' % (queued_analysis_id))
			return True
		except Exception as e:
			capture_exception(e)
			flush_print('Error Converting Queued Analysis: %s' % (queued_analysis_id))

		return False

	def run(self):
		arguments = self.parser.parse_args()
		set_config({
			'HOST': arguments.host,
			'TOKEN': arguments.token,
			'API_VERSION': '1.1',
		})

		if not arguments.id and not arguments.daemon:
			flush_print('You must either supply an id or use daemon mode')
			return

		init('https://5196a2999eb1497a8fd043d2683e30c0@sentry.io/1298461')

		if arguments.id:
			self.analyze(arguments.id)
		
		if arguments.daemon:
			self.start()
	
	def start(self):
		if self.running:
			return
		self.running = True
		flush_print('Starting analysis daemon')
		t = threading.Thread(target=self.daemon)
		t.start()

	def daemon(self):
		def spinning_cursor():
			while True:
				for cursor in '▁▂▃▄▅▆▇█▇▆▅▄▃▂▁':
					yield cursor

		spinner = spinning_cursor()

		while (self.running):
			queued_analyses = api.get_queued_analysis_index()
			ran = False
			for queued_analysis in queued_analyses:
				if queued_analysis['ended']:
					continue
				id = queued_analysis['id']
				ran = self.analyze(id)
			if not ran:
				for _ in range(15):
					message = next(spinner) + ' waiting for analyses...'
					flush_write(message)
					time.sleep(0.1)
					[sys.stdout.write('\b') for x in message]
	
	def stop(self):
		self.running = False
