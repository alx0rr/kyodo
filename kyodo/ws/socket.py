from threading import Thread
from websocket import WebSocketApp, enableTrace
from websocket import _exceptions as WSexceptions
from orjson import loads, dumps
from time import sleep
from typing import Any

from kyodo.utils import log, exceptions
from kyodo.utils.constants import ws_api, ws_ping_interval
from kyodo.ws.socket_handler import Handler


class Socket(Handler):
	"""
	Module for working with kyodo socket in real time. Not used separately from the client.
	"""

	token: str
	deviceId: str
	socket_enable: bool

	connection: WebSocketApp = None

	def __init__(self, sock_trace: bool = False, socket_daemon: bool = True):
		self.socket_daemon = socket_daemon
		enableTrace(sock_trace)

		Handler.__init__(self)



	def ws_connect(self):
		"""Connect to web socket"""
		
		if self.connection:
			log.debug("[ws][start] Socket already running")
			return

		if not self.token:
			raise exceptions.NeedAuthError

		try:
			self.connection = WebSocketApp(
				f"{ws_api}/?token={self.token}&deviceId={self.deviceId}",
				on_message=self.ws_resolve,
				on_open=self.ws_on_open,
				on_error=self.ws_on_error,
				on_close=self.ws_on_close,
				
				
			)
			Thread(target=self.connection.run_forever, daemon=self.socket_daemon).start()
		except Exception as e:
			self.connection = None
			log.error(
				f"[ws][start] Error starting socket: {e}"
			)


	def ws_disconnect(self) -> None:
		"""Disconnect from websocket"""

		if self.connection:
			log.debug("[ws][stop] Closing socket...")
			try:
				self.connection.close()
			except Exception as e:
					log.debug(f"[ws][stop] Error while closing Socket : {e}")
		else:
			log.debug(f"[ws][stop] Socket not running.")


	def reconnect(self):
		log.debug("[ws][reconnect] Socket reconnecting...")
		self.ws_disconnect()
		sleep(2)
		self.ws_connect()


	def ws_send(self, data: dict) -> None:
		"""Send message to websocket"""

		if self.connection is None:
			log.debug("[ws][send] Socket not running")
			return
		log.debug(f"[ws][send]: {data}")
		try:return self.connection.send(data)
		except WSexceptions.WebSocketConnectionClosedException:
			log.debug(f"[ws][send] Socket not available : {data}")
			self.reconnect()
		except Exception as e:
			log.debug(f"[ws][send] Error sending message: {e}")
			self.reconnect()
	

	def ws_resolve(self, ws: Any, data: str | bytes | bytearray):
		try:
			d = loads(data)
		except Exception as e:
			log.debug(f"[ws][receive] Failed to parse message: {e}")
			return
		
		log.debug(f"[ws][receive]: {d}")
		self.handle_data(d)

	def ws_on_close(self, ws: Any, data: str, status: int):
		log.debug(f"[ws][close] Socket closed: {data} [status: {status}]")
		self.connection = None

	def ws_on_error(self, ws: Any, error: Any) -> None:
		log.error(f"[ws][error]: {error}")

	def ws_on_open(self, ws: Any) -> None:
		log.debug(f"[ws][start] Socket started")
		Thread(target=self.__pinger, daemon=self.socket_daemon).start()




	def __pinger(self):
		log.debug(f"[ws][pinger] started.")
		while self.socket_enable and self.connection:
			try:
				if self.connection:
					self.ws_send('{"o":7,"d":{}}')
					sleep(ws_ping_interval)
			except Exception as e:
				log.debug(f"[ws][pinger] Ping error: {e}")
				sleep(2)



	def socket_wait(self):
		"""
		Starts a loop that continuously listens for new messages from the WebSocket connection.
		
		This method is used to keep the program running and process incoming messages in real-time. 
		It ensures that the WebSocket connection remains open, and the program doesn't exit unexpectedly while 
		awaiting messages. 

		The loop will run as long as `self.socket_enable` is True. The method sleeps for 3 seconds between 
		iterations to prevent unnecessary CPU usage while waiting for new data.

		Example:
			client.socket_wait()
		"""
		try:
			while self.socket_enable:
				sleep(3)
		except KeyboardInterrupt:
			log.debug("[ws][socket_wait] Socket wait cancelled")
			self.ws_disconnect()