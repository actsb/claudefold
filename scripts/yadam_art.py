#!/usr/bin/env python3
"""Generate the 2D art assets (SVG -> PNG) for the 만복 야담 video.

Usage:
    python3 scripts/yadam_art.py video/2026-09-yadam-manbok/assets [--svg-only]

Pure stdlib for the SVG generation (Pillow is used only, optionally, for the
contact sheet and the verification pass). Everything is deterministic (seeded
LCG) and idempotent: running twice yields byte-identical SVGs.
"""
import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RASTER = ROOT / 'scripts' / 'yadam_svg2png.mjs'

# ---------------------------------------------------------------- palette
OUT = '#3a2618'          # outline umber
CREAM = '#f7edd6'
PAPER = '#f1e3c3'
OCHRE = '#d9a441'
OCHRE_D = '#b7822a'
INDIGO = '#2e3f6f'
INDIGO_D = '#1b2748'
JADE = '#5f9d87'
JADE_L = '#9ccab3'
SKY = '#a8d2ea'
SKIN = '#f6d8b8'
SKIN_D = '#e2b58e'
RED = '#c4463d'
PINK = '#f4b3c0'
THATCH = '#d3ab5f'
THATCH_D = '#a9823a'
TILE = '#535868'
TILE_D = '#31343d'
WOOD = '#8a5a2e'
WOOD_D = '#5c3a1c'
WOOD_L = '#c48f57'
WALL = '#f2e7cd'
STONE = '#b3a78f'
GREEN = '#6aa554'
GREEN_D = '#3f7a3a'
GREEN_L = '#a9d17e'
EARTH = '#cdb07c'
EARTH_D = '#a98a55'

BW, BH = 2400, 1350

# ---------------------------------------------------------------- svg helpers
_SW = [4.0]  # current outline width


def n(v):
    if isinstance(v, float):
        s = f'{v:.2f}'.rstrip('0').rstrip('.')
        return '0' if s in ('', '-0') else s
    return str(v)


def attrs(a):
    return ' '.join(f'{k.rstrip("_").replace("_", "-")}="{n(v)}"' for k, v in a.items() if v is not None)


def el(tag, inner=None, **a):
    s = f'<{tag} {attrs(a)}'.rstrip()
    return s + '/>' if inner is None else s + '>' + inner + f'</{tag}>'


def g(inner, **a):
    return el('g', inner, **a)


def D(*tok):
    return ' '.join(t if isinstance(t, str) else n(float(t)) for t in tok)


def sh(tag, **a):
    a.setdefault('stroke', OUT)
    a.setdefault('stroke_width', _SW[0])
    a.setdefault('stroke_linejoin', 'round')
    a.setdefault('stroke_linecap', 'round')
    return el(tag, **a)


def circle(cx, cy, r, fill, **a):
    return sh('circle', cx=cx, cy=cy, r=r, fill=fill, **a)


def ellipse(cx, cy, rx, ry, fill, **a):
    return sh('ellipse', cx=cx, cy=cy, rx=rx, ry=ry, fill=fill, **a)


def rect(x, y, w, h, fill, rx=0, **a):
    return sh('rect', x=x, y=y, width=w, height=h, rx=rx, fill=fill, **a)


def path(d, fill='none', **a):
    return sh('path', d=d, fill=fill, **a)


def poly(pts, fill, **a):
    return sh('polygon', points=' '.join(f'{n(float(x))},{n(float(y))}' for x, y in pts), fill=fill, **a)


def line(x1, y1, x2, y2, **a):
    a.setdefault('stroke', OUT)
    a.setdefault('stroke_width', _SW[0])
    a.setdefault('stroke_linecap', 'round')
    return el('line', x1=x1, y1=y1, x2=x2, y2=y2, **a)


def flat(tag, **a):
    a['stroke'] = 'none'
    return el(tag, **a)


