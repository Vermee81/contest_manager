"""アプリケーション設定"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = (
        "mysql+aiomysql://contest_user:contest_pass@localhost:3306/contest_manager"
    )
    test_database_url: str = (
        "mysql+aiomysql://contest_user:contest_pass@localhost:3307/contest_manager_test"
    )

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}
