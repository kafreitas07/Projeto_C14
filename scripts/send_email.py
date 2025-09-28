import os
import smtplib
import ssl
import socket
from email.message import EmailMessage

def env(name: str) -> str:
    val = os.environ.get(name, "").strip()
    if not val:
        raise SystemExit(f"Variável de ambiente obrigatória ausente: {name}")
    return val

def split_list(raw: str) -> list[str]:
    return [e.strip() for e in raw.replace(";", ",").split(",") if e.strip()]

def main() -> None:
    to_list = split_list(env("TO_EMAIL"))
    cc_list = split_list(os.environ.get("CC_EMAILS", ""))
    bcc_list = split_list(os.environ.get("BCC_EMAILS", ""))

    # SMTP
    smtp_host = env("SMTP_HOST").strip()
    raw_port = os.environ.get("SMTP_PORT", "").strip()
    smtp_port = int(raw_port) if raw_port.isdigit() else 587
    smtp_user = os.environ.get("SMTP_USER", "").strip()
    smtp_pass = os.environ.get("SMTP_PASS", "").strip()
    smtp_from = os.environ.get("SMTP_FROM", (smtp_user or f"ci@{smtp_host}")).strip()

    if any(c in smtp_host for c in (" ", "/", "\\")) or ":" in smtp_host:
        raise SystemExit("SMTP_HOST inválido. Use apenas o hostname (ex.: smtp.gmail.com).")
    try:
        socket.getaddrinfo(smtp_host, smtp_port)
    except socket.gaierror:
        raise SystemExit("SMTP_HOST não resolve DNS. Verifique o Secret.")

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
    msg["To"] = ", ".join(to_list)
    if cc_list:
        msg["Cc"] = ", ".join(cc_list)
    msg.set_content(body)

    recipients = to_list + cc_list + bcc_list
    context = ssl.create_default_context()
    timeout = 20

    if smtp_port == 465:
        with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context, timeout=timeout) as server:
            if smtp_user and smtp_pass:
                server.login(smtp_user, smtp_pass)
            server.send_message(msg, to_addrs=recipients)
    else:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=timeout) as server:
            server.ehlo()
            try:
                server.starttls(context=context)
                server.ehlo()
            except smtplib.SMTPException:
                pass
            if smtp_user and smtp_pass:
                server.login(smtp_user, smtp_pass)
            server.send_message(msg, to_addrs=recipients)

    print("E-mail de notificação enviado.")

if __name__ == "__main__":
    main()
