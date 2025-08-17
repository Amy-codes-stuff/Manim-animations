from manim import *
import math
import random
import numpy as np

config.background_color = WHITE


class FullAnimationFlow(Scene):
    # Define a small epsilon for floating-point comparisons, accessible throughout the combined scene
    EPSILON = 1e-9

    def construct(self):
        square_side_pi = 4
        circle_radius_pi = square_side_pi / 2
        dot_inner_radius = 0.07
        dot_border_offset = 0.01

        square_pi = Square(side_length=square_side_pi, color=BLACK, stroke_width=3)
        square_label_pi = Tex("Square", font_size=35, color=BLACK).next_to(square_pi, UP)
        circle_pi = Circle(radius=circle_radius_pi, color=BLUE, stroke_width=3)
        circle_label_pi = Tex("Inscribed Circle", font_size=35, color=BLACK).next_to(circle_pi, DOWN)
        self.play(Create(circle_pi), Write(circle_label_pi), Create(square_pi), Write(square_label_pi))

        radius_line_pi = Line(circle_pi.get_center(), circle_pi.get_right(), color=RED, stroke_width=2)
        radius_label_pi = MathTex("r", font_size=35, color=BLACK).next_to(radius_line_pi, UP)
        side_line_left_pi = Line(square_pi.get_corner(UL), square_pi.get_corner(DL), color=GREEN, stroke_width=2)
        side_label_left_pi = MathTex("2r", font_size=35, color=BLACK).next_to(side_line_left_pi, LEFT)
        self.play(Create(radius_line_pi), Write(radius_label_pi), Create(side_line_left_pi), Write(side_label_left_pi), run_time=0.5)

        group_objects_pi = VGroup(square_pi, circle_pi, radius_line_pi, radius_label_pi, side_line_left_pi, side_label_left_pi, square_label_pi, circle_label_pi)
        self.play(group_objects_pi.animate.shift(LEFT * 4))

        # ... (Area formulas part remains the same)
        text_area_intro_pi = Text("Let's look at their areas...", font_size=40, color=BLACK).next_to(group_objects_pi,RIGHT, buff=1)
        self.play(Write(text_area_intro_pi), run_time = 0.5)
        self.play(FadeOut(text_area_intro_pi))
        area_circle_formula_pi = MathTex(
    "A_{\\text{circle}} = \\pi r^2",
    font_size=45,
    color=BLACK
).next_to(group_objects_pi, RIGHT, buff=1.5).align_to(group_objects_pi, UP)
        area_square_formula_pi = MathTex("A_{\\text{square}} = (2r)^2 = 4r^2", font_size=45, color=BLACK).next_to(area_circle_formula_pi, DOWN, aligned_edge=LEFT)
        self.play(Write(area_circle_formula_pi), Write(area_square_formula_pi)); self.wait(0.3)
        ratio_formula_pi = MathTex("\\frac{A_{\\text{circle}}}{A_{\\text{square}}} = \\frac{\\pi r^2}{4r^2}", font_size=45, color=BLACK).next_to(area_square_formula_pi, DOWN, aligned_edge=LEFT, buff=0.7)
        self.play(Write(ratio_formula_pi))
        simplified_ratio_pi = MathTex("= \\frac{\\pi}{4}", font_size=45, color=DARK_BLUE).next_to(ratio_formula_pi, RIGHT, buff=0.2)
        self.play(Write(simplified_ratio_pi)); self.wait(0.3)
        pi_formula_pi = MathTex("\\pi = 4 \\times \\frac{A_{\\text{circle}}}{A_{\\text{square}}}", font_size=50, color=DARK_BLUE).next_to(ratio_formula_pi, DOWN, aligned_edge=LEFT, buff=0.7)
        self.play(Write(pi_formula_pi)); self.wait(0.5)
        self.play(FadeOut(area_circle_formula_pi, area_square_formula_pi, ratio_formula_pi, simplified_ratio_pi, radius_line_pi, radius_label_pi, side_line_left_pi, side_label_left_pi, pi_formula_pi))

        geo_group_pi = VGroup(square_pi, circle_pi, square_label_pi, circle_label_pi)
        self.play(geo_group_pi.animate.shift(RIGHT * 4), run_time=0.75)
        self.wait(0.7)

        inside_points_pi = 0
        frac_counter_pi = MathTex(r"\frac{0}{0}", font_size=36, color=GREEN).next_to(square_pi.get_corner(UL),(LEFT+UP), buff = 1)
        self.add(frac_counter_pi)
        pi_value_display_pi = DecimalNumber(0, num_decimal_places=4, color=RED, font_size=40).next_to(square_pi.get_corner(DR),(RIGHT + DOWN), buff = 1)
        pi_label_display_pi = Text("π \u2248 ", font_size=40, color=RED).next_to(pi_value_display_pi, LEFT, buff=0.2)
        pi_group_display_pi = VGroup(pi_value_display_pi, pi_label_display_pi)
        self.add(pi_group_display_pi)

        total_points_pi = 1000
        batch_size_pi = 5
        all_dots_pi = VGroup()
        
        for i in range(0, total_points_pi, batch_size_pi):
            animations = []
            current_batch_count_pi = min(batch_size_pi, total_points_pi - i)

            for _ in range(current_batch_count_pi):
                x, y = random.uniform(-circle_radius_pi, circle_radius_pi), random.uniform(-circle_radius_pi, circle_radius_pi)
                point_coords_pi = [x, y, 0]

                if x**2 + y**2 <= circle_radius_pi**2:
                    inner_color = GREEN; inside_points_pi += 1
                else: inner_color = RED
                
                # ✅ CHANGED
                outer_dot = Dot(point=point_coords_pi, radius=dot_inner_radius + dot_border_offset, color=BLACK)
                inner_dot = Dot(point=point_coords_pi, radius=dot_inner_radius, color=inner_color)
                dot_pi = VGroup(outer_dot, inner_dot)

                all_dots_pi.add(dot_pi)
                animations.append(Create(dot_pi))

            self.play(*animations, run_time=0.05, rate_func=linear)
            current_total_pi = i + current_batch_count_pi
            new_frac_counter_pi = MathTex(rf"\frac{{{inside_points_pi}}}{{{current_total_pi}}}", font_size=36, color=GREEN).move_to(frac_counter_pi.get_center())
            self.play(Transform(frac_counter_pi, new_frac_counter_pi), run_time=0.1)
            
            if current_total_pi > 0: pi_value_display_pi.set_value(4 * inside_points_pi / current_total_pi)
            else: pi_value_display_pi.set_value(0)

        self.wait(0.5)
        self.play(FadeOut(all_dots_pi, geo_group_pi, frac_counter_pi)); self.wait(0.25)
        self.play(pi_group_display_pi.animate.move_to(ORIGIN).scale(2.5), run_time=1.5); self.wait(1)
        self.play(FadeOut(pi_group_display_pi)); self.wait(1)