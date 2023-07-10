from dataclasses import dataclass
import math
import random


@dataclass
class Point:
    x: float
    y: float


stage_margin = 10


@dataclass
class Rect:
    pos: Point
    width: float
    height: float

    def lb(self):
        return Point(self.pos.x + stage_margin, self.pos.y + stage_margin)

    def lt(self):
        return Point(self.pos.x + stage_margin, self.pos.y + self.height - stage_margin)

    def rb(self):
        return Point(self.pos.x + self.width - stage_margin, self.pos.y + stage_margin)

    def rt(self):
        return Point(self.pos.x + self.width - stage_margin, self.pos.y + self.height - stage_margin)

    def draw_on(self, fig, color):
        fig.add_shape(type="rect",
                      x0=self.pos.x,
                      y0=self.pos.y,
                      x1=self.pos.x + self.width,
                      y1=self.pos.y + self.height,
                      line=dict(width=3),
                      fillcolor=color,
                      opacity=0.6)


@dataclass
class Attendee:
    pos: Point
    tastes: list[float]


@dataclass
class Pillar:
    pos: Point
    radius: float


@dataclass
class MusicRoom:
    room: Rect
    stage: Rect
    musicians: list[int]
    attendees: list[Attendee]
    pillars: list[Pillar]
    filtered_attendees_count: int(0)
    filtered_pillars_count: int(0)

    def filtered_attendees(self):
        return self.filtered_attendees_count

    def filtered_pillars(self):
        return self.filtered_pillars_count

    def filter_attendees(self):
        listening_attendees = []
        filtered_attendees = []
        for ai, a in enumerate(self.attendees):
            filtered = False
            for pi, p in enumerate(self.pillars):
                if is_attendee_blocked_by_pillar(a, p, self.stage):
                    filtered = True
                    break
            if not filtered:
                listening_attendees.append(a)
            else:
                filtered_attendees.append(a)
        print(f" >> Attendee filter statistics: {len(filtered_attendees)} / {len(self.attendees)}")
        # print(f" >> Filtered attendees={filtered_attendees}")
        self.attendees = listening_attendees
        self.filtered_attendees_count = len(filtered_attendees)

    def filter_pillars(self):
        active_pillars = []
        filtered_pillars = []
        for p in self.pillars:
            active = False
            for a in self.attendees:
                if is_attendee_intersected_by_pillar(a, p, self.stage):
                    active = True
                    break
            if not active:
                filtered_pillars.append(p)
            else:
                active_pillars.append(p)
        # print(f" >> Attendee filter statistics: {len(filtered_pillars)} / {len(self.pillars)}")
        # print(f"Filtered pillars={filtered_pillars}")
        self.filtered_pillars_count = len(filtered_pillars)
        self.pillars = active_pillars

    def sample_placement(self):
        random.seed()
        rc = self.stage.width / 20
        rows = list(range(math.floor(rc)))
        random.shuffle(rows)

        placement = []
        musicians_left = len(self.musicians)
        for r in rows:
            rx = self.stage.pos.x + 10 + r * 20
            mys = []
            for c in range(math.floor(self.stage.height / 20)):
                mys.append(self.stage.pos.y + 10 + c * 20)
            random.shuffle(mys)
            for my in mys:
                placement.append(Point(rx, my))
                musicians_left -= 1
                if musicians_left == 0:
                    break
            if musicians_left == 0:
                break
        return placement


def dist2(p1: Point, p2: Point) -> float:
    return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2


def line_intersects_circle(l1: Point, l2: Point, center: Point, r: float) -> bool:
    # Line coefficients for ax+by+c=0
    # l1: musician 1
    # l2: attendee
    # center: musician 2
    a = l2.y - l1.y  # Dy
    b = l1.x - l2.x  # -Dx
    norm_ab = math.sqrt(a ** 2 + b ** 2)
    a, b = a / norm_ab, b / norm_ab
    c = ((l2.x * l1.y) - (l1.x * l2.y)) / norm_ab
    dist = abs(a * center.x + b * center.y + c)
    # Projection coefficients for ax+by+c=0..1 along the interval (l1, l2).
    a_orto, b_orto = -b / norm_ab, a / norm_ab
    c_orto = 1 - l2.x * a_orto - l2.y * b_orto

    def proj(p):
        return a_orto * p.x + b_orto * p.y + c_orto

    assert abs(proj(l1)) < 1e-5, proj(l1)
    assert abs(proj(l2) - 1.0) < 1e-5, proj(l2)
    p = proj(center)
    return l1 != center and dist < r and 0 < p < 1


def is_attendee_blocked_by_pillar(a: Attendee, p: Pillar, s: Rect):
    lb = line_intersects_circle(a.pos, s.lb(), p.pos, p.radius)
    lt = line_intersects_circle(a.pos, s.lt(), p.pos, p.radius)
    rb = line_intersects_circle(a.pos, s.rb(), p.pos, p.radius)
    rt = line_intersects_circle(a.pos, s.rt(), p.pos, p.radius)
    return lb and lt and rb and rt


def is_attendee_intersected_by_pillar(a: Attendee, p: Pillar, s: Rect):
    return True


def is_blocked_by(m1: Point, m2: Point, a: Attendee) -> bool:  # m1 is blocked by m2 from a
    return line_intersects_circle(m1, a.pos, m2, 5)


def score(a_index: int, m_index: int, placements: list[Point], room: MusicRoom) -> int:
    a, m_inst, m_pos = room.attendees[a_index], room.musicians[m_index], placements[m_index]
    if any(is_blocked_by(m_pos, m2_pos, a) for m2_pos in placements):
        return 0
    return math.ceil(1_000_000 * a.tastes[m_inst] / dist2(a.pos, m_pos))


def happiness(placements: list[Point], room: MusicRoom) -> int:
    return sum(score(a_idx, m_idx, placements, room)
               for a_idx in range(len(room.attendees))
               for m_idx in range(len(placements)))


def parse_input(filename_or_json):
    import json
    try:
        input = json.loads(filename_or_json)
    except Exception:
        with open(filename_or_json) as f:
            input = json.load(f)

    room = Rect(pos=Point(0, 0), width=input['room_width'], height=input['room_height'])
    stage = Rect(pos=Point(x=input['stage_bottom_left'][0], y=input['stage_bottom_left'][1]),
                 width=input['stage_width'], height=input['stage_height'])
    attns = [Attendee(pos=Point(x=a['x'], y=a['y']), tastes=a['tastes']) for a in input['attendees']]
    pillars = [Pillar(pos=Point(x=p['center'][0], y=p['center'][1]), radius=p['radius']) for p in input['pillars']]

    music_room = MusicRoom(room=room, stage=stage, musicians=input['musicians'], attendees=attns, pillars=pillars,
                           filtered_pillars_count=0, filtered_attendees_count=0)
    music_room.filter_attendees()
    music_room.filter_pillars()

    return music_room


room = parse_input("./problems/85.json")
