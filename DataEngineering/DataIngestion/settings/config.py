from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    # Pydantic will read the environment variables in a case-insensitive way, to set values for below

    #All enviroment variables
    KAFKA_HOST: str
    KAFKA_PORT: str
    KAFKA_HOST_2: str
    KAFKA_PORT_2: str
    KAFKA_TOPIC: str
    KAFKA_TOPIC_2: str
    # KAFKA_GROUP: str

    # MARIADB_HOST: str
    # MARIADB_PORT: int
    # MARIADB_USER: str
    # MARIADB_ROOT_PASS: str
    # MARIADB_PASS: str
    # MARIADB_DBNAME: str
    
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    POSTGRES_HOST2: str
    POSTGRES_PORT2: int
    POSTGRES_USER2: str
    POSTGRES_PASSWORD2: str
    POSTGRES_DB2: str

    S3_ENDPOINT_URL: str
    S3_ACCESS_KEY_ID: str
    S3_SECRET_ACCESS_KEY: str
    S3_REGION_NAME: str
    S3_BUCKET: str

    # class Config:
    #     env_file = "dev.env"    


Setting = Setting()
print(Setting)

