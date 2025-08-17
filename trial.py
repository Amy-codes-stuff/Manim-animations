from manim import *
import math
import random
import numpy as np

# Configuration - Apply once for the whole video
config.background_color = WHITE

# Re-define common colors
# GREEN = ManimColor('#006400')
# GREEN1 = ManimColor('#80EF80') # From piestimationverticle.py
# RED = ManimColor('#C4150C')
# DARK_BLUE = ManimColor("#00008B") # Defined missing color in previous snippets

class FullAnimation1(Scene):
    # Define a small epsilon for floating-point comparisons, accessible throughout the combined scene
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


        total_points_large = 500
        total_points_small = 20
        full_length = 6
        target_length = 2
        half_full = full_length / 2
        half_target = target_length / 2

        dot_radius = 0.07
        border_offset = 0.01
        total_points3 = 500
        side_length = 3.2
        half_side = side_length / 2
        inner_side = side_length / 2
        dot_radius_small = 0.07
        border_offset3 = 0.01

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
        for i in range(1, total_points_large + 1):
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
            total_count += 1
            est_prob = inside_count / total_count

            # Proper stacked fraction update
            counter_tex.become(
                MathTex(
                    rf"\frac{{{inside_count}}}{{{total_count}}}",
                    color=BLACK
                ).scale(1.2).to_corner(UL, buff=0.8)
            )
            prob_value.set_value(est_prob)

            self.add(dot)
            if i % 5 == 0 or i == total_points_large:
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

        for i in range(1, total_points3 + 1):
            x = random.uniform(-half_side, half_side)
            y = random.uniform(-half_side, half_side)
            pt = [x, y, 0]
            if -inner_side/2 <= x <= inner_side/2 and -inner_side/2 <= y <= inner_side/2:
                inside_count3 += 1
                inner_color = GREEN
            else:
                inner_color = RED

            total_count3 += 1
            est_prob3 = inside_count3 / total_count3

            frac_counter3.become(
                MathTex(rf"\frac{{{inside_count3}}}{{{total_count3}}}", font_size=36, color=BLACK).to_corner(UL, buff=0.8)
            )
            prob_value3.set_value(est_prob3)

            outer = Dot(pt, color=BLACK, radius=dot_radius_small + border_offset3)
            inner = Dot(pt, color=inner_color, radius=dot_radius_small)
            dot = VGroup(outer, inner)
            self.add(dot)
            dots_group.add(dot)  # Add to group

            if i % 5 == 0 or i == total_points3:
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


        
        
        # --- Start Scene 3: MonteCarloShapes ---
        square_side_mc = 3
        half_side_mc = square_side_mc / 2
        total_points_mc = 500
        batch_size_mc = 5

        # Setup for 1st Example (Left: Square & Triangle)
        square1_pos_mc = LEFT * 4.5
        square1_mc = Square(side_length=square_side_mc, color=BLACK).move_to(square1_pos_mc)
        bottom_left_1_mc = square1_mc.get_corner(DL)
        bottom_right_1_mc = square1_mc.get_corner(DR)
        top_mid_1_mc = square1_mc.get_top()
        triangle1_mc = Polygon(bottom_left_1_mc, bottom_right_1_mc, top_mid_1_mc, color=BLUE, fill_opacity=0.3)
        base_line_1_mc = Line(bottom_left_1_mc, bottom_right_1_mc, color=RED)
        #base_label_1_mc = MathTex(f"{square_side_mc}", font_size=28, color=RED).next_to(base_line_1_mc, DOWN)
        inside_triangle_count_mc = 0
        frac_counter1_mc = MathTex(r"\frac{0}{0}", font_size=30, color=GREEN).next_to(square1_mc.get_corner(UL), (LEFT*0.5 + UP * 0.3), buff=1)
        prob_value1_mc = DecimalNumber(0, num_decimal_places=4, color=RED, font_size=36).next_to(square1_mc.get_corner(DL), (RIGHT + DOWN * 0.3), buff=1)
        prob_label1_mc = Text("Area \u2248 ", font_size=32, color=RED).next_to(prob_value1_mc, LEFT, buff=0.2)
        triangle_vertices_for_check_mc = [bottom_left_1_mc, bottom_right_1_mc, top_mid_1_mc]
        all_dots_list1_mc = []
        plotted_dots_group1_mc = VGroup()

        # Setup for 2nd Example (Middle: Nested Square Frame)
        outer_frame_boundary_side_2_mc = 2
        inner_void_side_2_mc = 1
        outermost_square_2_mc = Square(side_length=square_side_mc, color=BLACK)
        outer_frame_square_2_mc = Square(side_length=outer_frame_boundary_side_2_mc, color=BLACK)
        inner_void_square_2_mc = Square(side_length=inner_void_side_2_mc, color=WHITE, fill_opacity=1)
        frame_shape_2_mc = Difference(outer_frame_square_2_mc.copy(), inner_void_square_2_mc.copy()).set_color(BLUE).set_opacity(0.5)
        outermost_side_line_bottom_2_mc = Line(outermost_square_2_mc.get_corner(DL), outermost_square_2_mc.get_corner(DR), color=RED)
        # outermost_side_label_bottom_2_mc = MathTex(f"{square_side_mc}", font_size=28, color=RED).next_to(outermost_side_line_bottom_2_mc, DOWN)
        outer_frame_side_line_right_2_mc = Line(outer_frame_square_2_mc.get_corner(DR), outer_frame_square_2_mc.get_corner(UR), color=RED)
        outer_frame_side_label_right_2_mc = MathTex(f"{outer_frame_boundary_side_2_mc}", font_size=28, color=GREEN).next_to(outer_frame_side_line_right_2_mc, RIGHT)
        inner_void_side_line_top_2_mc = Line(inner_void_square_2_mc.get_corner(UL), inner_void_square_2_mc.get_corner(UR), color=RED)
        inner_void_side_label_top_2_mc = MathTex(f"{inner_void_side_2_mc}", font_size=28, color=DARK_BLUE).next_to(inner_void_side_line_top_2_mc, UP)
        inside_frame_count_mc = 0
        frac_counter2_mc = MathTex(r"\frac{0}{0}", font_size=30, color=GREEN).next_to(outermost_square_2_mc.get_corner(UL), (LEFT*0.5 + UP * 0.3), buff=1)
        prob_value2_mc = DecimalNumber(0, num_decimal_places=4, color=RED, font_size=36).next_to(outermost_square_2_mc.get_corner(DL), (RIGHT + DOWN*0.3), buff=1)
        prob_label2_mc = Text("Area \u2248 ", font_size=32, color=RED).next_to(prob_value2_mc, LEFT, buff=0.2)
        all_dots_list2_mc = []
        plotted_dots_group2_mc = VGroup()

        # Setup for 3rd Example (Right: Square & Diagonal Hexagon)
        square2_pos_mc = RIGHT * 4.5
        square2_mc = Square(side_length=square_side_mc, color=BLACK).move_to(square2_pos_mc)
        band_offset_mc = 0.5
        dl_3_mc, dr_3_mc, ul_3_mc, ur_3_mc = square2_mc.get_corner(DL), square2_mc.get_corner(DR), square2_mc.get_corner(UL), square2_mc.get_corner(UR)
        p1_3_mc, p2_3_mc, p3_3_mc = ul_3_mc, ul_3_mc + RIGHT * band_offset_mc, dr_3_mc + UP * band_offset_mc
        p4_3_mc, p5_3_mc, p6_3_mc = dr_3_mc, dr_3_mc + LEFT * band_offset_mc, ul_3_mc + DOWN * band_offset_mc
        hexagon3_mc = Polygon(p1_3_mc, p2_3_mc, p3_3_mc, p4_3_mc, p5_3_mc, p6_3_mc, color=BLUE, fill_opacity=0.3)
        base_line_3_mc = Line(dl_3_mc, dr_3_mc, color=RED)
        height_line_3_mc = Line(ul_3_mc, dl_3_mc, color=RED)
        # base_label_3_mc = MathTex(f"{square_side_mc}", font_size=28, color=RED).next_to(base_line_3_mc, DOWN)
        height_label_3_mc = MathTex(f"{square_side_mc}", font_size=28, color=RED).next_to(height_line_3_mc, LEFT)
        inside_hexagon_count_mc = 0
        frac_counter3_mc = MathTex(r"\frac{0}{0}", font_size=30, color=GREEN).next_to(square2_mc.get_corner(UL), (LEFT*0.5 + UP * 0.3), buff=1)
        prob_value3_mc = DecimalNumber(0, num_decimal_places=4, color=RED, font_size=36).next_to(square2_mc.get_corner(DL), (RIGHT + DOWN * 0.3), buff=1)
        prob_label3_mc = Text("Area \u2248 ", font_size=32, color=RED).next_to(prob_value3_mc, LEFT, buff=0.2)
        hexagon_vertices_for_check_mc = [v[:2] for v in hexagon3_mc.get_vertices()]
        all_dots_list3_mc = []
        plotted_dots_group3_mc = VGroup()

        # ... (is_inside functions remain the same)
        def is_inside_triangle(p, a, b, c):
            def det(p1, p2, p3): return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1])
            s1, s2, s3 = det(p, a, b), det(p, b, c), det(p, c, a)
            epsilon = 1e-9
            return (s1 >= -epsilon and s2 >= -epsilon and s3 >= -epsilon) or (s1 <= epsilon and s2 <= epsilon and s3 <= epsilon)
        def is_inside_frame(x, y, outer_half, inner_half): return (-outer_half <= x <= outer_half) and (-outer_half <= y <= outer_half) and not ((-inner_half <= x <= inner_half) and (-inner_half <= y <= inner_half))
        def is_inside_polygon(p, vertices):
            x, y = p; n = len(vertices); inside = False; p1x, p1y = vertices[0]
            for i in range(n + 1):
                p2x, p2y = vertices[i % n]
                if y > min(p1y, p2y) and y <= max(p1y, p2y) and x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters: inside = not inside
                p1x, p1y = p2x, p2y
            return inside

        # Animate initial setups
        self.play(
            Create(square1_mc), Create(triangle1_mc), Create(base_line_1_mc),
            Create(outermost_square_2_mc), Create(frame_shape_2_mc), Create(outermost_side_line_bottom_2_mc),
             Create(outer_frame_side_line_right_2_mc), Write(outer_frame_side_label_right_2_mc),
            Create(inner_void_side_line_top_2_mc), Write(inner_void_side_label_top_2_mc),
            Create(square2_mc), Create(hexagon3_mc), Create(base_line_3_mc), Create(height_line_3_mc),
            Write(height_label_3_mc)
        )
        self.wait(1)
        self.add(frac_counter1_mc, prob_label1_mc, prob_value1_mc, frac_counter2_mc, prob_label2_mc, prob_value2_mc, frac_counter3_mc, prob_label3_mc, prob_value3_mc)
        self.wait(0.5)

        # Main Simultaneous Point Dropping Loop
        for i in range(total_points_mc):
            # Example 1: Triangle (Left)
            point_coords_1_mc = np.array([random.uniform(-half_side_mc, half_side_mc), random.uniform(-half_side_mc, half_side_mc), 0]) + square1_pos_mc
            if is_inside_triangle(point_coords_1_mc, *triangle_vertices_for_check_mc):
                color1_mc = GREEN; inside_triangle_count_mc += 1
            else: color1_mc = RED
            # ✅ CHANGED
            outer1 = Dot(point=point_coords_1_mc, radius=dot_inner_radius + dot_border_offset, color=BLACK)
            inner1 = Dot(point=point_coords_1_mc, radius=dot_inner_radius, color=color1_mc)
            dot1_mc = VGroup(outer1, inner1)
            all_dots_list1_mc.append(dot1_mc); plotted_dots_group1_mc.add(dot1_mc)

            # Example 2: Frame (Middle)
            point_coords_2_mc = np.array([random.uniform(-half_side_mc, half_side_mc), random.uniform(-half_side_mc, half_side_mc), 0])
            if is_inside_frame(point_coords_2_mc[0], point_coords_2_mc[1], outer_frame_boundary_side_2_mc / 2, inner_void_side_2_mc / 2):
                color2_mc = GREEN; inside_frame_count_mc += 1
            else: color2_mc = RED
            # ✅ CHANGED
            outer2 = Dot(point=point_coords_2_mc, radius=dot_inner_radius + dot_border_offset, color=BLACK)
            inner2 = Dot(point=point_coords_2_mc, radius=dot_inner_radius, color=color2_mc)
            dot2_mc = VGroup(outer2, inner2)
            all_dots_list2_mc.append(dot2_mc); plotted_dots_group2_mc.add(dot2_mc)

            # Example 3: Hexagon (Right)
            point_coords_3_mc = np.array([random.uniform(-half_side_mc, half_side_mc), random.uniform(-half_side_mc, half_side_mc), 0]) + square2_pos_mc
            if is_inside_polygon(point_coords_3_mc[:2], hexagon_vertices_for_check_mc):
                color3_mc = GREEN; inside_hexagon_count_mc += 1
            else: color3_mc = RED
            # ✅ CHANGED
            outer3 = Dot(point=point_coords_3_mc, radius=dot_inner_radius + dot_border_offset, color=BLACK)
            inner3 = Dot(point=point_coords_3_mc, radius=dot_inner_radius, color=color3_mc)
            dot3_mc = VGroup(outer3, inner3)
            all_dots_list3_mc.append(dot3_mc); plotted_dots_group3_mc.add(dot3_mc)

            if (i + 1) % batch_size_mc == 0 or i == total_points_mc - 1:
                self.add(*all_dots_list1_mc, *all_dots_list2_mc, *all_dots_list3_mc)
                frac_counter1_mc.become(MathTex(rf"\frac{{{inside_triangle_count_mc}}}{{{i + 1}}}", font_size=30, color=GREEN).move_to(frac_counter1_mc))
                prob_value1_mc.set_value(inside_triangle_count_mc / (i + 1))
                frac_counter2_mc.become(MathTex(rf"\frac{{{inside_frame_count_mc}}}{{{i + 1}}}", font_size=30, color=GREEN).move_to(frac_counter2_mc))
                prob_value2_mc.set_value(inside_frame_count_mc / (i + 1))
                frac_counter3_mc.become(MathTex(rf"\frac{{{inside_hexagon_count_mc}}}{{{i + 1}}}", font_size=30, color=GREEN).move_to(frac_counter3_mc))
                prob_value3_mc.set_value(inside_hexagon_count_mc / (i + 1))
                self.wait(0.1)
                all_dots_list1_mc, all_dots_list2_mc, all_dots_list3_mc = [], [], []

        self.wait(1)
        # ... (Final animation sequence remains the same)
        shapes_and_lines_group_mc = VGroup(square1_mc, triangle1_mc, base_line_1_mc, outermost_square_2_mc, outer_frame_square_2_mc, inner_void_square_2_mc, frame_shape_2_mc, outermost_side_line_bottom_2_mc, outer_frame_side_line_right_2_mc, outer_frame_side_label_right_2_mc, inner_void_side_line_top_2_mc, inner_void_side_label_top_2_mc, square2_mc, hexagon3_mc, base_line_3_mc, height_line_3_mc, height_label_3_mc)
        prob_group1_mc, prob_group2_mc, prob_group3_mc = VGroup(prob_label1_mc, prob_value1_mc), VGroup(prob_label2_mc, prob_value2_mc), VGroup(prob_label3_mc, prob_value3_mc)
        self.play(FadeOut(shapes_and_lines_group_mc, plotted_dots_group1_mc, plotted_dots_group2_mc, plotted_dots_group3_mc, frac_counter1_mc, frac_counter2_mc, frac_counter3_mc), run_time=0.75)
        self.play(prob_group1_mc.animate.move_to(square1_pos_mc).scale(1.2), prob_group2_mc.animate.move_to(ORIGIN).scale(1.2), prob_group3_mc.animate.move_to(square2_pos_mc).scale(1.2), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(prob_group1_mc, prob_group2_mc, prob_group3_mc)); self.wait(1)

        # --- Start Scene 4: MonteCarloAmoeba ---
        outer_side_amoeba = 4
        total_points_amoeba = 1000
        radius_amoeba = 1.0
        batch_size_amoeba = 5

        outer_square_amoeba = Square(side_length=outer_side_amoeba, color=BLACK)
        self.play(Create(outer_square_amoeba)); self.wait(0.5)

        def generate_amoeba_points(radius=1.0, n_points=300):
            thetas = np.linspace(0, 2 * math.pi, n_points)
            r_values = radius * (1 + 0.3 * np.sin(5 * thetas))
            x_coords, y_coords = r_values * np.cos(thetas), r_values * np.sin(thetas)
            return [np.array([x, y, 0]) for x, y in zip(x_coords, y_coords)]
        def is_inside_amoeba(point, radius=1.0):
            x, y = point[0], point[1]
            r_point = np.sqrt(x**2 + y**2)  # ✅ FIXED
            theta = np.arctan2(y, x)
            if theta < 0:
                theta += 2 * math.pi
            return r_point < radius * (1 + 0.3 * np.sin(5 * theta))

        amoeba_points = generate_amoeba_points(radius_amoeba)
        amoeba = VMobject().set_points_as_corners([*amoeba_points, amoeba_points[0]]).set_fill(BLUE, opacity=0.3).set_stroke(BLUE, width=2)
        self.play(Create(amoeba)); self.wait(0.5)

        outer_label_amoeba = MathTex(f"{outer_side_amoeba}", color=BLACK, font_size=28).next_to(outer_square_amoeba, RIGHT)
        inner_label_amoeba = MathTex(r"\text{Amoeba}", font_size=28).next_to(amoeba, LEFT, buff=1.0)
        self.play(Write(outer_label_amoeba), Write(inner_label_amoeba)); self.wait(0.5)

        inside_count_amoeba = 0
        frac_counter_amoeba = MathTex(r"\frac{0}{0}", font_size=36, color=GREEN).next_to(outer_square_amoeba.get_corner(UL),(LEFT+UP), buff = 1)
        prob_value_amoeba = DecimalNumber(0, num_decimal_places=4, color=RED, font_size=36).next_to(outer_square_amoeba.get_corner(DR),(RIGHT + DOWN), buff = 1)
        prob_label_amoeba = Text("Area \u2248 ", font_size=36, color=RED).next_to(prob_value_amoeba, LEFT, buff=0.2)
        prob_group_amoeba = VGroup(prob_label_amoeba, prob_value_amoeba)
        self.add(frac_counter_amoeba, prob_group_amoeba); self.wait(0.5)

        half_outer_amoeba = outer_side_amoeba / 2
        points_group_amoeba = VGroup()

        for i in range(0, total_points_amoeba, batch_size_amoeba):
            current_batch_count_amoeba = min(batch_size_amoeba, total_points_amoeba - i)
            batch_points_amoeba = VGroup()

            for j in range(current_batch_count_amoeba):
                point_coords_amoeba = np.array([random.uniform(-half_outer_amoeba, half_outer_amoeba), random.uniform(-half_outer_amoeba, half_outer_amoeba), 0])
                if is_inside_amoeba(point_coords_amoeba, radius_amoeba):
                    inner_color = GREEN; inside_count_amoeba += 1
                else: inner_color = RED
                # ✅ CHANGED
                outer_dot = Dot(point=point_coords_amoeba, radius=dot_inner_radius + dot_border_offset, color=BLACK)
                inner_dot = Dot(point=point_coords_amoeba, radius=dot_inner_radius, color=inner_color)
                dot_amoeba = VGroup(outer_dot, inner_dot)
                batch_points_amoeba.add(dot_amoeba)
            
            self.add(batch_points_amoeba)
            points_group_amoeba.add(batch_points_amoeba)
            total_so_far_amoeba = i + current_batch_count_amoeba
            
            new_frac_tex_amoeba = MathTex(rf"\frac{{{inside_count_amoeba}}}{{{total_so_far_amoeba}}}", font_size=36, color=GREEN).move_to(frac_counter_amoeba.get_center())
            self.play(Transform(frac_counter_amoeba, new_frac_tex_amoeba), run_time=0.1)
            prob_value_amoeba.set_value(inside_count_amoeba / total_so_far_amoeba)
            self.wait(0.1)

        self.wait(1)
        # ... (Final animation sequence remains the same)
        figure_group_amoeba = VGroup(outer_square_amoeba, amoeba, outer_label_amoeba, inner_label_amoeba, points_group_amoeba)
        self.play(figure_group_amoeba.animate.move_to(UP *1.75), FadeOut(frac_counter_amoeba), FadeOut(prob_group_amoeba))
        self.wait(0.25)
        estimated_formula_amoeba = MathTex(rf"\text{{Estimated Area}} \approx \frac{{{inside_count_amoeba}}}{{{total_points_amoeba}}} = {inside_count_amoeba / total_points_amoeba:.4f}", color=BLACK).scale_to_fit_width(7).next_to(figure_group_amoeba, DOWN, buff=1.2)
        self.play(Write(estimated_formula_amoeba)); self.wait(0.5)
        self.play(FadeOut(figure_group_amoeba, estimated_formula_amoeba)); self.wait(1)

        # --- Start Scene 5: PiEstimationFullVideo ---
        square_side_pi = 4
        circle_radius_pi = square_side_pi / 2

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

        # --- Start Scene 6: LogicpediaOutro (from outro.py) ---
        # ... (No changes in this section)
        try:
            logo = ImageMobject("logicpedia_logo.png")
            logo.scale(1.8).to_edge(UP).shift(DOWN*2)
            self.play(FadeIn(logo, shift=UP, scale=1.1), run_time=0.8)
            
            line1 = Text("For more such videos,", font="Arial", color=BLACK)
            line2 = Text("Like & Subscribe to Logicpedia!", font="Arial Bold", color=BLUE)
            text_group = VGroup(line1, line2).arrange(DOWN, buff=0.3).next_to(logo, DOWN)

            self.play(Write(line1), run_time=0.6)
            self.play(Write(line2), run_time=0.6)
            self.wait(1)
        except:
            # Fallback if the logo file is not found
            outro_text = Text("Thanks for watching!", font_size=48, color=BLACK)
            self.play(Write(outro_text))
        self.wait(2)