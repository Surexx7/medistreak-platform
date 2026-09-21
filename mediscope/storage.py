import os
import mimetypes
import uuid

from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from supabase import create_client


@deconstructible
class SupabaseStorage(Storage):
    def __init__(self):
        self.supabase_url = os.environ["SUPABASE_URL"]
        self.supabase_key = os.environ["SUPABASE_SECRET_KEY"]
        self.bucket = os.getenv("SUPABASE_BUCKET", "media")

        self.client = create_client(
            self.supabase_url,
            self.supabase_key,
        )

    def _open(self, name, mode="rb"):
        raise NotImplementedError(
            "Opening files directly is not supported by SupabaseStorage."
        )

    def _save(self, name, content):
        extension = os.path.splitext(name)[1]
        directory = os.path.dirname(name)

        filename = f"{uuid.uuid4().hex}{extension}"

        if directory:
            name = f"{directory}/{filename}"
        else:
            name = filename

        name = name.replace("\\", "/")

        content.seek(0)
        file_data = content.read()

        content_type = (
            getattr(content, "content_type", None)
            or mimetypes.guess_type(name)[0]
            or "application/octet-stream"
        )

        self.client.storage.from_(self.bucket).upload(
            path=name,
            file=file_data,
            file_options={
                "content-type": content_type,
                "upsert": "false",
            },
        )

        return name

    def delete(self, name):
        if name:
            self.client.storage.from_(self.bucket).remove([name])

    def exists(self, name):
        # Filenames are UUID-based, so collisions are effectively avoided.
        return False

    def url(self, name):
        if not name:
            return ""

        result = (
            self.client.storage
            .from_(self.bucket)
            .get_public_url(name)
        )

        return result

    def size(self, name):
        raise NotImplementedError(
            "File size lookup is not implemented for SupabaseStorage."
        )
    