def lin(id_, stops, x1=0, y1=0, x2=0, y2=1):
    s = ''.join(f'<stop offset="{n(o)}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{id_}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>'


def rad(id_, stops, cx=0.5, cy=0.5, r=0.5):
    s = ''.join(f'<stop offset="{n(o)}" stop-color="{c}"/>' for o, c in stops)
    return f'<radialGradient id="{id_}" cx="{cx}" cy="{cy}" r="{r}">{s}</radialGradient>'


def smooth(pts):
    """Quadratic spline through mid points (smooth, deterministic)."""
    if len(pts) < 3:
        return 'M' + ' L'.join(f'{n(float(x))},{n(float(y))}' for x, y in pts)
    d = f'M{n(float(pts[0][0]))},{n(float(pts[0][1]))}'
    for i in range(1, len(pts) - 1):
        mx = (pts[i][0] + pts[i + 1][0]) / 2
        my = (pts[i][1] + pts[i + 1][1]) / 2
        d += f' Q{n(float(pts[i][0]))},{n(float(pts[i][1]))} {n(mx)},{n(my)}'
    d += f' L{n(float(pts[-1][0]))},{n(float(pts[-1][1]))}'
    return d


def tube(pts, w, color, cap='round'):
    """Outlined tube (polyline): dark wide stroke under coloured stroke."""
    d = smooth(pts) if len(pts) > 2 else 'M' + ' L'.join(f'{n(float(x))},{n(float(y))}' for x, y in pts)
    o = el('path', d=d, fill='none', stroke=OUT, stroke_width=w + 2 * _SW[0], stroke_linecap=cap, stroke_linejoin='round')
    o += el('path', d=d, fill='none', stroke=color, stroke_width=w, stroke_linecap=cap, stroke_linejoin='round')
    return o


def svg_doc(w, h, body, defs=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<defs>{defs}</defs>{body}</svg>')


class Rng:
    def __init__(self, seed):
        self.s = (seed * 7919 + 13) & 0x7fffffff

    def r(self):
        self.s = (1103515245 * self.s + 12345) & 0x7fffffff
        return self.s / 0x7fffffff

    def u(self, a, b):
        return a + (b - a) * self.r()

    def ch(self, seq):
        return seq[int(self.r() * len(seq)) % len(seq)]


# ---------------------------------------------------------------- background primitives

def sky_rect(id_):
    return flat('rect', x=0, y=0, width=BW, height=BH, fill=f'url(#{id_})')


def cloud(x, y, s=1.0, fill='#ffffff', edge='#c9d7e3'):
    blobs = [(0, 0, 55), (60, -32, 72), (135, -14, 62), (190, 16, 46), (95, 22, 50)]
    o = ''.join(flat('circle', cx=x + bx * s, cy=y + by * s, r=(br + 4) * s, fill=edge) for bx, by, br in blobs)
    o += flat('rect', x=x - 44 * s, y=y + 6 * s, width=282 * s, height=44 * s, rx=22 * s, fill=edge)
    o += ''.join(flat('circle', cx=x + bx * s, cy=y + by * s, r=br * s, fill=fill) for bx, by, br in blobs)
    o += flat('rect', x=x - 40 * s, y=y + 10 * s, width=274 * s, height=36 * s, rx=18 * s, fill=fill)
    return o


def mountain(pts, fill, base=BH, stroke='none', sw=3):
    d = smooth(pts) + f' L{n(float(pts[-1][0]))},{base} L{n(float(pts[0][0]))},{base} Z'
    return el('path', d=d, fill=fill, stroke=stroke, stroke_width=sw, stroke_linejoin='round')


def ridge(seed, y, amp, nseg, fill, x0=-150, x1=BW + 150, base=BH, stroke='none'):
    r = Rng(seed)
    pts = []
    for i in range(nseg + 1):
        x = x0 + (x1 - x0) * i / nseg
        if i % 2:
            pts.append((x, y - amp * (0.45 + 0.55 * r.r())))
        else:
            pts.append((x, y + amp * 0.25 * r.r()))
    return mountain(pts, fill, base, stroke)


def fog(cx, cy, rx, ry, opacity=0.35, fill='#ffffff'):
    return el('ellipse', cx=cx, cy=cy, rx=rx, ry=ry, fill=fill, opacity=opacity, filter='url(#blur)')


BLUR = '<filter id="blur" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="28"/></filter>'
BLUR_S = '<filter id="blurs" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="10"/></filter>'


def lattice(x, y, w, h, lit=False, cols=3, rows=5, sw=3):
    o = rect(x, y, w, h, '#ffd873' if lit else '#f9f4e6')
    for i in range(1, cols):
        o += line(x + w * i / cols, y, x + w * i / cols, y + h, stroke=WOOD, stroke_width=sw)
    for j in range(1, rows):
        o += line(x, y + h * j / rows, x + w, y + h * j / rows, stroke=WOOD, stroke_width=sw)
    return o


def thatched(x, y, s=1.0, lit=False, snow=False, win=True, flip=False):
    """Thatched cottage, x = centre, y = ground line."""
    W = 360 * s
    wh = 140 * s
    rh = 125 * s
    o = rect(x - W / 2 + 18 * s, y - wh, W - 36 * s, wh, WALL)
    for px in (x - W / 2 + 18 * s, x + W / 2 - 34 * s, x - 8 * s):
        o += rect(px, y - wh, 16 * s, wh, WOOD)
    dx = x + W * 0.14 if not flip else x - W * 0.34
    dw, dh = 62 * s, 100 * s
    o += rect(dx, y - dh, dw, dh, WOOD_D)
    o += line(dx + dw / 2, y - dh + 8 * s, dx + dw / 2, y - 8 * s, stroke=WOOD, stroke_width=3 * s)
    if win:
        wx = (x - W * 0.34) if not flip else (x + W * 0.12)
        wy = y - wh + 26 * s
        ww = 66 * s
        o += lattice(wx, wy, ww, ww * 0.85, lit, cols=2, rows=2, sw=2.5 * s)
    ry = y - wh
    d = D('M', x - W / 2 - 26 * s, ry + 18 * s, 'Q', x - W / 2 + 6 * s, ry - rh * 0.72, x - W * 0.2, ry - rh,
          'L', x + W * 0.2, ry - rh, 'Q', x + W / 2 - 6 * s, ry - rh * 0.72, x + W / 2 + 26 * s, ry + 18 * s,
          'Q', x, ry + 34 * s, x - W / 2 - 26 * s, ry + 18 * s, 'Z')
    o += path(d, THATCH)
    for i in range(7):
        tx = x - W * 0.36 + i * W * 0.12
        o += line(tx, ry - rh * 0.5, tx + 5 * s, ry + 6 * s, stroke=THATCH_D, stroke_width=3 * s)
    if snow:
        d2 = D('M', x - W / 2 - 22 * s, ry + 6 * s, 'Q', x - W / 2 + 8 * s, ry - rh * 0.7, x - W * 0.2, ry - rh - 6 * s,
               'L', x + W * 0.2, ry - rh - 6 * s, 'Q', x + W / 2 - 8 * s, ry - rh * 0.7, x + W / 2 + 22 * s, ry + 6 * s,
               'Q', x + W * 0.3, ry - 20 * s, x + W * 0.05, ry - 8 * s, 'Q', x - W * 0.25, ry - 26 * s, x - W / 2 - 22 * s, ry + 6 * s, 'Z')
        o += path(d2, '#ffffff', stroke='#b9c4cf', stroke_width=3 * s)
    return o


def tiled(x, y, s=1.0, w=560, lit=False, doors=3, open_center=False, wall_h=150, roof_h=95):
    """Tile-roofed house, x = centre, y = ground line."""
    w *= s
    wh = wall_h * s
    rh = roof_h * s
    base = 24 * s
    o = rect(x - w / 2, y - base, w, base, STONE)
    o += rect(x - w / 2 + 10 * s, y - base - wh, w - 20 * s, wh, WALL)
    span = (w - 20 * s) / doors
    for i in range(doors):
        dx = x - w / 2 + 10 * s + i * span
        if open_center and i == doors // 2:
            o += rect(dx + 8 * s, y - base - wh + 12 * s, span - 16 * s, wh - 12 * s, '#5a3a1e')
            o += rect(dx + 8 * s, y - base - 30 * s, span - 16 * s, 30 * s, WOOD_L)
            for k in range(1, 4):
                o += line(dx + 8 * s, y - base - 30 * s + k * 8 * s, dx + span - 8 * s, y - base - 30 * s + k * 8 * s, stroke=WOOD, stroke_width=2 * s)
        else:
            o += lattice(dx + 16 * s, y - base - wh + 18 * s, span - 32 * s, wh - 30 * s, lit, cols=3, rows=5, sw=2.5 * s)
    for i in range(doors + 1):
        px = x - w / 2 + 10 * s + i * span - 9 * s
        o += rect(px, y - base - wh - 4 * s, 18 * s, wh + 4 * s, WOOD)
    ey = y - base - wh - 8 * s
    d = D('M', x - w / 2 - 70 * s, ey + 30 * s, 'Q', x, ey - 26 * s, x + w / 2 + 70 * s, ey + 30 * s,
          'L', x + w / 2 - 80 * s, ey - rh, 'Q', x, ey - rh - 18 * s, x - w / 2 + 80 * s, ey - rh, 'Z')
    o += path(d, TILE)
    for i in range(1, 12):
        t = i / 12
        ax = x - w / 2 - 70 * s + t * (w + 140 * s)
        ay = (1 - t) ** 2 * (ey + 30 * s) + 2 * t * (1 - t) * (ey - 26 * s) + t * t * (ey + 30 * s)
        bx = x - w / 2 + 80 * s + t * (w - 160 * s)
        o += line(ax, ay - 6 * s, bx, ey - rh + 2 * s, stroke=TILE_D, stroke_width=2.2 * s)
    o += path(D('M', x - w / 2 + 70 * s, ey - rh + 4 * s, 'Q', x, ey - rh - 34 * s, x + w / 2 - 70 * s, ey - rh + 4 * s,
                'L', x + w / 2 - 80 * s, ey - rh + 16 * s, 'Q', x, ey - rh - 8 * s, x - w / 2 + 80 * s, ey - rh + 16 * s, 'Z'), TILE_D)
    for i in range(0, 13):
        t = i / 12
        ax = x - w / 2 - 66 * s + t * (w + 132 * s)
        ay = (1 - t) ** 2 * (ey + 30 * s) + 2 * t * (1 - t) * (ey - 26 * s) + t * t * (ey + 30 * s)
        o += circle(ax, ay + 2 * s, 6 * s, '#9aa0ad', stroke_width=2 * s)
    return o


def stone_wall(x1, x2, y, h=110, s=1.0, seed=3, cap=True, snow=False):
    o = rect(x1, y - h, x2 - x1, h, '#b7ab92')
    r = Rng(seed)
    rows = max(1, int(h / (38 * s)))
    for j in range(rows):
        cy = y - h + 22 * s + j * 36 * s
        x = x1 + (j % 2) * 28 * s + 10
        while x < x2 - 22 * s:
            rw = r.u(26, 44) * s
            o += el('ellipse', cx=x + rw / 2, cy=cy, rx=rw / 2, ry=14 * s, fill=r.ch(['#a3977f', '#c9bea5', '#958870', '#b3a58c']), stroke=OUT, stroke_width=2)
            x += rw + 12 * s
    if cap:
        o += rect(x1 - 6, y - h - 14 * s, x2 - x1 + 12, 16 * s, '#ffffff' if snow else THATCH, rx=6)
    return o


def branch_tree(x, y, s, trunk_color, segs, widths):
    o = ''.join(el('path', d=smooth(seg), fill='none', stroke=OUT, stroke_width=(w + 6) * s, stroke_linecap='round', stroke_linejoin='round') for seg, w in zip(segs, widths))
    o += ''.join(el('path', d=smooth(seg), fill='none', stroke=trunk_color, stroke_width=w * s, stroke_linecap='round', stroke_linejoin='round') for seg, w in zip(segs, widths))
    return o


def plum_segs(x, y, s):
    return [[(x, y), (x - 12 * s, y - 90 * s), (x + 14 * s, y - 190 * s), (x + 4 * s, y - 290 * s)],
            [(x + 4 * s, y - 150 * s), (x + 80 * s, y - 205 * s), (x + 160 * s, y - 225 * s)],
            [(x - 6 * s, y - 120 * s), (x - 90 * s, y - 175 * s), (x - 160 * s, y - 260 * s)],
            [(x + 8 * s, y - 235 * s), (x + 60 * s, y - 310 * s)],
            [(x - 2 * s, y - 205 * s), (x - 60 * s, y - 300 * s)]]


def plum(x, y, s=1.0, color=PINK, seed=5, bare=False, snow=False):
    r = Rng(seed)
    segs = plum_segs(x, y, s)
    o = branch_tree(x, y, s, '#6e4a2b', segs, [28, 16, 16, 11, 11])
    if bare:
        if snow:
            for seg in segs[1:]:
                for (px, py) in seg[1:]:
                    o += flat('ellipse', cx=px, cy=py - 6 * s, rx=22 * s, ry=7 * s, fill='#ffffff')
        return o
    for seg in segs[1:]:
        for (px, py) in seg[1:]:
            for _ in range(7):
                bx = px + r.u(-48, 48) * s
                by = py + r.u(-44, 30) * s
                o += circle(bx, by, r.u(9, 14) * s, color, stroke_width=2.5)
                o += flat('circle', cx=bx, cy=by, r=3.2 * s, fill='#d94a5c')
    return o


def pine(x, y, s=1.0):
    """Minhwa-style pine: leaning trunk, flat foliage clouds on branches."""
    o = tube([(x, y), (x - 20 * s, y - 150 * s), (x + 30 * s, y - 300 * s)], 26 * s, '#6b4525')
    clusters = [((x + 30 * s, y - 300 * s), (x + 70 * s, y - 340 * s), 150, 40),
                ((x - 12 * s, y - 210 * s), (x - 130 * s, y - 250 * s), 130, 36),
                ((x + 8 * s, y - 130 * s), (x + 140 * s, y - 170 * s), 120, 34)]
    for (bx, by), (cx, cy), rx, ry in clusters:
        o += tube([(bx, by), (cx, cy + 10 * s)], 14 * s, '#6b4525')
    for (bx, by), (cx, cy), rx, ry in clusters:
        o += ellipse(cx - rx * 0.35 * s, cy + 6 * s, rx * 0.55 * s, ry * 0.9 * s, GREEN_D)
        o += ellipse(cx + rx * 0.35 * s, cy + 4 * s, rx * 0.55 * s, ry * 0.9 * s, GREEN_D)
        o += ellipse(cx, cy - 10 * s, rx * s, ry * s, '#3f7a3a')
        o += flat('ellipse', cx=cx - rx * 0.2 * s, cy=cy - 18 * s, rx=rx * 0.55 * s, ry=ry * 0.4 * s, fill='#5d9a4c')
    return o


def road_polygon(centers, color, edge=EARTH_D):
    """centers: list of (x, y, width) from far to near; returns a perspective road."""
    left = [(x - w / 2, y) for x, y, w in centers]
    right = [(x + w / 2, y) for x, y, w in centers][::-1]
    d = smooth(left) + ' ' + smooth(right).replace('M', 'L', 1) + ' Z'
    return el('path', d=d, fill=color, stroke=edge, stroke_width=6, stroke_linejoin='round')


def bush_tree(x, y, s=1.0, color=GREEN, light=GREEN_L, fruit=None, seed=7, trunk='#6e4a2b'):
    o = tube([(x, y), (x + 4 * s, y - 150 * s)], 30 * s, trunk)
    o += tube([(x + 2 * s, y - 110 * s), (x - 60 * s, y - 180 * s)], 14 * s, trunk)
    o += tube([(x + 2 * s, y - 130 * s), (x + 64 * s, y - 190 * s)], 14 * s, trunk)
    blobs = [(0, -230, 120, 95), (-95, -190, 90, 70), (95, -195, 90, 70), (0, -300, 80, 55)]
    for bx, by, rx, ry in blobs:
        o += ellipse(x + bx * s, y + by * s, rx * s, ry * s, color)
    for bx, by, rx, ry in blobs:
        o += flat('ellipse', cx=x + (bx - rx * 0.3) * s, cy=y + (by - ry * 0.35) * s, rx=rx * 0.5 * s, ry=ry * 0.4 * s, fill=light)
    if fruit:
        r = Rng(seed)
        for _ in range(12):
            bx, by, rx, ry = r.ch(blobs)
            o += circle(x + (bx + r.u(-rx * 0.7, rx * 0.7)) * s, y + (by + r.u(-ry * 0.6, ry * 0.6)) * s, 11 * s, fruit, stroke_width=2.5)
    return o


def jar(x, y, s=1.0, color='#6b4a2b'):
    d = D('M', x - 34 * s, y, 'L', x - 46 * s, y - 40 * s, 'Q', x - 58 * s, y - 100 * s, x - 34 * s, y - 130 * s,
          'L', x + 34 * s, y - 130 * s, 'Q', x + 58 * s, y - 100 * s, x + 46 * s, y - 40 * s, 'L', x + 34 * s, y, 'Z')
    o = path(d, color)
    o += flat('path', d=D('M', x - 30 * s, y - 60 * s, 'Q', x - 42 * s, y - 100 * s, x - 22 * s, y - 118 * s), stroke='#9c7248', stroke_width=8 * s, stroke_linecap='round', fill='none')
    o += ellipse(x, y - 130 * s, 40 * s, 12 * s, '#4e3319')
    return o


def grass_tuft(x, y, s=1.0, color=GREEN_D):
    o = ''
    for dx, h in ((-18, 40), (-6, 56), (8, 50), (20, 38)):
        o += el('path', d=D('M', x + dx * s, y, 'q', 4 * s, -h * 0.5 * s, 10 * s, -h * s), fill='none', stroke=color, stroke_width=5 * s, stroke_linecap='round')
    return o


def flower(x, y, s=1.0, color='#f0a0b0', center='#ffd75e'):
    o = ''
    for k in range(5):
        a = k * 2 * math.pi / 5
        o += circle(x + math.cos(a) * 9 * s, y + math.sin(a) * 9 * s, 7 * s, color, stroke_width=2)
    o += flat('circle', cx=x, cy=y, r=5 * s, fill=center)
    return o


def ground_path(pts, w, color, edge=EARTH_D):
    d = smooth(pts)
    o = el('path', d=d, fill='none', stroke=edge, stroke_width=w + 10, stroke_linecap='round', stroke_linejoin='round')
    o += el('path', d=d, fill='none', stroke=color, stroke_width=w, stroke_linecap='round', stroke_linejoin='round')
    return o


def moon(cx, cy, r):
    return (flat('circle', cx=cx, cy=cy, r=r * 1.9, fill='#ffe9a8', opacity=0.12)
            + flat('circle', cx=cx, cy=cy, r=r * 1.35, fill='#ffe9a8', opacity=0.16)
            + circle(cx, cy, r, '#fff1b8', stroke='#e6cf7c', stroke_width=4)
            + flat('circle', cx=cx - r * 0.3, cy=cy - r * 0.2, r=r * 0.18, fill='#f3dc93')
            + flat('circle', cx=cx + r * 0.25, cy=cy + r * 0.3, r=r * 0.12, fill='#f3dc93'))


def stars(seed, count, ymax=700):
    r = Rng(seed)
    o = ''
    for _ in range(count):
        x, y = r.u(0, BW), r.u(0, ymax)
        rr = r.u(2, 5)
        o += flat('circle', cx=x, cy=y, r=rr, fill='#fff6d0', opacity=r.u(0.5, 1))
    return o


def flag(x, y, h, color, s=1.0):
    o = tube([(x, y), (x, y - h)], 10 * s, WOOD_D)
    o += circle(x, y - h, 9 * s, OCHRE)
    o += path(D('M', x, y - h + 14 * s, 'L', x + 150 * s, y - h + 40 * s, 'L', x + 118 * s, y - h + 90 * s, 'L', x + 150 * s, y - h + 140 * s, 'L', x, y - h + 165 * s, 'Z'), color)
    return o


def apartment(x, y, w, h, color='#d8dbe0', win='#9bb3c9'):
    o = rect(x, y - h, w, h, color, stroke_width=3)
    cols = max(2, int(w / 40))
    rows = max(2, int(h / 46))
    for i in range(cols):
        for j in range(rows):
            o += flat('rect', x=x + 10 + i * (w - 20) / cols, y=y - h + 14 + j * (h - 24) / rows, width=(w - 20) / cols * 0.5, height=(h - 24) / rows * 0.5, fill=win)
    o += rect(x + w * 0.3, y - h - 14, w * 0.4, 14, color, stroke_width=3)
    return o


# ---------------------------------------------------------------- backgrounds

def village_scene(mode):
    night = mode == 'night'
    winter = mode == 'winter'
    if night:
        defs = lin('sky', [(0, '#0b1636'), (0.6, '#1e2f5e'), (1, '#3b4d7d')])
    elif winter:
        defs = lin('sky', [(0, '#8e98a6'), (0.6, '#c3cad3'), (1, '#e6e9ec')])
    else:
        defs = lin('sky', [(0, '#79bde8'), (0.55, '#b5dcf3'), (1, '#e9f4fb')])
    defs += BLUR
    b = sky_rect('sky')
    if night:
        b += stars(11, 140, 800)
        b += moon(1900, 250, 110)
    else:
        cl = '#ffffff' if not winter else '#dfe4ea'
        edge = '#c9d7e3' if not winter else '#b8c0ca'
        for x, y, s in ((180, 230, 1.1), (900, 150, 0.8), (1500, 260, 1.3), (2100, 170, 0.9)):
            b += cloud(x, y, s, cl, edge)
    if night:
        far, mid, near = '#243660', '#1d2d52', '#2f4a4f'
    elif winter:
        far, mid, near = '#b8c3cf', '#a7b3bf', '#e7ebee'
    else:
        far, mid, near = '#b7cfe0', '#8fb2a1', '#7fa86b'
    b += ridge(1, 560, 240, 12, far)
    if not winter:
        b += fog(1200, 640, 1300, 60, 0.35 if not night else 0.12)
    b += ridge(2, 690, 190, 10, mid)
    b += ridge(3, 800, 90, 8, near)
    ground = '#3d4552' if night else ('#f3f5f7' if winter else '#cdb77f')
    b += flat('rect', x=0, y=820, width=BW, height=BH - 820, fill=ground)
    road = '#4a5160' if night else ('#e4e8ec' if winter else '#dcc08a')
    b += ground_path([(1250, 860), (1100, 980), (1350, 1120), (1000, 1250), (1200, 1380)], 170, road, '#2f3540' if night else ('#c8ced4' if winter else EARTH_D))
    # back row
    for x, s in ((520, 0.72), (1320, 0.7), (2020, 0.74)):
        b += thatched(x, 905, s, lit=night, snow=winter)
    b += stone_wall(0, 1150, 960, 60, 0.7, seed=4, snow=winter)
    b += stone_wall(1450, BW, 960, 60, 0.7, seed=5, snow=winter)
    # trees
    if winter:
        b += plum(760, 940, 0.9, bare=True, snow=True)
        b += plum(1700, 960, 1.0, bare=True, snow=True)
    else:
        b += plum(760, 940, 0.9, PINK if not night else '#d79aa8', seed=6)
        b += plum(1700, 960, 1.0, '#f7c9d2' if not night else '#d79aa8', seed=8)
    # front row
    b += thatched(330, 1200, 1.15, lit=night, snow=winter)
    b += thatched(2060, 1190, 1.1, lit=night, snow=winter, flip=True)
    b += stone_wall(600, 950, 1200, 100, 1.0, seed=9, snow=winter)
    b += stone_wall(1520, 1750, 1210, 100, 1.0, seed=10, snow=winter)
    if winter:
        for x, y, s in ((330, 1200 - 265 * 1.15, 1.15), (2060, 1190 - 265 * 1.1, 1.1)):
            cx = x - 70 * s
            b += rect(cx - 14 * s, y - 40 * s, 28 * s, 60 * s, '#7b6455')
            for k in range(3):
                b += el('path', d=D('M', cx, y - 50 * s - k * 70 * s, 'q', 40 * s, -30 * s, 10 * s, -70 * s), fill='none', stroke='#ffffff', stroke_width=(22 - k * 4) * s, stroke_linecap='round', opacity=0.7)
        b += ridge(12, 1310, 60, 6, '#ffffff', base=BH + 50)
    else:
        for x, y in ((760, 1290), (1120, 1330), (1600, 1300), (1900, 1330)):
            b += grass_tuft(x, y, 1.2, '#4c8a3f' if not night else '#2c4a42')
        if not night:
            r = Rng(21)
            for _ in range(24):
                b += flower(r.u(40, 2360), r.u(1255, 1335), r.u(0.8, 1.2), r.ch(['#f2a4b8', '#f7d76a', '#ff9db0']))
            b += ridge(12, 1300, 50, 6, '#8fbb5f', base=BH + 50)
        else:
            b += ridge(12, 1300, 50, 6, '#2a3340', base=BH + 50)
    # azalea bushes on hill
    if not winter:
        for x, y, s in ((150, 830, 1.0), (2300, 840, 1.1), (1100, 850, 0.8)):
            b += ellipse(x, y, 70 * s, 42 * s, '#f28ab0' if not night else '#8d5a75')
            b += ellipse(x + 50 * s, y + 10 * s, 50 * s, 32 * s, '#f6a9c4' if not night else '#8d5a75')
    return defs, b


def bg_village_spring_day():
    return village_scene('spring')


def bg_village_night():
    return village_scene('night')


def bg_village_winter():
    return village_scene('winter')


def bg_yangban_yard():
    defs = lin('sky', [(0, '#86c4e6'), (1, '#e5f2fa')]) + BLUR
    b = sky_rect('sky')
    for x, y, s in ((200, 180, 0.9), (1400, 120, 1.0), (2050, 260, 0.7)):
        b += cloud(x, y, s)
    b += ridge(31, 560, 180, 10, '#b7cfe0')
    b += ridge(32, 660, 120, 8, '#8fb2a1')
    b += flat('rect', x=0, y=700, width=BW, height=BH - 700, fill='#d9c49a')
    # outer wall with tiled cap
    b += rect(-10, 560, BW + 20, 150, '#e6dcc3')
    b += path(D('M', -20, 560, 'L', BW + 20, 560, 'L', BW + 20, 530, 'L', -20, 530, 'Z'), TILE)
    for i in range(0, 49):
        b += line(i * 50 + 10, 532, i * 50 + 10, 558, stroke=TILE_D, stroke_width=2)
    b += rect(-10, 700, BW + 20, 14, STONE)
    # main house with daecheong maru
    b += tiled(1200, 880, 1.25, w=1240, doors=5, open_center=True, wall_h=190, roof_h=120)
    # stone steps
    b += rect(1090, 852, 220, 30, STONE)
    b += rect(1110, 870, 180, 18, '#a3987f')
    # side small building (left)
    b += tiled(230, 880, 0.9, w=420, doors=2, wall_h=150)
    # persimmon tree at left front
    b += bush_tree(560, 1180, 1.25, '#5f9a4a', '#98c66d', fruit='#ef8a2e', seed=12)
    # jangdokdae right
    b += rect(1650, 1080, 640, 40, STONE)
    b += stone_wall(1650, 2290, 1080, 60, 0.8, seed=13, cap=False)
    for x, s in ((1720, 0.85), (1830, 1.05), (1950, 0.95), (2080, 1.1), (2210, 0.9)):
        b += jar(x, 1080, s)
    b += jar(1770, 1170, 1.15)
    b += jar(2130, 1180, 1.0)
    # yard details
    for x, y in ((900, 1040), (1500, 1060), (1150, 1250), (760, 1300)):
        b += ellipse(x, y, 60, 22, '#c6b18a', stroke_width=3)
    b += grass_tuft(120, 1320, 1.4)
    b += grass_tuft(2350, 1330, 1.3)
    b += flower(1420, 1290, 1.4, '#f7d76a')
    b += flower(1470, 1310, 1.1, '#f2a4b8')
    b += ridge(33, 1330, 30, 6, '#c8b284', base=BH + 50)
    return defs, b


def screen_panel(x, y, w, h, seed):
    r = Rng(seed)
    o = rect(x, y, w, h, '#f6efdc', stroke_width=3)
    o += rect(x + 12, y + 12, w - 24, h - 24, 'none', stroke='#b89b6a', stroke_width=2)
    kind = seed % 3
    if kind == 0:
        o += mountain([(x + 20, y + h - 60), (x + w * 0.3, y + h * 0.45), (x + w * 0.55, y + h * 0.62), (x + w * 0.8, y + h * 0.35), (x + w - 20, y + h - 60)], '#6f7b91', base=y + h - 30)
        o += flat('rect', x=x + 20, y=y + h - 34, width=w - 40, height=6, fill='#6f7b91')
    elif kind == 1:
        o += tube([(x + w * 0.5, y + h - 40), (x + w * 0.35, y + h * 0.55), (x + w * 0.55, y + h * 0.25)], 8, '#5b4632')
        for _ in range(9):
            o += circle(x + w * 0.45 + r.u(-60, 60), y + h * 0.45 + r.u(-90, 60), 7, '#e98fa4', stroke_width=2)
    else:
        for k in range(3):
            bx = x + w * (0.3 + 0.2 * k)
            o += tube([(bx, y + h - 40), (bx + 6, y + h * 0.3)], 6, '#4f7d4a')
            o += el('path', d=D('M', bx + 3, y + h * 0.55, 'q', -40, -20, -60, 10), fill='none', stroke='#4f7d4a', stroke_width=5, stroke_linecap='round')
            o += el('path', d=D('M', bx + 3, y + h * 0.42, 'q', 40, -26, 62, -4), fill='none', stroke='#4f7d4a', stroke_width=5, stroke_linecap='round')
    return o


def bg_yangban_room():
    defs = lin('floor', [(0, '#cfa15a'), (1, '#e6bd77')]) + lin('wall', [(0, '#efe4cb'), (1, '#f7efdc')])
    b = flat('rect', x=0, y=0, width=BW, height=BH, fill='url(#wall)')
    # ceiling beams
    b += rect(-10, 60, BW + 20, 50, WOOD)
    b += rect(-10, 110, BW + 20, 22, WOOD_D)
    for x in (300, 900, 1500, 2100):
        b += rect(x - 12, 0, 24, 66, WOOD_D)
    # floor
    b += flat('rect', x=0, y=880, width=BW, height=BH - 880, fill='url(#floor)')
    b += line(0, 880, BW, 880, stroke=OUT, stroke_width=4)
    for i in range(1, 14):
        t = i / 14
        x0 = t * BW
        x1 = 1200 + (x0 - 1200) * 1.4
        b += line(x0, 880, x1, BH, stroke='#b48843', stroke_width=3)
    # folding screen
    for i in range(6):
        b += screen_panel(560 + i * 215, 250, 200, 600, seed=30 + i)
    b += rect(548, 240, 6 * 215 - 3, 20, '#3b2a1e')
    b += rect(548, 850, 6 * 215 - 3, 20, '#3b2a1e')
    # lattice door on the left
    b += rect(80, 180, 400, 700, WOOD_L)
    b += lattice(100, 200, 360, 660, cols=4, rows=8, sw=4)
    # mungap (low chest) left of centre
    b += rect(560, 960, 380, 130, '#7a4a25', rx=8)
    b += line(750, 960, 750, 1090, stroke=WOOD_D, stroke_width=4)
    for x in (655, 845):
        b += circle(x, 1025, 18, '#e0b64a', stroke_width=3)
        b += rect(x - 6, 1030, 12, 30, '#e0b64a', rx=4, stroke_width=2)
    b += rect(570, 1090, 20, 24, WOOD_D)
    b += rect(910, 1090, 20, 24, WOOD_D)
    # seoan (low desk) centre-right
    b += rect(1300, 1030, 520, 40, '#7a4a25', rx=6)
    b += rect(1320, 1070, 30, 70, '#5c3a1c')
    b += rect(1770, 1070, 30, 70, '#5c3a1c')
    b += path(D('M', 1330, 1030, 'Q', 1320, 1000, 1350, 985, 'L', 1770, 985, 'Q', 1800, 1000, 1790, 1030, 'Z'), '#a06432')
    # book on desk
    b += rect(1370, 990, 150, 34, INDIGO, rx=4)
    b += rect(1375, 985, 150, 34, INDIGO_D, rx=4)
    for x in (1395, 1420, 1445, 1470, 1495):
        b += flat('circle', cx=x, cy=990, r=3, fill='#f2e4c4')
    # brush & inkstone
    b += rect(1600, 1000, 110, 22, '#2b2b2b', rx=6)
    b += line(1560, 950, 1640, 1010, stroke=WOOD_D, stroke_width=8)
    # candle stand on right
    b += rect(2030, 1120, 90, 16, '#c99a3a', rx=6)
    b += rect(2065, 860, 20, 260, '#c99a3a')
    b += rect(2035, 850, 80, 14, '#c99a3a', rx=4)
    b += rect(2060, 720, 30, 132, '#fff5dc')
    b += path(D('M', 2075, 715, 'q', -22, -40, 0, -70, 'q', 22, 30, 0, 70, 'Z'), '#ffb347', stroke='#e07b1b', stroke_width=3)
    b += flat('circle', cx=2075, cy=690, r=80, fill='#ffd977', opacity=0.18)
    # cushion (bangseok)
    b += rect(1440, 1200, 260, 70, '#b8323a', rx=30)
    b += rect(1460, 1210, 220, 40, '#d4535a', rx=20, stroke='none')
    # small vase on mungap
    b += path(D('M', 690, 960, 'L', 680, 900, 'Q', 660, 870, 700, 850, 'L', 760, 850, 'Q', 800, 870, 780, 900, 'L', 770, 960, 'Z'), '#8fb8c9')
    b += tube([(730, 850), (740, 790), (720, 740)], 6, '#5b4632')
    b += circle(715, 738, 10, '#e98fa4', stroke_width=2)
    b += circle(745, 780, 9, '#e98fa4', stroke_width=2)
    return defs, b


def bg_servant_room():
    defs = lin('wall', [(0, '#a67c50'), (1, '#c39a68')]) + lin('floor', [(0, '#7c5a3a'), (1, '#9a7448')])
    b = flat('rect', x=0, y=0, width=BW, height=BH, fill='url(#wall)')
    r = Rng(41)
    for _ in range(90):
        b += flat('ellipse', cx=r.u(0, BW), cy=r.u(0, 900), rx=r.u(14, 50), ry=r.u(6, 20), fill='#8d6640', opacity=r.u(0.08, 0.2))
    b += rect(-10, 40, BW + 20, 46, WOOD_D)
    for x in (400, 1200, 2000):
        b += rect(x - 16, 0, 32, 46, WOOD)
    # floor
    b += flat('rect', x=0, y=900, width=BW, height=BH - 900, fill='url(#floor)')
    b += line(0, 900, BW, 900, stroke=OUT, stroke_width=4)
    # small window (top right)
    b += rect(1760, 250, 300, 260, WOOD)
    b += lattice(1780, 270, 260, 220, lit=False, cols=2, rows=2, sw=4)
    b += flat('rect', x=1780, y=270, width=260, height=220, fill='#dfe8ef', opacity=0.5)
    # herbs hanging
    for x in (520, 640):
        b += line(x, 200, x, 260, stroke='#cbbb8f', stroke_width=4)
        for k in range(5):
            a = -0.9 + k * 0.45
            b += el('path', d=D('M', x, 260, 'q', 40 * math.sin(a), 60, 70 * math.sin(a), 150), fill='none', stroke='#5f8a45', stroke_width=7, stroke_linecap='round')
            b += ellipse(x + 70 * math.sin(a), 410, 14, 30, '#7aa552', stroke_width=2.5, transform=f'rotate({-30 * math.sin(a)} {x + 70 * math.sin(a)} 410)')
    # straw mat
    b += path(D('M', 500, 1000, 'L', 1900, 1000, 'L', 2080, 1290, 'L', 320, 1290, 'Z'), '#d9c07a')
    for i in range(1, 12):
        t = i / 12
        b += line(500 + t * 1400, 1000, 320 + t * 1760, 1290, stroke='#b59a52', stroke_width=2.5)
    for j in range(1, 6):
        t = j / 6
        b += line(500 - t * 180, 1000 + t * 290, 1900 + t * 180, 1000 + t * 290, stroke='#b59a52', stroke_width=2.5)
    # folded blanket at right
    b += rect(1900, 820, 360, 90, '#8fa9c9', rx=14)
    b += rect(1900, 760, 360, 70, '#c0d1e8', rx=14)
    b += rect(1910, 700, 340, 70, '#8fa9c9', rx=14)
    # oil lamp on stand (left-centre)
    b += rect(1180, 980, 110, 18, WOOD_D, rx=4)
    b += rect(1225, 700, 20, 280, WOOD_D)
    b += ellipse(1235, 700, 46, 14, '#6b4a2b')
    b += path(D('M', 1210, 700, 'Q', 1200, 660, 1235, 655, 'Q', 1270, 660, 1260, 700, 'Z'), '#8b6a3a')
    b += path(D('M', 1235, 650, 'q', -14, -30, 0, -52, 'q', 14, 22, 0, 52, 'Z'), '#ffb347', stroke='#e07b1b', stroke_width=3)
    b += flat('circle', cx=1235, cy=640, r=120, fill='#ffd977', opacity=0.16)
    # medicine pot on brazier (left)
    b += ellipse(560, 1110, 120, 30, '#4a4a4a')
    b += rect(470, 1040, 180, 70, '#5a5a5a', rx=10)
    b += flat('rect', x=490, y=1060, width=140, height=30, fill='#e8672c', opacity=0.8)
    b += path(D('M', 500, 1040, 'L', 480, 940, 'Q', 470, 880, 520, 870, 'L', 600, 870, 'Q', 650, 880, 640, 940, 'L', 620, 1040, 'Z'), '#6b4a2b')
    b += ellipse(560, 870, 50, 14, '#8b6a3a')
    b += circle(560, 856, 12, '#8b6a3a')
    b += tube([(630, 960), (700, 880)], 16, '#6b4a2b')
    b += el('path', d=D('M', 500, 890, 'Q', 560, 770, 620, 890), fill='none', stroke=OUT, stroke_width=22, stroke_linecap='round')
    b += el('path', d=D('M', 500, 890, 'Q', 560, 770, 620, 890), fill='none', stroke='#6b4a2b', stroke_width=14, stroke_linecap='round')
    for k in range(3):
        b += el('path', d=D('M', 700 + k * 12, 860, 'q', 20, -50, -10, -110), fill='none', stroke='#ffffff', stroke_width=8, stroke_linecap='round', opacity=0.35)
    # water jar
    b += jar(2200, 1250, 1.3, '#6b4a2b')
    b += grass_tuft(350, 1320, 1.0, '#8b6a3a')
    return defs, b


def market_stall(x, y, s, cloth, goods):
    o = ''
    for px in (x - 190 * s, x + 190 * s):
        o += tube([(px, y), (px, y - 260 * s)], 14 * s, WOOD)
    o += path(D('M', x - 240 * s, y - 190 * s, 'L', x + 240 * s, y - 190 * s, 'L', x + 200 * s, y - 300 * s, 'L', x - 200 * s, y - 300 * s, 'Z'), cloth)
    o += path(D('M', x - 240 * s, y - 190 * s, 'Q', x - 120 * s, y - 165 * s, x, y - 190 * s, 'Q', x + 120 * s, y - 165 * s, x + 240 * s, y - 190 * s, 'L', x + 240 * s, y - 175 * s, 'Q', x + 120 * s, y - 150 * s, x, y - 175 * s, 'Q', x - 120 * s, y - 150 * s, x - 240 * s, y - 175 * s, 'Z'), cloth)
    o += rect(x - 200 * s, y - 100 * s, 400 * s, 24 * s, WOOD_L)
    o += rect(x - 180 * s, y - 76 * s, 24 * s, 76 * s, WOOD)
    o += rect(x + 156 * s, y - 76 * s, 24 * s, 76 * s, WOOD)
    gx = x - 150 * s
    for kind, color in goods:
        if kind == 'roll':
            o += rect(gx, y - 150 * s, 60 * s, 50 * s, color, rx=8 * s)
            o += rect(gx, y - 200 * s, 60 * s, 50 * s, color, rx=8 * s)
        elif kind == 'jar':
            o += jar(gx + 30 * s, y - 100 * s, 0.45 * s, color)
        elif kind == 'veg':
            for k in range(5):
                o += circle(gx + (k % 3) * 24 * s + 10 * s, y - 118 * s - (k // 3) * 22 * s, 13 * s, color, stroke_width=2.5)
        elif kind == 'bowl':
            o += path(D('M', gx, y - 130 * s, 'Q', gx + 35 * s, y - 90 * s, gx + 70 * s, y - 130 * s, 'Z'), color)
            o += ellipse(gx + 35 * s, y - 130 * s, 35 * s, 10 * s, '#fff')
        gx += 90 * s
    return o


def straw_bundle(x, y, s=1.0):
    o = path(D('M', x - 60 * s, y, 'L', x - 30 * s, y - 150 * s, 'L', x + 30 * s, y - 150 * s, 'L', x + 60 * s, y, 'Z'), '#d9c07a')
    for k in range(-2, 3):
        o += line(x + k * 20 * s, y - 8 * s, x + k * 9 * s, y - 140 * s, stroke=THATCH_D, stroke_width=2.5 * s)
    o += rect(x - 40 * s, y - 110 * s, 80 * s, 14 * s, '#8b6a3a', rx=4 * s)
    return o


def bg_market():
    defs = lin('sky', [(0, '#8cc6e6'), (1, '#e8f3fa')]) + BLUR
    b = sky_rect('sky')
    for x, y, s in ((300, 200, 1.0), (1300, 140, 0.8), (1900, 230, 1.1)):
        b += cloud(x, y, s)
    b += ridge(51, 580, 160, 10, '#b7cfe0')
    b += ridge(52, 690, 100, 8, '#93b598')
    b += flat('rect', x=0, y=720, width=BW, height=BH - 720, fill='#d4bb86')
    for x, s in ((250, 0.6), (700, 0.55), (1700, 0.6), (2200, 0.58)):
        b += thatched(x, 790, s)
    b += stone_wall(0, BW, 830, 40, 0.6, seed=53)
    b += market_stall(500, 1120, 1.0, '#e9dcc0', [('roll', INDIGO), ('roll', '#c84a4a'), ('roll', '#f0d060'), ('jar', '#6b4a2b')])
    b += market_stall(1230, 1100, 0.95, '#c4d9e6', [('veg', '#7ab648'), ('veg', '#e9832e'), ('bowl', '#d9c9a6'), ('bowl', '#d9c9a6')])
    b += market_stall(1950, 1130, 1.05, OCHRE, [('jar', '#6b4a2b'), ('jar', '#4e3319'), ('roll', '#8fb8c9'), ('veg', '#c84a4a')])
    b += straw_bundle(880, 1210, 1.0)
    b += straw_bundle(960, 1230, 0.8)
    b += jar(1620, 1250, 1.3)
    b += jar(1720, 1240, 1.0)
    for x, y in ((250, 1290), (1400, 1300), (2300, 1280)):
        b += ellipse(x, y, 60, 20, '#c1a76f', stroke_width=3)
    b += flat('rect', x=0, y=1300, width=BW, height=50, fill='#c9ad74')
    b += grass_tuft(120, 1330, 1.3, '#7f9d50')
    b += grass_tuft(2280, 1340, 1.1, '#7f9d50')
    return defs, b


def rock(x, y, s=1.0, color='#8f8a80'):
    o = path(D('M', x - 70 * s, y, 'Q', x - 80 * s, y - 60 * s, x - 30 * s, y - 80 * s, 'L', x + 30 * s, y - 90 * s, 'Q', x + 85 * s, y - 60 * s, x + 70 * s, y, 'Z'), color)
    o += flat('path', d=D('M', x - 40 * s, y - 40 * s, 'Q', x - 30 * s, y - 68 * s, x + 10 * s, y - 72 * s), stroke='#b5b0a6', stroke_width=6 * s, stroke_linecap='round', fill='none')
    return o


def bg_mountain_path():
    defs = lin('sky', [(0, '#7db8e0'), (0.5, '#c5e0f2'), (1, '#f0f5f8')]) + BLUR
    b = sky_rect('sky')
    b += cloud(1700, 160, 1.1)
    b += cloud(400, 250, 0.9)
    b += ridge(61, 430, 260, 12, '#9cb6cd')
    b += fog(1200, 560, 1400, 70, 0.55)
    b += ridge(62, 600, 220, 10, '#7f9fa8')
    b += fog(600, 720, 900, 60, 0.5)
    b += fog(1900, 700, 900, 60, 0.5)
    b += ridge(63, 760, 180, 9, '#5f8a6f')
    b += ridge(64, 880, 120, 8, '#4f7a52')
    b += flat('rect', x=0, y=950, width=BW, height=BH - 950, fill='#6d9a52')
    b += road_polygon([(1240, 930, 50), (1190, 1000, 110), (1330, 1110, 200), (1130, 1240, 330), (1230, 1400, 520)], '#d7bd86', '#a98a55')
    b += pine(300, 1000, 1.0)
    b += pine(2050, 980, 1.1)
    b += pine(1600, 900, 0.7)
    b += pine(800, 900, 0.65)
    b += rock(600, 1180, 1.2)
    b += rock(1850, 1230, 1.4)
    b += rock(700, 1290, 0.8, '#7f7a70')
    b += pine(150, 1400, 1.5)
    b += pine(2300, 1420, 1.5)
    for x, y in ((950, 1330), (1500, 1320), (1250, 1340)):
        b += grass_tuft(x, y, 1.3)
    return defs, b


def bg_rice_field_summer():
    defs = lin('sky', [(0, '#5fa9e0'), (0.6, '#b6dcf4'), (1, '#eef7fc')]) + lin('paddy', [(0, '#7fbb52'), (1, '#4d9a3c')]) + BLUR
    b = sky_rect('sky')
    for x, y, s in ((150, 150, 1.4), (900, 90, 1.0), (1500, 200, 1.6), (2100, 110, 1.1)):
        b += cloud(x, y, s)
    b += ridge(71, 600, 160, 10, '#a9c4d6')
    b += ridge(72, 690, 90, 8, '#6fa66a')
    b += flat('rect', x=0, y=720, width=BW, height=BH - 720, fill='url(#paddy)')
    for i in range(0, 25):
        t = i / 24
        x0 = -400 + t * 3200
        b += line(1200 + (x0 - 1200) * 0.2, 725, x0, BH, stroke='#3e8236', stroke_width=3)
    for j in range(1, 9):
        y = 720 + (j / 8) ** 1.6 * 630
        b += line(0, y, BW, y, stroke='#a6d67c', stroke_width=4 + j * 1.5, opacity=0.6)
    # levee paths
    b += ground_path([(0, 900), (800, 880), (1600, 895), (BW, 880)], 40, '#c9b27a', '#a98a55')
    # wondumak (hut on stilts)
    hx, hy = 1750, 1000
    for px in (hx - 120, hx + 120, hx - 50, hx + 50):
        b += tube([(px, hy), (px, hy - 200)], 16, WOOD)
    b += rect(hx - 170, hy - 220, 340, 26, WOOD_L)
    for px in (hx - 150, hx + 150):
        b += tube([(px, hy - 220), (px, hy - 330)], 12, WOOD)
    b += path(D('M', hx - 230, hy - 320, 'Q', hx - 200, hy - 420, hx - 60, hy - 440, 'L', hx + 60, hy - 440, 'Q', hx + 200, hy - 420, hx + 230, hy - 320, 'Q', hx, hy - 300, hx - 230, hy - 320, 'Z'), THATCH)
    for k in range(6):
        b += line(hx - 180 + k * 70, hy - 400, hx - 176 + k * 70, hy - 330, stroke=THATCH_D, stroke_width=3)
    b += tube([(hx + 190, hy), (hx + 250, hy - 210)], 8, WOOD)
    b += tube([(hx + 220, hy), (hx + 280, hy - 210)], 8, WOOD)
    for k in range(4):
        b += line(hx + 195 + k * 15, hy - 45 - k * 50, hx + 225 + k * 15, hy - 45 - k * 50, stroke=WOOD, stroke_width=8)
    b += bush_tree(300, 760, 0.55, '#4f8a42', '#82b45c')
    b += bush_tree(2250, 750, 0.5, '#4f8a42', '#82b45c')
    # foreground rice plants
    r = Rng(73)
    for _ in range(60):
        x = r.u(-20, BW + 20)
        y = r.u(1080, 1370)
        b += grass_tuft(x, y, r.u(1.2, 2.0), r.ch(['#2f7a33', '#3f9040', '#4f9d48']))
    return defs, b


def boat_shape(x, y, s=1.0):
    o = path(D('M', x - 300 * s, y - 90 * s, 'Q', x - 250 * s, y + 10 * s, x - 120 * s, y, 'L', x + 160 * s, y, 'Q', x + 280 * s, y - 10 * s, x + 320 * s, y - 100 * s, 'L', x + 260 * s, y - 60 * s, 'L', x - 240 * s, y - 60 * s, 'Z'), '#8b5a2e')
    o += path(D('M', x - 240 * s, y - 60 * s, 'L', x + 260 * s, y - 60 * s, 'Q', x + 300 * s, y - 85 * s, x + 320 * s, y - 100 * s, 'L', x - 300 * s, y - 90 * s, 'Z'), '#a87040')
    for k in range(4):
        o += line(x - 200 * s + k * 120 * s, y - 58 * s, x - 205 * s + k * 120 * s, y - 4 * s, stroke=WOOD_D, stroke_width=3 * s)
    o += line(x - 120 * s, y - 80 * s, x + 100 * s, y - 80 * s, stroke=WOOD_D, stroke_width=3 * s)
    return o


def bg_river_bank():
    defs = lin('sky', [(0, '#4e4a7d'), (0.35, '#c3688a'), (0.62, '#f19a5e'), (0.8, '#f8cc74')]) + lin('water', [(0, '#e1a26c'), (0.4, '#8a6f86'), (1, '#4a4e75')]) + BLUR
    b = sky_rect('sky')
    b += flat('circle', cx=1500, cy=700, r=230, fill='#ffe8a0', opacity=0.25)
    b += circle(1500, 700, 120, '#ffd66e', stroke='#f2b14a', stroke_width=4)
    b += ridge(81, 620, 180, 12, '#6a5276')
    b += ridge(82, 720, 110, 9, '#4a3c5c')
    b += flat('rect', x=0, y=760, width=BW, height=460, fill='url(#water)')
    r = Rng(83)
    for _ in range(40):
        y = r.u(780, 1180)
        w = r.u(60, 300) * (y - 700) / 300
        x = r.u(0, BW)
        b += flat('rect', x=x, y=y, width=w, height=5 + (y - 760) / 60, rx=4, fill='#ffd9a0', opacity=r.u(0.25, 0.6))
    b += flat('rect', x=1420, y=760, width=160, height=420, fill='#ffd066', opacity=0.18)
    b += boat_shape(700, 1080, 1.0)
    b += tube([(880, 1010), (960, 720)], 10, WOOD_D)
    # near bank
    b += path(D('M', -20, 1240, 'Q', 400, 1180, 900, 1220, 'Q', 1500, 1270, 2420, 1190, 'L', 2420, 1360, 'L', -20, 1360, 'Z'), '#6f5a44')
    b += path(D('M', -20, 1250, 'Q', 400, 1200, 900, 1235, 'Q', 1500, 1280, 2420, 1205, 'L', 2420, 1300, 'L', -20, 1300, 'Z'), '#8b6f4d', stroke='none')
    # reeds
    r2 = Rng(84)
    for _ in range(42):
        x = r2.u(0, BW)
        base_y = 1250 + (r2.r() - 0.5) * 60
        h = r2.u(220, 420)
        lean = r2.u(-40, 40)
        b += el('path', d=D('M', x, base_y, 'q', lean * 0.3, -h * 0.5, lean, -h), fill='none', stroke='#5a4a2c', stroke_width=5, stroke_linecap='round')
        b += ellipse(x + lean, base_y - h, 9, 34, '#a8865a', stroke_width=2.5, transform=f'rotate({lean * 0.4} {x + lean} {base_y - h})')
        for k in range(2):
            b += el('path', d=D('M', x + lean * 0.4, base_y - h * 0.45, 'q', 30 + k * 10, -20, 60 + k * 20, -70 - k * 20), fill='none', stroke='#5a4a2c', stroke_width=3, stroke_linecap='round')
    # birds
    for x, y, s in ((300, 300, 1.0), (380, 260, 0.8), (2000, 380, 0.9)):
        b += el('path', d=D('M', x - 30 * s, y, 'q', 15 * s, -22 * s, 30 * s, 0, 'q', 15 * s, -22 * s, 30 * s, 0), fill='none', stroke='#3b2f4a', stroke_width=4 * s, stroke_linecap='round')
    return defs, b


def bg_gwana_yard():
    defs = lin('sky', [(0, '#80bfe4'), (1, '#e4f1f9')]) + BLUR
    b = sky_rect('sky')
    b += cloud(300, 180, 1.0)
    b += cloud(1900, 120, 1.2)
    b += ridge(91, 520, 200, 10, '#b7cfe0')
    b += ridge(92, 640, 120, 8, '#8fb2a1')
    b += flat('rect', x=0, y=680, width=BW, height=BH - 680, fill='#dcc79f')
    # side walls
    b += rect(-10, 560, 620, 180, '#eadfc4')
    b += rect(1790, 560, 620, 180, '#eadfc4')
    b += rect(-20, 530, 640, 32, TILE)
    b += rect(1780, 530, 640, 32, TILE)
    for x in list(range(20, 620, 50)) + list(range(1800, 2400, 50)):
        b += line(x, 532, x, 560, stroke=TILE_D, stroke_width=2)
    # dongheon on a two-tier stone platform
    b += rect(400, 900, 1600, 60, STONE)
    b += rect(460, 850, 1480, 50, '#c2b69c')
    b += tiled(1200, 850, 1.3, w=1100, doors=5, open_center=True, wall_h=200, roof_h=130)
    # steps
    for k in range(4):
        b += rect(1090 - k * 20, 850 + k * 28, 220 + k * 40, 28, '#cfc4aa' if k % 2 else '#b9ad92')
    # flags
    b += flag(560, 900, 560, '#c84a4a', 1.1)
    b += flag(1840, 900, 560, INDIGO, 1.1)
    # paving
    for i in range(6):
        for j in range(3):
            b += rect(180 + i * 360 + (j % 2) * 120, 1000 + j * 110, 200, 70, '#d4c6a4', rx=10, stroke='#c1b28e', stroke_width=3)
    b += pine(140, 1010, 1.0)
    b += pine(2260, 1000, 1.0)
    b += flat('rect', x=0, y=1310, width=BW, height=40, fill='#cbb58a')
    b += grass_tuft(60, 1330, 1.2)
    b += grass_tuft(2340, 1330, 1.2)
    return defs, b


def bg_rain_road():
    defs = lin('sky', [(0, '#3f4552'), (0.55, '#6f7684'), (1, '#9aa0aa')]) + BLUR
    b = sky_rect('sky')
    b += cloud(200, 250, 1.6, '#7b8390', '#656c78')
    b += cloud(1400, 180, 1.3, '#7b8390', '#656c78')
    b += cloud(1000, 340, 1.1, '#8a919d', '#71788a')
    b += ridge(101, 640, 160, 10, '#5d6a72')
    b += fog(1200, 720, 1400, 60, 0.25, '#c9d0d8')
    b += ridge(102, 760, 110, 8, '#4a5f4f')
    b += flat('rect', x=0, y=800, width=BW, height=BH - 800, fill='#5c6a48')
    b += path(D('M', 900, 800, 'L', 1500, 800, 'L', 2300, 1360, 'L', 100, 1360, 'Z'), '#6b5238', stroke='#4a3826', stroke_width=5)
    b += path(D('M', 1000, 800, 'L', 1400, 800, 'L', 2000, 1360, 'L', 400, 1360, 'Z'), '#7a5f42', stroke='none')
    r = Rng(103)
    for _ in range(14):
        x = r.u(500, 1900)
        y = r.u(900, 1330)
        rx = r.u(60, 200) * (y - 800) / 400
        b += flat('ellipse', cx=x, cy=y, rx=rx, ry=rx * 0.22, fill='#9aa5ad', opacity=0.75)
        b += flat('ellipse', cx=x - rx * 0.2, cy=y - rx * 0.05, rx=rx * 0.5, ry=rx * 0.09, fill='#c4ccd2', opacity=0.7)
    b += bush_tree(250, 1000, 1.1, '#3d6a3a', '#5a8a4c', trunk='#4a3520')
    b += bush_tree(2150, 980, 1.2, '#3d6a3a', '#5a8a4c', trunk='#4a3520')
    b += pine(700, 900, 0.6)
    b += pine(1700, 890, 0.55)
    for x, y in ((300, 1300), (2200, 1320), (150, 1180), (2300, 1160)):
        b += grass_tuft(x, y, 1.4, '#3f6a3a')
    return defs, b


def city_gate(x, y, s=1.0):
    o = rect(x - 380 * s, y - 260 * s, 760 * s, 260 * s, '#a29a86')
    for j in range(5):
        for i in range(8):
            o += rect(x - 370 * s + i * 95 * s + (j % 2) * 40 * s, y - 250 * s + j * 50 * s, 80 * s, 40 * s, '#b3ab97', stroke_width=2)
    o += path(D('M', x - 90 * s, y, 'L', x - 90 * s, y - 130 * s, 'Q', x, y - 230 * s, x + 90 * s, y - 130 * s, 'L', x + 90 * s, y, 'Z'), '#3b3a44')
    o += tiled(x, y - 260 * s, s * 0.9, w=760, doors=4, wall_h=120, roof_h=90)
    o += tiled(x, y - 260 * s - 230 * s * 0.9, s * 0.8, w=700, doors=4, wall_h=110, roof_h=90)
    return o


def bg_hanyang_street():
    defs = lin('sky', [(0, '#7fbfe6'), (0.6, '#cfe6f5'), (1, '#f4f8fb')]) + BLUR
    b = sky_rect('sky')
    b += cloud(200, 160, 1.0)
    b += cloud(1300, 100, 0.9)
    b += cloud(2000, 220, 1.1)
    b += ridge(111, 520, 200, 10, '#9db8cc')
    b += ridge(112, 640, 120, 8, '#7ea08d')
    b += flat('rect', x=0, y=700, width=BW, height=BH - 700, fill='#d8c39a')
    b += path(D('M', 1040, 700, 'L', 1360, 700, 'L', 2500, 1360, 'L', -100, 1360, 'Z'), '#cbb27f', stroke='#a98a55', stroke_width=4)
    b += city_gate(1200, 700, 0.62)
    # receding houses left & right
    rows = [(880, 0.42, 1000, 1400), (990, 0.6, 760, 1640), (1140, 0.85, 460, 1940), (1330, 1.15, 90, 2310)]
    for y, s, lx, rx in rows:
        b += tiled(lx, y, s, w=520, doors=3)
        b += tiled(rx, y, s, w=520, doors=3)
    b += jar(700, 1330, 1.1)
    b += jar(1700, 1340, 1.0)
    b += ridge(113, 1330, 20, 6, '#c4ab76', base=BH + 50)
    return defs, b


def sheaf(x, y, s=1.0):
    o = path(D('M', x - 70 * s, y, 'L', x - 24 * s, y - 130 * s, 'L', x + 24 * s, y - 130 * s, 'L', x + 70 * s, y, 'Z'), '#e0c47c')
    for k in range(-3, 4):
        o += line(x + k * 18 * s, y - 6 * s, x + k * 6 * s, y - 120 * s, stroke=THATCH_D, stroke_width=2.5 * s)
    o += ellipse(x, y - 140 * s, 60 * s, 22 * s, '#c9a54a')
    o += rect(x - 36 * s, y - 60 * s, 72 * s, 12 * s, '#8b6a3a', rx=4 * s)
    return o


def dragonfly(x, y, s=1.0, ang=0):
    o = f'<g transform="rotate({ang} {x} {y})">'
    o += ellipse(x - 30 * s, y - 10 * s, 34 * s, 9 * s, '#f5f5fa', stroke='#7a8899', stroke_width=2, transform=f'rotate(-15 {x - 30 * s} {y - 10 * s})')
    o += ellipse(x + 30 * s, y - 10 * s, 34 * s, 9 * s, '#f5f5fa', stroke='#7a8899', stroke_width=2, transform=f'rotate(15 {x + 30 * s} {y - 10 * s})')
    o += ellipse(x - 28 * s, y + 8 * s, 30 * s, 8 * s, '#f5f5fa', stroke='#7a8899', stroke_width=2, transform=f'rotate(10 {x - 28 * s} {y + 8 * s})')
    o += ellipse(x + 28 * s, y + 8 * s, 30 * s, 8 * s, '#f5f5fa', stroke='#7a8899', stroke_width=2, transform=f'rotate(-10 {x + 28 * s} {y + 8 * s})')
    o += line(x, y - 4 * s, x, y + 70 * s, stroke='#c84a3a', stroke_width=7 * s)
    o += circle(x, y - 10 * s, 9 * s, '#c84a3a', stroke_width=2.5)
    o += '</g>'
    return o


def bg_autumn_yard():
    defs = lin('sky', [(0, '#8cc0e0'), (0.6, '#e2e9de'), (1, '#f6efd8')]) + BLUR
    b = sky_rect('sky')
    b += cloud(500, 170, 1.0)
    b += cloud(1800, 230, 0.9)
    b += ridge(121, 560, 200, 10, '#b4bfc9')
    b += ridge(122, 680, 120, 8, '#b48f5c')
    b += flat('rect', x=0, y=720, width=BW, height=BH - 720, fill='#dcc18a')
    b += thatched(1250, 880, 0.85)
    b += stone_wall(0, 1040, 900, 70, 0.8, seed=123)
    b += stone_wall(1460, BW, 900, 70, 0.8, seed=124)
    b += bush_tree(330, 960, 1.3, '#d9483b', '#f0785c', seed=125)
    b += bush_tree(2080, 950, 1.35, '#f0c530', '#f8e07a', seed=126)
    for x, y, s in ((900, 1180, 1.0), (1030, 1200, 1.1), (1160, 1180, 0.95), (960, 1060, 0.9), (1090, 1070, 0.9)):
        b += sheaf(x, y, s)
    r = Rng(127)
    for _ in range(40):
        x, y = r.u(0, BW), r.u(1000, 1340)
        col = r.ch(['#d9483b', '#f0c530', '#e8842e'])
        b += ellipse(x, y, 16, 9, col, stroke_width=2, transform=f'rotate({r.u(-60, 60)} {x} {y})')
    b += dragonfly(1500, 700, 1.3, 20)
    b += dragonfly(700, 620, 1.0, -30)
    b += dragonfly(1900, 560, 0.8, 10)
    b += dragonfly(1400, 1060, 1.1, -10)
    b += grass_tuft(200, 1320, 1.3, '#b5a04a')
    b += grass_tuft(1800, 1330, 1.2, '#b5a04a')
    b += ridge(128, 1320, 30, 6, '#cfb277', base=BH + 50)
    return defs, b


def sack(x, y, s=1.0):
    o = rect(x - 110 * s, y - 130 * s, 220 * s, 130 * s, '#dcc48a', rx=28 * s)
    for k in range(1, 5):
        o += line(x - 100 * s, y - 130 * s + k * 26 * s, x + 100 * s, y - 130 * s + k * 26 * s, stroke='#b59a52', stroke_width=2.5 * s)
    for k in range(-3, 4):
        o += line(x + k * 30 * s, y - 122 * s, x + k * 30 * s, y - 8 * s, stroke='#b59a52', stroke_width=2 * s)
    o += rect(x - 116 * s, y - 88 * s, 232 * s, 12 * s, '#8b6a3a', rx=4 * s)
    o += rect(x - 116 * s, y - 40 * s, 232 * s, 12 * s, '#8b6a3a', rx=4 * s)
    return o


def bg_storehouse():
    defs = lin('wall', [(0, '#7e5a37'), (1, '#9a7146')]) + lin('floor', [(0, '#8a7350'), (1, '#a08760')])
    b = flat('rect', x=0, y=0, width=BW, height=BH, fill='url(#wall)')
    for i in range(0, 26):
        b += line(i * 96, 0, i * 96, 900, stroke='#5c3f22', stroke_width=5)
    b += rect(-10, 90, BW + 20, 40, WOOD_D)
    b += rect(-10, 860, BW + 20, 40, WOOD_D)
    b += flat('rect', x=0, y=900, width=BW, height=BH - 900, fill='url(#floor)')
    b += line(0, 900, BW, 900, stroke=OUT, stroke_width=4)
    # light shaft
    b += flat('path', d=D('M', 1900, 130, 'L', 2400, 130, 'L', 2400, 1350, 'L', 1400, 1350, 'Z'), fill='#ffe9a8', opacity=0.12)
    # door (right) ajar
    b += rect(1880, 240, 440, 660, '#3d2a16')
    b += rect(1900, 260, 200, 640, WOOD_L)
    for k in range(1, 4):
        b += line(1900 + k * 50, 260, 1900 + k * 50, 900, stroke=WOOD_D, stroke_width=3)
    b += rect(1890, 380, 220, 22, WOOD_D)
    b += rect(1890, 760, 220, 22, WOOD_D)
    # padlock
    b += rect(2070, 560, 70, 90, '#c99a3a', rx=14)
    b += path(D('M', 2085, 560, 'L', 2085, 520, 'Q', 2085, 490, 2105, 490, 'Q', 2125, 490, 2125, 520, 'L', 2125, 560), stroke=OUT, stroke_width=16, stroke_linecap='round')
    b += path(D('M', 2085, 560, 'L', 2085, 520, 'Q', 2085, 490, 2105, 490, 'Q', 2125, 490, 2125, 520, 'L', 2125, 560), stroke='#d9b04a', stroke_width=9, stroke_linecap='round')
    b += flat('circle', cx=2105, cy=600, r=8, fill=OUT)
    # stacked sacks
    for row, (y, xs) in enumerate(((1330, (260, 520, 780, 1040, 1300, 1560)), (1200, (390, 650, 910, 1170, 1430)), (1070, (520, 780, 1040, 1300)), (940, (650, 910, 1170)))):
        for x in xs:
            b += sack(x, y, 1.0)
    # rope coil & scoop
    b += ellipse(2150, 1250, 120, 50, '#c9a25a')
    b += ellipse(2150, 1250, 60, 24, '#8b6a3a', stroke_width=3)
    b += ellipse(2150, 1225, 110, 44, '#d9b46c')
    b += ellipse(2150, 1225, 55, 20, '#8b6a3a', stroke_width=3)
    b += tube([(1950, 1300), (2060, 1160)], 10, WOOD)
    b += ellipse(2080, 1140, 40, 22, '#c9a25a', transform='rotate(-40 2080 1140)')
    return defs, b


def bg_park_modern():
    defs = lin('sky', [(0, '#7fbde8'), (0.5, '#c7e1f4'), (1, '#fbe3c4')]) + BLUR
    b = sky_rect('sky')
    b += cloud(300, 180, 1.0)
    b += cloud(1500, 120, 0.8)
    b += flat('circle', cx=2050, cy=330, r=150, fill='#ffd977', opacity=0.35)
    b += circle(2050, 330, 80, '#ffe28a', stroke='#f2c04a', stroke_width=3)
    b += ridge(131, 620, 130, 10, '#aebfd0')
    for x, w, h in ((80, 240, 420), (330, 200, 520), (1050, 260, 380), (1320, 220, 480), (1560, 240, 360), (2150, 230, 500), (2390, 180, 400)):
        b += apartment(x, 760, w, h)
    b += flat('rect', x=0, y=760, width=BW, height=BH - 760, fill='#7fb35c')
    b += path(D('M', -20, 900, 'Q', 700, 860, 1300, 930, 'Q', 1900, 1000, 2420, 940, 'L', 2420, 1090, 'Q', 1900, 1130, 1300, 1080, 'Q', 700, 1030, -20, 1060, 'Z'), '#cfc8bd', stroke='#9e968a', stroke_width=4)
    b += bush_tree(400, 900, 1.3, '#f0c530', '#f8e07a', seed=132)
    b += bush_tree(1900, 890, 1.4, '#f0c530', '#f8e07a', seed=133)
    b += bush_tree(1150, 820, 0.8, '#6aa554', '#a9d17e')
    # bench
    bx, by = 1450, 1250
    for px in (bx - 170, bx + 170):
        b += rect(px - 10, by - 110, 20, 110, '#4a4f58', rx=4)
        b += rect(px - 14, by - 170, 28, 60, '#4a4f58', rx=4)
    for k in range(3):
        b += rect(bx - 220, by - 118 + k * 22, 440, 16, '#b8763d', rx=6)
    for k in range(2):
        b += rect(bx - 220, by - 175 + k * 22, 440, 16, '#b8763d', rx=6)
    # street lamp
    b += rect(700, 830, 22, 460, '#4a4f58', rx=6)
    b += rect(680, 1280, 62, 30, '#4a4f58', rx=8)
    b += path(D('M', 711, 830, 'Q', 711, 760, 780, 760, 'L', 800, 760), stroke='#4a4f58', stroke_width=16, stroke_linecap='round')
    b += rect(780, 740, 90, 60, '#fff2c4', rx=10, stroke='#4a4f58', stroke_width=5)
    r = Rng(134)
    for _ in range(80):
        x, y = r.u(0, BW), r.u(1100, 1350)
        b += ellipse(x, y, 14, 8, '#f0c530', stroke_width=2, transform=f'rotate({r.u(-60, 60)} {x} {y})')
    for x, y in ((150, 1200), (2300, 1180), (1000, 1320)):
        b += grass_tuft(x, y, 1.4, '#4f8a3f')
    for x, y in ((250, 1300), (2200, 1300), (1050, 1150)):
        b += flower(x, y, 1.4, '#f2a4b8')
    return defs, b


def bg_title_card():
    defs = rad('paper', [(0, '#f8f0da'), (1, '#e9d8b2')], 0.5, 0.5, 0.75)
    b = flat('rect', x=0, y=0, width=BW, height=BH, fill='url(#paper)')
    r = Rng(141)
    for _ in range(400):
        x, y = r.u(0, BW), r.u(0, BH)
        b += line(x, y, x + r.u(-40, 40), y + r.u(-12, 12), stroke='#c9b48a', stroke_width=r.u(1, 2.5), opacity=r.u(0.15, 0.4))
    # ink brush edges
    strokes = [
        [(0, 60), (500, 40), (1000, 70), (1500, 35), (2000, 60), (2400, 30)],
        [(0, 1300), (500, 1320), (1000, 1290), (1500, 1325), (2000, 1295), (2400, 1320)],
        [(50, 0), (30, 400), (60, 800), (30, 1350)],
        [(2350, 0), (2370, 450), (2340, 900), (2370, 1350)],
    ]
    for i, sk in enumerate(strokes):
        for w, op in ((70, 0.10), (40, 0.14), (16, 0.2)):
            b += el('path', d=smooth(sk), fill='none', stroke='#2b2320', stroke_width=w, stroke_linecap='round', opacity=op)
    # plum branches top-left and bottom-right
    b += plum(160, 420, 1.0, '#f2a3b6', seed=142)
    b += f'<g transform="rotate(180 1200 675)">' + plum(160, 420, 1.0, '#f2a3b6', seed=143) + '</g>'
    # small red stamp bottom right (geometric, no text)
    b += rect(2170, 1120, 110, 110, '#c84a3a', rx=6, stroke='#8e2f24', stroke_width=4)
    b += rect(2190, 1140, 70, 70, 'none', stroke='#f6e2c8', stroke_width=5)
    b += line(2225, 1140, 2225, 1210, stroke='#f6e2c8', stroke_width=5)
    b += line(2190, 1175, 2260, 1175, stroke='#f6e2c8', stroke_width=5)
    return defs, b


BACKGROUNDS = {
    'village_spring_day': bg_village_spring_day,
    'village_night': bg_village_night,
    'yangban_yard': bg_yangban_yard,
    'yangban_room': bg_yangban_room,
    'servant_room': bg_servant_room,
    'market': bg_market,
    'mountain_path': bg_mountain_path,
    'rice_field_summer': bg_rice_field_summer,
    'river_bank': bg_river_bank,
    'gwana_yard': bg_gwana_yard,
    'rain_road': bg_rain_road,
    'village_winter': bg_village_winter,
    'hanyang_street': bg_hanyang_street,
    'autumn_yard': bg_autumn_yard,
    'storehouse': bg_storehouse,
    'park_modern': bg_park_modern,
    'title_card': bg_title_card,
}


# ---------------------------------------------------------------- characters

EOSA_FACE = dict(beard='medium', beard_color='#4a3b30', eyes='calm', brows='firm', mouth='straight_soft')

CHARACTERS = {
    'manbok': dict(hair='topknot_band', hair_color='#2a1d14', outfit='jambaengi', top='#dcc7a0', bottom='#8c6a45',
                   tie='#8c6a45', shoes='straw', eyes='big', brows='gentle', mouth='smile_big', blush=True, build='stout'),
    'sunok': dict(hair='jjok', hair_color='#2a1d14', outfit='chima', top='#bfe3d6', bottom='#f5f1e8', tie='#c4463d',
                  shoes='kkotsin', eyes='calm', brows='thin', mouth='smile_small', blush=True, female=True),
    'dolsoe': dict(scale=0.65, head_scale=1.12, hair='daenggi', hair_color='#2a1d14', outfit='pants', top='#d9cba8',
                   bottom='#7f6a4c', tie='#7f6a4c', shoes='straw', eyes='big', brows='gentle', mouth='smile_big', blush=True),
    'mother': dict(hair='jjok', hair_color='#ebe6dc', outfit='chima', top='#f7f2e8', bottom='#f3eee2', tie='#e8dfcf',
                   shoes='gomusin', eyes='calm', brows='thin', mouth='smile_small', wrinkles=True, head_dy=22, female=True),
    'kim_jinsa': dict(hat='gat', hair='cap', hair_color='#2a1d14', outfit='dopo', top='#cbdbd2', tie='#6f8f86', belly=34,
                      beard='long', beard_color='#d0cbc1', brows='stern', mouth='straight', eyes='calm', shoes='black'),
    'yongchil': dict(hat='tanggeon', hair='cap', hair_color='#2a1d14', outfit='pants', top='#5e3f29', bottom='#4a3120',
                     tie='#3a2618', beard='thin', eyes='narrow', brows='sly', mouth='sly', shoes='black'),
    'eosa_ragged': dict(hat='satgat', hair='cap', hair_color='#2a1d14', outfit='dopo', top='#a09b93', tie='#6b665f',
                        patches=True, bojim='small', shoes='straw', **EOSA_FACE),
    'eosa_official': dict(hat='samo', hair='cap', hair_color='#2a1d14', outfit='gwanbok', top='#b8323a', belt='#2e3f6f',
                          shoes='black', **EOSA_FACE),
    'satto': dict(hat='samo', hair='cap', hair_color='#2a1d14', outfit='gwanbok', top='#2e3f6f', belt='#b8323a', belly=44,
                  beard='moustache', beard_color='#2a1d14', eyes='small', brows='stern', mouth='pout', shoes='black', build='fat'),
    'villager_m': dict(hat='paeraengi', hair='cap', hair_color='#2a1d14', outfit='pants', top='#a9a69e', bottom='#8d8a82',
                       tie='#6f6c66', shoes='straw', eyes='calm', brows='gentle', mouth='smile_small'),
    'villager_f': dict(hat='scarf', hair='jjok', hair_color='#2a1d14', outfit='chima', top='#ece0c4', bottom='#2e3f6f',
                       tie='#7a3b3b', shoes='straw', female=True, eyes='calm', brows='thin', mouth='smile_small', blush=True),
    'merchant': dict(hat='paeraengi', hair='cap', hair_color='#2a1d14', outfit='pants', top='#8d5c3a', bottom='#6e5a45',
                     tie='#5a3a22', bojim='big', shoes='straw', eyes='calm', brows='gentle', mouth='smile_big', leg_wraps=True),
    'grandpa_modern': dict(hair='modern_gray', hair_color='#b9b9b9', outfit='modern_vest', top='#9fc0e0', vest='#6b6f7a',
                           bottom='#3f4a5a', glasses=True, wrinkles=True, eyes='calm', brows='gentle', mouth='smile_small', shoes='black'),
    'girl_modern': dict(scale=0.6, head_scale=1.12, hair='ponytail', hair_color='#3a2618', outfit='hoodie', top='#f28c8c',
                        bottom='#4a6fa5', shoes='sneaker', eyes='big', brows='gentle', mouth='smile_big', blush=True),
}

CHAR_POSES = {name: ['stand', 'sit'] for name in CHARACTERS}
CHAR_POSES['manbok'].append('walk')
CHAR_POSES['sunok'].append('walk')

STATES = [('closed', 'open'), ('open', 'open'), ('closed', 'closed'), ('open', 'closed')]  # (mouth, eyes)


def layout(pose):
    if pose == 'sit':
        return dict(H=800, head_cy=215, neck_top=305, sh_y=365, lap_top=560, lap_bottom=796, hem=580)
    return dict(H=1000, head_cy=245, neck_top=335, sh_y=395, hip=610, hem=615, ankle=945, shoe=976)


class Char:
    def __init__(self, name, spec, pose, mouth, eyes):
        self.name, self.s, self.pose, self.mouth, self.eyes = name, spec, pose, mouth, eyes
        self.L = layout(pose)
        self.hs = spec.get('head_scale', 1.0)
        self.cx = 300
        self.cy = self.L['head_cy'] + spec.get('head_dy', 0)
        self.rx = 104 * self.hs
        self.ry = 114 * self.hs
        self.sc = spec.get('scale', 1.0)
        self.skin = spec.get('skin', SKIN)
        self.wide = spec.get('build') in ('stout', 'fat')
        self.bx = 14 if self.wide else 0  # extra torso half-width

    # ---- metadata
    def eye_y(self):
        return self.cy - 12 * self.hs

    def mouth_y(self):
        return self.cy + 58 * self.hs

    # ---- shoes
    def shoe(self, x, y, flip=False):
        k = self.s.get('shoes', 'straw')
        if k == 'straw':
            o = ellipse(x, y, 50, 22, '#d9c37e')
            o += line(x - 30, y - 10, x + 30, y - 10, stroke=THATCH_D, stroke_width=3)
            o += line(x - 20, y + 2, x + 20, y + 2, stroke=THATCH_D, stroke_width=3)
            return o
        if k == 'black':
            return ellipse(x, y, 50, 22, '#2b2b2f') + flat('ellipse', cx=x - 12, cy=y - 8, rx=16, ry=6, fill='#55555c')
        if k == 'kkotsin':
            return ellipse(x, y, 46, 21, '#f4f1ea') + flat('circle', cx=x + (28 if not flip else -28), cy=y - 4, r=8, fill='#c4463d')
        if k == 'gomusin':
            return ellipse(x, y, 46, 21, '#f4f1ea')
        if k == 'sneaker':
            o = rect(x - 50, y - 24, 100, 46, '#f7f7f7', rx=20)
            o += flat('rect', x=x - 44, y=y + 4, width=88, height=12, rx=6, fill='#4a6fa5')
            o += flat('circle', cx=x + 14, cy=y - 10, r=6, fill='#f28c8c')
            return o
        return ellipse(x, y, 50, 22, '#2b2b2f')

    # ---- legs (stand / walk)
    def leg_points(self):
        L = self.L
        if self.pose == 'walk':
            return [((268, L['hip']), (205, L['ankle'] - 6)), ((332, L['hip']), (400, L['ankle']))]
        return [((262, L['hip']), (258, L['ankle'])), ((338, L['hip']), (342, L['ankle']))]

    def legs(self, color, short=False, wraps=False):
        L = self.L
        o = ''
        legs = self.leg_points()
        hipy = L['hip']
        if short:
            for (hx, hy), (fx, fy) in legs:
                o += tube([(hx, hy), (fx, fy)], 66, self.skin)
            for (hx, hy), (fx, fy) in legs:
                o += self.shoe(fx, L['shoe'], flip=(fx < 300))
            hip = el('rect', x=210 - self.bx, y=hipy - 30, width=180 + 2 * self.bx, height=90, rx=30, fill=OUT)
            fill = el('rect', x=214 - self.bx, y=hipy - 26, width=172 + 2 * self.bx, height=82, rx=26, fill=color)
            oo = ff = ''
            for (hx, hy), (fx, fy) in legs:
                kx, ky = hx + (fx - hx) * 0.5, hy + (fy - hy) * 0.5
                oo += el('path', d=D('M', hx, hy, 'L', kx, ky), fill='none', stroke=OUT, stroke_width=112, stroke_linecap='round')
                ff += el('path', d=D('M', hx, hy, 'L', kx, ky), fill='none', stroke=color, stroke_width=104, stroke_linecap='round')
            o += hip + oo + fill + ff
            for (hx, hy), (fx, fy) in legs:
                kx, ky = hx + (fx - hx) * 0.5, hy + (fy - hy) * 0.5
                o += line(kx - 40, ky + 30, kx + 40, ky + 30, stroke=OUT, stroke_width=4, opacity=0.5)
            return o
        oo = el('rect', x=210 - self.bx, y=hipy - 30, width=180 + 2 * self.bx, height=90, rx=30, fill=OUT)
        ff = el('rect', x=214 - self.bx, y=hipy - 26, width=172 + 2 * self.bx, height=82, rx=26, fill=color)
        for (hx, hy), (fx, fy) in legs:
            oo += el('path', d=D('M', hx, hy, 'L', fx, fy), fill='none', stroke=OUT, stroke_width=104, stroke_linecap='round')
            ff += el('path', d=D('M', hx, hy, 'L', fx, fy), fill='none', stroke=color, stroke_width=96, stroke_linecap='round')
        o += oo + ff
        if wraps:
            for (hx, hy), (fx, fy) in legs:
                for k in range(3):
                    t = 0.72 + k * 0.09
                    px, py = hx + (fx - hx) * t, hy + (fy - hy) * t
                    o += line(px - 44, py, px + 44, py, stroke='#e8dcc0', stroke_width=14)
                    o += line(px - 44, py, px + 44, py, stroke=OUT, stroke_width=2, opacity=0.5)
        for (hx, hy), (fx, fy) in legs:
            o += self.shoe(fx, L['shoe'], flip=(fx < 300))
        return o

    # ---- seated lap (pants/robe)
    def lap(self, color, robe=False):
        top, bot = self.L['lap_top'], self.L['lap_bottom']
        bx = self.bx
        if robe:
            d = D('M', 150 - bx, top - 20, 'L', 450 + bx, top - 20, 'Q', 540, top + 60, 545, top + 150,
                  'L', 555, bot - 30, 'Q', 555, bot, 520, bot, 'L', 80, bot, 'Q', 45, bot, 45, bot - 30,
                  'L', 55, top + 150, 'Q', 60, top + 60, 150 - bx, top - 20, 'Z')
            o = path(d, color)
            o += el('path', d=D('M', 120, top + 120, 'Q', 300, top + 40, 480, top + 120), fill='none', stroke=OUT, stroke_width=4, opacity=0.35)
            return o
        d = D('M', 165 - bx, top, 'L', 435 + bx, top, 'Q', 512, top + 40, 508, top + 130,
              'Q', 508, bot - 20, 470, bot, 'L', 130, bot, 'Q', 92, bot - 20, 92, top + 130,
              'Q', 88, top + 40, 165 - bx, top, 'Z')
        o = path(d, color)
        for sx in (-1, 1):
            o += el('path', d=D('M', 300 + sx * 60, bot - 8, 'Q', 300 + sx * 150, top + 150, 300 + sx * 95, top + 25), fill='none', stroke=OUT, stroke_width=4, opacity=0.45)
        return o

    def lap_feet(self):
        bot = self.L['lap_bottom']
        return self.shoe(250, bot - 22, flip=True) + self.shoe(350, bot - 22)

    # ---- torso pieces
    def neck(self):
        L = self.L
        return rect(272, L['neck_top'], 56, L['sh_y'] - L['neck_top'] + 34, self.skin, rx=10)

    def jeogori(self, color, hem, tie, female=False):
        L = self.L
        sy = L['sh_y']
        bx = self.bx
        d = D('M', 300, sy - 18, 'L', 412 + bx, sy, 'Q', 442 + bx, sy + 4, 448 + bx, sy + 36,
              'L', 456 + bx, hem, 'L', 144 - bx, hem, 'L', 152 - bx, sy + 36, 'Q', 158 - bx, sy + 4, 188 - bx, sy, 'Z')
        o = path(d, color)
        vb = sy + 64
        o += flat('polygon', points=f'{258},{sy - 6} {342},{sy - 6} {300},{vb + 6}', fill=self.skin)
        for x0 in (246, 354):
            o += line(x0, sy - 12, 300, vb, stroke=OUT, stroke_width=24)
        for x0 in (246, 354):
            o += line(x0, sy - 12, 300, vb, stroke='#fbf8f0', stroke_width=16)
        o += line(246, sy - 12, 300, vb, stroke=OUT, stroke_width=4)
        ln = 120 if female else 90
        o += el('path', d=D('M', 300, vb, 'q', -14, ln * 0.5, -36, ln), fill='none', stroke=OUT, stroke_width=20, stroke_linecap='round')
        o += el('path', d=D('M', 300, vb, 'q', 16, ln * 0.5, 8, ln + 10), fill='none', stroke=OUT, stroke_width=20, stroke_linecap='round')
        o += el('path', d=D('M', 300, vb, 'q', -14, ln * 0.5, -36, ln), fill='none', stroke=tie, stroke_width=13, stroke_linecap='round')
        o += el('path', d=D('M', 300, vb, 'q', 16, ln * 0.5, 8, ln + 10), fill='none', stroke=tie, stroke_width=13, stroke_linecap='round')
        o += circle(300, vb, 12, tie)
        return o

    def robe_body(self, color, belly=0, bottom=None):
        L = self.L
        sy = L['sh_y']
        bx = self.bx
        if self.pose == 'sit':
            return self.lap(color, robe=True) + self.jeogori_like_top(color)
        bottom = bottom or 955
        d = D('M', 300, sy - 18, 'L', 414 + bx, sy, 'Q', 446 + bx, sy + 4, 452 + bx, sy + 44,
              'Q', 480 + belly, sy + 240, 486 + belly * 0.4, sy + 420, 'Q', 492, bottom - 120, 484, bottom,
              'L', 116, bottom, 'Q', 108, bottom - 120, 114 - belly * 0.4, sy + 420, 'Q', 120 - belly, sy + 240, 148 - bx, sy + 44,
              'Q', 154 - bx, sy + 4, 186 - bx, sy, 'Z')
        return path(d, color)

    def jeogori_like_top(self, color):
        L = self.L
        sy = L['sh_y']
        bx = self.bx
        d = D('M', 300, sy - 18, 'L', 414 + bx, sy, 'Q', 446 + bx, sy + 4, 452 + bx, sy + 44,
              'L', 470 + bx, L['lap_top'] + 10, 'L', 130 - bx, L['lap_top'] + 10, 'L', 148 - bx, sy + 44,
              'Q', 154 - bx, sy + 4, 186 - bx, sy, 'Z')
        return path(d, color)

    def v_collar(self, tie, depth=64, cord=True):
        sy = self.L['sh_y']
        vb = sy + depth
        o = flat('polygon', points=f'{258},{sy - 6} {342},{sy - 6} {300},{vb + 6}', fill=self.skin)
        for x0 in (246, 354):
            o += line(x0, sy - 12, 300, vb, stroke=OUT, stroke_width=24)
        for x0 in (246, 354):
            o += line(x0, sy - 12, 300, vb, stroke='#fbf8f0', stroke_width=16)
        o += line(246, sy - 12, 300, vb, stroke=OUT, stroke_width=4)
        if cord:
            o += el('path', d=D('M', 300, vb + 4, 'q', -20, 60, -44, 130), fill='none', stroke=OUT, stroke_width=14, stroke_linecap='round')
            o += el('path', d=D('M', 300, vb + 4, 'q', -20, 60, -44, 130), fill='none', stroke=tie, stroke_width=8, stroke_linecap='round')
        return o

    def round_collar(self):
        sy = self.L['sh_y']
        o = path(D('M', 248, sy - 8, 'Q', 300, sy + 52, 352, sy - 8), self.skin, stroke_width=0)
        o += el('path', d=D('M', 244, sy - 14, 'Q', 300, sy + 60, 356, sy - 14), fill='none', stroke=OUT, stroke_width=22, stroke_linecap='round')
        o += el('path', d=D('M', 244, sy - 14, 'Q', 300, sy + 60, 356, sy - 14), fill='none', stroke='#f6f0e2', stroke_width=14, stroke_linecap='round')
        return o

    def belt(self, y, color, wide=True):
        bx = self.bx
        belly = self.s.get('belly', 0)
        o = rect(128 - bx - belly * 0.6, y - 16, 344 + 2 * bx + belly * 1.2, 32, color, rx=8)
        if wide:
            for x in (200, 300, 400):
                o += rect(x - 16, y - 11, 32, 22, '#e5c25a', rx=4, stroke_width=2.5)
        return o

    def hyungbae(self, y):
        o = rect(240, y, 120, 110, '#f4e6c0', rx=6)
        o += el('path', d=D('M', 262, y + 78, 'q', 20, -50, 60, -46, 'q', 22, 4, 26, 24), fill='none', stroke='#3b4a7a', stroke_width=7, stroke_linecap='round')
        o += el('path', d=D('M', 262, y + 78, 'q', 30, 14, 62, -4), fill='none', stroke='#3b4a7a', stroke_width=7, stroke_linecap='round')
        o += flat('circle', cx=336, cy=y + 32, r=7, fill='#c84a3a')
        for k in range(3):
            o += el('path', d=D('M', 252 + k * 36, y + 96, 'q', 10, -12, 24, 0), fill='none', stroke='#8f7a55', stroke_width=4, stroke_linecap='round')
        return o

    def chima(self, color):
        L = self.L
        sy = L['sh_y']
        top = sy + 112
        if self.pose == 'sit':
            bot = L['lap_bottom']
            d = D('M', 180, top, 'L', 420, top, 'Q', 460, top + 20, 500, top + 90, 'Q', 560, bot - 80, 560, bot - 20,
                  'Q', 560, bot, 530, bot, 'L', 70, bot, 'Q', 40, bot, 40, bot - 20, 'Q', 40, bot - 80, 100, top + 90,
                  'Q', 140, top + 20, 180, top, 'Z')
            o = path(d, color)
            for k in range(-2, 3):
                o += el('path', d=D('M', 300 + k * 40, top + 30, 'Q', 300 + k * 90, bot - 120, 300 + k * 110, bot - 8), fill='none', stroke=OUT, stroke_width=3, opacity=0.3)
            return o
        bot = 986
        if self.pose == 'walk':
            d = D('M', 212, top, 'L', 388, top, 'Q', 402, top + 8, 410, top + 70, 'L', 486, bot - 26, 'Q', 380, bot + 8, 300, bot - 6,
                  'Q', 200, bot + 6, 122, bot - 34, 'L', 190, top + 70, 'Q', 198, top + 8, 212, top, 'Z')
        else:
            d = D('M', 212, top, 'L', 388, top, 'Q', 402, top + 8, 410, top + 70, 'L', 474, bot - 12, 'Q', 300, bot + 12, 126, bot - 12,
                  'L', 190, top + 70, 'Q', 198, top + 8, 212, top, 'Z')
        o = path(d, color)
        for k in range(-2, 3):
            o += el('path', d=D('M', 300 + k * 36, top + 40, 'Q', 300 + k * 52, top + 300, 300 + k * 72, bot - 20), fill='none', stroke=OUT, stroke_width=3, opacity=0.3)
        return o

    # ---- arms
    def arm_points(self):
        sy = self.L['sh_y']
        bx = self.bx
        if self.pose == 'walk':
            return [[(192 - bx, sy + 16), (150 - bx, sy + 110), (138 - bx, sy + 176)],
                    [(408 + bx, sy + 16), (448 + bx, sy + 116), (446 + bx, sy + 212)]]
        if self.pose == 'sit':
            return [[(192 - bx, sy + 16), (168 - bx, sy + 120), (200, sy + 250)],
                    [(408 + bx, sy + 16), (432 + bx, sy + 120), (400, sy + 250)]]
        return [[(192 - bx, sy + 16), (166 - bx, sy + 120), (170 - bx, sy + 232)],
                [(408 + bx, sy + 16), (434 + bx, sy + 120), (430 + bx, sy + 232)]]

    def arms(self, color, wide=False, sleeve_cuff=None):
        o = ''
        w = 132 if wide else 84
        for pts in self.arm_points():
            o += tube(pts, w, color)
            hx, hy = pts[-1]
            if wide:
                o += circle(hx, hy + 22, 27, self.skin)
            else:
                if sleeve_cuff:
                    o += circle(hx, hy, 46, sleeve_cuff)
                o += circle(hx, hy + 22, 27, self.skin)
        return o

    # ---- head & face
    def head(self):
        cx, cy, rx, ry, hs = self.cx, self.cy, self.rx, self.ry, self.hs
        s = self.s
        o = ellipse(cx - rx + 2, cy + 14 * hs, 20 * hs, 24 * hs, self.skin)
        o += ellipse(cx + rx - 2, cy + 14 * hs, 20 * hs, 24 * hs, self.skin)
        o += ellipse(cx, cy, rx, ry, self.skin)
        if s.get('blush'):
            o += flat('circle', cx=cx - 64 * hs, cy=cy + 36 * hs, r=22 * hs, fill='#f39aa0', opacity=0.45)
            o += flat('circle', cx=cx + 64 * hs, cy=cy + 36 * hs, r=22 * hs, fill='#f39aa0', opacity=0.45)
        if s.get('wrinkles'):
            for sx in (-1, 1):
                ex = cx + sx * 44 * hs
                o += el('path', d=D('M', ex + sx * 30 * hs, cy - 4 * hs, 'l', sx * 14 * hs, -6 * hs), fill='none', stroke=OUT, stroke_width=3, opacity=0.5, stroke_linecap='round')
                o += el('path', d=D('M', ex + sx * 30 * hs, cy + 6 * hs, 'l', sx * 14 * hs, 6 * hs), fill='none', stroke=OUT, stroke_width=3, opacity=0.5, stroke_linecap='round')
                o += el('path', d=D('M', cx + sx * 40 * hs, cy + 40 * hs, 'q', sx * 10 * hs, 20 * hs, sx * 4 * hs, 40 * hs), fill='none', stroke=OUT, stroke_width=3, opacity=0.4, stroke_linecap='round')
            o += el('path', d=D('M', cx - 40 * hs, cy - 72 * hs, 'q', 40 * hs, -12 * hs, 80 * hs, 0), fill='none', stroke=OUT, stroke_width=3, opacity=0.4, stroke_linecap='round')
        # nose
        o += el('path', d=D('M', cx + 2 * hs, cy + 6 * hs, 'q', 16 * hs, 22 * hs, -4 * hs, 32 * hs), fill='none', stroke=OUT, stroke_width=3.5, stroke_linecap='round')
        # eyes
        ey = self.eye_y()
        kind = s.get('eyes', 'calm')
        for sx in (-1, 1):
            ex = cx + sx * 44 * hs
            if self.eyes == 'open':
                if kind == 'big':
                    o += ellipse(ex, ey, 21 * hs, 24 * hs, '#ffffff', stroke_width=3.5)
                    o += flat('circle', cx=ex + sx * 2 * hs, cy=ey + 3 * hs, r=13 * hs, fill='#2a1d14')
                    o += flat('circle', cx=ex - 5 * hs, cy=ey - 6 * hs, r=5 * hs, fill='#ffffff')
                elif kind == 'narrow':
                    o += ellipse(ex, ey, 25 * hs, 9 * hs, '#ffffff', stroke_width=3.5)
                    o += flat('ellipse', cx=ex + sx * 4 * hs, cy=ey + 1 * hs, rx=9 * hs, ry=7 * hs, fill='#2a1d14')
                    o += flat('circle', cx=ex - 2 * hs, cy=ey - 2 * hs, r=2.5 * hs, fill='#ffffff')
                elif kind == 'small':
                    o += ellipse(ex, ey, 16 * hs, 16 * hs, '#ffffff', stroke_width=3.5)
                    o += flat('circle', cx=ex + sx * 2 * hs, cy=ey + 2 * hs, r=9 * hs, fill='#2a1d14')
                    o += flat('circle', cx=ex - 4 * hs, cy=ey - 4 * hs, r=3.5 * hs, fill='#ffffff')
                else:  # calm
                    o += ellipse(ex, ey, 19 * hs, 19 * hs, '#ffffff', stroke_width=3.5)
                    o += flat('circle', cx=ex + sx * 2 * hs, cy=ey + 2 * hs, r=11 * hs, fill='#2a1d14')
                    o += flat('circle', cx=ex - 4 * hs, cy=ey - 5 * hs, r=4 * hs, fill='#ffffff')
            else:
                depth = 8 if kind == 'narrow' else 16
                o += el('path', d=D('M', ex - 21 * hs, ey, 'q', 21 * hs, depth * hs, 42 * hs, 0), fill='none', stroke=OUT, stroke_width=5, stroke_linecap='round')
        # brows
        by = ey - 40 * hs
        brow = s.get('brows', 'gentle')
        for sx in (-1, 1):
            ex = cx + sx * 44 * hs
            if brow == 'stern':
                d = D('M', ex - sx * 26 * hs, by + 2 * hs, 'L', ex + sx * 24 * hs, by - 12 * hs)
                o += el('path', d=d, fill='none', stroke=OUT, stroke_width=8, stroke_linecap='round')
            elif brow == 'sly':
                d = D('M', ex - sx * 24 * hs, by + 8 * hs, 'q', sx * 20 * hs, -22 * hs, sx * 46 * hs, -10 * hs)
                o += el('path', d=d, fill='none', stroke=OUT, stroke_width=6, stroke_linecap='round')
            elif brow == 'firm':
                d = D('M', ex - sx * 26 * hs, by + 4 * hs, 'q', sx * 26 * hs, -14 * hs, sx * 50 * hs, -2 * hs)
                o += el('path', d=d, fill='none', stroke=OUT, stroke_width=7, stroke_linecap='round')
            elif brow == 'thin':
                d = D('M', ex - 24 * hs, by + 4 * hs, 'q', 24 * hs, -14 * hs, 48 * hs, 0)
                o += el('path', d=d, fill='none', stroke=OUT, stroke_width=4, stroke_linecap='round')
            else:
                d = D('M', ex - 24 * hs, by + 4 * hs, 'q', 24 * hs, -16 * hs, 48 * hs, 0)
                o += el('path', d=d, fill='none', stroke=OUT, stroke_width=6, stroke_linecap='round')
        if s.get('glasses'):
            for sx in (-1, 1):
                o += circle(cx + sx * 44 * hs, ey, 30 * hs, 'none', stroke='#3a3a3a', stroke_width=5)
            o += line(cx - 14 * hs, ey - 2, cx + 14 * hs, ey - 2, stroke='#3a3a3a', stroke_width=5)
            o += line(cx - 74 * hs, ey - 4, cx - rx - 8, ey - 8, stroke='#3a3a3a', stroke_width=5)
            o += line(cx + 74 * hs, ey - 4, cx + rx + 8, ey - 8, stroke='#3a3a3a', stroke_width=5)
        # mouth
        o += self.mouth_shape()
        return o

    def mouth_shape(self):
        cx, hs = self.cx, self.hs
        my = self.mouth_y()
        kind = self.s.get('mouth', 'smile_small')
        if self.mouth == 'open':
            w = {'smile_big': 34, 'smile_small': 28, 'straight': 26, 'straight_soft': 27, 'sly': 28, 'pout': 24}[kind] * hs
            h = 46 * hs if self.s.get('beard') in (None, 'thin', 'moustache') else 38 * hs
            if self.s.get('beard') == 'moustache':
                h = 40 * hs
            d = D('M', cx - w, my - 6 * hs, 'Q', cx, my + 2 * hs, cx + w, my - 6 * hs,
                  'Q', cx + w * 0.85, my + h, cx, my + h, 'Q', cx - w * 0.85, my + h, cx - w, my - 6 * hs, 'Z')
            o = f'<clipPath id="mouthclip"><path d="{d}"/></clipPath>'
            o += path(d, '#7a2a2c', stroke_width=4)
            o += flat('ellipse', cx=cx, cy=my + h * 0.85, rx=w * 0.6, ry=h * 0.3, fill='#e06a72', clip_path='url(#mouthclip)')
            o += flat('rect', x=cx - w, y=my - 8 * hs, width=2 * w, height=12 * hs, fill='#ffffff', clip_path='url(#mouthclip)')
            o += path(d, 'none', stroke_width=4)
            return o
        if kind == 'smile_big':
            d = D('M', cx - 32 * hs, my - 8 * hs, 'q', 32 * hs, 34 * hs, 64 * hs, 0)
            return el('path', d=d, fill='none', stroke=OUT, stroke_width=5.5, stroke_linecap='round')
        if kind == 'smile_small':
            d = D('M', cx - 26 * hs, my - 4 * hs, 'q', 26 * hs, 20 * hs, 52 * hs, 0)
            return el('path', d=d, fill='none', stroke=OUT, stroke_width=5, stroke_linecap='round')
        if kind == 'straight':
            d = D('M', cx - 26 * hs, my + 2 * hs, 'q', 26 * hs, 2 * hs, 52 * hs, 0)
            return el('path', d=d, fill='none', stroke=OUT, stroke_width=5.5, stroke_linecap='round')
        if kind == 'straight_soft':
            d = D('M', cx - 26 * hs, my, 'q', 26 * hs, 8 * hs, 52 * hs, 0)
            return el('path', d=d, fill='none', stroke=OUT, stroke_width=5, stroke_linecap='round')
        if kind == 'sly':
            d = D('M', cx - 28 * hs, my + 8 * hs, 'q', 30 * hs, 10 * hs, 58 * hs, -16 * hs)
            return el('path', d=d, fill='none', stroke=OUT, stroke_width=5, stroke_linecap='round')
        d = D('M', cx - 20 * hs, my + 6 * hs, 'q', 20 * hs, -12 * hs, 40 * hs, 0)  # pout
        return el('path', d=d, fill='none', stroke=OUT, stroke_width=5.5, stroke_linecap='round')

    # ---- hair
    def hair_cap(self):
        cx, cy, rx, ry, hs = self.cx, self.cy, self.rx, self.ry, self.hs
        style = self.s.get('hair', 'cap')
        color = self.s.get('hair_color', '#2a1d14')
        top = cy - ry - 8 * hs
        if style in ('jjok', 'daenggi'):
            d = D('M', cx - rx - 4, cy - 6 * hs, 'Q', cx - rx - 8, top, cx, top, 'Q', cx + rx + 8, top, cx + rx + 4, cy - 6 * hs,
                  'Q', cx + rx - 4, cy - 66 * hs, cx + 36 * hs, cy - 70 * hs, 'Q', cx + 8 * hs, cy - 68 * hs, cx, cy - 52 * hs,
                  'Q', cx - 8 * hs, cy - 68 * hs, cx - 36 * hs, cy - 70 * hs, 'Q', cx - rx + 4, cy - 66 * hs, cx - rx - 4, cy - 6 * hs, 'Z')
            o = path(d, color)
            o += line(cx, top + 4, cx, cy - 56 * hs, stroke='#8a7a6a' if color > '#a' else '#1a1a1a', stroke_width=2.5, opacity=0.6)
            return o
        if style == 'modern_gray':
            d = D('M', cx - rx - 4, cy - 10 * hs, 'Q', cx - rx - 8, top + 6, cx - 10 * hs, top + 4, 'Q', cx + rx + 6, top + 2, cx + rx + 4, cy - 14 * hs,
                  'Q', cx + rx - 8, cy - 70 * hs, cx + 50 * hs, cy - 78 * hs, 'Q', cx - 10 * hs, cy - 84 * hs, cx - 40 * hs, cy - 62 * hs,
                  'Q', cx - rx + 8, cy - 60 * hs, cx - rx - 4, cy - 10 * hs, 'Z')
            return path(d, color)
        if style == 'ponytail':
            d = D('M', cx - rx - 4, cy - 2 * hs, 'Q', cx - rx - 8, top, cx, top, 'Q', cx + rx + 8, top, cx + rx + 4, cy - 2 * hs,
                  'Q', cx + rx - 6, cy - 40 * hs, cx + 40 * hs, cy - 52 * hs, 'Q', cx + 10 * hs, cy - 40 * hs, cx - 20 * hs, cy - 56 * hs,
                  'Q', cx - 60 * hs, cy - 66 * hs, cx - rx - 4, cy - 2 * hs, 'Z')
            o = path(d, color)
            o += el('path', d=D('M', cx - rx - 6, cy - 20 * hs, 'Q', cx - 20 * hs, cy - ry - 30 * hs, cx + rx + 6, cy - 20 * hs), fill='none', stroke='#f28c8c', stroke_width=14, stroke_linecap='round')
            return o
        # cap: plain hair under a hat / topknot (flat hairline)
        d = D('M', cx - rx - 4, cy - 10 * hs, 'Q', cx - rx - 8, top, cx, top, 'Q', cx + rx + 8, top, cx + rx + 4, cy - 10 * hs,
              'Q', cx + rx - 6, cy - 70 * hs, cx, cy - 74 * hs, 'Q', cx - rx + 6, cy - 70 * hs, cx - rx - 4, cy - 10 * hs, 'Z')
        return path(d, color)

    def hair_back(self):
        """Elements drawn behind the head (bun, ponytail, hood)."""
        cx, cy, rx, ry, hs = self.cx, self.cy, self.rx, self.ry, self.hs
        style = self.s.get('hair')
        color = self.s.get('hair_color', '#2a1d14')
        o = ''
        if style == 'jjok' and not self.s.get('hat'):
            o += ellipse(cx + rx - 4, cy + 58 * hs, 36 * hs, 28 * hs, color)
            o += line(cx + rx - 40 * hs, cy + 48 * hs, cx + rx + 44 * hs, cy + 62 * hs, stroke='#d9a441', stroke_width=7)
        if style == 'ponytail':
            o += tube([(cx + 60 * hs, cy - ry + 10), (cx + rx + 40 * hs, cy + 20 * hs), (cx + rx + 20 * hs, cy + ry + 60 * hs)], 34 * hs, color)
            o += ellipse(cx + rx + 20 * hs, cy + ry + 62 * hs, 22 * hs, 18 * hs, color)
        if self.s.get('outfit') == 'hoodie':
            o += ellipse(cx, cy + ry - 10, 140 * hs, 100 * hs, self.s['top'])
        return o

    def hair_front(self):
        """Extras drawn over the hair cap (topknot, band) and braid over body."""
        cx, cy, rx, ry, hs = self.cx, self.cy, self.rx, self.ry, self.hs
        style = self.s.get('hair')
        color = self.s.get('hair_color', '#2a1d14')
        o = ''
        if style == 'topknot_band':
            o += ellipse(cx, cy - ry - 16 * hs, 24 * hs, 20 * hs, color)
            o += el('path', d=D('M', cx - rx - 4, cy - 34 * hs, 'Q', cx, cy - 88 * hs, cx + rx + 4, cy - 34 * hs), fill='none', stroke=OUT, stroke_width=38)
            o += el('path', d=D('M', cx - rx - 4, cy - 34 * hs, 'Q', cx, cy - 88 * hs, cx + rx + 4, cy - 34 * hs), fill='none', stroke='#f1e6cf', stroke_width=30)
            o += poly([(cx + rx - 2, cy - 44 * hs), (cx + rx + 44 * hs, cy - 70 * hs), (cx + rx + 34 * hs, cy - 30 * hs)], '#f1e6cf')
            o += poly([(cx + rx - 2, cy - 44 * hs), (cx + rx + 40 * hs, cy - 10 * hs), (cx + rx + 10 * hs, cy - 4 * hs)], '#f1e6cf')
        if style == 'daenggi':
            pts = [(cx + 70 * hs, cy + 60 * hs), (cx + 108 * hs, cy + ry + 60 * hs), (cx + 96 * hs, cy + ry + 200 * hs)]
            o += tube(pts, 30 * hs, color)
            for k in range(4):
                t = 0.35 + k * 0.17
                px = cx + 70 * hs + (96 * hs - 70 * hs + 20 * hs) * t
                py = cy + 60 * hs + (ry + 200 * hs - 60 * hs) * t
                o += el('path', d=D('M', px - 12 * hs, py - 8 * hs, 'l', 12 * hs, 10 * hs, 'l', 12 * hs, -10 * hs), fill='none', stroke='#6b5a4a', stroke_width=3, stroke_linecap='round')
            ex, eyy = cx + 96 * hs, cy + ry + 200 * hs
            o += poly([(ex, eyy), (ex - 22 * hs, eyy + 44 * hs), (ex + 26 * hs, eyy + 40 * hs)], '#c4463d')
        return o

    def hat(self):
        cx, cy, rx, ry, hs = self.cx, self.cy, self.rx, self.ry, self.hs
        kind = self.s.get('hat')
        o = ''
        if kind == 'gat':
            o += ellipse(cx, cy - ry + 26 * hs, 205 * hs, 38 * hs, '#141414', opacity=0.9)
            o += path(D('M', cx - 62 * hs, cy - ry + 30 * hs, 'L', cx + 62 * hs, cy - ry + 30 * hs, 'L', cx + 50 * hs, cy - ry - 78 * hs,
                        'Q', cx, cy - ry - 92 * hs, cx - 50 * hs, cy - ry - 78 * hs, 'Z'), '#1a1a1a')
            o += flat('ellipse', cx=cx, cy=cy - ry + 26 * hs, rx=170 * hs, ry=24 * hs, fill='#2c2c2c', opacity=0.6)
            for sx in (-1, 1):
                o += line(cx + sx * 150 * hs, cy - ry + 46 * hs, cx + sx * 26 * hs, cy + ry + 14 * hs, stroke='#2b2b2b', stroke_width=4)
                o += circle(cx + sx * 84 * hs, cy + 48 * hs, 7 * hs, '#e8d39a', stroke_width=2)
        elif kind == 'tanggeon':
            o += path(D('M', cx - 66 * hs, cy - ry + 34 * hs, 'Q', cx - 74 * hs, cy - ry - 30 * hs, cx - 34 * hs, cy - ry - 44 * hs,
                        'L', cx + 34 * hs, cy - ry - 44 * hs, 'Q', cx + 74 * hs, cy - ry - 30 * hs, cx + 66 * hs, cy - ry + 34 * hs, 'Z'), '#1f1f1f')
            o += path(D('M', cx - 44 * hs, cy - ry - 40 * hs, 'Q', cx - 40 * hs, cy - ry - 66 * hs, cx, cy - ry - 66 * hs,
                        'Q', cx + 40 * hs, cy - ry - 66 * hs, cx + 44 * hs, cy - ry - 40 * hs, 'Z'), '#1f1f1f')
            o += el('path', d=D('M', cx - rx - 2, cy - 44 * hs, 'Q', cx, cy - 82 * hs, cx + rx + 2, cy - 44 * hs), fill='none', stroke='#1f1f1f', stroke_width=14)
        elif kind == 'samo':
            o += path(D('M', cx - rx + 4, cy - 44 * hs, 'Q', cx - rx - 2, cy - ry - 34 * hs, cx, cy - ry - 40 * hs,
                        'Q', cx + rx + 2, cy - ry - 34 * hs, cx + rx - 4, cy - 44 * hs, 'Z'), '#1a1a1a')
            o += rect(cx - 58 * hs, cy - ry - 104 * hs, 116 * hs, 78 * hs, '#1a1a1a', rx=28 * hs)
            for sx in (-1, 1):
                o += ellipse(cx + sx * (rx + 52 * hs), cy - ry + 26 * hs, 58 * hs, 22 * hs, '#1a1a1a')
        elif kind == 'paeraengi':
            o += poly([(cx - 158 * hs, cy - ry + 44 * hs), (cx + 158 * hs, cy - ry + 44 * hs), (cx + 56 * hs, cy - ry - 56 * hs), (cx - 56 * hs, cy - ry - 56 * hs)], '#d9c68e')
            for k in range(-3, 4):
                o += line(cx + k * 16 * hs, cy - ry - 52 * hs, cx + k * 42 * hs, cy - ry + 40 * hs, stroke=THATCH_D, stroke_width=2.5)
            o += line(cx - 150 * hs, cy - ry + 30 * hs, cx + 150 * hs, cy - ry + 30 * hs, stroke=THATCH_D, stroke_width=3)
            o += ellipse(cx, cy - ry - 58 * hs, 30 * hs, 10 * hs, '#c9b27a')
            for sx in (-1, 1):
                o += line(cx + sx * 120 * hs, cy - ry + 52 * hs, cx + sx * 20 * hs, cy + ry + 10 * hs, stroke='#6b5a4a', stroke_width=3.5)
        elif kind == 'satgat':
            o += poly([(cx - 240 * hs, cy - ry + 60 * hs), (cx + 240 * hs, cy - ry + 60 * hs), (cx, cy - ry - 120 * hs)], '#c8b078')
            for k in range(-5, 6):
                o += line(cx, cy - ry - 110 * hs, cx + k * 44 * hs, cy - ry + 58 * hs, stroke=THATCH_D, stroke_width=2.5)
            o += line(cx - 236 * hs, cy - ry + 60 * hs, cx + 236 * hs, cy - ry + 60 * hs, stroke=THATCH_D, stroke_width=3)
            for sx in (-1, 1):
                o += line(cx + sx * 140 * hs, cy - ry + 66 * hs, cx + sx * 22 * hs, cy + ry + 10 * hs, stroke='#6b5a4a', stroke_width=3.5)
        elif kind == 'scarf':
            top = cy - ry - 12 * hs
            d = D('M', cx - rx - 8, cy + 10 * hs, 'Q', cx - rx - 14, top, cx, top, 'Q', cx + rx + 14, top, cx + rx + 8, cy + 10 * hs,
                  'Q', cx + rx - 2, cy - 62 * hs, cx, cy - 70 * hs, 'Q', cx - rx + 2, cy - 62 * hs, cx - rx - 8, cy + 10 * hs, 'Z')
            o += path(d, '#f4efe2')
            o += poly([(cx + rx - 4, cy - 20 * hs), (cx + rx + 50 * hs, cy - 50 * hs), (cx + rx + 40 * hs, cy + 6 * hs)], '#f4efe2')
            o += poly([(cx + rx - 4, cy - 20 * hs), (cx + rx + 44 * hs, cy + 30 * hs), (cx + rx + 6 * hs, cy + 34 * hs)], '#f4efe2')
        return o

    def beard(self):
        cx, cy, rx, ry, hs = self.cx, self.cy, self.rx, self.ry, self.hs
        kind = self.s.get('beard')
        col = self.s.get('beard_color', '#2a1d14')
        o = ''
        if kind in ('long', 'medium'):
            ln = 170 * hs if kind == 'long' else 70 * hs
            d = D('M', cx - rx + 10, cy + 26 * hs, 'Q', cx - rx - 4, cy + ry + ln * 0.4, cx - 34 * hs, cy + ry + ln,
                  'Q', cx, cy + ry + ln + 16 * hs, cx + 34 * hs, cy + ry + ln, 'Q', cx + rx + 4, cy + ry + ln * 0.4, cx + rx - 10, cy + 26 * hs,
                  'Q', cx + 60 * hs, cy + ry - 2 * hs, cx, cy + ry - 6 * hs, 'Q', cx - 60 * hs, cy + ry - 2 * hs, cx - rx + 10, cy + 26 * hs, 'Z')
            o += path(d, col)
            for k in range(-2, 3):
                o += el('path', d=D('M', cx + k * 22 * hs, cy + ry + 10 * hs, 'q', k * 6, ln * 0.4, k * 10, ln * 0.7), fill='none', stroke=OUT, stroke_width=2.5, opacity=0.35)
            # moustache
            for sx in (-1, 1):
                o += el('path', d=D('M', cx + sx * 8 * hs, cy + 40 * hs, 'q', sx * 26 * hs, -6 * hs, sx * 50 * hs, 22 * hs), fill='none', stroke=OUT, stroke_width=13, stroke_linecap='round')
                o += el('path', d=D('M', cx + sx * 8 * hs, cy + 40 * hs, 'q', sx * 26 * hs, -6 * hs, sx * 50 * hs, 22 * hs), fill='none', stroke=col, stroke_width=8, stroke_linecap='round')
        elif kind == 'thin':
            for sx in (-1, 1):
                o += el('path', d=D('M', cx + sx * 6 * hs, cy + 42 * hs, 'q', sx * 24 * hs, -8 * hs, sx * 48 * hs, 14 * hs), fill='none', stroke=OUT, stroke_width=4, stroke_linecap='round')
            o += el('path', d=D('M', cx, cy + ry - 4 * hs, 'l', 0, 34 * hs), fill='none', stroke=OUT, stroke_width=5, stroke_linecap='round')
        elif kind == 'moustache':
            for sx in (-1, 1):
                o += el('path', d=D('M', cx + sx * 6 * hs, cy + 42 * hs, 'q', sx * 30 * hs, -14 * hs, sx * 54 * hs, 20 * hs), fill='none', stroke=OUT, stroke_width=15, stroke_linecap='round')
                o += el('path', d=D('M', cx + sx * 6 * hs, cy + 42 * hs, 'q', sx * 30 * hs, -14 * hs, sx * 54 * hs, 20 * hs), fill='none', stroke=col, stroke_width=9, stroke_linecap='round')
        return o

    # ---- accessories
    def bojim_back(self):
        sy = self.L['sh_y']
        kind = self.s.get('bojim')
        if kind == 'big':
            o = rect(80, sy - 110, 440, 350, '#cfa85c', rx=100)
            o += line(300, sy - 100, 300, sy + 230, stroke='#8b6a3a', stroke_width=7)
            o += line(92, sy + 60, 508, sy + 60, stroke='#8b6a3a', stroke_width=7)
            o += rect(240, sy - 150, 120, 60, '#cfa85c', rx=24)
            return o
        if kind == 'small':
            o = rect(120, sy - 70, 360, 280, '#55608a', rx=80)
            o += line(300, sy - 60, 300, sy + 200, stroke='#3a4160', stroke_width=6)
            o += rect(250, sy - 100, 100, 50, '#55608a', rx=20)
            return o
        return ''

    def bojim_straps(self):
        sy = self.L['sh_y']
        if not self.s.get('bojim'):
            return ''
        col = '#cfa85c' if self.s['bojim'] == 'big' else '#55608a'
        o = ''
        for a, b in (((236, sy - 6), (366, sy + 220)), ((364, sy - 6), (234, sy + 220))):
            o += line(a[0], a[1], b[0], b[1], stroke=OUT, stroke_width=26)
        for a, b in (((236, sy - 6), (366, sy + 220)), ((364, sy - 6), (234, sy + 220))):
            o += line(a[0], a[1], b[0], b[1], stroke=col, stroke_width=18)
        o += circle(300, sy + 108, 20, col)
        return o

    def patches(self):
        if not self.s.get('patches'):
            return ''
        sy = self.L['sh_y']
        o = rect(190, sy + 260, 70, 60, '#7b766e', rx=6, stroke_width=3)
        o += rect(380, sy + 380, 60, 70, '#6e6a63', rx=6, stroke_width=3)
        if self.pose != 'sit':
            o += rect(300, sy + 470, 80, 55, '#7b766e', rx=6, stroke_width=3)
        for x, y, w in ((190, sy + 260, 70), (380, sy + 380, 60)):
            for k in range(3):
                o += line(x + 8 + k * (w - 16) / 2, y - 6, x + 8 + k * (w - 16) / 2, y + 6, stroke=OUT, stroke_width=2.5)
        return o

    # ---- outfits
    def body(self):
        s = self.s
        outfit = s['outfit']
        pose = self.pose
        L = self.L
        o = self.bojim_back()
        o += self.hair_back()
        if outfit in ('pants', 'jambaengi'):
            if pose == 'sit':
                o += self.lap(s['bottom'])
                o += self.lap_feet()
            else:
                o += self.legs(s['bottom'], short=(outfit == 'jambaengi'), wraps=s.get('leg_wraps', False))
            o += self.neck()
            o += self.jeogori(s['top'], L['hem'] if pose != 'sit' else L['lap_top'] + 20, s.get('tie', s['top']))
            o += self.patches()
            o += self.bojim_straps()
            o += self.arms(s['top'])
        elif outfit == 'chima':
            if pose != 'sit':
                (hx, hy), (fx, fy) = self.leg_points()[0]
                (hx2, hy2), (fx2, fy2) = self.leg_points()[1]
                o += self.shoe(fx if pose == 'walk' else 262, L['shoe'], flip=True) + self.shoe(fx2 if pose == 'walk' else 338, L['shoe'])
            o += self.chima(s['bottom'])
            o += self.neck()
            o += self.jeogori(s['top'], L['sh_y'] + 130, s.get('tie', RED), female=True)
            o += self.arms(s['top'])
        elif outfit == 'dopo':
            if pose != 'sit':
                o += self.shoe(258, L['shoe'], flip=True) + self.shoe(342, L['shoe'])
            o += self.neck()
            o += self.robe_body(s['top'], s.get('belly', 0))
            o += self.v_collar(s.get('tie', '#6f8f86'), depth=70)
            o += line(300, L['sh_y'] + 74, 262, (955 if pose != 'sit' else L['lap_bottom'] - 30), stroke=OUT, stroke_width=3, opacity=0.4)
            o += self.patches()
            o += self.bojim_straps()
            o += self.belt(L['sh_y'] + 165, s.get('tie', '#6f8f86'), wide=False)
            o += self.arms(s['top'], wide=True)
        elif outfit == 'gwanbok':
            if pose != 'sit':
                o += self.shoe(258, L['shoe'], flip=True) + self.shoe(342, L['shoe'])
            o += self.neck()
            o += self.robe_body(s['top'], s.get('belly', 0))
            o += self.round_collar()
            o += self.hyungbae(L['sh_y'] + 40)
            o += self.belt(L['sh_y'] + 180, s.get('belt', INDIGO), wide=True)
            o += self.arms(s['top'], wide=True)
        elif outfit == 'modern_vest':
            if pose == 'sit':
                o += self.lap(s['bottom'])
                o += self.lap_feet()
            else:
                o += self.legs(s['bottom'])
            o += self.neck()
            sy = L['sh_y']
            hem = L['hem'] if pose != 'sit' else L['lap_top'] + 20
            o += path(D('M', 300, sy - 18, 'L', 412, sy, 'Q', 442, sy + 4, 448, sy + 36, 'L', 456, hem, 'L', 144, hem, 'L', 152, sy + 36, 'Q', 158, sy + 4, 188, sy, 'Z'), s['top'])
            o += path(D('M', 190, sy - 4, 'L', 210, hem - 10, 'L', 390, hem - 10, 'L', 410, sy - 4, 'L', 340, sy + 8, 'L', 300, sy + 110, 'L', 260, sy + 8, 'Z'), s['vest'])
            o += poly([(258, sy - 8), (300, sy + 40), (342, sy - 8), (300, sy - 22)], '#f7f7f7')
            o += line(300, sy + 40, 300, sy - 22, stroke=OUT, stroke_width=3)
            for k in range(3):
                o += circle(300, sy + 130 + k * 44, 7, '#e5c25a', stroke_width=2.5)
            o += self.arms(s['top'])
        elif outfit == 'hoodie':
            if pose == 'sit':
                o += self.lap(s['bottom'])
                o += self.lap_feet()
            else:
                o += self.legs(s['bottom'])
            o += self.neck()
            sy = L['sh_y']
            hem = L['hem'] if pose != 'sit' else L['lap_top'] + 20
            o += path(D('M', 300, sy - 18, 'L', 412, sy, 'Q', 442, sy + 4, 448, sy + 36, 'L', 456, hem, 'L', 144, hem, 'L', 152, sy + 36, 'Q', 158, sy + 4, 188, sy, 'Z'), s['top'])
            o += rect(210, hem - 120, 180, 80, s['top'], rx=18)
            o += el('path', d=D('M', 250, sy, 'Q', 300, sy + 46, 350, sy), fill='none', stroke=OUT, stroke_width=4)
            for sx in (-1, 1):
                o += line(300 + sx * 22, sy + 34, 300 + sx * 30, sy + 130, stroke='#f7f7f7', stroke_width=7)
                o += line(300 + sx * 22, sy + 34, 300 + sx * 30, sy + 130, stroke=OUT, stroke_width=2, opacity=0.5)
            o += self.arms(s['top'], sleeve_cuff=None)
        return o

    def render(self):
        _SW[0] = 4.0 / self.sc
        H = self.L['H']
        inner = self.body()
        inner += self.head()
        inner += self.hair_cap()
        inner += self.hair_front()
        inner += self.hat()
        inner += self.beard()
        tf = f'translate(300 {H}) scale({n(self.sc)}) translate(-300 -{H})'
        body = g(inner, transform=tf)
        _SW[0] = 4.0
        return svg_doc(600, H, body)

    def meta(self):
        H = self.L['H']
        return {'eye_y': round(H - (H - self.eye_y()) * self.sc), 'mouth_y': round(H - (H - self.mouth_y()) * self.sc)}


# ---------------------------------------------------------------- props

def prop_ox():
    w, h = 720, 520
    o = ''
    # legs (back pair first)
    for x in (210, 470):
        o += tube([(x, 330), (x - 10, 470)], 46, '#7a4e2a')
        o += ellipse(x - 12, 490, 34, 18, '#2b2b2f')
    o += path(D('M', 150, 250, 'Q', 130, 150, 260, 130, 'L', 500, 120, 'Q', 620, 130, 610, 240, 'L', 600, 340, 'Q', 560, 380, 480, 372, 'L', 220, 375, 'Q', 150, 360, 150, 250, 'Z'), '#8b5a2b')
    for x in (270, 540):
        o += tube([(x, 340), (x + 6, 470)], 48, '#8b5a2b')
        o += ellipse(x + 8, 490, 36, 18, '#2b2b2f')
    # tail
    o += tube([(160, 210), (100, 300), (110, 400)], 14, '#7a4e2a')
    o += ellipse(112, 412, 16, 26, '#3a2618')
    # head
    o += path(D('M', 560, 150, 'Q', 690, 160, 700, 250, 'Q', 700, 320, 640, 330, 'L', 580, 320, 'Q', 540, 260, 560, 150, 'Z'), '#8b5a2b')
    o += ellipse(660, 300, 46, 30, '#c99a6a')
    o += flat('ellipse', cx=678, cy=298, rx=8, ry=6, fill=OUT)
    o += flat('ellipse', cx=646, cy=300, rx=8, ry=6, fill=OUT)
    o += ellipse(590, 200, 16, 20, '#ffffff', stroke_width=3)
    o += flat('circle', cx=594, cy=204, r=9, fill=OUT)
    o += ellipse(560, 180, 24, 14, '#7a4e2a', transform='rotate(-30 560 180)')
    for sx, x in ((-1, 600), (1, 650)):
        o += path(D('M', x, 150, 'q', sx * 10, -60, sx * 50, -70, 'q', 10, 30, sx * -30, 70, 'Z'), '#e9dcc0')
    # yoke rope
    o += path(D('M', 560, 260, 'Q', 500, 240, 470, 250), 'none', stroke='#a98a55', stroke_width=6)
    return w, h, o


def prop_jige():
    w, h = 520, 640
    o = ''
    for x in (200, 320):
        o += tube([(x, 620), (x - 30 if x < 260 else x + 30, 60)], 22, WOOD)
    for y in (200, 330, 460):
        t = (620 - y) / 560
        o += line(200 - 30 * t - 10, y, 320 + 30 * t + 10, y, stroke=WOOD_D, stroke_width=14)
    o += line(170, 560, 80, 620, stroke=WOOD_D, stroke_width=14)
    o += line(350, 560, 440, 620, stroke=WOOD_D, stroke_width=14)
    r = Rng(151)
    for k in range(16):
        x1 = r.u(90, 200)
        y1 = r.u(140, 420)
        x2 = x1 + r.u(240, 330)
        y2 = y1 + r.u(-40, 40)
        o += line(x1, y1, x2, y2, stroke=OUT, stroke_width=18)
        o += line(x1, y1, x2, y2, stroke=r.ch(['#8a5a2e', '#a06a38', '#6e4a2b']), stroke_width=12)
    o += rect(150, 250, 230, 22, '#c9b27a', rx=6)
    o += rect(150, 380, 230, 22, '#c9b27a', rx=6)
    for y in (110, 300):
        o += el('path', d=D('M', 180, y, 'q', 80, -50, 160, 0), fill='none', stroke='#c9b27a', stroke_width=12, stroke_linecap='round')
    return w, h, o


def prop_rice_sack():
    w, h = 420, 470
    o = path(D('M', 60, 440, 'L', 50, 200, 'Q', 50, 120, 120, 100, 'L', 300, 100, 'Q', 370, 120, 370, 200, 'L', 360, 440, 'Q', 210, 470, 60, 440, 'Z'), '#dcc48a')
    for k in range(1, 7):
        o += line(60, 120 + k * 46, 360, 120 + k * 46, stroke='#b59a52', stroke_width=3)
    for k in range(1, 6):
        o += line(60 + k * 50, 108, 60 + k * 50, 446, stroke='#b59a52', stroke_width=2.5)
    o += path(D('M', 120, 100, 'Q', 150, 40, 210, 30, 'Q', 270, 40, 300, 100, 'Z'), '#cdb579')
    o += rect(120, 88, 180, 22, '#8b6a3a', rx=6)
    o += rect(50, 230, 320, 18, '#8b6a3a', rx=6)
    o += rect(52, 350, 316, 18, '#8b6a3a', rx=6)
    return w, h, o


def prop_coin_pouch():
    w, h = 340, 380
    o = path(D('M', 90, 340, 'Q', 30, 300, 40, 220, 'Q', 50, 150, 150, 120, 'L', 210, 120, 'Q', 310, 150, 320, 220, 'Q', 330, 300, 270, 340, 'Z'), '#c89a3a')
    o += path(D('M', 130, 120, 'Q', 120, 70, 150, 50, 'L', 210, 50, 'Q', 240, 70, 230, 120, 'Z'), '#c89a3a')
    o += el('path', d=D('M', 110, 118, 'Q', 180, 150, 250, 118), fill='none', stroke='#c4463d', stroke_width=12, stroke_linecap='round')
    o += el('path', d=D('M', 110, 118, 'q', -30, 40, -10, 90), fill='none', stroke='#c4463d', stroke_width=8, stroke_linecap='round')
    o += el('path', d=D('M', 250, 118, 'q', 30, 40, 10, 90), fill='none', stroke='#c4463d', stroke_width=8, stroke_linecap='round')
    for cx, cy in ((250, 320), (290, 345), (215, 350)):
        o += circle(cx, cy, 28, '#d9b04a')
        o += rect(cx - 8, cy - 8, 16, 16, '#6b4a2b', stroke_width=2.5)
    return w, h, o


def scroll_paper(x, y, w, h, cols=7, torn=None):
    o = ''
    if torn is None:
        o += rect(x, y, w, h, '#f6ecd4')
    else:
        o += path(torn, '#f6ecd4')
    for k in range(1, cols):
        o += line(x + w * k / cols, y + 26, x + w * k / cols, y + h - 26, stroke='#8f7a55', stroke_width=3)
    o += rect(x + 12, y + 12, w - 24, h - 24, 'none', stroke='#b2925b', stroke_width=3)
    return o


def stamp(x, y, s=1.0):
    o = rect(x, y, 60 * s, 60 * s, '#c84a3a', rx=4, stroke='#8e2f24', stroke_width=3)
    o += rect(x + 12 * s, y + 12 * s, 36 * s, 36 * s, 'none', stroke='#f6e2c8', stroke_width=4)
    o += line(x + 30 * s, y + 12 * s, x + 30 * s, y + 48 * s, stroke='#f6e2c8', stroke_width=4)
    return o


def prop_nobi_document():
    w, h = 640, 400
    o = scroll_paper(90, 60, 460, 280)
    o += stamp(470, 250, 1.0)
    for x in (40, 550):
        o += rect(x, 40, 50, 320, WOOD, rx=14)
        o += circle(x + 25, 40, 20, '#d9b04a')
        o += circle(x + 25, 360, 20, '#d9b04a')
    return w, h, o


def prop_torn_document():
    w, h = 720, 400
    left = D('M', 60, 60, 'L', 330, 60, 'L', 310, 110, 'L', 345, 160, 'L', 300, 210, 'L', 340, 260, 'L', 305, 340, 'L', 60, 340, 'Z')
    right = D('M', 380, 60, 'L', 660, 60, 'L', 660, 340, 'L', 360, 340, 'L', 395, 260, 'L', 355, 210, 'L', 400, 160, 'L', 365, 110, 'Z')
    o = scroll_paper(60, 60, 280, 280, cols=4, torn=left)
    o += scroll_paper(380, 60, 280, 280, cols=4, torn=right)
    o += stamp(580, 250, 1.0)
    return w, h, o


def prop_herb_basket():
    w, h = 520, 420
    o = ''
    r = Rng(161)
    for k in range(14):
        x = 120 + k * 22 + r.u(-10, 10)
        o += el('path', d=D('M', x, 260, 'q', r.u(-40, 40), -80, r.u(-30, 30), -160), fill='none', stroke='#4f8a45', stroke_width=7, stroke_linecap='round')
        o += ellipse(x + r.u(-30, 30), 110 + r.u(-20, 40), 14, 30, r.ch(['#6aa554', '#7fb35c', '#5b9a48']), stroke_width=2.5, transform=f'rotate({r.u(-40, 40)} {x} 120)')
    o += path(D('M', 40, 240, 'L', 480, 240, 'L', 430, 400, 'L', 90, 400, 'Z'), '#c9a25a')
    for k in range(1, 4):
        o += line(40 + 10 * k, 240 + 40 * k, 480 - 10 * k, 240 + 40 * k, stroke='#8b6a3a', stroke_width=4)
    for k in range(1, 9):
        o += line(40 + 55 * k, 240, 90 + 42 * k, 400, stroke='#8b6a3a', stroke_width=4)
    o += el('path', d=D('M', 70, 240, 'Q', 260, 20, 450, 240), fill='none', stroke=OUT, stroke_width=22, stroke_linecap='round')
    o += el('path', d=D('M', 70, 240, 'Q', 260, 20, 450, 240), fill='none', stroke='#a97f45', stroke_width=14, stroke_linecap='round')
    return w, h, o


def prop_medicine_pot():
    w, h = 460, 400
    o = ellipse(230, 380, 150, 18, '#2b2b2f', opacity=0.25, stroke='none')
    o += path(D('M', 130, 370, 'L', 100, 240, 'Q', 90, 150, 170, 130, 'L', 290, 130, 'Q', 370, 150, 360, 240, 'L', 330, 370, 'Z'), '#6b4a2b')
    o += ellipse(230, 130, 64, 18, '#8b6a3a')
    o += path(D('M', 190, 120, 'Q', 200, 90, 230, 86, 'Q', 260, 90, 270, 120, 'Z'), '#8b6a3a')
    o += circle(230, 84, 14, '#8b6a3a')
    o += el('path', d=D('M', 360, 260, 'q', 70, -20, 80, -90), fill='none', stroke=OUT, stroke_width=30, stroke_linecap='round')
    o += el('path', d=D('M', 360, 260, 'q', 70, -20, 80, -90), fill='none', stroke='#6b4a2b', stroke_width=20, stroke_linecap='round')
    o += el('path', d=D('M', 100, 220, 'q', -60, 10, -50, 70), fill='none', stroke=OUT, stroke_width=26, stroke_linecap='round')
    o += el('path', d=D('M', 100, 220, 'q', -60, 10, -50, 70), fill='none', stroke='#6b4a2b', stroke_width=16, stroke_linecap='round')
    for k in range(3):
        o += el('path', d=D('M', 210 + k * 20, 70, 'q', 16, -30, 0, -60), fill='none', stroke='#dfe6ec', stroke_width=7, stroke_linecap='round', opacity=0.8)
    return w, h, o


def prop_candle():
    w, h = 300, 620
    o = rect(90, 580, 120, 24, '#c99a3a', rx=8)
    o += rect(138, 300, 24, 280, '#c99a3a')
    o += ellipse(150, 420, 30, 14, '#c99a3a')
    o += rect(110, 290, 80, 16, '#c99a3a', rx=4)
    o += rect(128, 150, 44, 140, '#fff5dc')
    o += line(150, 150, 150, 132, stroke=OUT, stroke_width=4)
    o += path(D('M', 150, 130, 'q', -28, -40, 0, -84, 'q', 28, 44, 0, 84, 'Z'), '#ffb347', stroke='#e07b1b', stroke_width=3)
    o += flat('path', d=D('M', 150, 122, 'q', -10, -20, 0, -40, 'q', 10, 20, 0, 40, 'Z'), fill='#fff1a8')
    return w, h, o


def prop_boat():
    w, h = 720, 300
    o = boat_shape(350, 250, 1.0)
    o += tube([(560, 240), (610, 40)], 10, WOOD_D)
    return w, h, o


def prop_paper_lantern():
    w, h = 320, 520
    o = tube([(160, 100), (160, 40)], 8, WOOD_D)
    o += line(60, 40, 260, 40, stroke=WOOD_D, stroke_width=10)
    o += rect(110, 92, 100, 20, WOOD, rx=4)
    o += path(D('M', 90, 110, 'Q', 30, 250, 90, 400, 'L', 230, 400, 'Q', 290, 250, 230, 110, 'Z'), '#e86a5a')
    for k in range(1, 5):
        y = 110 + k * 58
        o += el('path', d=D('M', 60 + (k % 2) * 6, y, 'Q', 160, y + 14, 260 - (k % 2) * 6, y), fill='none', stroke='#b23b30', stroke_width=3)
    o += flat('ellipse', cx=130, cy=230, rx=26, ry=60, fill='#ffb3a0', opacity=0.5)
    o += rect(110, 400, 100, 20, WOOD, rx=4)
    for k in range(4):
        o += line(140 + k * 14, 420, 136 + k * 14, 500, stroke='#c4463d', stroke_width=6)
    return w, h, o


def prop_book():
    w, h = 420, 320
    o = rect(60, 70, 300, 220, INDIGO_D, rx=6)
    o += rect(40, 50, 300, 220, INDIGO, rx=6)
    o += rect(60, 70, 60, 180, '#f2e4c4', rx=4)
    for y in (90, 130, 170, 210, 250):
        o += flat('circle', cx=52, cy=y, r=5, fill='#f2e4c4')
        o += line(52, y, 60, y, stroke='#f2e4c4', stroke_width=3)
    return w, h, o


def prop_hanji_sign():
    w, h = 500, 720
    o = rect(80, 40, 340, 40, WOOD, rx=10)
    o += rect(100, 80, 300, 560, '#f6ecd4')
    for k in range(1, 4):
        o += line(100 + 75 * k, 110, 100 + 75 * k, 610, stroke='#8f7a55', stroke_width=3)
    o += rect(112, 92, 276, 536, 'none', stroke='#b2925b', stroke_width=3)
    o += rect(80, 640, 340, 40, WOOD, rx=10)
    o += stamp(320, 540, 0.9)
    o += el('path', d=D('M', 250, 40, 'L', 250, 10), fill='none', stroke=OUT, stroke_width=6)
    return w, h, o


def prop_magpie():
    w, h = 520, 420
    o = path(D('M', 180, 200, 'Q', 120, 60, 260, 40, 'Q', 330, 60, 290, 180, 'Z'), '#1e1e24')
    o += path(D('M', 190, 250, 'Q', 90, 330, 60, 300, 'Q', 130, 260, 200, 210, 'Z'), '#1e1e24')
    o += path(D('M', 120, 240, 'Q', 30, 300, 20, 290, 'L', 130, 210, 'Z'), '#1e1e24')
    o += path(D('M', 150, 190, 'Q', 220, 150, 330, 170, 'Q', 420, 190, 440, 220, 'Q', 380, 300, 260, 290, 'Q', 170, 280, 150, 190, 'Z'), '#1e1e24')
    o += path(D('M', 190, 230, 'Q', 260, 220, 330, 240, 'Q', 340, 280, 260, 290, 'Q', 190, 280, 190, 230, 'Z'), '#f4f4f4')
    o += flat('path', d=D('M', 230, 120, 'Q', 270, 90, 300, 130, 'Q', 260, 150, 230, 120, 'Z'), fill='#f4f4f4')
    o += path(D('M', 400, 190, 'Q', 460, 170, 490, 200, 'Q', 470, 240, 420, 240, 'Z'), '#1e1e24')
    o += circle(445, 205, 9, '#ffffff', stroke_width=2.5)
    o += flat('circle', cx=447, cy=206, r=4, fill=OUT)
    o += poly([(490, 200), (520, 212), (490, 226)], '#3a3a44')
    o += path(D('M', 250, 100, 'Q', 220, 60, 250, 40, 'Q', 280, 70, 300, 120, 'Z'), '#3a4c8a', stroke='none')
    return w, h, o


def prop_umbrella_straw():
    w, h = 620, 620
    o = path(D('M', 100, 620, 'Q', 90, 380, 220, 300, 'L', 400, 300, 'Q', 530, 380, 520, 620, 'Z'), '#c9b27a')
    r = Rng(171)
    for k in range(-8, 9):
        x = 310 + k * 22
        o += line(x, 320 + abs(k) * 4, x + k * 6, 610, stroke=THATCH_D, stroke_width=3)
    for y in (400, 480, 560):
        o += el('path', d=D('M', 110, y, 'Q', 310, y + 30, 510, y), fill='none', stroke='#8b6a3a', stroke_width=4)
    o += poly([(60, 300), (560, 300), (310, 80)], '#c8b078')
    for k in range(-5, 6):
        o += line(310, 90, 310 + k * 46, 298, stroke=THATCH_D, stroke_width=2.5)
    o += line(66, 300, 554, 300, stroke=THATCH_D, stroke_width=3)
    o += circle(310, 80, 12, '#a98a55')
    return w, h, o


PROPS = {
    'ox': prop_ox, 'jige': prop_jige, 'rice_sack': prop_rice_sack, 'coin_pouch': prop_coin_pouch,
    'nobi_document': prop_nobi_document, 'torn_document': prop_torn_document, 'herb_basket': prop_herb_basket,
    'medicine_pot': prop_medicine_pot, 'candle': prop_candle, 'boat': prop_boat, 'paper_lantern': prop_paper_lantern,
    'book': prop_book, 'hanji_sign': prop_hanji_sign, 'magpie': prop_magpie, 'umbrella_straw': prop_umbrella_straw,
}


# ---------------------------------------------------------------- driver

def write(p, text):
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists() and p.read_text() == text:
        return
    p.write_text(text)


def generate(out):
    out = Path(out)
    svgdir = out / 'svg'
    jobs = []
    manifest = {'bg': {}, 'char': {}, 'prop': {}}
    for name, fn in BACKGROUNDS.items():
        defs, body = fn()
        svg = svg_doc(BW, BH, body, defs)
        sp = svgdir / 'bg' / f'{name}.svg'
        write(sp, svg)
        jobs.append({'svg': str(sp), 'png': str(out / 'bg' / f'{name}.png'), 'transparent': False})
        manifest['bg'][name] = {'w': BW, 'h': BH, 'file': f'bg/{name}.png'}
    for name, spec in CHARACTERS.items():
        entry = {'poses': {}}
        for pose in CHAR_POSES[name]:
            H = layout(pose)['H']
            states = {}
            for mouth, eyes in STATES:
                c = Char(name, spec, pose, mouth, eyes)
                svg = c.render()
                fn_ = f'{name}_{pose}_{mouth}_{eyes}'
                sp = svgdir / 'char' / f'{fn_}.svg'
                write(sp, svg)
                jobs.append({'svg': str(sp), 'png': str(out / 'char' / f'{fn_}.png'), 'transparent': True})
                states[f'{mouth}_{eyes}'] = f'char/{fn_}.png'
                if pose == 'stand' and mouth == 'closed' and eyes == 'open':
                    entry.update(c.meta())
            entry['poses'][pose] = {'w': 600, 'h': H, 'states': states}
        manifest['char'][name] = entry
    for name, fn in PROPS.items():
        w, h, body = fn()
        svg = svg_doc(w, h, body)
        sp = svgdir / 'prop' / f'{name}.svg'
        write(sp, svg)
        jobs.append({'svg': str(sp), 'png': str(out / 'prop' / f'{name}.png'), 'transparent': True})
        manifest['prop'][name] = {'w': w, 'h': h, 'file': f'prop/{name}.png'}
    write(out / 'manifest.json', json.dumps(manifest, indent=1, ensure_ascii=False) + '\n')
    write(svgdir / 'jobs.json', json.dumps(jobs, indent=0) + '\n')
    return manifest, jobs


def rasterise(jobs_path):
    subprocess.run(['node', str(RASTER), str(jobs_path)], check=True)


def contact_sheet(out, manifest):
    try:
        from PIL import Image
    except ImportError:
        print('Pillow not available; skipping contact sheet')
        return
    out = Path(out)
    tw, th = 480, 270
    bgs = list(manifest['bg'].items())
    chars = list(manifest['char'].items())
    cols = 5
    bg_rows = math.ceil(len(bgs) / cols)
    ch, cw = 360, 216
    ch_cols = 10
    ch_rows = math.ceil(len(chars) / ch_cols)
    W = cols * tw
    Hh = bg_rows * th + ch_rows * ch + 40
    sheet = Image.new('RGB', (W, Hh), (60, 60, 60))
    for i, (name, m) in enumerate(bgs):
        im = Image.open(out / m['file']).convert('RGB').resize((tw - 6, th - 6))
        sheet.paste(im, ((i % cols) * tw + 3, (i // cols) * th + 3))
    y0 = bg_rows * th + 40
    for i, (name, m) in enumerate(chars):
        f = m['poses']['stand']['states']['closed_open']
        im = Image.open(out / f).convert('RGBA')
        im = im.resize((cw - 8, ch - 8))
        bgc = Image.new('RGBA', im.size, (200, 190, 170, 255))
        bgc.alpha_composite(im)
        sheet.paste(bgc.convert('RGB'), ((i % ch_cols) * (W // ch_cols) + 10, y0 + (i // ch_cols) * ch))
    sheet.save(out / 'contact_sheet.png')
    print('wrote', out / 'contact_sheet.png')


def verify(out, manifest):
    try:
        from PIL import Image
    except ImportError:
        print('Pillow not available; skipping verification')
        return True
    out = Path(out)
    ok = True
    count = 0
    for name, m in manifest['bg'].items():
        p = out / m['file']
        im = Image.open(p)
        count += 1
        if im.size != (m['w'], m['h']):
            print('BAD SIZE', p, im.size)
            ok = False
    for name, m in manifest['char'].items():
        for pose, pm in m['poses'].items():
            for st, f in pm['states'].items():
                p = out / f
                im = Image.open(p)
                count += 1
                if im.size != (pm['w'], pm['h']) or im.mode != 'RGBA':
                    print('BAD', p, im.size, im.mode)
                    ok = False
                    continue
                px = im.getpixel((0, 0))[3], im.getpixel((pm['w'] - 1, 0))[3]
                if px != (0, 0):
                    print('CORNERS NOT TRANSPARENT', p, px)
                    ok = False
    for name, m in manifest['prop'].items():
        p = out / m['file']
        im = Image.open(p)
        count += 1
        if im.size != (m['w'], m['h']) or im.mode != 'RGBA' or im.getpixel((0, 0))[3] != 0:
            print('BAD', p, im.size, im.mode)
            ok = False
    print(f'verified {count} png(s):', 'OK' if ok else 'PROBLEMS')
    return ok


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    out = Path(argv[1])
    manifest, jobs = generate(out)
    print(f'wrote {len(jobs)} svg(s) under {out / "svg"}')
    if '--svg-only' in argv:
        return 0
    rasterise(out / 'svg' / 'jobs.json')
    verify(out, manifest)
    contact_sheet(out, manifest)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
