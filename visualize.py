#from model import parse_input

import sys
import numpy
import plotly
import plotly.express as px
import plotly.graph_objects as go
import requests as rq


def render_room(room, placement=[], grads=[], soft_score=None, grad_mult=1.0, calc_scores=False):
    @dataclass
    class Line:
        src: Point
        dst: Point
        raw_score: float
        norm_score: float  # -1 .. 0 .. 1 range

        def normalize(self, mins, maxs):
            delta = abs(maxs - mins) * 1.2
            self.norm_score = (abs(self.raw_score) - mins) / delta

        def color(self):
            if self.raw_score < 0:
                return f'rgb(255, 50, 50)'
            else:
                return f'rgb(25, 25, 255)'

        def opacity(self):
            return self.norm_score

    fig = go.Figure(data=go.Scatter(mode='markers'))
    room.room.draw_on(fig, color="Grey")
    room.stage.draw_on(fig, color="rgb(255, 127, 127)")

    xs = [a.pos.x for a in room.attendees]
    ys = [a.pos.y for a in room.attendees]
    a_hovers = []
    lines = []

    if calc_scores:
        for ai in range(len(xs)):
            scores = []
            for mi in range(len(placement)):
                s = score(ai, mi, placement, room)
                scores.append(str(s))
                lines.append(Line(dst=placement[mi], src=room.attendees[ai].pos, raw_score=s, norm_score=0.0))
            a_hovers.append(f"[ {', '.join(scores)} ]")

            # normalize lines
            max_score = -sys.float_info.max
            for l in lines:
                max_score = max(abs(l.raw_score), max_score)
            for l in lines:
                l.normalize(0, max_score)
    else:
        a_hovers = ["..."] * len(xs)
    fig.add_trace(go.Scatter(x=xs, y=ys, mode='markers + text', name='attendees',
                             text=[f"A{i}" for i in range(len(xs))],
                             textposition="top right",
                             customdata=a_hovers,
                             hovertemplate="Musician scores: %{customdata}",
                             marker=dict(size=3,
                                         symbol="diamond",
                                         line=dict(width=1,
                                                   color='DarkSlateGrey')
                                         )))

    xs = []
    ys = []
    for sp in placement:
        xs.append(sp.x)
        ys.append(sp.y)
    fig.add_trace(go.Scatter(x=xs, y=ys, mode='markers + text', name='musicians',
                             text=[f"m{i}" for i in range(len(xs))],
                             textposition="bottom left",
                             marker=dict(size=10,
                                         line=dict(width=2,
                                                   color='DarkSlateGrey')
                                         )))
    for p in room.pillars:
        fig.add_trace(go.Scatter(
            x=[p.pos.x], y=[p.pos.y],
            mode='markers', name='pillars',
            showlegend=False,
            hoverinfo='none',
            marker=dict(
                size=p.radius,
                color='rgb(64,64,64,0.3)',
                line=dict(width=2, color='Black'))))

    if placement and calc_scores:
        hp = happiness(placement, room)
        fig.add_annotation(text=f"hard_score={hp}, soft_score={soft_score}",
                           align="left")
    for i, g in enumerate(grads):
        color = 'rgb(204, 0, 204)'
        fig.add_trace(go.Scatter(x=[placement[i].x, placement[i].x + g.x * grad_mult],
                                 y=[placement[i].y, placement[i].y + g.y * grad_mult],
                                 mode='lines',
                                 name='scores',
                                 line=dict(width=2, color=color, dash="longdash"),
                                 opacity=1))
    for l in lines:
        color = l.color()
        op = l.opacity()
        # print(f"Line={l}, color={color}, opacity={op}")
        fig.add_trace(go.Scatter(x=[l.src.x, l.dst.x], y=[l.src.y, l.dst.y],
                                 mode='lines',
                                 name='scores',
                                 line=dict(width=1, color=color),
                                 opacity=op,
                                 showlegend=False))
    fig.data = fig.data[::-1]
    fig.show(renderer="colab")


def get_room(num: int) -> MusicRoom:
    r = rq.get(f"https://cdn.icfpcontest.com/problems/{num}.json")
    room = parse_input(r.content)
    return room


def render_problem(num, calc_scores):
    room = get_room(num)
    render_room(room, room.sample_placement(), calc_scores=calc_scores)


def render_musicians(room: MusicRoom, vars: ModelVars):
    placements = points(vars)
    new_room = MusicRoom(room=room.stage, stage=room.stage,
                         musicians=room.musicians,
                         attendees=[], pillars=[])
    render_room(new_room, placements)