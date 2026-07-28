import uuid
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

from app.config import Settings


class StorageService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.backend = settings.storage_backend.lower()
        if self.backend == "local":
            Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)

    def save_bytes(self, data: bytes, filename: str, subdir: str = "") -> str:
        safe_name = f"{uuid.uuid4().hex}_{Path(filename).name}"
        key = f"{subdir}/{safe_name}" if subdir else safe_name

        if self.backend == "s3":
            return self._save_s3(data, key)
        return self._save_local(data, key)

    def _save_local(self, data: bytes, key: str) -> str:
        dest = Path(self.settings.upload_dir) / key
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        return str(dest)

    def _save_s3(self, data: bytes, key: str) -> str:
        if not self.settings.s3_bucket:
            raise RuntimeError("S3_BUCKET is not configured")
        s3_key = f"{self.settings.s3_prefix.rstrip('/')}/{key}"
        client = boto3.client("s3", region_name=self.settings.aws_region)
        client.put_object(
            Bucket=self.settings.s3_bucket,
            Key=s3_key,
            Body=data,
            ContentType="application/zip",
        )
        return f"s3://{self.settings.s3_bucket}/{s3_key}"

    def read_bytes(self, storage_path: str) -> bytes:
        if storage_path.startswith("s3://"):
            return self._read_s3(storage_path)
        path = Path(storage_path)
        if not path.exists():
            raise FileNotFoundError(storage_path)
        return path.read_bytes()

    def _read_s3(self, storage_path: str) -> bytes:
        without = storage_path[5:]
        bucket, _, key = without.partition("/")
        if not bucket or not key:
            raise FileNotFoundError(storage_path)
        client = boto3.client("s3", region_name=self.settings.aws_region)
        try:
            obj = client.get_object(Bucket=bucket, Key=key)
        except ClientError as exc:
            raise FileNotFoundError(storage_path) from exc
        return obj["Body"].read()

    def delete(self, storage_path: str | None) -> None:
        if not storage_path:
            return
        if storage_path.startswith("s3://"):
            self._delete_s3(storage_path)
        else:
            path = Path(storage_path)
            if path.exists():
                path.unlink()

    def _delete_s3(self, storage_path: str) -> None:
        # s3://bucket/key
        without = storage_path[5:]
        bucket, _, key = without.partition("/")
        if not bucket or not key:
            return
        client = boto3.client("s3", region_name=self.settings.aws_region)
        try:
            client.delete_object(Bucket=bucket, Key=key)
        except ClientError:
            pass

    def open_local_path(self, storage_path: str) -> Path | None:
        if storage_path.startswith("s3://"):
            return None
        path = Path(storage_path)
        return path if path.exists() else None

    def ensure_dirs(self) -> None:
        if self.backend == "local":
            Path(self.settings.upload_dir).mkdir(parents=True, exist_ok=True)
            Path(self.settings.git_workdir).mkdir(parents=True, exist_ok=True)
