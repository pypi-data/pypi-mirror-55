"""TaskBase"""
import json
import logging
import os
from typing import Dict, Any, List

from celery_service_task import MessageMetadata


class TransactionsList:
    LOCK_NAMING = '{key}.lock'

    def __init__(self, key, redis, limit):
        self.redis = redis
        self.key = key
        self.limit = limit
        self.lock_key = self.__class__.LOCK_NAMING

        with self.redis.lock(name=self.lock_key):
            if self.redis.exists(self.key) <= 0:
                self.redis.set(key, json.dumps([]))

    def get(self) -> List[str]:
        raw = self.redis.get(self.key)
        if raw is None:
            return []
        else:
            return json.loads(raw.decode())

    def add(self, t_id):
        with self.redis.lock(name=self.lock_key):
            l = self.get()
            l.append(t_id)
            if len(l) > self.limit:
                l = l[1:]
            self.redis.set(self.key, json.dumps(l))

    def exists(self, t_id):
        return t_id in self.get()



class TaskBase:
    TRANSACTION_IDX_SIZE: int = 256

    def __init__(self, conf: Dict[str, Any], redis, redis_key):
        self.conf: Dict[str, Any] = conf
        self.transaction_idx: TransactionsList = TransactionsList(redis_key, redis, self.__class__.TRANSACTION_IDX_SIZE)

    def run_task(self, payload: Dict[str, Any], meta: MessageMetadata, t_id: str) -> bool:
        if not self.transaction_idx.exists(t_id):
            self.transaction_idx.add(t_id)
            return self.task(payload, meta)
        else:
            logging.info('{klass} - This message is a replica - {t_id}'.format(
                klass=self.__class__.__name__.upper(),
                t_id=t_id
            ))
            return False

    def task(self, payload: Dict[str, Any], meta: MessageMetadata) -> bool:
        raise NotImplementedError
