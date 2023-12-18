# coding: utf-8
import redis

from utils.env import Env


def new_connection():
    return redis.Redis(
        host=Env.RDS_HOST,
        port=int(Env.RDS_PORT),
        db=int(Env.RDS_DB),
        password=Env.RDS_PASSWORD,
    )
