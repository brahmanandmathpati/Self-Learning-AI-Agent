"""Sign-in for the dashboard: email + password accounts, optional Google sign-in, and a view-only guest mode.

* Every visitor can open every page and see every result straight away (view-only).
* Members (email/password or Google) can also start training, generate insights and save ratings.
* "Log in" / "Sign up" live in the top-right corner of the navbar and open a centred dialog.
* Google sign-in appears only when an ``[auth]`` section exists in ``.streamlit/secrets.toml`` (Streamlit's
  built-in ``st.login``); without it the button is simply hidden.
* "Keep me signed in" stores a random token in a cookie (only its hash is in the database), so a refresh or a
  new visit within 30 days signs the member straight back in.
* "Forgot password?" emails a single-use reset link (30 minutes) when ``[smtp]`` secrets are configured.
* Accounts live in SQLite by default, or in PostgreSQL (e.g. Supabase) when ``[accounts] url`` is set.
"""

from __future__ import annotations

import html
import json
import logging
import os

import streamlit as st

from sla import settings
from sla.accounts import REMEMBER_DAYS, Account, AccountError, AccountStore
from sla.app import mailer
from sla.app.components.icons import icon

KEY = "sla_user"
OPEN = "sla_auth_open"
COOKIE = "sla_remember"
TOKEN = "sla_remember_token"
KIND_LABEL = {"member": "Member", "google": "Google", "guest": "Guest · view only"}


@st.cache_resource(show_spinner=False)
def _store(path: str) -> AccountStore:
    return AccountStore(path)


def accounts_target() -> str:
    """Where accounts live: ``[accounts] url`` secret or SLA_ACCOUNTS_URL (PostgreSQL), else the SQLite file."""
    try:
        url = dict(st.secrets.get("accounts", {})).get("url", "")
    except Exception:  # noqa: BLE001
        url = ""
    return url or os.environ.get("SLA_ACCOUNTS_URL", "") or str(settings.users_db_path())


_FAILED: set[str] = set()


def store() -> AccountStore:
    """The account store; falls back to the local SQLite file if a configured cloud database cannot be reached."""
    target, local = accounts_target(), str(settings.users_db_path())
    if target != local and target not in _FAILED:
        try:
            return _store(target)
        except Exception:  # noqa: BLE001 - wrong URL / database down: keep the app usable
            _FAILED.add(target)
            logging.getLogger(__name__).exception("Cloud accounts database unavailable; using %s", local)
    return _store(local)


# ------------------------------------------------------------------ Google (Streamlit built-in OIDC)
def _auth_secrets() -> dict:
    try:
        return dict(st.secrets.get("auth", {}))
    except Exception:  # noqa: BLE001 - no secrets file at all is the normal case
        return {}


def google_enabled() -> bool:
    auth = _auth_secrets()
    return bool(auth) and ("client_id" in auth or "google" in auth) and hasattr(st, "login")


def _google_user() -> dict | None:
    try:
        if getattr(st.user, "is_logged_in", False):
            return {"name": st.user.get("name") or st.user.get("email") or "Google user",
                    "email": st.user.get("email") or "", "kind": "google"}
    except Exception:  # noqa: BLE001
        return None
    return None


def _google_login() -> None:
    if "google" in _auth_secrets():
        st.login("google")
    else:
        st.login()


# ------------------------------------------------------------------ session helpers
def current_user() -> dict | None:
    """The signed-in user ({name, email, kind}); ``None`` for a visitor who has not chosen anything yet."""
    user = st.session_state.get(KEY)
    if not user and not st.session_state.get("sla_cookie_checked"):
        st.session_state["sla_cookie_checked"] = True  # check the remember-me cookie once per browser session
        user = _from_cookie()
    return user if user else _google_user()


def _from_cookie() -> dict | None:
    try:
        token = st.context.cookies.get(COOKIE, "")
    except Exception:  # noqa: BLE001 - no browser context in bare/test mode
        token = ""
    if not isinstance(token, str) or not token:
        return None
    acc = store().account_for_token(token, "remember")
    if not acc:
        return None
    st.session_state[TOKEN] = token
    st.session_state[KEY] = {"name": acc.name, "email": acc.email, "kind": "member"}
    return st.session_state[KEY]


def _queue_cookie(value: str, days: int) -> None:
    """Set (or clear, with days=0) the remember-me cookie on the next render."""
    st.session_state["sla_cookie_js"] = (value, days)


