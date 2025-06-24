from manim import *
import random
import numpy as np
config.background_color = WHITE
dark_green = ManimColor('#006400')
dark_red = ManimColor('#C4150C')

class PiEstimationFullVideo(Scene):
    def construct(self):

        square_side = 4
        circle_radius = square_side / 2

        square = Square(side_length=square_side, color=DARK_BLUE, stroke_width=3)
        square_label = Tex("Square", font_size=35, color=BLACK).next_to(square, UP)

        circle = Circle(radius=circle_radius, color=RED, stroke_width=3)
        circle_label = Tex("Inscribed Circle", font_size=35, color=BLACK).next_to(circle, DOWN)

        self.play(Create(circle), Write(circle_label), Create(square), Write(square_label))

        radius_line = Line(circle.get_center(), circle.get_right(), color=RED, stroke_width=2)
        radius_label = MathTex("r", font_size=35, color=BLACK).next_to(radius_line, UP)

        side_line_left = Line(square.get_corner(UL), square.get_corner(DL), color=GREEN, stroke_width=2)
        side_label_left = MathTex("2r", font_size=35, color=BLACK).next_to(side_line_left, LEFT)
        self.play(Create(radius_line), Write(radius_label), Create(side_line_left), Write(side_label_left), run_time=0.5)

        group_objects = VGroup(square, circle, radius_line, radius_label, side_line_left, side_label_left, square_label, circle_label)
        self.play(group_objects.animate.shift(LEFT * 3))

        text_area_intro = Text("Let's look at their areas...", font_size=40, color=BLACK).next_to(group_objects, RIGHT, buff=1)
        self.play(Write(text_area_intro), run_time = 0.5)
        self.play(FadeOut(text_area_intro))

        area_circle_formula = MathTex(
            "A_{\\text{circle}} = \\pi r^2",
            font_size=45, color=BLACK
        ).next_to(group_objects, RIGHT, buff=1, aligned_edge=UP)

        area_square_formula = MathTex(
            "A_{\\text{square}} = (2r)^2 = 4r^2",
            font_size=45, color=BLACK
        ).next_to(area_circle_formula, DOWN, aligned_edge=LEFT)
        self.play(Write(area_circle_formula), Write(area_square_formula))
        self.wait(0.3)

        ratio_formula = MathTex(
            "\\frac{A_{\\text{circle}}}{A_{\\text{square}}} = \\frac{\\pi r^2}{4r^2}",
            font_size=45, color=BLACK
        ).next_to(area_square_formula, DOWN, aligned_edge=LEFT, buff=0.7)
        self.play(Write(ratio_formula))

        simplified_ratio = MathTex(
            "= \\frac{\\pi}{4}",
            font_size=45, color=DARK_BLUE
        ).next_to(ratio_formula, RIGHT, buff=0.2)
        self.play(Write(simplified_ratio))
        self.wait(0.3)

        pi_formula = MathTex(
            "\\pi = 4 \\times \\frac{A_{\\text{circle}}}{A_{\\text{square}}}",
            font_size=50, color=DARK_BLUE
        ).next_to(ratio_formula, DOWN, aligned_edge=LEFT, buff=0.7)
        self.play(Write(pi_formula))
        self.wait(0.5)

        self.play(FadeOut(area_circle_formula,area_square_formula, ratio_formula,
                           simplified_ratio, radius_line, radius_label, side_line_left, side_label_left, square_label, circle_label, pi_formula ))



        geo_group = VGroup(square, circle)
        self.play(geo_group.animate.shift(RIGHT * 3), run_time = 0.75)
        self.wait(0.7)



        inside_counter = Integer(0, font_size=36).to_corner(UL).set_color(dark_green)
        equal_sign = Text("/", font_size=36, color=BLACK).next_to(inside_counter, RIGHT, buff=0.8)
        total_counter = Integer(0, font_size=36).next_to(equal_sign, RIGHT, buff=0.2).set_color(BLACK)

        self.add(inside_counter, equal_sign, total_counter)

        pi_value = DecimalNumber(0, num_decimal_places=4, color=RED, font_size=40).to_corner(DR)
        pi_label = Text("π ≈ ", font_size=40, color=RED).next_to(pi_value, LEFT, buff=0.2)

        pi_group = VGroup(pi_value, pi_label)

        self.add(pi_group)

        total_points = 10000  # Increase for more accuracy
        batch_size = 100       # Batch animation
        all_dots = VGroup()
        inside_points = 0

        for i in range(0, total_points, batch_size):
            animations = []
            batch_inside = 0 #count inside points

            for _ in range(batch_size):
                x = random.uniform(-circle_radius, circle_radius)
                y = random.uniform(-circle_radius, circle_radius)
                point_coords = [x, y, 0]
                dot = Dot(point=point_coords, radius=0.025)

                if x**2 + y**2 <= circle_radius**2:
                    dot.set_color(dark_green)
                    inside_points += 1
                    
                else:
                    dot.set_color(dark_red)

                all_dots.add(dot)
                animations.append(Create(dot))

            self.play(*animations, run_time=0.05, rate_func=linear)

            # Update every batch (not every point for performance)

            current_total = min(i + batch_size, total_points)
            total_counter.set_value(current_total)
            inside_counter.set_value(inside_points)
            pi_value.set_value(4 * inside_points / (i + batch_size))

        self.wait(0.5)
        self.play(FadeOut(all_dots, geo_group, inside_counter, total_counter, equal_sign))
        self.wait(0.25)

        self.play(pi_group.animate.move_to(ORIGIN).scale(3),run_time=1.5)
        self.wait(1)
        self.play(FadeOut(*self.mobjects))