# Protocol fixtures

`protocol-v2/numeric-v2.json` is the firmware-owned golden protocol-v2 fixture,
copied byte-for-byte from PhysicalLink Android's root `test-fixtures/` directory.
Native Python oracles resolve it relative to this repository, never Android.

Keep both repositories' copies synchronized. For any intentional protocol-fixture
change, review the wire-format impact, compare the JSON bytes (SHA-256 or git diff),
and transfer the identical reviewed file to both repositories. Run native codec,
metadata-page, and Android protocol/codec/connection-manager tests. Coordinate the
two repository changes and record the counterpart revision in their reviews.
Do not regenerate expected vectors merely to make a failing encoder pass.
Protocol version 2, UUIDs, metadata, and numeric encoding remain unchanged.