def _cookie_script() -> None:
    pending = st.session_state.pop("sla_cookie_js", None)
    if not pending:
        return
    value, days = pending
    js = (f"document.cookie = {json.dumps(COOKIE)} + '=' + {json.dumps(value)} + '; Max-Age={days * 86400}; "
          "Path=/; SameSite=Lax' + (location.protocol === 'https:' ? '; Secure' : '');")
    with st.container(key="cookiejar"):
        st.html(f"<script>{js}</script>", unsafe_allow_javascript=True)


def can_act() -> bool:
    """True for members; guests and anonymous visitors are view-only."""
    user = current_user()
    return bool(user) and user["kind"] != "guest"


def sign_out() -> None:
    user = current_user()
    st.session_state.pop(KEY, None)
    token = st.session_state.pop(TOKEN, None)
    if token:
        store().revoke_token(token)
        _queue_cookie("", 0)
    if user and user["kind"] == "google":
        st.logout()


def _enter(name: str, email: str, kind: str, remember: Account | None = None) -> None:
    st.session_state[KEY] = {"name": name, "email": email, "kind": kind}
    st.session_state.pop(OPEN, None)
    if remember is not None:
        token = store().issue_token(remember.user_id, "remember")
        st.session_state[TOKEN] = token
        _queue_cookie(token, REMEMBER_DAYS)
    st.rerun(scope="app")  # closes the dialog and refreshes the whole page


def open_auth(mode: str = "Log in") -> None:
    """Button callback: open the dialog on the next run (kept open until done or dismissed).

    Modes: 'Log in', 'Sign up', 'Forgot' (ask for a reset link), 'Reset' (choose a new password from a link)."""
    st.session_state[OPEN] = mode
    if mode in ("Log in", "Sign up"):
        st.session_state["auth_mode"] = mode


def _close_auth() -> None:
    st.session_state.pop(OPEN, None)
    st.session_state.pop("sla_reset_token", None)


def check_reset_link() -> None:
    """A visitor opened ``?reset=<token>`` from the email: remember the token and open the new-password dialog."""
    token = st.query_params.get("reset")
    if token:
        st.session_state["sla_reset_token"] = token
        del st.query_params["reset"]
        open_auth("Reset")


def initials(name: str) -> str:
    return "".join(p[0] for p in name.split()[:2]).upper() or "G"


# ------------------------------------------------------------------ the log-in / sign-up dialog
@st.dialog("Welcome to the AI Learning Lab", width="small", on_dismiss=_close_auth)
def auth_dialog() -> None:
    """Centred dialog with Log in | Sign up, optional Google, and guest access."""
    mode = st.session_state.get(OPEN)
    if mode == "Forgot":
        _forgot_form()
        return
    if mode == "Reset":
        _reset_form()
        return
    choice = st.segmented_control("Account", ["Log in", "Sign up"], key="auth_mode",
                                  label_visibility="collapsed", width="stretch") or "Log in"
    if choice == "Log in":
        with st.form("signin", border=False):
            email = st.text_input("Email", placeholder="you@example.com", autocomplete="email")
            pw = st.text_input("Password", type="password", autocomplete="current-password")
            keep = st.checkbox("Keep me signed in for 30 days", value=True)
            if st.form_submit_button("Log in", type="primary", width="stretch"):
                acc = store().verify(email, pw)
                if acc:
                    _enter(acc.name, acc.email, "member", acc if keep else None)
                st.error("Email or password is not correct.")
        st.button("Forgot password?", key="forgot_btn", type="tertiary", on_click=open_auth, args=("Forgot",))
    else:
        with st.form("signup", border=False):
            name = st.text_input("Your name", max_chars=60, autocomplete="name")
            email2 = st.text_input("Email", placeholder="you@example.com", autocomplete="email")
            pw2 = st.text_input("Password (at least 8 characters)", type="password", autocomplete="new-password")
            pw3 = st.text_input("Confirm password", type="password", autocomplete="new-password")
            keep2 = st.checkbox("Keep me signed in for 30 days", value=True, key="keep_signup")
            if st.form_submit_button("Create account", type="primary", width="stretch"):
                if pw2 != pw3:
                    st.error("The two passwords do not match.")
                else:
                    try:
                        acc = store().create(email2, name, pw2)
                    except AccountError as exc:
                        st.error(str(exc))
                    else:
                        _enter(acc.name, acc.email, "member", acc if keep2 else None)
    st.markdown('<div class="sla-or"><span>or</span></div>', unsafe_allow_html=True)
    if google_enabled():
        st.button("Continue with Google", on_click=_google_login, width="stretch", key="google_btn",
                  icon=":material/account_circle:")
    if st.button("Continue as guest", width="stretch", key="guest_btn", icon=":material/visibility:"):
        _enter("Guest", "", "guest")
    st.caption("Guests can view everything. Passwords are stored only as salted hashes, never as text.")


