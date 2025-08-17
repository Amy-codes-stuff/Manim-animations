from manim import *
import math
import random
import numpy as np
config.background_color = WHITE

class GeometricProbabilityLineandaquare(Scene):
    def construct(self):
        total_points_large = 500   #line
        total_points_small = 20
        full_length = 6
        target_length = 2
        half_full = full_length / 2
        half_target = target_length / 2

        dot_radius = 0.07
        border_offset = 0.01
        total_points3 = 1000   #square
        side_length = 3.2
        half_side = side_length / 2
        inner_side = side_length / 2
        dot_radius_small = 0.07
        border_offset3 = 0.01

        batch_size_line = 1     # For 500 points on the line
        batch_size_square = 20

        growing_rect = Rectangle(width=side_length, height=0.001, color=BLACK, stroke_width=6).move_to(ORIGIN)
        

        # STEP 1: Draw main line
        main_line = Line(LEFT * half_full, RIGHT * half_full, color=BLACK, stroke_width=5.5)
        line_label = MathTex(r"\textbf{A~line}").scale(0.8).next_to(main_line, UP * 0.8)
        self.play(Create(main_line),FadeIn(line_label))
        self.add(growing_rect) 
        self.wait(0.8)

        # STEP 2: Highlight target region
        target_segment = Line(LEFT * half_target, RIGHT * half_target, color=BLUE, stroke_width=10).move_to(ORIGIN)
        target_label = MathTex(r"Target~region").scale(0.7).set_color(BLUE).next_to(target_segment, DOWN * 0.8)
        self.play(Create(target_segment), FadeIn(target_label))
        self.wait(0.8)

        # STEP 3: Place FIRST random point
        first_x = 0.75 * half_full
        first_outer = Dot([first_x, 0, 0], color=BLACK, radius=dot_radius + border_offset)
        first_inner = Dot([first_x, 0, 0], color=RED, radius=dot_radius)
        first_dot = VGroup(first_outer, first_inner)
        self.play(FadeIn(first_dot))

        # Label for the first random point
        if -half_target <= first_x <= half_target:
            first_text = MathTex(r"Inside~target~region").scale(0.7).set_color(GREEN).next_to(first_dot, UP * 1.2)
        else:
            first_text = MathTex(r"Outside~target~region").scale(0.7).set_color(RED).next_to(first_dot, UP * 1.2)

        self.play(FadeIn(first_text))
        self.wait(1.2)
        self.play(FadeOut(first_text))

        # STEP 4: Fire 20 random points
        firing_text = MathTex(r"\textbf{Firing~20~random~points...}").scale(0.7).to_corner(UL)
        self.play(FadeIn(firing_text))

        dots_group = VGroup(first_dot)
        inside_20 = 1 if -half_target <= first_x <= half_target else 0

        for _ in range(total_points_small - 1):
            x = random.uniform(-half_full, half_full)
            pt = [x, 0, 0]

            if -half_target <= x <= half_target:
                inside_20 += 1
                inner_color = GREEN
            else:
                inner_color = RED

            outer = Dot(pt, color=BLACK, radius=dot_radius + border_offset)
            inner = Dot(pt, color=inner_color, radius=dot_radius)
            dot = VGroup(outer, inner)
            dots_group.add(dot)
            self.play(FadeIn(dot), run_time=0.03)
 
        self.wait(0.5)

        # Combine and shift everything

        line_content = VGroup(main_line,growing_rect, target_segment, target_label,dots_group)
        line_content.save_state()
        self.play(line_content.animate.shift(LEFT * 3).scale(0.9))

   

        true_prob = target_length / full_length
        true_prob_text = Tex(
            rf"$P = \dfrac{{\text{{Length of target}}}}{{\text{{Total length}}}} = "
            rf"\dfrac{{{target_length}}}{{{full_length}}} = {true_prob:.2f}$",
            color=BLACK
        ).scale(0.9).next_to(main_line, RIGHT, buff=2.75, aligned_edge=LEFT).shift(UP*2) # closer to the line
        self.play(Write(true_prob_text))
        self.wait(1.5)

        # === STEP 5: Show FIRST probability (near top but not hugging edge) ===
        empirical_prob_20 = inside_20 / total_points_small
        empirical_text = Tex(
            rf"$P = \dfrac{{{inside_20}}}{{20}} \approx {empirical_prob_20:.2f}$",
            color=BLACK
        ).scale(0.9).next_to(true_prob_text,DOWN , buff=1.0,aligned_edge= LEFT)  # slightly below top edge
        self.play(Write(empirical_text))
        self.wait(1)

        # STEP 8: Clear all 20 dots before 500-shot simulation
        self.play( FadeOut(true_prob_text), FadeOut(empirical_text))
        self.play(Succession(
    line_content.animate.shift(RIGHT * 3),
    Restore(line_content)
))
        self.play(FadeOut(firing_text), FadeOut(dots_group))
        

        # STEP 9: Setup proper fraction counter for 500 simulation
        inside_count = 0
        total_count = 0

        # Proper fraction counter in fraction style
        counter_tex = MathTex(r"\frac{0}{0}", color=BLACK).scale(1.2).to_corner(UL, buff=0.8)

        # TOP-RIGHT: live probability
        prob_value = DecimalNumber(0, num_decimal_places=3, color=RED, font_size=36).to_corner(UR, buff=0.6)
        prob_label = MathTex(r"P =", font_size=36, color=RED).next_to(prob_value, LEFT, buff=0.2)

        self.add(counter_tex, prob_label, prob_value)
        self.wait(0.5)

        # STEP 10: Fire 500 points on the shifted line
        for i in range(1, total_points_large + 1, batch_size_line):
            dot_group = VGroup()
            for j in range(batch_size_line):
                if i + j > total_points_large:
                    break
                x = random.uniform(-half_full, half_full)
                pt = [x, 0, 0]

                if -half_target <= x <= half_target:
                    inside_count += 1
                    outer = Dot(pt, color=BLACK, radius=dot_radius + border_offset)
                    inner = Dot(pt, color=GREEN, radius=dot_radius)
                else:
                    outer = Dot(pt, color=BLACK, radius=dot_radius + border_offset)
                    inner = Dot(pt, color=RED, radius=dot_radius)

                dot = VGroup(outer, inner)
                dot_group.add(dot)
                total_count += 1

            est_prob = inside_count / total_count
            counter_tex.become(
                MathTex(
                    rf"\frac{{{inside_count}}}{{{total_count}}}",
                    color=BLACK
                ).scale(1.2).to_corner(UL, buff=0.8)
            )
            prob_value.set_value(est_prob)
            self.add(dot_group)
            self.wait(0.01)

        # STEP 11: Final probability closer below the line
        final_prob_text = Tex(
            rf"After 500 points: $P = \dfrac{{{inside_count}}}{{500}} \approx {inside_count/500:.3f}$",
            color=BLACK
        ).scale(0.9).next_to(main_line, DOWN, buff=0.8)  # reduced blank space below
        self.play(Write(final_prob_text))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects if mob != growing_rect])
        self.wait(0.5)



        
        self.play(growing_rect.animate.stretch_to_fit_height(side_length), run_time=2, rate_func=smooth)
        square = Square(side_length=side_length, color=BLACK, stroke_width=6).move_to(ORIGIN)
        self.play(Transform(growing_rect, square))
        square_label = MathTex(r"\textbf{Square~side} = " + str(side_length)).scale(0.8).next_to(square, UP)
        self.play(FadeIn(square_label))
        self.wait(0.8)

        inner_square = Square(side_length=inner_side, color=BLUE).move_to(ORIGIN)
        self.play(Create(inner_square))
        self.wait(0.8)

        inside_count3 = 0
        total_count3 = 0

        # Use LaTeX-style fraction
        frac_counter3 = MathTex(r"\frac{%d}{%d}" % (inside_count3, total_count3 if total_count3 != 0 else 1), font_size=36, color=BLACK)
        frac_counter3.to_corner(UL, buff=0.8)

        # Probability value and label
        prob_value3 = DecimalNumber(0, num_decimal_places=3, color=RED, font_size=36).to_corner(UR, buff=0.8)
        prob_label3 = MathTex(r"P =", font_size=36, color=RED).next_to(prob_value3, LEFT, buff=0.2)

        self.add(frac_counter3, prob_label3, prob_value3)

        self.wait(0.5)

        dots_group = VGroup()  # Collect all dots here

        for i in range(1, total_points3 + 1, batch_size_square):
            batch_group = VGroup()
            for j in range(batch_size_square):
                if i + j > total_points3:
                    break
                x = random.uniform(-half_side, half_side)
                y = random.uniform(-half_side, half_side)
                pt = [x, y, 0]
                if -inner_side/2 <= x <= inner_side/2 and -inner_side/2 <= y <= inner_side/2:
                    inside_count3 += 1
                    inner_color = GREEN
                else:
                    inner_color = RED

                total_count3 += 1
                outer = Dot(pt, color=BLACK, radius=dot_radius_small + border_offset3)
                inner = Dot(pt, color=inner_color, radius=dot_radius_small)
                dot = VGroup(outer, inner)
                batch_group.add(dot)
                dots_group.add(dot)

            est_prob3 = inside_count3 / total_count3
            frac_counter3.become(
                MathTex(rf"\frac{{{inside_count3}}}{{{total_count3}}}", font_size=36, color=BLACK).to_corner(UL, buff=0.8)
            )
            prob_value3.set_value(est_prob3)

            self.add(batch_group)
            self.wait(0.01)

        squaregroup = VGroup(growing_rect, inner_square,dots_group)
        self.play(squaregroup.animate.shift(LEFT*2.5))

        theoretical_prob = (inner_side ** 2) / (side_length ** 2)
        experimental_prob = inside_count3 / total_points3
        theoretical_text = Tex(
    rf"$P = \dfrac{{\text{{Inner area}}}}{{\text{{Outer area}}}} = "
    rf"\dfrac{{{inner_side}^2}}{{{side_length}^2}} = {theoretical_prob:.2f}$",
    color=BLACK
).scale(0.7).next_to(square, RIGHT, buff = 0.5).shift(LEFT+UP)

        experimental_text = Tex(
            rf" $P \approx \dfrac{{\text{{Inner points}}}}{{\text{{Total points}}}} = "
            rf"\dfrac{{{inside_count3}}}{{{total_points3}}} = {experimental_prob:.3f}$",
            color=BLACK
        ).scale(0.7).next_to(theoretical_text, DOWN, buff=1.0).align_to(theoretical_text, LEFT)
        self.remove(square_label)
        self.play(Write(theoretical_text))
        self.play(Write(experimental_text))
        self.wait(3)
        self.play(FadeOut(*self.mobjects)) 