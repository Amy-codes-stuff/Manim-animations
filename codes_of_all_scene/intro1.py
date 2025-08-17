from manim import *
import math
import random
import numpy as np

# Configuration - Apply once for the whole video
config.background_color = WHITE

class IntroductionScene(Scene):
    EPSILON = 1e-9

    def construct(self):
        # --- Dot Style Parameters (Applied throughout the animation) ---
        # The original radius was 0.025. This new style uses a slightly larger, bordered dot.
        dot_inner_radius = 0.07
        dot_border_offset = 0.01

        # --- Start Scene 1: Introduction (from intro.py) ---
        # ... (No changes in this section)
        title = MathTex(r"\text{What is } \pi?", font_size=60, color=BLUE).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeOut(title))

        # === STEP 1: Start with a big base circle (radius=2) ===
        base_circle = Circle(radius=2, color=BLUE, stroke_width=6)
        diameter_line = Line(base_circle.get_left(), base_circle.get_right(), color=PURPLE)
        diameter_label = MathTex(r"\text{Diameter}", font_size=30, color=BLACK).next_to(diameter_line, DOWN)
        circlegroup = VGroup(base_circle,diameter_label, diameter_line)
        self.play(Create(base_circle), Create(diameter_line), Write(diameter_label))
        self.wait(1)

        # === STEP 2: Compute fitted radius so straightened circumference fits ===
        frame_w = config.frame_width    # e.g. 9.0
        margin_ratio = 0.8              # leave 10% margin on each side
        max_line_length = frame_w * margin_ratio
        fit_radius = max_line_length / (2 * math.pi)  # ensures line fits inside frame

        # Shrink BOTH base circle + diameter to the fit radius
        shrink_factor = fit_radius / 2.0  # since initial radius was 2
        self.play(
            base_circle.animate.scale(shrink_factor),
            diameter_line.animate.scale(shrink_factor),
            diameter_label.animate.scale(shrink_factor),
            run_time=0.8
        )

        # AFTER scaling → NOW draw the circumference border with gradient
        outer_border = (
            Circle(radius=fit_radius+0.05, stroke_width=7,color=RED)
               # nice gradient for the circumference
            .rotate(90 * DEGREES, Z_AXIS)           # like your StraighteningCircle example
            .move_to(base_circle.get_center())
        )
        self.play(DrawBorderThenFill(outer_border))
        self.wait(0.5)

        # After shrinking, recalc circumference length for final fitted radius
        circum_length = 2 * math.pi * fit_radius

        # === STEP 3: Prepare straight line (same gradient color) ===
        straight_line = Line(color=RED,
            start=[-circum_length / 2, 0, 0],
            end=[circum_length / 2, 0, 0],
            stroke_width=6
        ).move_to(DOWN * 1.5)

        # Pause before transformation
        self.wait()

        # === STEP 4: Smooth transformation (like StraighteningCircle) ===
        self.play(
            ReplacementTransform(outer_border, straight_line),
            circlegroup.animate.shift(UP * 0.5)
            )

        self.wait()

        # Add label below straightened circumference
        circum_text = MathTex(r"\text{Circumference}", font_size=34, color=BLACK).next_to(straight_line, DOWN, buff=0.2)
        self.play(Write(circum_text))
        self.wait(0.5)

        # Explanation text
        pi_intro = MathTex(r"\text{This distance is called the circumference...}", font_size=34, color=BLACK)
        pi_intro.next_to(base_circle, UP * 5)

        pi_hint = MathTex(r"\text{And it's closely tied to a special number: } \pi", font_size=34, color=BLUE_D)
        pi_hint.next_to(pi_intro, DOWN, buff=0.5)

        self.play(Write(pi_intro))
        self.play(Write(pi_hint))

        # Remove inner circle and diameter after explanation
        self.play(FadeOut(base_circle, diameter_line, diameter_label, pi_hint, pi_intro))
        self.wait(0.25)

        # Move unwrapped line to center
        cir_group = VGroup(straight_line, circum_text)
        self.play(cir_group.animate.move_to(ORIGIN))

        # Show formula
        formula = MathTex(r"C = \pi d", font_size=50, color=BLACK)
        formula.next_to(straight_line, UP, buff=0.5)
        self.play(Write(formula))
        self.wait(0.5)

        # Show value of π
        pi_value = MathTex(r"\pi \approx 3.14159265", font_size=40, color=BLUE)
        pi_value.next_to(circum_text, DOWN, buff=0.4)
        self.play(Write(pi_value))
        self.wait(0.5)

        # Transition
        self.play(FadeOut(straight_line, formula, circum_text))
        self.play(pi_value.animate.move_to(ORIGIN).scale(2))
        self.wait(3)
        self.play(FadeOut(*self.mobjects))