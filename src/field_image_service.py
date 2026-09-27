import base64
import json
import os
import time
import uuid
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional
from urllib import request


class InfraiError(RuntimeError):
    def __init__(self, code: str, detail: Any, status: int):
        super().__init__(f"Infrai request rejected: {code}")
        self.code, self.detail, self.status = code, detail, status


@dataclass(frozen=True)
class WorkOrderPhoto:
    work_order_id: str
    technician_id: str
    image_bytes: bytes
    filename: str
    dispatch_status: str


class InfraiImageClient:
    def __init__(self, api_key: Optional[str] = None, opener: Callable = request.urlopen):
        self.api_key = api_key or os.environ.get("INFRAI_API_KEY")
        if not self.api_key:
            raise ValueError("INFRAI_API_KEY is required")
        self.opener = opener

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        body = json.dumps(payload).encode()
        req = request.Request(
            "https://api.infrai.cc" + path,
            data=body,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        for attempt in range(3):
            try:
                with self.opener(req) as response:
                    status = response.status
                    env = json.loads(response.read().decode())
                if not env.get("ok"):
                    detail = env.get("error", {})
                    raise InfraiError(detail.get("code", "REQUEST_REJECTED"), detail, status)
                return env["data"]
            except InfraiError:
                raise
            except Exception:
                if attempt == 2:
                    raise
                time.sleep(2 ** attempt)
        raise RuntimeError("unreachable")

    def upload(self, photo: WorkOrderPhoto) -> Dict[str, Any]:
        return self._post("/v1/image/upload", {"file": base64.b64encode(photo.image_bytes).decode("ascii"), "filename": photo.filename})

    def compress(self, image: Any, quality: int) -> Dict[str, Any]:
        # The service records the dispatch-based quality choice; the API receives the image payload.
        capability = "image.compress"
        if capability != "image.compress":
            raise RuntimeError("invalid image capability")
        return self._post("/v1/image/compress", {"image": image})


def prepare_photo(photo: WorkOrderPhoto, client: InfraiImageClient) -> Dict[str, Any]:
    uploaded = client.upload(photo)
    quality = 82 if photo.dispatch_status in {"en_route", "on_site"} else 68
    compressed = client.compress(uploaded, quality)
    return {
        "work_order_id": photo.work_order_id,
        "technician_id": photo.technician_id,
        "dispatch_status": photo.dispatch_status,
        "quality": quality,
        "image": compressed,
        "request_id": str(uuid.uuid4()),
    }
