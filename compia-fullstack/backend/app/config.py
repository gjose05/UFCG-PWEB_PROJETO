from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    app_env:str='development'; secret_key:str='change-me'; database_url:str='postgresql+psycopg://compia:compia@localhost:5432/compia'; cors_origins:str='http://localhost:5173'; frontend_url:str='http://localhost:5173'; shipping_flat_rate:float=19.90; payment_provider:str='mock'; stripe_secret_key:str=''; stripe_webhook_secret:str=''; admin_email:str='admin@compia.com.br'; admin_password:str='Admin123!'
    model_config=SettingsConfigDict(env_file='.env',extra='ignore')
    @property
    def cors_list(self): return [x.strip() for x in self.cors_origins.split(',') if x.strip()]
@lru_cache
def get_settings(): return Settings()
settings=get_settings()
