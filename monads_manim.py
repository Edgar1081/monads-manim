from manim import *
import random

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
        edge_config_GF = {"stroke_width": 4, "tip_config": {"tip_length": 0.15, "tip_width": 0.15}}
        return DiGraph(vertices, edges, layout=layout, edge_config=edge_config_GF)

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
        laws = Text("That respect some laws:", font_size=30).to_edge(ORIGIN + RIGHT + 3 * UP)
        lawid = Text("Identiy law", font_size=25).next_to(laws, DOWN, buff=0.5)
        lawidL = Tex("$f \\circ Id = f = Id \\circ f$", font_size=30).next_to(lawid, DOWN, buff=0.5)
        lawAs = Text("Associativity law", font_size=25).next_to(lawidL, DOWN, buff=1)
        lawAsL = Tex("$h \\circ (g \\circ f) = (h \\circ g) \\circ f$", font_size=30).next_to(lawAs, DOWN, buff=0.5)
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

        custom_labels = {1: ("Int", LEFT), 2: ("Bool", RIGHT)}
        labintbool = []
        for v, (text, direction) in custom_labels.items():
            label = Tex(text).scale(0.6).next_to(gf[v], direction, buff=0.1)
            labintbool.append(label)
        self.play(*[Create(label) for label in labintbool])

        labintbool[0].add_updater(lambda m: m.next_to(gf[1], LEFT, buff=0.1))

        v1, v2 = gf[1], gf[2]
        edge_midpoint = (v1.get_center() + v2.get_center()) / 2
        edge_label = Tex("even").scale(0.5).move_to(edge_midpoint + 0.2 * UP)
        self.play(Create(edge_label))

        arcs = []
        labels = []
        for radius, txt, offset in [(2.5, "odd", 2*DOWN), (-2.5, "$(> 10)$", 2*UP)]:
            arc = ArcBetweenPoints(2 * LEFT, 2 * RIGHT, radius=radius)
            arc.add_tip(tip_length=0.15, tip_width=0.15)
            label = Tex(txt).scale(0.5).move_to(arc.point_from_proportion(0.5) + 0.3 * offset)
            arcs.append(arc)
            labels.append(label)
            self.play(Create(arc), run_time=2)
            self.play(Create(label))

        return gf, labintbool, [edge_label] + labels + labintbool + [gf.edges[(1,2)]] + arcs

    def get_cats(self, n, seed, edge_prob):
        vertices = list(range(1, n + 1))
        random.seed(seed)

        edges = [
            (i, j)
            for i in vertices
            for j in vertices
            if i != j and random.random() < edge_prob
        ]
        edge_config_GF = {
            "stroke_width": 4,
            "tip_config": {
                "tip_length": 0.2,
                "tip_width": 0.2
            }
        }
        return DiGraph(vertices,edges, edge_config=edge_config_GF, vertex_config={"color":RED}, layout="circular")

    def func_int_bool(self, gf, extras):
        evenpath = extras[-3]
        oddpath = extras[-2]
        greatpath = extras[-1]

        d1 = Dot().set_color(RED)
        label12 = Tex("12").scale(0.5)
        labeltrue = Tex("True").scale(0.5)
        label12.next_to(d1, DOWN, buff=0.1)
        labeltrue.next_to(d1, DOWN, buff=0.1)

        d2 = Dot().set_color(PURPLE)
        label12o = Tex("12").scale(0.5)
        labelfalseo = Tex("False").scale(0.5)
        label12o.next_to(d2, DOWN, buff=0.1)

        d3 = Dot().set_color(BLUE)
        label12g = Tex("12").scale(0.5)
        labeltrueg = Tex("True").scale(0.5)
        label12g.next_to(d3, UP, buff=0.1)

        self.add(d1, label12)

        self.play(
            MoveAlongPath(d1, evenpath),
            Transform(label12, labeltrue),
            UpdateFromFunc(label12, lambda m: m.next_to(d1, LEFT + DOWN, buff=0.1)),
            rate_func=smooth,
            run_time=2.5
        )
        self.play(FadeOut(d1), FadeOut(label12))

        self.add(d2, label12o)
        self.play(
            MoveAlongPath(d2, oddpath),
            Transform(label12o, labelfalseo),
            UpdateFromFunc(label12o, lambda m: m.next_to(d2, 2*DOWN, buff=0.1)),
            rate_func=smooth,
            run_time=2.5
        )
        self.play((FadeOut(d2), FadeOut(label12o)))

        self.add(d3, label12g)
        self.play(
            MoveAlongPath(d3, greatpath),
            Transform(label12g, labeltrueg),
            UpdateFromFunc(label12g, lambda m: m.next_to(d3, 2*UP, buff=0.1)),
            rate_func=smooth,
            run_time=2.5
        )

        intdot = Dot()
        intlabel = Tex("$Int$").scale(0.6)
        intlabel.next_to(intdot, LEFT, buff=0.1)
        
        self.play(FadeOut(d3), FadeOut(label12g))
        self.play(FadeOut(gf), *[FadeOut(m) for m in extras],
                  gf[1].animate.move_to(ORIGIN), Create(intdot), Create(intlabel))

        loop = Arc(
            start_angle=PI*0.15,
            angle=TAU * 0.85,
            radius=0.45
        ).move_arc_center_to(gf[1].get_center() + 0.4*LEFT)

        loop.add_tip(at_start=False, tip_length=0.15, tip_width=0.15)
        endolabel = Tex("$(+ 1)$").scale(0.5)
        endolabel.next_to(loop, LEFT, buff=0.1)
        self.play(Create(loop), Create(endolabel))
        self.wait(1)
        dendo = Dot().set_color(GOLD)
        label12endo = Tex("12").scale(0.5)
        label13endo = Tex("13").scale(0.5)
        label12endo.next_to(dendo, UP + RIGHT, buff=0.1)
        endotext = Text("endomorphism",font_size=20)
        endotext.next_to(dendo, 4*RIGHT)
       
        self.play(
            MoveAlongPath(dendo, loop),
            Transform(label12endo, label13endo),
            UpdateFromFunc(label12endo, lambda m: m.next_to(dendo, DOWN + 1.5*RIGHT, buff=0.1)),
            FadeIn(endotext),
            Circumscribe(endotext, color=GOLD),
            rate_func=smooth,
            run_time=2.5
        )
        self.wait(1)


        self.play(FadeOut(loop), FadeOut(endolabel),
                  FadeOut(dendo), FadeOut(label12endo),
                  FadeOut(intdot),FadeOut(intlabel),
                  FadeOut(endotext))

    def arc_between_circles(self, c1, c2, radius=4, tip=True, arc="arc", color=WHITE):
        start_center = c1.get_center()
        end_center = c2.get_center()
        direction_vector = end_center - start_center
        direction_unit = direction_vector / np.linalg.norm(direction_vector)
        start_point = start_center + c1.radius * direction_unit
        end_point = end_center - c2.radius * direction_unit

        if(arc == "Line"):
            arc = Line(start_point, end_point, stroke_width=10).set_color(
                color=["#5ce1e6","#ff72e4","#5ce1e6"])
        else:
            arc = ArcBetweenPoints(start_point, end_point, radius=radius, stroke_width=6, color=color)
        if tip:
            arc.add_tip(tip_length=0.2, tip_width=0.2,tip_shape=StealthTip)
        return arc

    def connect_2cat_edges(self, cat1, cat2):
        arcs = []

        cat1edges = [cat1.edges[e] for e in cat1.edges.keys()]
        cat2edges = [cat2.edges[e] for e in cat2.edges.keys()]

        for i in range(len(cat1edges)):
            arcedges = ArcBetweenPoints(
                cat1edges[i].get_center(),
                cat2edges[i%(len(cat2edges))].get_center(),
                radius=8, stroke_width=2).set_color(
                    color=["#5de0e6", "#004aad"])
            arcedges.add_tip(tip_length=0.15, tip_width=0.15).get_tip().set_color(
                color=["#004aad"])
            arcs.append(arcedges)
        return arcs

    def connect_2cat_objs(self, cat1, cat2):
        arcs = []
        for i in cat1.vertices:
            arcobjs = ArcBetweenPoints(cat1[i].get_center(),
                                       cat2[i%(len(cat2.vertices))+1].get_center(),
                                       radius=8, stroke_width=2).set_color(
                                           color=["#ff3131", "#ff914d", "#fff84d"]
                                       )
            arcobjs.add_tip(tip_length=0.15, tip_width=0.15).get_tip().set_color(
                color=["#fff84d"])
            arcs.append(arcobjs)
        return arcs

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
        hask = Tex("Hask", font_size=30).to_edge(UP)
        self.play(FadeOut(category), FadeOut(categoryt), FadeOut(g2), FadeOut(obj), FadeOut(mrp), FadeOut(*lawsC))
        self.clear()
        self.play(Transform(g, haskdot))
        self.clear()
        self.play(Transform(haskdot, hask))

        gf, labels, extras = self.show_gf_category()
        self.wait(3)
        self.func_int_bool(gf,extras)
        self.play(FadeOut(hask))

        fuctC = Text("Functor", font_size=30).to_edge(UP)
        self.play(Transform(haskdot, fuctC))
        cat1 = self.get_cats(4, 2, 0.5)
        cat2 = self.get_cats(5, 3, 0.3)
        cat3 = self.get_cats(8, 4, 0.2)
        cat4 = self.get_cats(6, 5, 0.2)

        self.play(Create(cat1))
        self.play(cat1.animate.move_to(2 * DOWN + 4 * RIGHT).scale(0.5), run_time=2)
        circle_1 = Circle(radius=1.5, color=BLUE).move_to(cat1)
        self.play(Create(circle_1))

        self.play(Create(cat2))
        self.play(cat2.animate.move_to(2 * DOWN + 4 * LEFT).scale(0.5), run_time=2)
        circle_2 = Circle(radius=1.5, color=BLUE).move_to(cat2)
        self.play(Create(circle_2))

        self.play(Create(cat3))
        self.play(cat3.animate.move_to(2 * UP + 4 * LEFT).scale(0.5), run_time=2)
        circle_3 = Circle(radius=1.5, color=BLUE).move_to(cat3)
        self.play(Create(circle_3))

        self.play(Create(cat4))
        self.play(cat4.animate.move_to(2 * UP + 4 * RIGHT).scale(0.5), run_time=2)
        circle_4 = Circle(radius=1.5, color=BLUE).move_to(cat4)
        self.play(Create(circle_4))

        arc2_1 = self.arc_between_circles(circle_2, circle_1, arc="Line")
        arc3_4 = self.arc_between_circles(circle_3, circle_4, arc="Line")
        arc2_3 = self.arc_between_circles(circle_2, circle_3, arc="Line")
        arc1_4 = self.arc_between_circles(circle_1, circle_4, arc="Line")
        self.play(Create(arc2_1),Create(arc2_3),Create(arc3_4), Create(arc1_4))
        self.wait(3)
        self.play(
            FadeOut(cat1, cat2, circle_1, circle_2, arc2_1, arc1_4, arc2_3),
            cat3.animate.move_to(ORIGIN + 4*LEFT),
            circle_3.animate.move_to(ORIGIN + 4*LEFT),
            cat4.animate.move_to(ORIGIN + 4*RIGHT),
            circle_4.animate.move_to(ORIGIN + 4*RIGHT),
            arc3_4.animate.move_to(ORIGIN)
        )

        arcobjs = self.connect_2cat_objs(cat3, cat4)
        self.play(
            *[Create(arcobj) for arcobj in arcobjs]
        )

        self.wait(2)
        self.play(
            *[FadeOut(arcobj) for arcobj in arcobjs]
        )

        arcmrps = self.connect_2cat_edges(cat3, cat4)
        for arcmrp in arcmrps:
            self.play(Create(arcmrp), run_time=0.1)



        
        self.wait(3)
        self.play(
            FadeOut(arc3_4),
            FadeOut(circle_4),
            FadeOut(cat4),
            cat3.animate.move_to(ORIGIN),
            circle_3.animate.move_to(ORIGIN),
            *[FadeOut(arcmrp) for arcmrp in arcmrps]
        )


        self.play(
            cat3.animate.move_to(ORIGIN),
            circle_3.animate.move_to(ORIGIN),
        )

        endoFunc = Arc(
            start_angle=PI*0.40,
            angle=TAU * 0.60,
            radius=1,
            stroke_width=8
        ).set_color(color=["#0097b2", "#7ed957", "#0097b2"]).move_arc_center_to(
            cat3.get_center() + 1.5*LEFT)
        endoFunc.add_tip(at_start=False, tip_length=0.2, tip_width=0.2, tip_shape=StealthTip)

        endoFuncText = Text("endofunctor",font_size=20)
        endoFuncText.next_to(circle_3, 2*RIGHT)

        self.play(Create(endoFunc),
                  Create(endoFuncText),
                  Circumscribe(endoFuncText,
                               color=["#0097b2", "#7ed957", "#0097b2"])
                  )

        self.wait(3)

        self.play(
            FadeOut(circle_3),
            FadeOut(cat3),
            FadeOut(endoFunc),
            FadeOut(endoFuncText),
        )

        self.wait(3)

    
