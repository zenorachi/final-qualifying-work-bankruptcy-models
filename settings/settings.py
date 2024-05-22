from pydantic import BaseSettings, Field, AnyHttpUrl


class Settings(BaseSettings):
    fns_api_url: AnyHttpUrl | None = Field(env="FNS_API_URL", default=None)
    token: str | None = Field(env='TOKEN', default=None)
    company_inn: str | None = Field(env="COMPANY_INN", default=None)
    cert: str | None = Field(env="CERT", default=None)
    key: str | None = Field(env="KEY", default=None)
    liquidity_file: str | None = Field(env="LIQUIDITY_FILE", default=None)

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


def get_settings() -> Settings:
    return Settings()
