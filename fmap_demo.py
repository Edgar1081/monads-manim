from manim import *

class MonadsScene(Scene):
    def create_title(self, text):
        title = Text(text, font_size=48).move_to(ORIGIN)
        self.play(FadeIn(title))
        self.wait(0.5)
        self.play(FadeOut(title))

    def show_category(self):
        category = Text("Category")
        categoryt = Text("Theory")
        category.move_to(UP)
        categoryt.next_to(category, DOWN, buff=0.5)
        self.play(FadeIn(category))
        self.wait(0.5)
        self.play(FadeIn(categoryt))
        return category, categoryt

    def create_graph(self, vertices, edges, edge_config, layout="circular"):
        return DiGraph(vertices, edges, layout=layout, edge_config=edge_config)

    def highlight_objects_and_morphisms(self, g2):
        obj = Text("Objects", font_size=30).to_edge(ORIGIN + 2 * LEFT + 3 * UP)
        mrp = Text("Mophisms", font_size=30).next_to(obj, DOWN, buff=2)
        arr = Text("Arrows", font_size=30).next_to(obj, DOWN, buff=2)
        colors = color_gradient([PURPLE, TEAL], length_of_output=5)
        self.play(Create(obj))
        self.play(Circumscribe(obj, Circle, color=colors))
        self.play(Create(mrp))
        self.play(Create(g2), run_time=1)
        self.play(Circumscribe(mrp, Circle, color=colors))
        self.play(Transform(mrp, arr))
        return obj, mrp

    def show_laws(self):
        laws = Text("That respect some laws:", font_size=25).to_edge(ORIGIN + RIGHT + 3 * UP)
        lawid = Text("Identiy law", font_size=20).next_to(laws, DOWN, buff=0.5)
        lawidL = Tex("$f \\circ Id = f = Id \\circ f$", font_size=20).next_to(lawid, DOWN, buff=0.5)
        lawAs = Text("Associativity law", font_size=20).next_to(lawidL, DOWN, buff=1)
        lawAsL = Tex("$h \\circ (g \\circ f) = (h \\circ g) \\circ f$", font_size=20).next_to(lawAs, DOWN, buff=0.5)
        lawsC = [laws, lawid, lawAs, lawidL, lawAsL]
        self.play(*[Create(mob) for mob in lawsC])
        colors = color_gradient([PURPLE, TEAL], length_of_output=5)
        self.play(Circumscribe(lawidL, color=colors), Circumscribe(lawAsL, color=colors))
        return lawsC

    def show_gf_category(self):
        verticesGF = [1, 2]
        edgesGF = [(1, 2)]
        layout = {1: 2 * LEFT, 2: 2 * RIGHT}
        edge_config_GF = {"stroke_width": 4, "tip_config": {"tip_length": 0.15, "tip_width": 0.15}}
        gf = self.create_graph(verticesGF, edgesGF, edge_config_GF, layout=layout)
        self.play(Create(gf))

        custom_labels = {1: ("Int", UP), 2: ("Bool", UP)}
        labintbool = []
        for v, (text, direction) in custom_labels.items():
            label = Tex(text).scale(0.6).next_to(gf[v], direction, buff=0.1)
            labintbool.append(label)
        self.play(*[Create(label) for label in labintbool])

        v1, v2 = gf[1], gf[2]
        edge_midpoint = (v1.get_center() + v2.get_center()) / 2
        edge_label = Tex("even").scale(0.5).move_to(edge_midpoint + 0.2 * UP)
        self.play(Create(edge_label))

        # Extra arcs
        arcs = []
        labels = []
        for radius, txt, offset in [(3, "odd", DOWN), (-3, "$(> 10)$", UP)]:
            arc = ArcBetweenPoints(2 * LEFT, 2 * RIGHT, radius=radius)
            arc.add_tip(tip_length=0.15, tip_width=0.15)
            label = Tex(txt).scale(0.5).move_to(arc.point_from_proportion(0.5) + 0.3 * offset)
            arcs.append(arc)
            labels.append(label)
            self.play(Create(label))
            self.play(Create(arc), run_time=3)

        return gf, labintbool, [edge_label] + labels + arcs

    def get_cats(self, n):
        vertices = list(range(1, n + 1))
        edges = [(i, j) for i in vertices for j in vertices if i != j]
        return DiGraph(vertices, edges, layout="circular")

    def construct(self):
        self.create_title("Monads in Functional Programming")
        category, categoryt = self.show_category()

        vertices = [1, 2, 3, 4, 5, 6]
        edges = [(1, 2), (2, 3), (3, 4), (1, 3), (1, 6), (1, 5), (5, 6), (5, 4), (3, 5)]
        edge_config = {"stroke_width": 2, "tip_config": {"tip_length": 0.15, "tip_width": 0.15}}

        g = self.create_graph(vertices, [], edge_config)
        g2 = self.create_graph(vertices, edges, edge_config)

        self.play(Transform(category, g[1]))
        self.play(Transform(categoryt, g[2]))
        self.play(Create(g))

        obj, mrp = self.highlight_objects_and_morphisms(g2)
        lawsC = self.show_laws()
        self.wait(5)

        haskdot = Dot()
        hask = Tex("$Hask$", font_size=30).to_edge(UP)
        self.play(FadeOut(category), FadeOut(categoryt), FadeOut(g2), FadeOut(obj), FadeOut(mrp), FadeOut(*lawsC))
        self.clear()
        self.play(Transform(g, haskdot))
        self.clear()
        self.play(Transform(haskdot, hask))

        gf, labels, extras = self.show_gf_category()
        self.wait(3)
        self.play(*[FadeOut(label) for label in labels])
        self.play(FadeOut(gf), *[FadeOut(m) for m in extras], FadeOut(hask))

        fuctC = Text("Functor", font_size=30).to_edge(UP)
        self.play(Transform(haskdot, fuctC))
        cat1 = self.get_cats(4)
        self.play(Create(cat1))
        self.wait(3)
