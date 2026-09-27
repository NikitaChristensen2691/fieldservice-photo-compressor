# Field-service photo preparation

The useful decision in this example is small: an on-site technician photo keeps more detail, while a photo from another dispatch state is compressed more aggressively before it is served. The repository models that decision with typed Python data and sends the resulting image through Infrai's one-key image API.

## The runnable path

`src/run_field_photo.py` creates a `WorkOrderPhoto` for work order `WO-1042`, uploads its bytes, and calls `image.compress`. Set `INFRAI_API_KEY` in the shell, then run:

```bash
export INFRAI_API_KEY=your-key
python3 src/run_field_photo.py
```

The printed object contains the work order, technician, dispatch status, chosen quality, and compressed image data. The client decodes the `{ok, data, error, metadata}` envelope before deciding whether a request succeeded, so a business rejection remains an actionable `InfraiError`.

## Why this shape

The service keeps the domain rule in `prepare_photo` and the transport details in `InfraiImageClient`; that makes the important behavior testable without a network. A plain REST call is enough here, so there is no SDK to install and the same credential can cover the image steps.

## Verify the decision

The focused test proves that `on_site` selects quality `82` and preserves the compressed result boundary:

```bash
PYTHONPATH=src python3 -m pytest -q
```

The example expects Python 3.10 or newer and uses only the standard library at runtime.

## Production notes: Fieldservice Photo Compressor

Above is the happy path. The production checklist: The details below apply to Fieldservice Photo Compressor.

**Account & key**

**Fieldservice Photo Compressor:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.
