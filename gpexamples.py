from manim import *
import random

config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 16.0
config.frame_width = 9.0
config.background_color = WHITE

dark_green1 = ManimColor("#014401")
dark_green = ManimColor('#80EF80')
dark_red = ManimColor('#FF2C2C')

class NestedSquareProbabilityScene(Scene):
    def construct(self):

        outer_side = 4.0
        inner_side = outer_side / 2

        # Step 1: Outer and Inner squares
        outer_square = Square(side_length=outer_side, color=BLACK)
        # Added fill_color and fill_opacity for the tinted blue covering
        inner_square = Square(side_length=inner_side, color=BLUE, fill_opacity=0.3).move_to(outer_square.get_center())

        # Step 2: Labels
        outer_label = MathTex(f"{outer_side}", color=BLACK, font_size=28).next_to(outer_square, RIGHT)
        inner_label = MathTex(f"{inner_side}", color=BLACK, font_size=28).next_to(inner_square, LEFT)

        self.play(Create(outer_square), Create(inner_square), Write(outer_label), Write(inner_label))
        self.wait(1)

        # Step 3: Counters in LaTeX frac format
        inside_count = 0
        
        # Initialize the counter as a MathTex fraction
        frac_counter = MathTex(r"\frac{0}{0}", font_size=36, color=PURE_GREEN).next_to(outer_square.get_corner(UL),(LEFT+UP), buff = 1)
        
        # Initial probability display for running counter
        prob_value = DecimalNumber(0, num_decimal_places=4, color=BLACK, font_size=36).next_to(outer_square.get_corner(DR),(RIGHT + DOWN), buff = 1)
        # The label for the running probability
        running_prob_label = Text("Area ≈ ", font_size=36, color=BLACK).next_to(prob_value, LEFT, buff=0.2)

        running_prob_group = VGroup(running_prob_label, prob_value) # Group for the running display
        self.add(frac_counter, running_prob_group) # Add the frac_counter and running_prob_group

        # Step 4: Point dropping
        total_points = 1000
        half_outer = outer_side / 2
        half_inner = inner_side / 2
        points_group = VGroup()
        batch_size = 500


        for i in range(0, total_points, batch_size):
            batch_points = VGroup()
            num_current_points = min(batch_size, total_points - i) # Ensure we don't exceed total_points

            for j in range(num_current_points):
                x = random.uniform(-half_outer, half_outer)
                y = random.uniform(-half_outer, half_outer)
                point = [x, y, 0]

                if -half_inner <= x <= half_inner and -half_inner <= y <= half_inner:
                    color = dark_green
                    inside_count += 1
                else:
                    color = dark_red

                dot = Dot(point=point, radius=0.025, color=color)
                batch_points.add(dot)

            # Add all dots in batch
            self.add(batch_points)
            points_group.add(batch_points) # Add to the main group of all points for potential later manipulation

            # Update values after batch
            total_so_far = i + num_current_points
            
            # Update the MathTex fraction counter
            # Use .become() to animate the change of the MathTex object
            new_frac_tex = MathTex(
                r"\frac{" + f"{inside_count}" + r"}{" + f"{total_so_far}" + r"}",
                font_size=36,
                color=dark_green
            ).move_to(frac_counter.get_center()) # Keep it at the same position

            self.play(Transform(frac_counter, new_frac_tex), run_time=0.1) # Animate the counter change
            
            # Update the running probability value
            prob_value.set_value(inside_count / total_so_far)

            self.wait(0.1)
        
        self.wait(1)
        # Fade out the fraction counter and the running probability group
        self.play(FadeOut(frac_counter), FadeOut(running_prob_group)) 
        
        # Step 5: Group figure and shift up
        figure_group = VGroup(
            outer_square, inner_square, outer_label, inner_label, points_group)
        self.play(figure_group.animate.shift(UP * 3))


        # Step 6: Area ratio and final estimated probability (on right)
        area_formula = MathTex(
            r"\frac{\text{Area of inner square}}{\text{Area of outer square}} = "
            + r"\frac{" + f"{inner_side}^2" + "}{" + f"{outer_side}^2" + "} = "
            + f"\\frac{{{int(inner_side ** 2)}}}{{{int(outer_side ** 2)}}} = {inner_side ** 2 / outer_side ** 2:.2f}",
            color=BLACK, font_size = 36
        )

        # Create a new text for the final estimated probability display
        # This will combine the "Estimated P" text with the final numerical value
        final_estimated_prob_display = MathTex(
            r"\text{Estimated Area} \approx " + f"{inside_count / total_points:.4f}",
            color=BLACK, font_size = 38
        )

        # Arrange the formulas vertically
        formula_group = VGroup(area_formula, final_estimated_prob_display).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        # Position the formula group to the right of the shifted figure
        formula_group.next_to(figure_group, DOWN, buff=1.5)

        self.play(Write(area_formula))
        self.play(Write(final_estimated_prob_display)) 
        self.wait(1)
        
        # Fade out all mobjects at the end
        self.play(FadeOut(*self.mobjects))