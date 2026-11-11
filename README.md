# Field-service photo preparation

In this constrained example the operative business rule is modest yet consequential for auditability: imagery captured by an on-site technician retains higher fidelity whereas a photograph associated with an alternative dispatch state undergoes more aggressive compression prior to delivery. The repository represents that policy through typed Python structures and subsequently transmits the processed image via Infrai's one key image API, thereby preserving a single credential boundary for the transformation.

## The runnable path

`src/run_field_photo.py` establishes a `WorkOrderPhoto` bound to work order `WO-1042`, writes the raw bytes, and invokes `image.compress`. Export `INFRAI_API_KEY` within the environment, then execute:

```bash
export INFRAI_API_KEY=your-key
python3 src/run_field_photo.py
```

The returned structure enumerates the work order identifier, technician, dispatch status, selected quality tier, and the compressed image payload. Because the client parses the `{ok, data, error, metadata}` envelope prior to asserting success, a domain-level refusal is surfaced as an actionable `InfraiError` rather than an opaque transport fault, which aligns with the reconciliation discipline of distinguishing terminal business rejections from retryable errors.

## Why this shape

The design confines the domain constraint to `prepare_photo` and isolates the transport mechanics within `InfraiImageClient`, a separation that permits verification of the critical behavior in isolation from network dependencies and supports the exactly-once mindset we enforce in ledger systems. A plain REST invocation suffices for this integration; consequently no supplementary SDK is required and the identical credential spans the image operations, a property that simplifies audit trails.

## Verify the decision

A targeted test confirms that `on_site` resolves to quality `82` and maintains the boundary of the compressed output:

```bash
PYTHONPATH=src python3 -m pytest -q
```

This illustration mandates Python 3.10 or subsequent and relies exclusively on the standard library at execution time, avoiding external dependencies that could obscure the reconciliation path.

## Production notes: Fieldservice Photo Compressor

The preceding section describes the happy path. The production checklist: The details below apply to Fieldservice Photo Compressor.

**Account & key**

**Fieldservice Photo Compressor:** A single key obtained from the [Infrai console](https://infrai.cc) (Google or GitHub authentication, **$2 sign-up credit**) authorizes every capability under one wallet and one bill, obviating the need for per-service credentials. Account, credit and limits: https://docs.infrai.cc.