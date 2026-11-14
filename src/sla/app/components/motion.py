"""Decorative motion graphics (inline SVG + CSS). Purely visual: they never show data."""

from __future__ import annotations

_LOOP = [("OBSERVE", 50, 8, "#4632C9"), ("CHOOSE", 92, 50, "#9965E8"),
         ("ACT", 50, 92, "#199e70"), ("LEARN", 8, 50, "#3987e5")]


def learning_loop() -> str:
    """Rotating 'observe -> act -> reward -> learn' loop with a travelling signal."""
    nodes = "".join(
        f'<g class="sla-node" style="animation-delay:{i * 0.5}s"><circle cx="{x}" cy="{y}" r="4.2" class="sla-halo" '
        f'stroke="{c}" style="animation-delay:{i}s"/><circle cx="{x}" cy="{y}" r="4.2" fill="#FFFFFF" '
        f'stroke="{c}" stroke-width="1.4"/><text x="{x}" y="{y - 7 if y < 50 else y + 11 if y > 50 else y - 7}" '
        f'fill="#5A4763" font-size="5" text-anchor="middle" font-weight="700">{t}</text></g>'
        for i, (t, x, y, c) in enumerate(_LOOP))
    return (
        '<svg class="sla-loop" viewBox="-6 -6 112 112" aria-hidden="true">'
        '<defs><linearGradient id="slaGold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#AF98E4"/>'
        '<stop offset="1" stop-color="#4632C9"/></linearGradient><radialGradient id="slaCore">'
        '<stop offset="0" stop-color="#FFFFFF"/><stop offset=".7" stop-color="#F3EEFA"/>'
        '<stop offset="1" stop-color="#DCD0F6"/></radialGradient></defs>'
        '<circle cx="50" cy="50" r="42" class="sla-ring"/>'
        '<circle cx="50" cy="50" r="42" class="sla-arc"/>'
        '<circle cx="50" cy="50" r="19" fill="url(#slaCore)" stroke="#AF98E4" stroke-width=".6" class="sla-core"/>'
        '<circle cx="50" cy="50" r="27" class="sla-ring2"/>'
        '<circle r="2.4" fill="#9965E8" class="sla-signal"><animateMotion dur="4s" repeatCount="indefinite" '
        'path="M50,8 A42,42 0 1,1 49.99,8"/></circle>'
        '<circle r="1.6" fill="#4632C9" opacity=".8"><animateMotion dur="6s" repeatCount="indefinite" '
        'path="M50,23 A27,27 0 1,0 49.99,23"/></circle>'
        f'{nodes}<text x="50" y="49" fill="#040207" font-size="7" font-weight="700" text-anchor="middle" '
        'font-family="Playfair Display, Georgia, serif">AGENT</text>'
        '<text x="50" y="57" fill="#6B5B73" font-size="3.8" text-anchor="middle">learns from reward</text></svg>')


def neural_flow() -> str:
    """Small network with signals flowing left to right (input -> hidden -> output)."""
    layers = [[20, 50, 80], [12, 37, 63, 88], [12, 37, 63, 88], [35, 65]]
    xs = [8, 70, 132, 194]
    edges, nodes = [], []
    for li in range(len(layers) - 1):
        for a in layers[li]:
            for b in layers[li + 1]:
                d = (a * 7 + b * 3 + li * 11) % 30 / 10
                edges.append(f'<line x1="{xs[li]}" y1="{a}" x2="{xs[li + 1]}" y2="{b}" class="sla-edge" '
                             f'style="animation-delay:-{d:.1f}s"/>')
    colors = ["#4632C9", "#9965E8", "#9965E8", "#199e70"]
    for li, ys in enumerate(layers):
        for k, y in enumerate(ys):
            nodes.append(f'<circle cx="{xs[li]}" cy="{y}" r="4" fill="#FFFFFF" stroke="{colors[li]}" '
                         f'stroke-width="1.5" class="sla-neuron" style="animation-delay:{(li + k) * 0.25}s"/>')
    labels = ('<g fill="#64748B" font-size="6" text-anchor="middle"><text x="8" y="99">state</text>'
              '<text x="101" y="99">hidden layers</text><text x="194" y="99">Q-values</text></g>')
    return (f'<svg class="sla-net" viewBox="0 0 202 102" aria-hidden="true">{"".join(edges)}{"".join(nodes)}'
            f'{labels}</svg>')
