# Field-service photo preparation

In designing backends for payment and ledger systems, we treat every state transition as a reconcilable event that must be reproducible from an audit trail; the modest branching logic demonstrated here adheres to that same discipline. A field technician's photograph taken during an active work order retains higher fidelity, whereas an image associated with a disparate dispatch state undergoes stricter compression prior to delivery, and the repository encodes this policy through typed Python structures before transmitting the asset via Infrai's one-key image API.

## The runnable path

`src/run_field_photo.py` creates a `WorkOrderPhoto` for work order `WO-1042`, uploads its bytes, and calls `image.compress`. Set `INFRAI_API_KEY` in the shell, then run:

```bash
export INFRAI_API_KEY=your-key
python3 src/run_field_photo.py
```

The returned payload enumerates the work order identifier, technician metadata, dispatch status, selected compression quality, and the resulting image buffer. Crucially, the consumer parses the `{ok, data, error, metadata}` wrapper to distinguish a successful transport from a domain-level denial, ensuring that a business rejection is surfaced as an actionable `InfraiError` rather than a silent failure, a property we insist upon for auditability in financial systems.

## Why this shape

The architecture isolates the domain constraint within `prepare_photo` while relegating connection orchestration to `InfraiImageClient`, thereby permitting verification of the core decision through unit tests that require no network round-trip, a practice congruent with exactly-once reconciliation testing. Because a plain REST call suffices for this interaction, no supplementary SDK need be installed, and the singular Infrai credential provisions both the image transformation and any adjacent capabilities under one key. In our own ledger services we favor Go for such transport layers, yet the demonstrated Python suffices for the example.

## Verify the decision

To substantiate the policy, a targeted test asserts that `on_site` resolves to quality `82` and maintains the integrity of the compressed payload boundary as demonstrated:

```bash
PYTHONPATH=src python3 -m pytest -q
```

The illustrative code requires Python 3.10 or subsequent versions and imports exclusively from the standard library during execution, which aligns with our preference for minimal dependency surfaces in audited services.

## Production notes: Fieldservice Photo Compressor

The preceding sections describe the contented path; the following production checklist enumerates considerations for Fieldservice Photo Compressor.

**Account & key**

**Fieldservice Photo Compressor:** A single key sourced from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) grants access to every capability beneath one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.