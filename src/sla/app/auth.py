"""Sign-in for the dashboard: email + password accounts, optional Google sign-in, and a view-only guest mode.

* Every visitor can open every page and see every result straight away (view-only).
* Members (email/password or Google) can also start training, generate insights and save ratings.
* "Log in" / "Sign up" live in the top-right corner of the navbar and open a centred dialog.
* Google sign-in appears only when an ``[auth]`` section exists in ``.streamlit/secrets.toml`` (Streamlit's
  built-in ``st.login``); without it the button is simply hidden.
"""

from __future__ import annotations

import html

import streamlit as st

from sla import settings
from sla.accounts import AccountError, AccountStore
from sla.app.components.icons import icon

KEY = "sla_user"
OPEN = "sla_auth_open"
KIND_LABEL = {"member": "Member", "google": "Google", "guest": "Guest · view only"}


@st.cache_resource(show_spinner=False)
def _store(path: str) -> AccountStore:
    return AccountStore(path)


def store() -> AccountStore:
    return _store(str(settings.users_db_path()))


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
    return user if user else _google_user()


def can_act() -> bool:
    """True for members; guests and anonymous visitors are view-only."""
    user = current_user()
    return bool(user) and user["kind"] != "guest"


def sign_out() -> None:
    user = current_user()
    st.session_state.pop(KEY, None)
    if user and user["kind"] == "google":
        st.logout()


def _enter(name: str, email: str, kind: str) -> None:
    st.session_state[KEY] = {"name": name, "email": email, "kind": kind}
    st.session_state.pop(OPEN, None)
    st.rerun(scope="app")  # closes the dialog and refreshes the whole page


def open_auth(mode: str = "Log in") -> None:
    """Button callback: open the log-in / sign-up dialog on the next run (kept open until done or dismissed)."""
    st.session_state[OPEN] = mode
    st.session_state["auth_mode"] = mode


def _close_auth() -> None:
    st.session_state.pop(OPEN, None)


def initials(name: str) -> str:
    return "".join(p[0] for p in name.split()[:2]).upper() or "G"


# ------------------------------------------------------------------ the log-in / sign-up dialog
@st.dialog("Welcome to the AI Learning Lab", width="small", on_dismiss=_close_auth)
def auth_dialog() -> None:
    """Centred dialog with Log in | Sign up, optional Google, and guest access."""
    choice = st.segmented_control("Account", ["Log in", "Sign up"], key="auth_mode",
                                  label_visibility="collapsed", width="stretch") or "Log in"
    if choice == "Log in":
        with st.form("signin", border=False):
            email = st.text_input("Email", placeholder="you@example.com", autocomplete="email")
            pw = st.text_input("Password", type="password", autocomplete="current-password")
            if st.form_submit_button("Log in", type="primary", width="stretch"):
                acc = store().verify(email, pw)
                if acc:
                    _enter(acc.name, acc.email, "member")
                st.error("Email or password is not correct.")
    else:
        with st.form("signup", border=False):
            name = st.text_input("Your name", max_chars=60, autocomplete="name")
            email2 = st.text_input("Email", placeholder="you@example.com", autocomplete="email")
            pw2 = st.text_input("Password (at least 8 characters)", type="password", autocomplete="new-password")
            pw3 = st.text_input("Confirm password", type="password", autocomplete="new-password")
            if st.form_submit_button("Create account", type="primary", width="stretch"):
                if pw2 != pw3:
                    st.error("The two passwords do not match.")
                else:
                    try:
                        acc = store().create(email2, name, pw2)
                    except AccountError as exc:
                        st.error(str(exc))
                    else:
                        _enter(acc.name, acc.email, "member")
    st.markdown('<div class="sla-or"><span>or</span></div>', unsafe_allow_html=True)
    if google_enabled():
        st.button("Continue with Google", on_click=_google_login, width="stretch", key="google_btn",
                  icon=":material/account_circle:")
    if st.button("Continue as guest", width="stretch", key="guest_btn", icon=":material/visibility:"):
        _enter("Guest", "", "guest")
    st.caption("Guests can view everything. Passwords are stored only as salted hashes, never as text.")


# ------------------------------------------------------------------ navbar corner + member gate
def topbar() -> None:
    """Top-right corner of the navbar: Log in + Sign up, or the signed-in user's avatar menu."""
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