def hask_cat(objects, names, arcs, arclabs, lay):
    edge_config = {
        "stroke_width": 4,
        "tip_config": {
            "tip_length": 0.2,
            "tip_width": 0.2
        }
    }
    labelsText = []
    edgesLabs = []
    graph = DiGraph(objects, arcs, edge_config=edge_config,layout=lay)
    for ob in graph.vertices:
        dot = graph.vertices[ob]
        dot.scale(0.65)
        name, pos = names[ob]
        label = Tex("$" + name + "$").scale(0.8)
        label.add_updater(lambda m, d=dot, p=pos: m.next_to(d, p, buff=0.1))
        labelsText.append(label)

    for elabk in arclabs:
        arc = graph.edges[elabk]
        elabv, elabp = arclabs[elabk]
        label = Tex(elabv).scale(0.8)
        label.add_updater(lambda m, d=arc, p=elabp: m.next_to(d, p, buff=0.1))
        edgesLabs.append(label)

    return graph, labelsText, edgesLabs

def get_cats(n, seed, edge_prob):
    vertices = list(range(1, n + 1))
    random.seed(seed)
    edges = [
        (i, j)
        for i in vertices
        for j in vertices
        if i != j and random.random() < edge_prob
    ]
    edge_config_GF = {
        "stroke_width": 4,
        "tip_config": {
            "tip_length": 0.2,
            "tip_width": 0.2
        }
    }
    return DiGraph(vertices,edges,
                   edge_config=edge_config_GF,
                   vertex_config={"color":RED}, layout="circular")

