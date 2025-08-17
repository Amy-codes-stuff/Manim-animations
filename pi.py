from manim import *
import math
import random
import numpy as np

# Configuration - Apply once for the whole video
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 16.0
config.frame_width = 9.0
config.background_color = WHITE

# Re-define common colors
dark_green = ManimColor('#006400')
dark_green1 = ManimColor('#80EF80') # From piestimationverticle.py
dark_red = ManimColor('#C4150C')
DARK_BLUE = ManimColor("#00008B") # Defined missing color in previous snippets

class FullAnimationFlow(Scene):
    # Define a small epsilon for floating-point comparisons, accessible throughout the combined scene
    EPSILON = 1e-9

    def construct(self):
        # --- Start Scene 1: Introduction (from intro.py) ---
        # Title (Optional)
        title = Text("What is \u03c0?", font_size=60, color=BLUE).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeOut(title))

        # Step 1: Draw the circle
        circle = Circle(radius=2, color=BLACK )
        diameter_line = Line(circle.get_left(), circle.get_right(), color=RED)
        diameter_label = Tex("Diameter", font_size=30, color=BLACK).next_to(diameter_line, DOWN)

        self.play(Create(circle), Create(diameter_line), Write(diameter_label))
        self.wait(1)

        # Step 3: Unwrap circumference
        unwrapped_circumference = Line(ORIGIN, RIGHT * 2 * math.pi, color=TEAL, stroke_width=7)
        unwrapped_circumference.move_to(ORIGIN).shift(DOWN * 2.5)
        circum_text = Text("Circumference", font_size=34, color=BLACK).next_to(unwrapped_circumference, DOWN, buff=0.2)

        self.play(
            ReplacementTransform(circle.copy().set_opacity(0), unwrapped_circumference),
            Write(circum_text),
            run_time=1
        )
        self.wait(0.25)
        pi_intro = MathTex(r"\text{This distance is called the circumference...}", font_size=36, color=BLACK)
        pi_intro.next_to(circle, UP * 5)

        pi_hint = MathTex(r"\text{And it's closely tied to a special number: } \pi", font_size=36, color=BLUE_D)
        pi_hint.next_to(pi_intro, DOWN, buff=0.5)


        self.wait(0.25)
        self.play(Write(pi_intro))
        self.play(Write(pi_hint))
        # Remove original objects
        self.play(FadeOut(circle, diameter_line, diameter_label, pi_hint, pi_intro))
        self.wait(0.25)

        # Move unwrapped line to center
        cir_group = VGroup(unwrapped_circumference, circum_text)
        self.play(cir_group.animate.move_to(ORIGIN))

        # Step 4: Show formula
        formula = MathTex("C = \\pi d", font_size=50, color=BLACK)
        formula.next_to(unwrapped_circumference, UP, buff=0.5)
        self.play(Write(formula))
        self.wait(0.5)

        # Show value of π
        pi_value_intro = MathTex(r"\pi \approx 3.14159265", font_size=40, color=RED) # Renamed to avoid conflict
        pi_value_intro.next_to(circum_text, DOWN, buff=0.4)
        self.play(Write(pi_value_intro))
        self.wait(0.5)

        # Transition to next part
        self.play(FadeOut(unwrapped_circumference, formula, circum_text))
        self.play(pi_value_intro.animate.move_to(ORIGIN).scale(2))
        self.wait(3)
        self.play(FadeOut(pi_value_intro)) # Ensure all objects from this section are faded out
        self.wait(1) # Pause between sections

        # --- Start Scene 2: NestedSquareProbabilityScene (from gpexamples.py) ---
        outer_side = 4.0
        inner_side = outer_side / 2

        # Step 1: Outer and Inner squares
        outer_square = Square(side_length=outer_side, color=BLACK)
        inner_square = Square(side_length=inner_side, color=BLUE, fill_opacity=0.3).move_to(outer_square.get_center())

        # Step 2: Labels
        outer_label = MathTex(f"{outer_side}", color=BLACK, font_size=28).next_to(outer_square, RIGHT)
        inner_label = MathTex(f"{inner_side}", color=BLACK, font_size=28).next_to(inner_square, LEFT)

        self.play(Create(outer_square), Create(inner_square), Write(outer_label), Write(inner_label))
        self.wait(1)

        # Step 3: Counters in LaTeX frac format
        inside_count_gp = 0 # Renamed to avoid conflict
        frac_counter_gp = MathTex(r"\frac{0}{0}", font_size=36, color=dark_green).next_to(outer_square.get_corner(UL),(LEFT+UP), buff = 1)
        prob_value_gp = DecimalNumber(0, num_decimal_places=4, color=BLACK, font_size=36).next_to(outer_square.get_corner(DR),(RIGHT + DOWN), buff = 1)
        running_prob_label_gp = Text("Area \u2248 ", font_size=36, color=BLACK).next_to(prob_value_gp, LEFT, buff=0.2)

        running_prob_group_gp = VGroup(running_prob_label_gp, prob_value_gp)
        self.add(frac_counter_gp, running_prob_group_gp)

        # Step 4: Point dropping
        total_points_gp = 1000 # Renamed to avoid conflict
        half_outer_gp = outer_side / 2 # Renamed to avoid conflict
        half_inner_gp = inner_side / 2 # Renamed to avoid conflict
        points_group_gp = VGroup() # Renamed to avoid conflict
        batch_size_gp = 500 # Renamed to avoid conflict


        for i in range(0, total_points_gp, batch_size_gp):
            batch_points_gp = VGroup()
            num_current_points_gp = min(batch_size_gp, total_points_gp - i)

            for j in range(num_current_points_gp):
                x = random.uniform(-half_outer_gp, half_outer_gp)
                y = random.uniform(-half_outer_gp, half_outer_gp)
                point = [x, y, 0]

                if -half_inner_gp <= x <= half_inner_gp and -half_inner_gp <= y <= half_inner_gp:
                    color = dark_green
                    inside_count_gp += 1
                else:
                    color = dark_red

                dot = Dot(point=point, radius=0.025, color=color)
                batch_points_gp.add(dot)

            self.add(batch_points_gp)
            points_group_gp.add(batch_points_gp)

            total_so_far_gp = i + num_current_points_gp
            
            new_frac_tex_gp = MathTex(
                r"\frac{" + f"{inside_count_gp}" + r"}{" + f"{total_so_far_gp}" + r"}",
                font_size=36,
                color=dark_green
            ).move_to(frac_counter_gp.get_center())

            self.play(Transform(frac_counter_gp, new_frac_tex_gp), run_time=0.1)
            prob_value_gp.set_value(inside_count_gp / total_so_far_gp)

            self.wait(0.1)
        
        self.wait(1)
        self.play(FadeOut(frac_counter_gp), FadeOut(running_prob_group_gp)) 
        
        # Step 5: Group figure and shift up
        figure_group_gp = VGroup(
            outer_square, inner_square, outer_label, inner_label, points_group_gp)
        self.play(figure_group_gp.animate.shift(UP * 3))


        # Step 6: Area ratio and final estimated probability (on right)
        area_formula_gp = MathTex(
            r"\frac{\text{Area of inner square}}{\text{Area of outer square}} = "
            + r"\frac{" + f"{inner_side}^2" + "}{" + f"{outer_side}^2" + "} = "
            + f"\\frac{{{int(inner_side ** 2)}}}{{{int(outer_side ** 2)}}} = {inner_side ** 2 / outer_side ** 2:.2f}",
            color=BLACK, font_size = 36
        )

        final_estimated_prob_display_gp = MathTex(
            r"\text{Estimated Area} \approx " + f"{inside_count_gp / total_points_gp:.4f}",
            color=BLACK, font_size = 38
        )

        formula_group_gp = VGroup(area_formula_gp, final_estimated_prob_display_gp).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        formula_group_gp.next_to(figure_group_gp, DOWN, buff=1.5)

        self.play(Write(area_formula_gp))
        self.play(Write(final_estimated_prob_display_gp)) 
        self.wait(1)
        
        self.play(FadeOut(figure_group_gp, formula_group_gp)) # Explicitly fade out objects from this section
        self.wait(1) # Pause between sections


        # --- Start Scene 3: SimultaneousMonteCarlo (from threeexamplesimultaneous.py) ---
        square_side_mc = 3 # Renamed to avoid conflict
        half_side_mc = square_side_mc / 2
        total_points_mc = 1000
        batch_size_mc = 500

        # --- Setup for 1st Example (Top: Square & Triangle) ---
        square1_pos_mc = UP * 5
        square1_mc = Square(side_length=square_side_mc, color=BLACK).move_to(square1_pos_mc)

        bottom_left_1_mc = square1_mc.get_corner(DL)
        bottom_right_1_mc = square1_mc.get_corner(DR)
        top_mid_1_mc = square1_mc.get_top()
        triangle1_mc = Polygon(bottom_left_1_mc, bottom_right_1_mc, top_mid_1_mc, color=BLUE, fill_opacity=0.3)

        base_line_1_mc = Line(bottom_left_1_mc, bottom_right_1_mc, color=RED)
        base_label_1_mc = MathTex(f"{square_side_mc}", font_size=28, color=RED).next_to(base_line_1_mc, DOWN)

        inside_triangle_count_mc = 0
        frac_counter1_mc = MathTex(r"\frac{0}{0}", font_size=30, color=dark_green)
        frac_counter1_mc.next_to(square1_mc.get_corner(UL), (LEFT*0.5 + UP * 0.3), buff=1)
        prob_value1_mc = DecimalNumber(0, num_decimal_places=4, color=RED, font_size=36).next_to(square1_mc.get_corner(DR), (RIGHT + DOWN * 0.3), buff=1)
        prob_label1_mc = Text("Area \u2248 ", font_size=32, color=RED).next_to(prob_value1_mc, LEFT, buff=0.2)
        
        triangle_vertices_for_check_mc = [bottom_left_1_mc, bottom_right_1_mc, top_mid_1_mc]
        all_dots_list1_mc = []
        plotted_dots_group1_mc = VGroup()


        # --- Setup for 2nd Example (Middle: Nested Square Frame) ---
        outer_frame_boundary_side_2_mc = 2
        inner_void_side_2_mc = 1          
        
        outermost_square_2_mc = Square(side_length=square_side_mc, color=BLACK)
        outer_frame_square_2_mc = Square(side_length=outer_frame_boundary_side_2_mc, color=BLACK)
        inner_void_square_2_mc = Square(side_length=inner_void_side_2_mc, color=WHITE, fill_opacity=1)

        frame_shape_2_mc = Difference(outer_frame_square_2_mc.copy(), inner_void_square_2_mc.copy())
        frame_shape_2_mc.set_color(BLUE).set_opacity(0.5)

        outermost_side_line_bottom_2_mc = Line(outermost_square_2_mc.get_corner(DL), outermost_square_2_mc.get_corner(DR), color=RED)
        outermost_side_label_bottom_2_mc = MathTex(f"{square_side_mc}", font_size=28, color=dark_red).next_to(outermost_side_line_bottom_2_mc, DOWN)
        
        outer_frame_side_line_right_2_mc = Line(outer_frame_square_2_mc.get_corner(DR), outer_frame_square_2_mc.get_corner(UR), color=RED)
        outer_frame_side_label_right_2_mc = MathTex(f"{outer_frame_boundary_side_2_mc}", font_size=28, color=dark_green).next_to(outer_frame_side_line_right_2_mc, RIGHT)

        inner_void_side_line_top_2_mc = Line(inner_void_square_2_mc.get_corner(UL), inner_void_square_2_mc.get_corner(UR), color=RED)
        inner_void_side_label_top_2_mc = MathTex(f"{inner_void_side_2_mc}", font_size=28, color=DARK_BLUE).next_to(inner_void_side_line_top_2_mc, UP)

        inside_frame_count_mc = 0
        frac_counter2_mc = MathTex(r"\frac{0}{0}", font_size=30, color=dark_green).next_to(outermost_square_2_mc.get_corner(UL), (LEFT*0.5 + UP * 0.3), buff=1)
        prob_value2_mc = DecimalNumber(0, num_decimal_places=4, color=RED, font_size=36).next_to(outermost_square_2_mc.get_corner(DR), (RIGHT + DOWN * 0.3), buff=1)
        prob_label2_mc = Text("Area \u2248 ", font_size=32, color=RED).next_to(prob_value2_mc, LEFT, buff=0.2)
        
        all_dots_list2_mc = []
        plotted_dots_group2_mc = VGroup()


        # --- Setup for 3rd Example (Bottom: Square & Diagonal Hexagon) ---
        square2_pos_mc = DOWN * 5
        square2_mc = Square(side_length=square_side_mc, color=BLACK).move_to(square2_pos_mc)
        band_offset_mc = 0.5

        dl_3_mc = square2_mc.get_corner(DL)
        dr_3_mc = square2_mc.get_corner(DR)
        ul_3_mc = square2_mc.get_corner(UL)
        ur_3_mc = square2_mc.get_corner(UR)

        p1_3_mc = ul_3_mc                               
        p2_3_mc = ul_3_mc + RIGHT * band_offset_mc         
        p3_3_mc = dr_3_mc + UP * band_offset_mc            
        p4_3_mc = dr_3_mc                               
        p5_3_mc = dr_3_mc + LEFT * band_offset_mc          
        p6_3_mc = ul_3_mc + DOWN * band_offset_mc          

        hexagon3_mc = Polygon(p1_3_mc, p2_3_mc, p3_3_mc, p4_3_mc, p5_3_mc, p6_3_mc, color=BLUE, fill_opacity=0.3)

        base_line_3_mc = Line(dl_3_mc, dr_3_mc, color=RED)
        height_line_3_mc = Line(ul_3_mc, dl_3_mc, color=RED)
        base_label_3_mc = MathTex(f"{square_side_mc}", font_size=28, color=RED).next_to(base_line_3_mc, DOWN)
        height_label_3_mc = MathTex(f"{square_side_mc}", font_size=28, color=RED).next_to(height_line_3_mc, LEFT)

        inside_hexagon_count_mc = 0
        frac_counter3_mc = MathTex(r"\frac{0}{0}", font_size=30, color=dark_green).next_to(square2_mc.get_corner(UL), (LEFT*0.5 + UP * 0.3), buff=1)
        prob_value3_mc = DecimalNumber(0, num_decimal_places=4, color=RED, font_size=36).next_to(square2_mc.get_corner(DR), (RIGHT + DOWN * 0.3), buff=1)
        prob_label3_mc = Text("Area \u2248 ", font_size=32, color=RED).next_to(prob_value3_mc, LEFT, buff=0.2)

        hexagon_vertices_for_check_mc = [v[:2] for v in hexagon3_mc.get_vertices()]
        all_dots_list3_mc = []
        plotted_dots_group3_mc = VGroup()


        # --- Common `is_inside_` functions ---
        def is_inside_triangle(p, a, b, c):
            def det(p1, p2, p3):
                return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1])
            s1 = det(p, a, b)
            s2 = det(p, b, c)
            s3 = det(p, c, a)
            return (s1 >= -self.EPSILON and s2 >= -self.EPSILON and s3 >= -self.EPSILON) or \
                   (s1 <= self.EPSILON and s2 <= self.EPSILON and s3 <= self.EPSILON)

        def is_inside_frame(x, y, outer_half_side, inner_half_side):
            is_inside_outer = (-outer_half_side <= x <= outer_half_side) and \
                              (-outer_half_side <= y <= outer_half_side)
            is_inside_void = (-inner_half_side <= x <= inner_half_side) and \
                             (-inner_half_side <= y <= inner_half_side)
            return is_inside_outer and not is_inside_void
        
        def is_inside_polygon(p, vertices):
            def sign(p1, p2, p3):
                return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0]) 
            
            x_p, y_p = p
            num_vertices = len(vertices)
            
            if num_vertices < 3:
                return False

            first_sign_val = sign(vertices[0], vertices[1], (x_p, y_p))

            for i in range(num_vertices):
                v1 = vertices[i]
                v2 = vertices[(i + 1) % num_vertices]
                current_sign_val = sign(v1, v2, (x_p, y_p))

                if abs(current_sign_val) < self.EPSILON:
                    continue
                
                if (first_sign_val > self.EPSILON and current_sign_val < -self.EPSILON) or \
                   (first_sign_val < -self.EPSILON and current_sign_val > self.EPSILON):
                    return False
            return True


        # --- Animate initial setups for all three figures simultaneously ---
        self.play(
            Create(square1_mc), Create(triangle1_mc), Create(base_line_1_mc),
            Write(base_label_1_mc),
            
            Create(outermost_square_2_mc), Create(frame_shape_2_mc),
            Create(outermost_side_line_bottom_2_mc), Write(outermost_side_label_bottom_2_mc),
            Create(outer_frame_side_line_right_2_mc), Write(outer_frame_side_label_right_2_mc),
            Create(inner_void_side_line_top_2_mc), Write(inner_void_side_label_top_2_mc),
            
            Create(square2_mc), Create(hexagon3_mc), Create(base_line_3_mc), Create(height_line_3_mc),
            Write(base_label_3_mc), Write(height_label_3_mc)
        )
        self.wait(1)

        self.add(frac_counter1_mc, prob_label1_mc, prob_value1_mc,
                 frac_counter2_mc, prob_label2_mc, prob_value2_mc,
                 frac_counter3_mc, prob_label3_mc, prob_value3_mc)

        self.wait(0.5)

        # --- Main Simultaneous Point Dropping Loop ---
        for i in range(total_points_mc):
            # --- Example 1: Triangle (Top) ---
            random_x_offset_1_mc = random.uniform(-half_side_mc, half_side_mc)
            random_y_offset_1_mc = random.uniform(-half_side_mc, half_side_mc)
            point_coords_1_mc = np.array([random_x_offset_1_mc, random_y_offset_1_mc, 0]) + square1_pos_mc

            if is_inside_triangle(point_coords_1_mc, *triangle_vertices_for_check_mc):
                color1_mc = dark_green
                inside_triangle_count_mc += 1
            else:
                color1_mc = dark_red
            dot1_mc = Dot(point=point_coords_1_mc, radius=0.025, color=color1_mc)
            all_dots_list1_mc.append(dot1_mc)
            plotted_dots_group1_mc.add(dot1_mc)

            # --- Example 2: Frame (Middle) ---
            random_x_offset_2_mc = random.uniform(-half_side_mc, half_side_mc)
            random_y_offset_2_mc = random.uniform(-half_side_mc, half_side_mc)
            point_coords_2_mc = np.array([random_x_offset_2_mc, random_y_offset_2_mc, 0])
            
            if is_inside_frame(point_coords_2_mc[0], point_coords_2_mc[1], outer_frame_boundary_side_2_mc / 2, inner_void_side_2_mc / 2):
                color2_mc = dark_green
                inside_frame_count_mc += 1
            else:
                color2_mc = dark_red
            dot2_mc = Dot(point=point_coords_2_mc, radius=0.025, color=color2_mc)
            all_dots_list2_mc.append(dot2_mc)
            plotted_dots_group2_mc.add(dot2_mc)

            # --- Example 3: Hexagon (Bottom) ---
            random_x_offset_3_mc = random.uniform(-half_side_mc, half_side_mc)
            random_y_offset_3_mc = random.uniform(-half_side_mc, half_side_mc)
            point_coords_3_mc = np.array([random_x_offset_3_mc, random_y_offset_3_mc, 0]) + square2_pos_mc

            if is_inside_polygon(point_coords_3_mc[:2], hexagon_vertices_for_check_mc):
                color3_mc = dark_green
                inside_hexagon_count_mc += 1
            else:
                color3_mc = dark_red
            dot3_mc = Dot(point=point_coords_3_mc, radius=0.025, color=color3_mc)
            all_dots_list3_mc.append(dot3_mc)
            plotted_dots_group3_mc.add(dot3_mc)

            # --- Batch Update for all examples ---
            if (i + 1) % batch_size_mc == 0 or i == total_points_mc - 1:
                self.add(*all_dots_list1_mc, *all_dots_list2_mc, *all_dots_list3_mc)

                frac_counter1_mc.become(MathTex(r"\frac{" + f"{inside_triangle_count_mc}" + r"}{" + f"{i + 1}" + r"}", font_size=30, color=dark_green).move_to(frac_counter1_mc))
                prob_value1_mc.set_value(inside_triangle_count_mc / (i + 1))

                frac_counter2_mc.become(MathTex(r"\frac{" + f"{inside_frame_count_mc}" + r"}{" + f"{i + 1}" + r"}", font_size=30, color=dark_green).move_to(frac_counter2_mc))
                prob_value2_mc.set_value(inside_frame_count_mc / (i + 1))

                frac_counter3_mc.become(MathTex(r"\frac{" + f"{inside_hexagon_count_mc}" + r"}{" + f"{i + 1}" + r"}", font_size=30, color=dark_green).move_to(frac_counter3_mc))
                prob_value3_mc.set_value(inside_hexagon_count_mc / (i + 1))
                
                self.wait(0.1)

                all_dots_list1_mc = []
                all_dots_list2_mc = []
                all_dots_list3_mc = []

        self.wait(1)

        # --- Final Animation Sequence for SimultaneousMonteCarlo ---
        shapes_and_lines_group_mc = VGroup( # Renamed
            square1_mc, triangle1_mc, base_line_1_mc, base_label_1_mc,
            outermost_square_2_mc, outer_frame_square_2_mc, inner_void_square_2_mc, frame_shape_2_mc,
            outermost_side_line_bottom_2_mc, outermost_side_label_bottom_2_mc,
            outer_frame_side_line_right_2_mc, outer_frame_side_label_right_2_mc,
            inner_void_side_line_top_2_mc, inner_void_side_label_top_2_mc,
            square2_mc, hexagon3_mc, base_line_3_mc, height_line_3_mc, base_label_3_mc, height_label_3_mc
        )

        prob_group1_mc = VGroup(prob_label1_mc, prob_value1_mc)
        prob_group2_mc = VGroup(prob_label2_mc, prob_value2_mc)
        prob_group3_mc = VGroup(prob_label3_mc, prob_value3_mc)


        self.play(
            FadeOut(shapes_and_lines_group_mc),
            FadeOut(plotted_dots_group1_mc),
            FadeOut(plotted_dots_group2_mc),
            FadeOut(plotted_dots_group3_mc),
            FadeOut(frac_counter1_mc),
            FadeOut(frac_counter2_mc),
            FadeOut(frac_counter3_mc),
            run_time = 0.75
        )
        self.play(
            prob_group1_mc.animate.move_to(square1_pos_mc).scale(2),
            prob_group2_mc.animate.move_to(ORIGIN).scale(2),
            prob_group3_mc.animate.move_to(square2_pos_mc).scale(2),
            run_time=1.5
        )
        self.wait(1)
        self.play(FadeOut(prob_group1_mc, prob_group2_mc, prob_group3_mc)) # Fade out the final moved groups
        self.wait(1) # Pause between sections


        # --- Start Scene 4: PiEstimationFullVideo (from piestimationverticle.py) ---
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
        self.play(group_objects_pi.animate.shift(UP * 4))

        text_area_intro_pi = Text("Let's look at their areas...", font_size=40, color=BLACK).next_to(group_objects_pi,DOWN, buff=1)
        self.play(Write(text_area_intro_pi), run_time = 0.5)
        self.play(FadeOut(text_area_intro_pi))

        area_circle_formula_pi = MathTex(
            "A_{\\text{circle}} = \\pi r^2",
            font_size=45, color=BLACK
        ).next_to(group_objects_pi,DOWN, buff=1, aligned_edge=LEFT).shift(RIGHT*0.5)

        area_square_formula_pi = MathTex(
            "A_{\\text{square}} = (2r)^2 = 4r^2",
            font_size=45, color=BLACK
        ).next_to(area_circle_formula_pi, DOWN, aligned_edge=LEFT)
        self.play(Write(area_circle_formula_pi), Write(area_square_formula_pi))
        self.wait(0.3)

        ratio_formula_pi = MathTex(
            "\\frac{A_{\\text{circle}}}{A_{\\text{square}}} = \\frac{\\pi r^2}{4r^2}",
            font_size=45, color=BLACK
        ).next_to(area_square_formula_pi, DOWN, aligned_edge=LEFT, buff=0.7)
        self.play(Write(ratio_formula_pi))

        simplified_ratio_pi = MathTex(
            "= \\frac{\\pi}{4}",
            font_size=45, color=DARK_BLUE
        ).next_to(ratio_formula_pi, RIGHT, buff=0.2)
        self.play(Write(simplified_ratio_pi))
        self.wait(0.3)

        pi_formula_pi = MathTex(
            "\\pi = 4 \\times \\frac{A_{\\text{circle}}}{A_{\\text{square}}}",
            font_size=50, color=DARK_BLUE
        ).next_to(ratio_formula_pi, DOWN, aligned_edge=LEFT, buff=0.7)
        self.play(Write(pi_formula_pi))
        self.wait(0.5)

        self.play(FadeOut(area_circle_formula_pi, area_square_formula_pi, ratio_formula_pi,
                            simplified_ratio_pi, radius_line_pi, radius_label_pi, side_line_left_pi, side_label_left_pi, pi_formula_pi))

        geo_group_pi = VGroup(square_pi, circle_pi, square_label_pi, circle_label_pi)
        self.play(geo_group_pi.animate.shift(DOWN * 4), run_time = 0.75)
        self.wait(0.7)

        inside_points_pi = 0
        frac_counter_pi = MathTex(r"\frac{0}{0}", font_size=36, color=dark_green).next_to(square_pi.get_corner(UL),(LEFT+UP), buff = 1)
        self.add(frac_counter_pi)

        pi_value_display_pi = DecimalNumber(0, num_decimal_places=4, color=RED, font_size=40).next_to(square_pi.get_corner(DR),(RIGHT + DOWN), buff = 1)
        pi_label_display_pi = Text("π \u2248 ", font_size=40, color=RED).next_to(pi_value_display_pi, LEFT, buff=0.2)

        pi_group_display_pi = VGroup(pi_value_display_pi, pi_label_display_pi)
        self.add(pi_group_display_pi)

        total_points_pi = 1000
        batch_size_pi = 500
        all_dots_pi = VGroup()
        

        for i in range(0, total_points_pi, batch_size_pi):
            animations = []
            current_batch_count_pi = min(batch_size_pi, total_points_pi - i)

            for _ in range(current_batch_count_pi):
                x = random.uniform(-circle_radius_pi, circle_radius_pi)
                y = random.uniform(-circle_radius_pi, circle_radius_pi)
                point_coords_pi = [x, y, 0]

                dot_pi = Dot(point=point_coords_pi, radius=0.025)

                if x**2 + y**2 <= circle_radius_pi**2:
                    dot_pi.set_color(dark_green1)
                    inside_points_pi += 1
                else:
                    dot_pi.set_color(dark_red)

                all_dots_pi.add(dot_pi)
                animations.append(Create(dot_pi))

            self.play(*animations, run_time=0.05, rate_func=linear)

            current_total_pi = i + current_batch_count_pi

            new_frac_counter_pi = MathTex(
                r"\frac{" + f"{inside_points_pi}" + r"}{" + f"{current_total_pi}" + r"}",
                font_size=36,
                color=dark_green
            ).move_to(frac_counter_pi.get_center())

            self.play(Transform(frac_counter_pi, new_frac_counter_pi), run_time=0.1)
            
            if current_total_pi > 0:
                pi_value_display_pi.set_value(4 * inside_points_pi / current_total_pi)
            else:
                pi_value_display_pi.set_value(0)

        self.wait(0.5)
        self.play(FadeOut(all_dots_pi, geo_group_pi, frac_counter_pi))
        self.wait(0.25)

        self.play(pi_group_display_pi.animate.move_to(ORIGIN).scale(2.5), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(pi_group_display_pi)) # Fade out the final pi value group
        self.wait(1) # Pause between sections


        # --- Start Scene 5: LogicpediaOutro (from outro.py) ---
        logo = ImageMobject("logicpedia_logo.png")
        logo.scale(1.8)
        logo.to_edge(UP).shift(DOWN*2)

        line1 = Text("For more such videos,", font="Arial", color=BLACK)
        line2 = Text("Like & Subscribe to Logicpedia!", font="Arial Bold", color=BLUE)

        text_group = VGroup(line1, line2).arrange(DOWN, buff=0.3)
        text_group.next_to(logo, DOWN)

        self.play(FadeIn(logo, shift=UP, scale=1.1), run_time=0.8)
        self.play(Write(line1), run_time=0.6)
        self.play(Write(line2), run_time=0.6)

        self.wait(1)
        # End of FullAnimationFlow