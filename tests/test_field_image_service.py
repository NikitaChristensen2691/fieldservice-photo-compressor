from field_image_service import WorkOrderPhoto, prepare_photo


class FakeClient:
    def upload(self, photo):
        return {"id": "img-1"}

    def compress(self, image, quality):
        return {"id": "compressed-1", "quality": quality}


def test_dispatch_status_keeps_on_site_photos_sharp():
    photo = WorkOrderPhoto("WO-1", "tech-1", b"x", "site.jpg", "on_site")
    result = prepare_photo(photo, FakeClient())
    assert result["quality"] == 82
    assert result["image"]["id"] == "compressed-1"