def _forgot_form() -> None:
    st.markdown("**Forgot your password?** Enter your email and we will send a link to choose a new one.")
    if not mailer.smtp_enabled():
        st.info("Password reset by email is not set up on this site yet. Ask the site owner to add the email "
                "settings, or create a new account.", icon=":material/mail:")
    else:
        with st.form("forgot", border=False):
            email = st.text_input("Email", placeholder="you@example.com", autocomplete="email")
            if st.form_submit_button("Send reset link", type="primary", width="stretch"):
                acc = store().by_email(email)
                if acc:
                    token = store().issue_token(acc.user_id, "reset")
                    try:
                        mailer.send_reset(acc.email, acc.name, f"{mailer.app_url()}?reset={token}")
                    except Exception:  # noqa: BLE001 - never reveal SMTP details to visitors
                        st.error("The email could not be sent right now. Please try again later.")
                        return
                # Same message either way, so the form does not reveal which emails have accounts.
                st.success("If an account exists for that email, a reset link is on its way. It works for 30 "
                           "minutes.")
    st.button("Back to log in", key="back_login", type="tertiary", on_click=open_auth, args=("Log in",))


def _reset_form() -> None:
    token = st.session_state.get("sla_reset_token", "")
    acc = store().account_for_token(token, "reset")
    if not acc:
        st.error("This reset link has expired or was already used. Please ask for a new one.")
        st.button("Ask for a new link", key="new_link", on_click=open_auth, args=("Forgot",), type="primary")
        return
    st.markdown(f"**Choose a new password** for {html.escape(acc.email)}.")
    with st.form("reset", border=False):
        pw = st.text_input("New password (at least 8 characters)", type="password", autocomplete="new-password")
        pw2 = st.text_input("Confirm new password", type="password", autocomplete="new-password")
        if st.form_submit_button("Save new password", type="primary", width="stretch"):
            if pw != pw2:
                st.error("The two passwords do not match.")
                return
            try:
                store().set_password(acc.user_id, pw)
            except AccountError as exc:
                st.error(str(exc))
                return
            store().account_for_token(token, "reset", consume=True)
            st.session_state.pop("sla_reset_token", None)
            _enter(acc.name, acc.email, "member")


# ------------------------------------------------------------------ navbar corner + member gate
def topbar() -> None:
    """Top-right corner of the navbar: Log in + Sign up, or the signed-in user's avatar menu."""
    check_reset_link()
    user = current_user()
    with st.container(key="topauth", horizontal=True, horizontal_alignment="right", vertical_alignment="center"):
        if not user:
            st.button("Log in", key="nav_login", type="tertiary", on_click=open_auth, args=("Log in",))
            st.button("Sign up", key="nav_signup", type="primary", on_click=open_auth, args=("Sign up",))
        else:
            with st.popover(initials(user["name"]), help=f"Signed in as {user['name']}"):
                sub = html.escape(user["email"]) if user["email"] else "Exploring in view-only mode"
                st.markdown(f'<div class="sla-me"><div class="av">{html.escape(initials(user["name"]))}</div><div>'
                            f'<b>{html.escape(user["name"])}</b><span class="kind {user["kind"]}">'
                            f'{KIND_LABEL[user["kind"]]}</span><small>{sub}</small></div></div>',
                            unsafe_allow_html=True)
                if user["kind"] == "guest":
                    st.button("Log in or sign up", key="menu_login", type="primary", width="stretch",
                              on_click=open_auth)
                st.button("Sign out", key="menu_signout", on_click=sign_out, width="stretch", icon=":material/logout:")
    _cookie_script()
    if st.session_state.get(OPEN):
        auth_dialog()


def member_gate(action: str, key: str) -> bool:
    """For guests and visitors: a short lock notice whose button opens the log-in dialog. Returns can_act()."""
    if can_act():
        return True
    with st.container(key=f"lock_{key}"):
        c1, c2 = st.columns([4, 1], vertical_alignment="center")
        c1.markdown(f'<div class="sla-lock">{icon("eye", 15)}<span><b>View-only mode.</b> '
                    f'Log in to {html.escape(action)}.</span></div>', unsafe_allow_html=True)
        c2.button("Log in", key=f"signin_{key}", width="stretch", type="primary", on_click=open_auth)
    return False
