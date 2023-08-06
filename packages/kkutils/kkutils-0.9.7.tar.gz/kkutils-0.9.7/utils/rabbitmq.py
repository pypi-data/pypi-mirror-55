#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: zhangkai
Email: kai.zhang1@nio.com
Last modified: 2018-09-29 00:59:38
'''
import asyncio
import logging
import os
import pickle
from functools import partial

import aio_pika
import pika

from .log_utils import Logger
logging.getLogger('pika').setLevel(logging.ERROR)


class Pika:

    def __init__(self, queue='test', **kwargs):
        if any([key in kwargs for key in ['host', 'port', 'user', 'pwd', 'vhost']]):
            host = kwargs.pop('host', 'localhost')
            port = kwargs.pop('port', 5672)
            user = kwargs.pop('user', 'guest')
            pwd = kwargs.pop('pwd', 'guest')
            vhost = kwargs.pop('vhost', '/')
            self.uri = f'amqp://{user}:{pwd}@{host}:{port}{vhost}'
        elif 'uri' in kwargs:
            self.uri = kwargs.pop('uri')
        elif 'MQ_URI' in os.environ:
            self.uri = os.environ['MQ_URI']
        else:
            host = os.environ.get('MQ_HOST', 'localhost')
            port = os.environ.get('MQ_PORT', 5672)
            user = os.environ.get('MQ_USER', 'guest')
            pwd = os.environ.get('MQ_PWD', 'guest')
            vhost = os.environ.get('MQ_VHOST', '/')
            self.uri = f'amqp://{user}:{pwd}@{host}:{port}{vhost}'

        self.logger = Logger()
        self.queue = queue
        self.channels = {}
        self.connect()

    def get_channel(self, queue=None):
        queue = queue or self.queue
        if self.connection.is_closed:
            self.connect()

        if not (queue in self.channels and not self.channels[queue].is_closed):
            channel = self.connection.channel()
            channel.basic_qos(prefetch_count=1)
            channel.queue_declare(queue=queue, auto_delete=False, durable=False)
            self.channels[queue] = channel

        return queue, self.channels[queue]

    def connect(self):
        parameter = pika.URLParameters(self.uri)
        self.connection = pika.BlockingConnection(parameter)
        self.logger.info(self.connection)

    def _consume(self, process, channel, method_frame, header_frame, body):
        try:
            process(pickle.loads(body))
        except Exception as e:
            self.logger.exception(e)
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    def consume(self, process, queue=None):
        queue, channel = self.get_channel(queue)
        channel.basic_consume(queue, partial(self._consume, process))
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
            self.close()

    def publish(self, msg, queue=None):
        queue, channel = self.get_channel(queue)
        channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=pickle.dumps(msg))

    def close(self):
        for channel in self.channels.values():
            if not channel.is_closed:
                channel.close()
        if not self.connection.is_closed:
            self.connection.close()


class AioPika(Pika):

    def __init__(self, queue='test', workers=1, **kwargs):
        super().__init__(queue, **kwargs)
        self.workers = workers

    def connect(self):
        self.loop = asyncio.get_event_loop()
        if self.loop.is_running():
            self.loop.create_task(self._connect())
        else:
            self.loop.run_until_complete(self._connect())

    async def _connect(self):
        self.connection = await aio_pika.connect_robust(self.uri, loop=self.loop)
        self.logger.info(self.connection)

    async def get_channel(self, queue):
        queue = queue or self.queue
        if self.connection.is_closed:
            await self._connect()

        if not (queue in self.channels and not self.channels[queue].is_closed):
            channel = await self.connection.channel()
            await channel.set_qos(prefetch_count=1)
            self.channels[queue] = channel

        return queue, self.channels[queue]

    async def _consume(self, process, queue):
        async for msg in queue:
            try:
                await process(pickle.loads(msg.body))
            except Exception as e:
                self.logger.exception(e)
            finally:
                await msg.ack()

    async def consume(self, process, queue=None):
        queue, channel = await self.get_channel(queue)
        queue = await channel.declare_queue(queue, auto_delete=False, durable=False)
        for _ in range(self.workers):
            self.loop.create_task(self._consume(process, queue))

    async def publish(self, msg, queue=None):
        queue, channel = await self.get_channel(queue)
        await channel.default_exchange.publish(aio_pika.Message(pickle.dumps(msg)),
                                               routing_key=queue)

    async def close(self):
        for channel in self.channels.values():
            if not channel.is_closed:
                await channel.close()
        if not self.connection.is_closed:
            await self.connection.close()
