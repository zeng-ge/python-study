import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

class Setting(BaseSettings):
    PROJECT_NAME: str = "test"
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")

setting = Setting()
print(setting.PROJECT_NAME, setting.model_dump())

# 通过SettingsConfigDict拿值时， os.environ取不到PROJECT_NAME
print("os get env:", os.environ.get("PROJECT_NAME"))
if not os.environ.get("PROJECT_NAME"):
    print("project name not inited")

# 在Setting的__init__内加载时，通过setting.PROJECT_NAME拿不到值, 通过SettingsConfigDict也可以在Setting内部拿到值
load_dotenv()
print("os get env:", os.environ.get("PROJECT_NAME"))

if os.environ.get("PROJECT_NAME"):
    print("project name inited")
