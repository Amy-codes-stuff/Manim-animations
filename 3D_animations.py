from manim import *

class CalculusSlopes(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range=[-3, 3],
            y_range=[-4, 14],
            x_length=6,
            y_length=7,
        ).add_coordinates()

        graph1 = plane.plot(lambda x: x**2, x_range=[-3, 3], color=RED)
        graph1_lab = (
            MathTex("f(x) = x^2")
            .next_to(graph1, UR, buff=0.2)
            .set_color(RED)
            .scale(0.8)
        )

        c = ValueTracker(-4)
        k = ValueTracker(-3)

        graph2 = always_redraw(
            lambda: plane.plot(
                lambda x: x**2 + c.get_value(),
                x_range=[-3, 3],
                color=YELLOW
            )
        )

        graph2_lab = always_redraw(
            lambda: MathTex(f"f(x) = x^2 + {c.get_value():.1f}")
            .next_to(graph2, UR, buff=0.2)
            .set_color(YELLOW)
            .scale(0.8)
        )

        dot1 = always_redraw(
            lambda: Dot(color=RED)
            .move_to(plane.coords_to_point(
                k.get_value(), graph1.underlying_function(k.get_value())
            ))
        )

        dot2 = always_redraw(
            lambda: Dot(color=YELLOW)
            .move_to(plane.coords_to_point(
                k.get_value(), graph2.underlying_function(k.get_value())
            ))
        )

        slope1 = always_redraw(
            lambda: self.color_secant(
                plane.get_secant_slope_group(
                    x=k.get_value(),
                    graph=graph1,
                    dx=0.01,
                    secant_line_length=5,
                ),
                RED
            )
        )

        slope2 = always_redraw(
            lambda: self.color_secant(
                plane.get_secant_slope_group(
                    x=k.get_value(),
                    graph=graph2,
                    dx=0.01,
                    secant_line_length=5,
                ),
                YELLOW
            )
        )

        self.play(
            LaggedStart(
                DrawBorderThenFill(plane),
                Create(graph1),
                Create(graph2),
                lag_ratio=0.8
            ),
            run_time=5
        )

        self.add(graph1_lab, graph2_lab, dot1, dot2, slope1, slope2)

        self.play(
            k.animate.set_value(0),
            c.animate.set_value(2),
            run_time=5,
            rate_func=linear
        )

        self.play(
            k.animate.set_value(3),
            c.animate.set_value(-2),
            run_time=5,
            rate_func=linear
        )

        self.wait()

    def color_secant(self, secant_group, color):
        secant_line = secant_group[1]  # Line is the second item in group
        secant_line.set_color(color)
        return secant_group
