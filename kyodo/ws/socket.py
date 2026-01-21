from aiohttp import ClientSession, WSMsgType, ClientWebSocketResponse, ClientConnectionError, WSServerHandshakeError, ClientTimeout
from asyncio import create_task, TimeoutError, CancelledError
from asyncio import sleep as asleep
from json import loads, dumps
import asyncio

from ..utils import log, exceptions
from ..utils.constants import ws_api
from .socket_handler import Handler

class Socket(Handler):

	"""
	Module for working with kyodo socket in real time. Not used separately from the client.
	"""

	token: str
	deviceId: str

	socket_enable: bool

	def __init__(self):
		self.connection: ClientWebSocketResponse = None
		self.task_receiver = None
		self.task_pinger = None
		self.ws_client_session = None

		Handler.__init__(self)
	

	async def ws_on_close(self, code: int, reason: str) -> None:
		log.debug("[ws][close] Closed with code %s and reason %s", code, reason)
		if self.task_receiver:
			self.task_receiver.cancel()


	async def ws_resolve(self):
		retry_count = 0
		max_retries = 5
		
		while True:
			try:
				if self.connection is None:
					await asleep(1)
					continue
				
				retry_count = 0 
					
				try:
					msg = await asyncio.wait_for(
						self.connection.receive(), 
						timeout=35
					)
				except asyncio.TimeoutError:
					log.debug("[ws][receive] Timeout, attempting reconnect...")
					await self.reconnect()
					continue
				except CancelledError:
					log.debug("[ws][receive] Task cancelled")
					return
					
				if msg.type != WSMsgType.TEXT:
					continue
					
				try:
					data = loads(msg.data)
				except Exception as e:
					log.debug(f"[ws][receive] Failed to parse message: {e}")
					continue

				log.debug(f"[ws][receive]: {data}")
				await self.handle_data(data)
				
			except (WSServerHandshakeError, ClientConnectionError) as e:
				log.debug(f"[ws][receive] Connection error: {e}")
				retry_count += 1
				if retry_count > max_retries:
					log.error("[ws][receive] Max retries exceeded")
					return
				await self.reconnect()
				continue
			except CancelledError:
				log.debug("[ws][receive] Task cancelled")
				return
			except Exception as e:
				log.error(f"[ws][receive] Unexpected error: {e}")
				retry_count += 1
				if retry_count > max_retries:
					log.error("[ws][receive] Max retries exceeded")
					return
				await self.reconnect()
				continue


	async def ws_connect(self):
		"""Connect to web socket"""
		if self.connection:
			log.debug("[ws][start] Socket already running")
			return
		
		if not self.token:
			raise exceptions.NeedAuthError
		
		if self.ws_client_session:
			try:
				log.debug("[ws][start] Closing old session...")
				await asyncio.wait_for(self.ws_client_session.close(), timeout=5)
			except:
				pass
			self.ws_client_session = None
		
		try:
			self.ws_client_session = ClientSession(
				base_url=ws_api,
				timeout=ClientTimeout(total=20, connect=15, sock_connect=10, sock_read=15)
			)
			
			self.connection = await asyncio.wait_for(
				self.ws_client_session.ws_connect(
					f"/?token={self.token}&deviceId={self.deviceId}",
					proxy=self.req.proxy,
					heartbeat=20,
					autoclose=True
				),
				timeout=20
			)

			if not self.task_receiver:
				self.task_receiver = create_task(self.ws_resolve())
			if not self.task_pinger:
				self.task_pinger = create_task(self.__pinger())
			
			log.debug("[ws][start] Socket started successfully")
		except asyncio.TimeoutError:
			self.connection = None
			if self.ws_client_session:
				try:
					await asyncio.wait_for(self.ws_client_session.close(), timeout=5)
				except:
					pass
			self.ws_client_session = None
			log.error("[ws][start] WebSocket connection timeout")
		except Exception as e:
			self.connection = None
			if self.ws_client_session:
				try:
					await asyncio.wait_for(self.ws_client_session.close(), timeout=5)
				except:
					pass
			self.ws_client_session = None
			log.error(
				f"[ws][start] Error starting socket: {e}"
			)


	async def ws_disconnect(self):
		"""Disconnect from websocket"""
		log.debug("[ws][stop] Closing socket...")
		
		if self.task_pinger:
			log.debug(f"[ws][pinger] Closing...")
			self.task_pinger.cancel()
			self.task_pinger = None
		
		# Закрой соединение
		if self.connection:
			log.debug("[ws][stop] Closing connection...")
			try:
				await asyncio.wait_for(self.connection.close(), timeout=3.0)
			except Exception as e:
				log.debug(f"[ws][stop] Error closing connection: {e}")
			self.connection = None
		
		# Закрой сессию
		if self.ws_client_session:
			log.debug("[ws][stop] Closing session...")
			try:
				await asyncio.wait_for(self.ws_client_session.close(), timeout=3.0)
			except Exception as e:
				log.debug(f"[ws][stop] Error closing session: {e}")
			self.ws_client_session = None
		
		log.debug("[ws][stop] Socket closed")


	async def reconnect(self):
		log.debug("[ws][reconnect] Socket reconnecting...")
		await self.ws_disconnect()
		await asleep(2)
		try:
			await asyncio.wait_for(self.ws_connect(), timeout=25)
		except asyncio.TimeoutError:
			log.error("[ws][reconnect] Reconnection timeout")
		except Exception as e:
			log.error(f"[ws][reconnect] Reconnection failed: {e}")


	async def __pinger(self):
		log.debug(f"[ws][pinger] started.")
		while self.connection:
			try:
				if self.connection:
					await self.ws_send('{"o":7,"d":{}}')
					await asleep(10)
			except Exception as e:
				log.debug(f"[ws][pinger] Ping error: {e}")
				await asleep(2)


	async def ws_send(self, data: str | dict):
		"""Send message to websocket"""
		if self.connection is None:
			log.debug("[ws][send] Socket not running")
			return
		
		try:
			log.debug(f"[ws][send]: {data}")
			await self.connection.send_str(
				data if isinstance(data, str) else dumps(data)
			)
		except CancelledError:
			raise
		except Exception as e:
			log.debug(f"[ws][send] Error sending message: {e}")
			await self.reconnect()


	async def socket_wait(self):
		"""
		Starts a loop that continuously listens for new messages from the WebSocket connection.
		
		This method is used to keep the program running and process incoming messages in real-time. 
		It ensures that the WebSocket connection remains open, and the program doesn't exit unexpectedly while 
		awaiting messages. 

		The loop will run as long as `self.socket_enable` is True. The method sleeps for 3 seconds between 
		iterations to prevent unnecessary CPU usage while waiting for new data.

		Example:
			await client.socket_wait()
		"""
		try:
			while self.socket_enable:
				await asleep(3)
		except CancelledError:
			log.debug("[ws][socket_wait] Socket wait cancelled")
			await self.ws_disconnect()