def endo_func(cat_circle,pos=1, labelLay=None,):
    ang = PI/4
    shift=(2/6)
    match pos:
        case 2:
            shift+=(1/2)
        case 3:
            shift+=2*(1/2)
        case 4:
            shift+=3*(1/2)

    ang = ang*pos

    endoFunc = Arc(
        start_angle=PI+shift*PI,
        angle=TAU * 0.90,
        radius=1,
        stroke_width=8
    ).set_color(color=["#0097b2", "#7ed957", "#0097b2"])
    larger_circ = Circle().surround(cat_circle, buffer_factor=endoFunc.radius)
    p = larger_circ.point_at_angle(ang + (pos-1)*(PI/4))
    endoFunc.add_tip(at_start=False, tip_length=0.2, tip_width=0.2, tip_shape=StealthTip)
    endoFunc.move_arc_center_to(p)
    if labelLay is not None:
        name, pos = labelLay
        endolab = Tex(name).scale(0.8)
        endolab.add_updater(lambda m, a=endoFunc, p=pos: m.next_to(a,p,buff=0.1))
        return endoFunc, endolab

    return endoFunc

def color_substring(tex, subs, colors):
    return -1


def values_path(digraph, values_from_to):
   print("xd")
   
        
class FunctorScene(Scene):
    def construct(self):
        funcDefOb = Tex(
            r"$\mathcal{C}$, $\mathcal{D}$ categories\\"
            r"A functor F associates each object $X \in \mathcal{C}$\\"
            r"to an object $F(X) \in \mathcal{D}$",
        )
        funcDefOb[0][0].set_color("#0097b2")
        funcDefOb[0][2].set_color("#7ed957")
        funcDefOb[0][21].set_color(["#0097b2","#7ed957","#0097b2"])
        funcDefOb[0][42].set_color(["#ff3131"])
        funcDefOb[0][44].set_color(["#0097b2"])
        funcDefOb[0][55:57].set_color(["#0097b2","#7ed957","#0097b2"])
        funcDefOb[0][57].set_color(["#ff3131"])
        funcDefOb[0][58].set_color(["#0097b2","#7ed957","#0097b2"])
        funcDefOb[0][60].set_color(["#7ed957"])

        funcDefOb.move_to(2 * UP)

        funcDefArr = Tex(
            r"F  associates each morphism  $f : X \rightarrow Y$  in  $\mathcal{C}$\\"
            r"to a morphism  $F(f) : F(X) \rightarrow F(Y)$  in  $\mathcal{D}$",
        )
        funcDefArr[0][0].set_color(["#0097b2","#7ed957","#0097b2"])
        funcDefArr[0][25].set_color("#ff3131")
        funcDefArr[0][27].set_color("#ff3131")
        funcDefArr[0][30].set_color("#0097b2")
        funcDefArr[0][42:44].set_color(["#0097b2","#7ed957","#0097b2"])
        funcDefArr[0][45].set_color(["#0097b2","#7ed957","#0097b2"])
        funcDefArr[0][47:49].set_color(["#0097b2","#7ed957","#0097b2"])
        funcDefArr[0][50].set_color(["#0097b2","#7ed957","#0097b2"])
        funcDefArr[0][49].set_color("#ff3131")
        funcDefArr[0][52:54].set_color(["#0097b2","#7ed957","#0097b2"])
        funcDefArr[0][55].set_color(["#0097b2","#7ed957","#0097b2"])
        funcDefArr[0][54].set_color("#ff3131")
        funcDefArr[0][58].set_color("#7ed957")

        funcDefArr.next_to(funcDefOb, DOWN, buff=0.5)


        funclawId = Tex(
            r"$F(Id_X) = Id_{F(X)}$"
        )
        funclawId[0][0:2].set_color(["#0097b2","#7ed957","#0097b2"])
        funclawId[0][5].set_color(["#0097b2","#7ed957","#0097b2"])
        funclawId[0][4].set_color("#ff3131")
        funclawId[0][9:11].set_color(["#0097b2","#7ed957","#0097b2"])
        funclawId[0][12].set_color(["#0097b2","#7ed957","#0097b2"])
        funclawId[0][11].set_color("#ff3131")
        funclawId.move_to(2 * UP)

        funclawCom = Tex(
            r"$F(g \circ f) = F(g) \circ F(f)$",
        )
        funclawCom[0][0:2].set_color(["#0097b2","#7ed957","#0097b2"])
        funclawCom[0][5].set_color(["#0097b2","#7ed957","#0097b2"])
        funclawCom[0][7:9].set_color(["#0097b2","#7ed957","#0097b2"])
        funclawCom[0][10].set_color(["#0097b2","#7ed957","#0097b2"])
        funclawCom[0][12:14].set_color(["#0097b2","#7ed957","#0097b2"])
        funclawCom[0][15].set_color(["#0097b2","#7ed957","#0097b2"])

        self.play(Write(funcDefOb))
        self.play(Write(funcDefArr))
        self.wait(4)
        self.play(Unwrite(funcDefOb))
        self.play(Unwrite(funcDefArr))

        self.play(Write(funclawId))
        self.play(Write(funclawCom))
        self.wait(3)
        self.play(Unwrite(funclawId))
        self.play(Unwrite(funclawCom))

        centerDot = Dot()
        haskCat = get_cats(6, 1234, 0.1)
        circleHask = Circle(color=["#8c52ff", "#5ce1e6"]).surround(haskCat, buffer_factor=1)
        hask = Tex("Hask", font_size=30).to_edge(UP)

        self.play(
            Create(centerDot)
        )

        self.play(
            Transform(centerDot, hask),
        )
        endoList, endoLab = endo_func(circleHask,1,("[  ]", UP + RIGHT))

        self.play(
            Create(haskCat),
            Create(circleHask),
            Create(endoList),
            Create(endoLab)
        )

        self.wait(4)

        layout={1: ORIGIN + 2*LEFT, 2: ORIGIN+2*RIGHT}
        edgesLabsLay = {(1,2): ("[ ]", DOWN)}
        dotnames = {1: ("Int", LEFT), 2: ("Int", RIGHT)}
        haskListFunctor, labels, edgesLabs= hask_cat([1, 2], dotnames,
                                                     [(1, 2)],edgesLabsLay,layout)
        self.play(
            Create(hask),
            Create(haskListFunctor),
            *[Create(label) for label in labels],
            *[Create(elabel) for elabel in edgesLabs]
        )

        self.wait(3)
        self.play(
            haskListFunctor.animate.move_to(2*DOWN)
        )
        
        layout2={1: ORIGIN + 2*LEFT, 2: ORIGIN+2*RIGHT}
        edgesLabsLay2 = {(1,2): ("[ ]", UP)}
        dotnames2 = {1: ("Int", LEFT), 2: ("Int", RIGHT)}
        haskListFunctor2, labels2, edgesLabs2= hask_cat([1, 2], dotnames2,
                                                        [(1, 2)],edgesLabsLay2,layout2)
        self.play(
            Create(haskListFunctor2),
            *[Create(label) for label in labels2],
            *[Create(elabel) for elabel in edgesLabs2]
        )
        self.play(
            haskListFunctor2.animate.move_to(2*UP)
        )
        self.wait(3)
