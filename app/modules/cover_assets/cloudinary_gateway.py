import cloudinary
import cloudinary.uploader

from app.core.config import get_settings


class CloudinaryConfigurationError(RuntimeError):
    pass


class CloudinaryGateway:
    def __init__(self):
        self.settings = get_settings()

    def upload_cover(
        self,
        file_content: bytes,
        filename: str,
        content_type: str,
        folder: str | None = None,
    ) -> dict:
        self._configure()

        result = cloudinary.uploader.upload(
            file_content,
            folder=folder or self.settings.cloudinary_folder,
            resource_type="image",
            public_id=self._build_public_id(filename),
            overwrite=True,
        )

        return {
            "secure_url": result.get("secure_url"),
            "public_id": result.get("public_id"),
            "content_type": content_type,
        }

    def _configure(self) -> None:
        cloud_name = self._clean(self.settings.cloudinary_cloud_name)
        api_key = self._clean(self.settings.cloudinary_api_key)
        api_secret = self._clean(self.settings.cloudinary_api_secret)

        if not cloud_name or not api_key or not api_secret:
            raise CloudinaryConfigurationError("Cloudinary no está configurado.")

        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True,
        )

    def _clean(self, value: str | None) -> str | None:
        if value is None:
            return None

        stripped = value.strip()
        return stripped or None

    def _build_public_id(self, filename: str) -> str:
        stem = filename.rsplit(".", 1)[0] if filename else "cover"
        safe_stem = "".join(char if char.isalnum() else "-" for char in stem.lower())
        return safe_stem.strip("-") or "cover"
