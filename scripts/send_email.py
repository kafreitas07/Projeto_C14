import os
import smtplib
import ssl
from email.message import EmailMessage

def env(name: str, default: str | None = None) -> str:
    val = os.environ.get(name, default)
    if val is None or (isinstance(val, str) and not val.strip()):
        raise SystemExit(f"Variável de ambiente obrigatória ausente: {name}")
    return val

def main() -> None:
    to_email   = env("TO_EMAIL")
    smtp_host  = env("SMTP_HOST")
    smtp_port  = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user  = os.environ.get("SMTP_USER", "")
    smtp_pass  = os.environ.get("SMTP_PASS", "")
    smtp_from  = os.environ.get("SMTP_FROM", smtp_user or f"ci@{smtp_host}")

    test_status  = os.environ.get("TEST_STATUS", "unknown")
    build_status = os.environ.get("BUILD_STATUS", "unknown")
    run_url      = os.environ.get("RUN_URL", "")
    commit_sha   = os.environ.get("COMMIT_SHA", "")[:7]

    subject = f"[CI] Tests: {test_status.upper()} | Build: {build_status.upper()} | {commit_sha or 'n/a'}"
    body = (
        "Pipeline executado!\n\n"
        f"Resultados:\n- Tests: {test_status}\n- Build: {build_status}\n\n"
        f"Detalhes: {run_url}\n"
    )

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = smtp_from
    msg["To"] = to_email
    msg.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.ehlo()
        try:
            server.starttls(context=context)
            server.ehlo()
        except smtplib.SMTPException:
            pass

        if smtp_user and smtp_pass:
            server.login(smtp_user, smtp_pass)

        server.send_message(msg)

    print("E-mail de notificação enviado.")

if __name__ == "__main__":
    main()
