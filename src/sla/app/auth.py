"""Sign-in for the dashboard: email + password accounts, optional Google sign-in, and a view-only guest mode.

* Members (email/password or Google) can use everything.
* Guests can open every page and see every result, but cannot start training, write insights or save ratings.
* Google sign-in appears only when an ``[auth]`` section exists in ``.streamlit/secrets.toml`` (Streamlit's
  built-in ``st.login``); without it the button is simply hidden.
"""

from __future__ import annotations

import html

import streamlit as st

from sla import settings
from sla.accounts import AccountError, AccountStore
from sla.app.components.icons import icon
from sla.app.components.motion import learning_loop

KEY = "sla_user"
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
    """The signed-in user ({name, email, kind}) or ``None`` when nobody has signed in yet."""
    user = st.session_state.get(KEY)
    return user if user else _google_user()


def can_act() -> bool:
    """True for members; guests (and visitors who have not signed in) are view-only."""
    user = current_user()
    return bool(user) and user["kind"] != "guest"


def sign_out() -> None:
    user = current_user()
    st.session_state.pop(KEY, None)
    if user and user["kind"] == "google":
        st.logout()


def member_gate(action: str, key: str) -> bool:
    """For guests: show a short lock notice with a sign-in button. Returns whether the action is allowed."""
    if can_act():
        return True
    with st.container(key=f"lock_{key}"):
        c1, c2 = st.columns([4, 1], vertical_alignment="center")
        c1.markdown(f'<div class="sla-lock">{icon("eye", 15)}<span><b>Guest mode is view-only.</b> '
                    f'Sign in to {html.escape(action)}.</span></div>', unsafe_allow_html=True)
        c2.button("Sign in", key=f"signin_{key}", on_click=sign_out, width="stretch")
    return False


def _enter(name: str, email: str, kind: str) -> None:
    st.session_state[KEY] = {"name": name, "email": email, "kind": kind}
    st.rerun()


# ------------------------------------------------------------------ sign-in screen
_HIDE_SIDEBAR = """<style>
section[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], [data-testid="stExpandSidebarButton"],
[data-testid="stSidebarCollapseButton"] { display: none !important; }
</style>"""


def login_screen() -> None:
    """Full-page sign-in: brand panel on the left, sign-in / create-account / guest options on the right."""
    st.markdown(_HIDE_SIDEBAR, unsafe_allow_html=True)
    left, right = st.columns([1.1, 1], gap="large", vertical_alignment="center")
    with left:
        st.markdown(
            '<div class="sla-auth-brand"><div class="eyebrow">Self-Learning AI Agent</div>'
            '<h1>Welcome to the <span class="gold">AI Learning Lab</span></h1>'
            '<p>Sign in to train agents, write insights and rate them — or continue as a guest to explore every '
            'result in view-only mode.</p>'
            f'<div class="sla-auth-art">{learning_loop()}</div>'
            '<ul class="sla-auth-list">'
            f'<li>{icon("check", 14)}<span><b>Members</b> — start training, run experiments, generate and rate '
            'insights.</span></li>'
            f'<li>{icon("eye", 14)}<span><b>Guests</b> — see the overview, charts, evaluation and ablation '
            'results.</span></li></ul></div>', unsafe_allow_html=True)
    with right, st.container(key="card_auth"):
        st.markdown('<div class="sla-auth-head"><h3>Sign in</h3><p>Use your account, or try the lab as a guest.</p>'
                    '</div>', unsafe_allow_html=True)
        tab_in, tab_up = st.tabs(["Sign in", "Create account"])
        with tab_in, st.form("signin", border=False):
            email = st.text_input("Email", placeholder="you@example.com", autocomplete="email")
            pw = st.text_input("Password", type="password", autocomplete="current-password")
            if st.form_submit_button("Sign in", type="primary", width="stretch"):
                acc = store().verify(email, pw)
                if acc:
                    _enter(acc.name, acc.email, "member")
                st.error("Email or password is not correct.")
        with tab_up, st.form("signup", border=False):
            name = st.text_input("Your name", max_chars=60, autocomplete="name")
            email2 = st.text_input("Email ", placeholder="you@example.com", autocomplete="email")
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
        if google_enabled():
            st.markdown('<div class="sla-or"><span>or</span></div>', unsafe_allow_html=True)
            st.button("Continue with Google", on_click=_google_login, width="stretch", key="google_btn",
                      icon=":material/account_circle:")
        st.markdown('<div class="sla-or"><span>or</span></div>', unsafe_allow_html=True)
        if st.button("Continue as guest", width="stretch", key="guest_btn", icon=":material/visibility:"):
            _enter("Guest", "", "guest")
        st.caption("Guest mode is view-only. Passwords are stored only as salted hashes, never as text.")


def sidebar_card() -> None:
    """Who is signed in, their access level, and a sign-out button."""
    user = current_user()
    if not user:
        return
    initials = "".join(p[0] for p in user["name"].split()[:2]).upper() or "G"
    sub = html.escape(user["email"]) if user["email"] else "Explore every page · view only"
    st.markdown(f'<div class="sla-side sla-me"><div class="av">{html.escape(initials)}</div><div>'
                f'<b>{html.escape(user["name"])}</b><span class="kind {user["kind"]}">'
                f'{KIND_LABEL[user["kind"]]}</span><small>{sub}</small></div></div>', unsafe_allow_html=True)
    label = "Sign in" if user["kind"] == "guest" else "Sign out"
    st.button(label, key="signout_btn", on_click=sign_out, width="stretch", icon=":material/logout:")
