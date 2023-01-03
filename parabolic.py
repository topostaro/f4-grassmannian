from sage.modules.vector_integer_dense import vector
from sage.matrix.constructor import matrix
from sage.combinat.root_system.weyl_characters import WeylCharacterRing


# 最高ウェイト表現のウェイトを最高ウェイトとの差で表す関数。
def root_difference_multiplicities(character_ring, highest_weight) -> dict:
    weight_multiplicities = character_ring(highest_weight).weight_multiplicities()
    A = matrix([ vector(sr) for sr in character_ring.simple_roots() ]).transpose()

    result ={}

    for k, v in weight_multiplicities.items():
        Y = vector(k) - vector(highest_weight)
        result[tuple(A.solve_right(Y))] = v
    
    return result

# Parabolic subgroupを表すクラス
class ParabolicSubgroup:
    def __init__(self, G, L, crossed_out_nodes) -> None:
        self.G = G
        self.L = L
        self.crossed_out_nodes = crossed_out_nodes
        self.R_G = WeylCharacterRing(self.G)
        self.R_L = WeylCharacterRing(self.L)

    def __repr__(self) -> str:
        return f'the parabolic subgroup of {self.G} with crossed-out nodes {self.crossed_out_nodes}'

    def dynkin_diagram(self):
        return self.G.marked_nodes(self.crossed_out_nodes).dynkin_diagram()

    def ambient_space(self):
        return self.R_G.space()
    
    def ambient_space_dimension(self):
        return self.R_G.space().dimension()

    # Sagemathのライブラリでは1-indexを用いるが、ここでは簡単のためとりあえず0-indexで表す
    def simple_roots(self):
        return [ self.R_G.simple_roots()[i] for i in set(1..self.G.rank()) - set(self.crossed_out_nodes)]

    def positive_roots(self):
        L = self.ambient_space()

        # positive rootからcutoutされるsimple rootを引き, positiveでなければuncrossed nodeから生成されると判定
        roots = [ pr for pr in self.G.root_system().root_lattice().positive_roots()]
        for i in self.crossed_out_nodes:
            roots = [ pr for pr in roots if not (pr - (self.G.root_system().root_lattice().simple_roots())[i]).is_positive_root()]

        # ambient spaceの元に変換
        return [ L(pr) for pr in roots ]

    # 引数の`weight`は基本ウェイトを基底にして表示したもの
    def weight_muliplicities(self, weight) -> dict:
        # GとLのディンキン図の頂点のずれを補正する関数
        def correct_index(index: int) -> int:
            for i in range(len(self.crossed_out_nodes)):
                if index + i < self.crossed_out_nodes[i]:
                    return index + i
            return index + len(self.crossed_out_nodes)

        fws_L = [fw for fw in self.R_L.fundamental_weights()] # conversion from 1-index to 0-index
        weight_for_L = [ weight[i - 1] for i in set(1..len(weight))-set(self.crossed_out_nodes)] 
        weight_for_L = sum( weight_for_L[i] * fws_L[i] for i in range(self.L.rank()))

        fws_G = [fw for fw in self.R_G.fundamental_weights()]
        weight_for_G = sum( weight[i] * fws_G[i] for i in range(self.G.rank()))

        mul_set = root_difference_multiplicities(self.R_L, weight_for_L)

        result = {}
        for k, v in mul_set.items():
            w = weight_for_G \
                + sum(k[i - 1] * self.R_G.simple_roots()[correct_index(i)] 
                    for i in (1..self.L.rank()))
            result[w] = v

        return result
    
    def weyl_dimension(self, weight: list) -> int:
        return self.ambient_space().weyl_dimension(sum(weight[i - 1] * self.R_G.fundamental_weights()[i] for i in (1..self.G.rank())))