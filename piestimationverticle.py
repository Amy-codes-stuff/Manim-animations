from manim import *
import random
import numpy as np

# Orientation change for vertical video (YouTube Shorts)
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 16.0
config.frame_width = 9.0
config.background_color = WHITE

dark_green = ManimColor('#006400')
dark_green1 = ManimColor('#80EF80')
dark_red = ManimColor('#FF2C2C')

class PiEstimationFullVideo(Scene):
    def construct(self):

        square_side = 4
        circle_radius = square_side / 2

        square = Square(side_length=square_side, color=BLACK, stroke_width=3)
        square_label = Tex("Square", font_size=35, color=BLACK).next_to(square, UP)

        circle = Circle(radius=circle_radius, color=BLUE, stroke_width=3)
        circle_label = Tex("Inscribed Circle", font_size=35, color=BLACK).next_to(circle, DOWN)

        self.play(Create(circle), Write(circle_label), Create(square), Write(square_label))

        radius_line = Line(circle.get_center(), circle.get_right(), color=RED, stroke_width=2)
        radius_label = MathTex("r", font_size=35, color=BLACK).next_to(radius_line, UP)

        side_line_left = Line(square.get_corner(UL), square.get_corner(DL), color=GREEN, stroke_width=2)
        side_label_left = MathTex("2r", font_size=35, color=BLACK).next_to(side_line_left, LEFT)
        self.play(Create(radius_line), Write(radius_label), Create(side_line_left), Write(side_label_left), run_time=0.5)

        group_objects = VGroup(square, circle, radius_line, radius_label, side_line_left, side_label_left, square_label, circle_label)
        self.play(group_objects.animate.shift(UP * 4))

        text_area_intro = Text("Let's look at their areas...", font_size=40, color=BLACK).next_to(group_objects,DOWN, buff=1)
        self.play(Write(text_area_intro), run_time = 0.5)
        self.play(FadeOut(text_area_intro))

        area_circle_formula = MathTex(
            "A_{\\text{circle}} = \\pi r^2",
            font_size=45, color=BLACK
        ).next_to(group_objects,DOWN, buff=1, aligned_edge=LEFT).shift(RIGHT*0.5)

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

        self.play(FadeOut(area_circle_formula, area_square_formula, ratio_formula,
                            simplified_ratio, radius_line, radius_label, side_line_left, side_label_left, pi_formula))

        # Shift the geometric group down to prepare for point plotting
        geo_group = VGroup(square, circle, square_label, circle_label) # Include labels in the group that moves
        self.play(geo_group.animate.shift(DOWN * 4), run_time = 0.75)
        self.wait(0.7)

        # --- Counter in LaTeX frac format ---
        inside_points = 0
        frac_counter = MathTex(r"\frac{0}{0}", font_size=36, color=dark_green).next_to(square.get_corner(UL),(LEFT+UP), buff = 1)
        self.add(frac_counter) # Add the new frac_counter

        pi_value = DecimalNumber(0, num_decimal_places=4, color=RED, font_size=40).next_to(square.get_corner(DR),(RIGHT + DOWN), buff = 1)
        pi_label = Text("π ≈ ", font_size=40, color=RED).next_to(pi_value, LEFT, buff=0.2)

        pi_group = VGroup(pi_value, pi_label)
        self.add(pi_group)

        total_points = 1000
        batch_size = 500
        all_dots = VGroup()
        

        for i in range(0, total_points, batch_size):
            animations = []
            current_batch_count = min(batch_size, total_points - i) # Ensure last batch doesn't exceed total_points

            for _ in range(current_batch_count):
                x = random.uniform(-circle_radius, circle_radius)
                y = random.uniform(-circle_radius, circle_radius)
                point_coords = [x, y, 0] # Points are generated relative to the center (0,0,0)

                dot = Dot(point=point_coords, radius=0.025)

                # Check if point is inside the circle
                if x**2 + y**2 <= circle_radius**2:
                    dot.set_color(dark_green1)
                    inside_points += 1
                else:
                    dot.set_color(dark_red)

                all_dots.add(dot)
                animations.append(Create(dot))

            self.play(*animations, run_time=0.05, rate_func=linear)

            current_total = i + current_batch_count # Calculate total points plotted so far

            # Update the MathTex fraction counter
            new_frac_counter = MathTex(
                r"\frac{" + f"{inside_points}" + r"}{" + f"{current_total}" + r"}",
                font_size=36,
                color=dark_green
            ).move_to(frac_counter.get_center()) # Keep its position

            self.play(Transform(frac_counter, new_frac_counter), run_time=0.1) # Animate the update
            
            # Update pi value based on the current count
            if current_total > 0: # Avoid division by zero
                pi_value.set_value(4 * inside_points / current_total)
            else:
                pi_value.set_value(0) # Or keep it at 0 if no points yet

        self.wait(0.5)
        # Fade out all dots, geometric shapes, and the fraction counter
        self.play(FadeOut(all_dots, geo_group, frac_counter))
        self.wait(0.25)

        # Move the pi estimation to the center and scale it
        self.play(pi_group.animate.move_to(ORIGIN).scale(2.5), run_time=1.5) # Adjusted scale for better visibility
        self.wait(1)
        self.play(FadeOut(*self.mobjects))