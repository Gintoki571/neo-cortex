---
id: chat-10
kind: chat
title: "#incidents: found the stale keys"
date: 2026-07-25T09:30:00Z
author: Chen Wei
participants: [Chen Wei, Sam Okafor]
labels: [config, bank-connector]
---

# #incidents

**[2026-07-25 09:30] Chen Wei:** found it. the tidewater cutoff override is still stored under the bankbridge.banks.tidewater.cutoff key in config-service. bank-connector reads bank_connector.banks.tidewater.cutoff, so it never sees the override
**[2026-07-25 09:32] Sam Okafor:** oh no. I missed the config keys in the rename. my bad
**[2026-07-25 09:34] Chen Wei:** not only your fault, the fallback should not have been silent. quick fix: I'll add an alias so bank-connector reads both namespaces for now
**[2026-07-25 09:36] Sam Okafor:** ok, do it. I'll migrate the keys properly right after and resubmit the Tidewater batches by hand
**[2026-07-25 09:38] Chen Wei:** alias is in. give the config push a minute to sync
**[2026-07-25 09:41] Sam Okafor:** migrated the keys to the new namespace. the old ones are still there but nothing reads them now
**[2026-07-25 09:44] Chen Wei:** good. want me to remove the alias later, or leave it?
**[2026-07-25 09:45] Sam Okafor:** leave it for a week, then remove. I'll check the batches before we delete anything
**[2026-07-25 09:47] Chen Wei:** works for me
**[2026-07-25 09:50] Sam Okafor:** resubmitting the Tidewater batches now, same-day, before their cutoff. thanks Chen
**[2026-07-25 09:52] Chen Wei:** np. tell me if the batches bounce
**[2026-07-25 09:55] Chen Wei:** I'll add a note to the config change log so the next person knows why the alias exists
