import os 
import json
import environs
from dataclasses import dataclass



@dataclass
class Config:
    APPLICATION_NAME: str
    LISTEN_PORT: int
    DEBUG: bool
    DATABASE: dict


    @classmethod
    def load(cls):
        env = environs.Env()
        env.read_env()

        config = {
            "APPLICATION_NAME" : "NOTES"
        }

        cloud_provider = env("CLOUD_PROVIDER", "LOCAL")

        if cloud_provider == "cloud":
            config.update(Config.from_cloud(env))
        else:
            config.update(Config.from_local(env))
        return cls(**config)
    
    @staticmethod
    def from_cloud(env: environs.Env):
        return_value = {
            "LISTEN_PORT" : 9000,
            "DEBUG" : False
        }
        return return_value
    

    @staticmethod
    def from_local(env: environs.Env):
        return {
            "LISTEN_PORT" : 9000,
            "DEBUG" : True,
            "DATABASE" : {
                "username": env("DB_USER"),
                "password": env("DB_PASSWORD"),
                "engine": env("DB_ENGINE", "LOCAL"),
                "host": env("DB_HOST"),
                "port": env.int("DB_PORT", 3306),
                "dbname": env("DB_NAME", "notes_db")
            },
        }



