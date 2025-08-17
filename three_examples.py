from manim import *
import random

config.background_color = WHITE


class threeexample(Scene):
    def construct(self):

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
