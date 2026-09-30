<p align="center">
  <img src="header.png" alt="Abraxas Labs — nextcloud-webhook-tokenneeded" width="100%">
</p>

<p align="center">
  <a href="https://abraxaslabs.tech"><strong>abraxaslabs.tech</strong></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/abraxas">github.com/abraxas</a>
  &nbsp;·&nbsp;
  <a href="https://x.com/abraxas_null">@abraxas_null</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/abraxas/nextcloud-webhook-tokenneeded">nextcloud-webhook-tokenneeded</a>
</p>

# nextcloud-webhook-tokenneeded

**Nextcloud Server** `35.0.0` — Nextcloud GmbH

Unpublished Nextcloud source finding: `WebhooksController::create()` nulls `tokenNeeded` unless the caller is a full instance admin. `update()` does not. A delegated Webhooks settings admin (not in `admin`) can store `tokenNeeded.user_ids: ["admin"]` on an existing webhook, then receive a one-hour unscoped `PERMANENT_TOKEN` app password for that uid when the event fires.

**A bad actor who was only trusted to manage webhooks can log in as `admin` (or any user they name) for one hour, skip 2FA, and read or overwrite that person's files.**

| | |
|---|---|
| ID | Unpublished Nextcloud source finding #2 (no CVE yet) |
| CWE | [CWE-863, CWE-269](https://cwe.mitre.org/data/definitions/863.html) |
| CVSS | **High: 8.8** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Product | [Nextcloud Server](https://github.com/nextcloud/server) |
| Affected | **35.0.0** (`da02f41`) official `nextcloud:35.0.0-apache` |
| Patched | vendor patch — see references |
| Auth | delegated Webhooks settings admin (`IDelegatedSettings`) |
| License | [GNU Affero GPL v3.0](LICENSE) |
| Lab | `127.0.0.1` only · vendor/client disclosure pack, not a scanner |

---

## What an attacker can do

You gave someone the **Webhooks** settings job. They are not in the `admin` group. Nextcloud still lets them edit an existing webhook so that, on the next matching event, the server **mails them a one-hour login** for any uid they list, including `admin`.

With that login they can:

- Open **all of that person's files** (not only something the webhook was supposed to see)
- **Download and overwrite** those files
- Use Files / WebDAV **as that person**
- **Skip 2FA** (this is an app password, not a password prompt)

They do not need a PHP shell on the host. They do not need to be a full instance admin. A stranger on the internet with no account cannot do this. The hole is the staffer you already trusted with webhooks, impersonating the people you did not.

---

## Advisory (from the source map)

`apps/webhook_listeners/lib/Controller/WebhooksController.php` `create()` lines 158-161 null `tokenNeeded` unless `groupManager->isAdmin()`. `update()` lines 217-252 pass `$tokenNeeded` through. Mapper persists it. `TokenService::createEphemeralToken` mints `IToken::PERMANENT_TOKEN` (1h). `WebhookCall` POSTs `authentication.user_ids`. PR `#60543` closed create only.

---

## Entry

- **Method:** `POST`
- **Path:** `/ocs/v2.php/apps/webhook_listeners/api/v1/webhooks/{id}`
- **Router:** `WebhooksController::update`. `#[AuthorizedAdminSetting(settings: Admin::class)]`. `Admin` implements `IDelegatedSettings`.
- **Notes:** Delegated unpublished Nextcloud #2 CWE-863/CWE-269 v35.0.0. Witness: `NEXTCLOUD-WEBHOOK-TOKENNEEDED-WITNESS` in admin private DAV via stolen Bearer. Not eval. Not a reverse shell. Not the ExApp path. Disclose via [hackerone.com/nextcloud](https://hackerone.com/nextcloud) only. Do **not** open a public GitHub issue on nextcloud/server.

### Call chain

- `occ admin-delegation:add OCA\WebhookListeners\Settings\Admin webhookers`
- delegated `hooker` `POST /ocs/v2.php/apps/webhook_listeners/api/v1/webhooks` with `tokenNeeded.user_ids=['admin']` (create strips)
- delegated `hooker` `POST /ocs/v2.php/apps/webhook_listeners/api/v1/webhooks/{id}` same body (update stores tokenNeeded)
- later HTTP PUT DAV `NodeCreatedEvent`; `WebhooksEventListener` queues `WebhookCall`
- `php cron.php`: `TokenService::createEphemeralToken` `PERMANENT_TOKEN` 1h; POST to catcher
- unauth `GET /remote.php/dav/files/admin/NEXTCLOUD-WEBHOOK-TOKENNEEDED-WITNESS.txt` `Authorization: Bearer <token>`

### Lab preconditions

- Nextcloud Server 35.0.0 (`nextcloud:35.0.0-apache`)
- `webhook_listeners` enabled
- Webhooks settings delegated to a non-admin group
- `allow_local_remote_servers` true so Guzzle can POST to docker DNS `hook`
- Fireable `IWebhookCompatibleEvent` after the webhook exists

### Witness

`NEXTCLOUD-WEBHOOK-TOKENNEEDED-WITNESS` in the admin private DAV file, `X-User-Id: admin`, via Bearer stolen from the catcher JSON.

### Not success

- eval/base64/system payload
- reverse shell
- ExApp path
- create() already minting tokens
- update 403
- empty authentication

---

## Patch / remediation

**Do this first:** Apply the vendor patch for **Nextcloud Server**. See references.

**Verify after upgrade**

- Re-run `nextcloud-webhook-tokenneeded-Abraxas-Labs.py` against the patched build: the mapped witness must **not** appear.
- Confirm `update()` nulls `tokenNeeded` the same way `create()` already does unless the caller is a full instance admin.
- A WAF signature is delay, not a patch.

**If you cannot update immediately**

- Do not delegate Webhooks settings to non-admin groups.
- Hunt for webhook listeners whose `tokenNeeded` names uids the registrant should not impersonate.

---

## Reproduction (authorized lab)

Target **only** `http://127.0.0.1:18320` (or the loopback you bound). Do not point this script at the internet.

Official image `nextcloud:35.0.0-apache` on loopback `:18320`, catcher `:18321`. Then:

```bash
cd lab
./run.sh
```

Or, with the stack already up:

```bash
python3 nextcloud-webhook-tokenneeded-Abraxas-Labs.py
```

Success is the **witness** above (`NEXTCLOUD-WEBHOOK-TOKENNEEDED-WITNESS` as `admin` over Bearer DAV). Generic 200 HTML is not it. This pack does **not** include a reverse shell.

---

## Lab images

Loopback stack used to reproduce. Official `nextcloud:35.0.0-apache` plus a catcher image.

- [`lab/docker-compose.yml`](lab/docker-compose.yml)
- [`lab/run.sh`](lab/run.sh)
- [`lab/hook/Dockerfile`](lab/hook/Dockerfile)

Publish nothing except `127.0.0.1`.

---

## References

- [github.com/nextcloud/server](https://github.com/nextcloud/server) tag [v35.0.0](https://github.com/nextcloud/server/releases/tag/v35.0.0) (`da02f41`)
- Nearby create-only fix: [nextcloud/server#60543](https://github.com/nextcloud/server/pull/60543)
- Vendor intake: [hackerone.com/nextcloud](https://hackerone.com/nextcloud). Do **not** open a public GitHub issue.

- Abraxas Labs: [abraxaslabs.tech](https://abraxaslabs.tech) · [github.com/abraxas](https://github.com/abraxas) · [@abraxas_null](https://x.com/abraxas_null)

---

## Records (structured)

```
# Nextcloud unpublished #2 — webhook update honors tokenNeeded

CWE: CWE-863, CWE-269
Severity: High (HTTP lab SUCCESS, 88%)

## Description

WebhooksController::create() nulls tokenNeeded unless the caller is a full instance admin. update() does not. A delegated Webhooks settings admin (not in admin) can POST an existing webhook with tokenNeeded.user_ids: ["admin"] and a URI they control. On the next matching event, TokenService::createEphemeralToken mints an unscoped PERMANENT_TOKEN (1h) and WebhookCall POSTs it. That token is a full DAV/app-password session for the named uid.

## Product

Nextcloud Server 35.0.0 (nextcloud:35.0.0-apache). Lab oracle: NEXTCLOUD-WEBHOOK-TOKENNEEDED-WITNESS in the admin private file via stolen Bearer, not a shell. Vendor later: HackerOne https://hackerone.com/nextcloud only.
```

---

## License

This disclosure pack is licensed under the **GNU Affero General Public License v3.0**. See [LICENSE](LICENSE).

---

## Disclaimer

This pack is for **the vendor, the site owner, and licensed labs**. The script talks to `127.0.0.1`. Using it against systems you do not own is not authorized by Abraxas Labs. No warranty.

<p align="center">
  <a href="https://abraxaslabs.tech">abraxaslabs.tech</a> ·
  <a href="https://github.com/abraxas">github.com/abraxas</a> ·
  <a href="https://x.com/abraxas_null">@abraxas_null</a>
</p>
