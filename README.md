# Civic Pulse

An offline-first emergency alert prototype based on `spec.md`.

## Run locally

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py app.py
```

Open `http://127.0.0.1:5000`.

The app uses SQLite by default (`civic_pulse.db`, ignored by Git). Register a citizen, choose an emergency category, and press the emergency button. The browser requests GPS permission and the server stores the alert with its location and status.

## SMS and offline behavior

The default `CIVIC_PULSE_SMS_PROVIDER=demo` mode never pretends an SMS was delivered. It stores the alert as `Saved Offline` and exposes a retry endpoint. Connect a real provider inside `send_sms()` in [app.py](./app.py) and set the provider environment variable before deployment. SMS availability, recharge requirements, SIM status, and carrier coverage remain external constraints.

This browser prototype cannot guarantee background retries when the browser is closed. A production mobile application should use the platform's background task facilities for reliable retry scheduling.
