from typing import Literal
from urllib.parse import urlsplit

from pydantic import EmailStr, Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="EDUTRACK_", extra="ignore", env_file_encoding="utf-8"
    )

    environment: Literal["development", "production", "test"] = "development"
    sql_server: str = r"localhost\SQLEXPRESS"
    sql_database: str = "EduTrackIA"
    trust_server_certificate: bool = False
    database_url: SecretStr | None = None
    db_writes_enabled: bool = False
    jwt_secret: SecretStr | None = None
    token_minutes: int = Field(default=20, ge=5, le=60)
    cors_origins: list[str] = ["http://localhost:3002", "http://127.0.0.1:3002"]
    openai_api_key: SecretStr | None = Field(default=None, validation_alias="OPENAI_API_KEY")
    openai_model: str | None = Field(default=None, validation_alias="OPENAI_MODEL")
    # Ativar somente depois da migração explícita e da configuração do remetente.
    email_verification_enabled: bool = False
    sendgrid_api_key: SecretStr | None = Field(default=None, validation_alias="SENDGRID_API_KEY")
    email_from: EmailStr | None = None
    email_from_name: str = Field(default="EduTrack", min_length=1, max_length=100)
    password_reset_enabled: bool = False
    frontend_url: str = "http://localhost:3002"

    @model_validator(mode="after")
    def validate_security(self):
        frontend = urlsplit(self.frontend_url)
        local_http = frontend.scheme == "http" and frontend.hostname in {"localhost", "127.0.0.1", "::1"}
        if frontend.username or frontend.password or frontend.query or frontend.fragment or not frontend.hostname or (frontend.scheme != "https" and not local_http):
            raise ValueError("FRONTEND_URL exige HTTPS ou loopback local, sem credenciais, consulta ou fragmento.")
        if self.password_reset_enabled and not self.jwt_secret:
            raise ValueError("Recuperação de senha exige JWT_SECRET persistente.")
        if self.jwt_secret and len(self.jwt_secret.get_secret_value()) < 32:
            raise ValueError("JWT_SECRET precisa ter pelo menos 32 caracteres aleatórios.")
        if "*" in self.cors_origins:
            raise ValueError("Informe as origens exatas permitidas no CORS.")
        if self.email_verification_enabled and not self.jwt_secret:
            raise ValueError("Verificação por e-mail exige JWT_SECRET persistente para proteger os códigos.")
        if self.environment == "production":
            if frontend.scheme != "https":
                raise ValueError("Produção exige FRONTEND_URL com HTTPS.")
            if not self.jwt_secret or self.trust_server_certificate:
                raise ValueError("Produção exige JWT_SECRET e certificado SQL confiável.")
            if any(not origin.startswith("https://") for origin in self.cors_origins):
                raise ValueError("Produção exige HTTPS nas origens permitidas.")
        return self

    @property
    def ai_configured(self) -> bool:
        return bool(self.openai_api_key and self.openai_model)

    @property
    def email_configured(self) -> bool:
        return bool(self.sendgrid_api_key and self.email_from)

    def sqlalchemy_url(self):
        if self.database_url:
            return self.database_url.get_secret_value()
        # Autenticação integrada: a identidade Windows executando a API acessa o SQL Server.
        return URL.create(
            "mssql+pyodbc",
            host=self.sql_server,
            database=self.sql_database,
            query={
                "driver": "ODBC Driver 18 for SQL Server",
                "Encrypt": "yes",
                "TrustServerCertificate": "yes" if self.trust_server_certificate else "no",
                "LongAsMax": "Yes",
            },
        )
