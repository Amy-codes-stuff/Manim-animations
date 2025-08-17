from manim import *
import math
import random

config.background_color = WHITE

class ProbabilityLineSegment(Scene):
    def construct(self):
        radius = 3
        line = NumberLine(x_range=[-radius, radius], length=2 * radius, include_ticks=True)
        line.set_color(BLACK)

        target_segment = Line(start=line.n2p(-1), end=line.n2p(1), color=BLUE, stroke_width=8)
        target_segment.set_z_index(1)

        counter_tex = MathTex(r"\frac{0}{0}", font_size=36, color=BLACK).to_corner(UL, buff=0.8)
        prob_value = DecimalNumber(0, num_decimal_places=3, include_sign=False, color=BLACK)
        prob_label = MathTex(r"P =", font_size=36, color=BLACK)
        prob_group = VGroup(prob_label, prob_value).arrange(RIGHT, buff=0.1).to_corner(UR, buff=0.8)

        dot_radius = 0.04
        total_points = 10
        dot_radius_small = 0.02
        batch_size = 5

        inner_color = GREEN
        outer_color = BLACK
        border_offset = 0.005

        self.add(line, target_segment, counter_tex, prob_group)

        inside_count = 0
        total_count = 0
        temp_batch = []

        for i in range(1, total_points + 1):
            x = random.uniform(-radius, radius)
            pt = [x, 0, 0]

            if -1 <= x <= 1:
                inside_count += 1
                dot_color = inner_color
            else:
                dot_color = RED

            outer = Dot(pt, color=outer_color, radius=dot_radius + border_offset)
            inner = Dot(pt, color=dot_color, radius=dot_radius)
            dot = VGroup(outer, inner)

            temp_batch.append(dot)
            total_count += 1
            est_prob = inside_count / total_count

            counter_tex.become(MathTex(rf"\frac{{{inside_count}}}{{{total_count}}}", font_size=36, color=BLACK).to_corner(UL, buff=0.8))
            prob_value.set_value(est_prob)

            if len(temp_batch) == batch_size or i == total_points:
                self.add(*temp_batch)
                self.wait(0.01)
                temp_batch = []


class ProbabilitySquare(Scene):
    def construct(self):
        side_length = 3
        inner_side = 1
        square = Square(side_length=side_length, color=BLACK).shift(DOWN * 0.5)
        inner_square = Square(side_length=inner_side, color=BLUE, fill_opacity=0.5).move_to(square.get_center())

        frac_counter3 = MathTex(r"\frac{0}{0}", font_size=36, color=BLACK).to_corner(UL, buff=0.8)
        prob_value3 = DecimalNumber(0, num_decimal_places=3, include_sign=False, color=BLACK)
        prob_label3 = MathTex(r"P =", font_size=36, color=BLACK)
        prob_group3 = VGroup(prob_label3, prob_value3).arrange(RIGHT, buff=0.1).to_corner(UR, buff=0.8)

        dot_radius_small = 0.02
        total_points3 = 10
        batch_size_square = 5
        border_offset3 = 0.005

        self.add(square, inner_square, frac_counter3, prob_group3)

        half_side = side_length / 2
        inside_count3 = 0
        total_count3 = 0
        temp_batch = []
        dots_group = VGroup()

        for i in range(1, total_points3 + 1):
            x = random.uniform(-half_side, half_side)
            y = random.uniform(-half_side, half_side)
            pt = [x, y, 0]

            if -inner_side / 2 <= x <= inner_side / 2 and -inner_side / 2 <= y <= inner_side / 2:
                inside_count3 += 1
                inner_color = GREEN
            else:
                inner_color = RED

            outer = Dot(pt, color=BLACK, radius=dot_radius_small + border_offset3)
            inner = Dot(pt, color=inner_color, radius=dot_radius_small)
            dot = VGroup(outer, inner)
            dots_group.add(dot)

            total_count3 += 1
            est_prob3 = inside_count3 / total_count3

            frac_counter3.become(
                MathTex(
                    rf"\frac{{{inside_count3}}}{{{total_count3}}}",
                    font_size=36,
                    color=BLACK
                ).to_corner(UL, buff=0.8)
            )
            prob_value3.set_value(est_prob3)

            temp_batch.append(dot)

            if len(temp_batch) == batch_size_square or i == total_points3:
                self.add(*temp_batch)
                self.wait(0.01)
                temp_batch = []

        self.add(dots_group)
        self.wait(1)
