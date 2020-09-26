from LRC_TME8_definitions_Allen import *
intervalles_nb = 13


# Fonction pour retourner l'ensemble transposé de donné
def transposeSet(S):
    if S is None:
        return set([])
    S_t = set([])  # L'ensemble transposé
    # Parcourant par tous les éléments de S, on prend leurs transposés et on les ajoute dans l'ensemble transposé
    for s in S:
        S_t.add(transpose[s])
    return S_t


# Fonction pour retourner l'ensemble symétrique de donné
def symetrieSet(S):
    if S is None:
        return set([])
    S_sym = set([])  # L'ensemble symétrique
    # Parcourant par tous les éléments de S, on prend leurs symétriques et on les ajoute dans l'ensemble symétrique
    for s in S:
        S_sym.add(symetrie[s])
    return S_sym


# Fonction auxiliaire pour faciliter un peu l'écriture de la fonction suivante (compose)
# Elle retourne une composition r1 o r2 si elle est indiquée dans le tableau et None sinon
def _composeBase(r1, r2):
    return compositionBase.get((r1, r2))


# Fonction correspondante à composition de relations données
def compose(r1, r2):
    # cas où on a au moins une relation "="
    if r1 == '=':
        return {r2}
    if r2 == '=':
        return {r1}
    # cas où on a une composition directement du tableau
    if _composeBase(r1, r2) is not None:
        return _composeBase(r1, r2)
    # cas où on peut obtenir une composition par transposition
    if _composeBase(transpose[r2], transpose[r1]) is not None:
        return transposeSet(_composeBase(transpose[r2], transpose[r1]))
    # cas où on peut obtenir une composition par symétrie
    if _composeBase(symetrie[r1], symetrie[r2]) is not None:
        return symetrieSet(_composeBase(symetrie[r1], symetrie[r2]))
    # cas où on peut obtenir une composition en utilisant ces deux opérations;
    # remarque : si on n'est dans aucun de ces 4 cas, on va retourner un ensemble vide
    return symetrieSet(transposeSet(_composeBase(transpose[symetrie[r2]], transpose[symetrie[r1]])))


# Fonction qui a pour des arguments deux ensembles de relations S1 et S2 et qui retourne (S1 o S2)
def compositionSet(S1, S2):
    comp_S = set([])
    # Parcours de tous les éléments de S1 et de S2
    for r1 in S1:
        for r2 in S2:
            # On ajoute dans l'ensemble du résultat composition deux-à-deux de toutes relations de S1 et de S2
            comp_S = comp_S.union(compose(r1, r2))
    return comp_S


class Graphe:

    # constructeur le plus simple
    def __init__(self, noeuds=None, relations=None):
        self.noeuds = noeuds.copy() if noeuds is not None else set([])
        self.relations = relations.copy() if relations is not None else {}

    # méthode pour copier les objets superficiellement
    def __copy__(self):
        gcopy = Graphe(self.noeuds, self.relations)
        return gcopy

    # méthode pour afficher les graphes
    def __str__(self):
        return 'Graphe {0}\nnoeuds : {1}\nrelations : {2}\n{3}'.format('{', self.noeuds, self.relations, '}')

    # méthode pour copier les objets superficiellement
    def copy(self):
        return self.__copy__()

    # méthode pour retourner les relations entre deux noeuds donnés
    def getRelations(self, i, j):
        S_initial = self.relations.get((i, j))
        if S_initial is None:
            S_initial = set([])
        return S_initial.union(transposeSet(self.relations.get((j, i))))

    # méthode qui fait une propagation des relations entre i et j selon l'algorithme d'Allen
    # ATTENTION : cette méthode ne change pas le graphe initial mais retourne un nouveau avec des relations propagées
    def propagation(self, i, j):
        pile_rels = [(i, j, self.getRelations(i, j))]
        gtemp = self.copy()
        rel_appended = []
        # On suppose par défaut que s'il n'y a pas de relations entre deux noeuds on a toutes les relations possibles
        for n1 in gtemp.noeuds:
            for n2 in gtemp.noeuds:
                if n1 != n2 and len(gtemp.getRelations(n1, n2)) == 0:
                    gtemp = gtemp.ajouter(n1, n2,
                                          {'<', 'm', 'o', 'et', 'dt', 's', '=', 'st', 'd', 'e', 'ot', 'mt', '>'}
                                          )
                    rel_appended.append((n1, n2))
        # Algorithme d'Allen
        while len(pile_rels) != 0:
            i, j, rel_ij = pile_rels.pop()
            for k in gtemp.noeuds:
                if k == i or k == j:
                    continue
                new_rel_ik = gtemp.getRelations(i, k).intersection(
                    compositionSet(rel_ij, gtemp.getRelations(j, k))
                )
                new_rel_kj = gtemp.getRelations(k, j).intersection(
                    compositionSet(gtemp.getRelations(k, i), rel_ij)
                )
                if len(new_rel_ik) == 0 or len(new_rel_kj) == 0:
                    return None
                if new_rel_ik != gtemp.getRelations(i, k):
                    gtemp.relations[(i, k)] = new_rel_ik
                    gtemp.relations[(k, i)] = set()
                    pile_rels.append((i, k, new_rel_ik))
                if new_rel_kj != gtemp.getRelations(k, j):
                    gtemp.relations[(k, j)] = new_rel_kj
                    gtemp.relations[(j, k)] = set()
                    pile_rels.append((k, j, new_rel_kj))
        # Parmi les relations ajoutées au début
        # on supprime les relations qui consistent à toutes les relations possibles
        for n1, n2 in rel_appended:
            if len(gtemp.getRelations(n1, n2)) == intervalles_nb:
                gtemp.relations.pop((n1, n2))
        return gtemp

    # méthode qui ajoute une relation dans un graphe
    # ATTENTION : cette méthode ne change pas le graphe initial mais retourne un nouveau avec la relation ajoutée
    def ajouter(self, i, j, relation):
        gtemp = self.copy()
        gtemp.noeuds = gtemp.noeuds.union({i, j})
        gtemp.relations[(i, j)] = gtemp.getRelations(i, j).union(relation)
        return gtemp


if __name__ == '__main__':
    # Tests de la fonction transposeSet
    print('Tests de la fonction transposeSet\n')
    s1 = {'>', 'e', 'dt'}
    print('Test 1')
    print('L\'ensemble donné : {0}\nL\'ensemble transposé : {1}'.format(s1, transposeSet(s1)))
    s2 = {'=', 'st', '<', 'mt', 'o'}
    print('Test 2')
    print('L\'ensemble donné : {0}\nL\'ensemble transposé : {1}'.format(s2, transposeSet(s2)))
    s3 = {'>', 'et', 'ot', 'm', '>'}
    print('Test 3')
    print('L\'ensemble donné : {0}\nL\'ensemble transposé : {1}'.format(s3, transposeSet(s3)))
    print()

    # Tests de la fonction symetrieSet
    print('Tests de la fonction symetrieSet\n')
    s1 = {'>', 'e', 'dt'}
    print('Test 1')
    print('L\'ensemble donné : {0}\nL\'ensemble symétrique : {1}'.format(s1, symetrieSet(s1)))
    s2 = {'=', 'st', '<', 'mt', 'o'}
    print('Test 2')
    print('L\'ensemble donné : {0}\nL\'ensemble symétrique : {1}'.format(s2, symetrieSet(s2)))
    s3 = {'>', 'et', 'ot', 'm', '>'}
    print('Test 3')
    print('L\'ensemble donné : {0}\nL\'ensemble symétrique : {1}'.format(s3, symetrieSet(s3)))
    print()

    # Tests de la composition
    print('Tests de la composition')
    print('(= o d) = {0}'.format(compose('=', 'd')))
    print('(m o d) = {0}'.format(compose('m', 'd')))
    print('(ot o >) = {0}'.format(compose('ot', '>')))
    print('(> o e) = {0}'.format(compose('>', 'e')))
    print('(ot o m) = {0}'.format(compose('ot', 'm')))
    print()

    # Tests de la composition des ensembles
    print('Tests de la composition des ensembles')
    s1 = {'m', 'o'}
    s2 = {'dt', 'et', 'st', '='}
    print('s1 o s2 = {0}\noù s1 = {1} et s2 = {2}'.format(compositionSet(s1, s2), s1, s2))
    s3 = {'e', '=', 'et'}
    s4 = {'s', '=', 'd', 'e'}
    print('s3 o s4 = {0}\noù s3 = {1} et s4 = {2}'.format(compositionSet(s3, s4), s3, s4))
    print()

    # Tests de la classe Graphe
    # Initialization
    print('Tests de la classe Graphe')
    print('On a un graphe suivant:\n')
    g1 = Graphe(noeuds={'A', 'B', 'C'}, relations={('A', 'B'): {'m', 'o'}, ('B', 'C'): {'dt', 'et', 'st', '='}})
    print(g1)
    # Tests de la méthode Graphe.getRelations
    print('Relations entre C et B : {0}'.format(g1.getRelations('C', 'B')))
    print('Relations entre B et A : {0}'.format(g1.getRelations('B', 'A')))
    # Tests de la méthode Graphe.ajouter
    g2 = Graphe(noeuds=set([]), relations={})
    g2 = g2.ajouter('A', 'B', {'m'})
    g2 = g2.ajouter('A', 'B', {'o'})
    g2 = g2.ajouter('B', 'C', {'dt', 'et'})
    g2 = g2.ajouter('C', 'B', {'s', '='})
    print('Relations de g1 :')
    print('Entre A et B : {0}'.format(g1.getRelations('A', 'B')))
    print('Entre B et C : {0}'.format(g1.getRelations('B', 'C')))
    print('Relations de g2 :')
    print('Entre A et B : {0}'.format(g2.getRelations('A', 'B')))
    print('Entre B et C : {0}'.format(g2.getRelations('B', 'C')))
    # Test de la méthode Graphe.propagation
    g3 = Graphe(noeuds={'A', 'B', 'C'}, relations={('A', 'B'): {'<'}, ('A', 'C'): {'>'}})
    g3 = g3.ajouter('B', 'C', {'='})
    print('Graph g3')
    print(g3)
    print('Résultat de propagation')
    print(g3.propagation('B', 'C'))
    # On voit que pour ce graphe avec ces relations si on ajoute B {=} C on obtient None
    # Ce résultat est attendu car on a déjà A {<} B et A {>} C alors B {=} C est une contradiction
    g4 = Graphe(noeuds={'A', 'B', 'C'}, relations={('A', 'B'): {'<'}, ('A', 'C'): {'<'}})
    g4 = g4.ajouter('B', 'C', {'='})
    print('Graph g4')
    print(g4)
    print('Résultat de propagation')
    print(g4.propagation('B', 'C'))
    # En même temps on voit que pour ce graphe suivant une propagation ne change rien
    # En fait, si A {<} B et A {<} C on n'obtiendra pas des nouvelles informations en disant que B {=} C

    # Exercice 2 Questions 5 et 6
    # On initialise le graphe par des informations données dans l'énoncé
    gr_ex_2_q_5_6 = Graphe(
        noeuds={'L', 'R', 'S'},
        relations={('L', 'S'): {'ot', 'mt'}, ('S', 'R'): {'<', 'm', 'mt', '>'}}
    )
    # On propage toutes les relations qu'on a
    gr_ex_2_q_5_6 = gr_ex_2_q_5_6.propagation('L', 'S')
    gr_ex_2_q_5_6 = gr_ex_2_q_5_6.propagation('S', 'R')
    # Affichage de relations après une propagation
    print('\nExercice 2 Questions 5 et 6')
    print('L {0} S'.format(gr_ex_2_q_5_6.getRelations('L', 'S')))
    print('S {0} R'.format(gr_ex_2_q_5_6.getRelations('S', 'R')))
    print('L {0} R'.format(gr_ex_2_q_5_6.getRelations('L', 'R')))
    # On modélise ces connaissance comme L {o, s, d} R
    gr_ex_2_q_5_6 = Graphe(
        noeuds={'L', 'R', 'S'},
        relations={('L', 'S'): {'ot', 'mt'}, ('S', 'R'): {'<', 'm', 'mt', '>'}}
    )
    gr_ex_2_q_5_6 = gr_ex_2_q_5_6.ajouter('L', 'R', {'o', 's', 'd'})
    gr_ex_2_q_5_6 = gr_ex_2_q_5_6.propagation('L', 'R')
    gr_ex_2_q_5_6 = gr_ex_2_q_5_6.propagation('L', 'S')
    gr_ex_2_q_5_6 = gr_ex_2_q_5_6.propagation('S', 'R')
    # On a donc supprimer certains cas pas possibles

    print('Après avoir appris et propager une nouvelle connaissance')
    print('L {0} S'.format(gr_ex_2_q_5_6.getRelations('L', 'S')))
    print('S {0} R'.format(gr_ex_2_q_5_6.getRelations('S', 'R')))
    print('L {0} R'.format(gr_ex_2_q_5_6.getRelations('L', 'R')))

    # On résout l'exercice 2 du TD en utilisant la classe et les fonctions réalisées
    gr_ex_2_TD = Graphe()
    gr_ex_2_TD = gr_ex_2_TD.ajouter('J', 'D', {'o', 'et', 'dt', 's', '=', 'st', 'd', 'e', 'ot'})
    gr_ex_2_TD = gr_ex_2_TD.ajouter('J', 'C', {'e', '=', 'et'})
    gr_ex_2_TD = gr_ex_2_TD.ajouter('D', 'P', {'<', 'm'})
    print('\nExercice 2 Question 7')
    print('Relations dans le graphe avant une propagation :')
    print('J {0} D'.format(gr_ex_2_TD.getRelations('J', 'D')))
    print('J {0} C'.format(gr_ex_2_TD.getRelations('J', 'C')))
    print('D {0} P'.format(gr_ex_2_TD.getRelations('D', 'P')))
    # On ajoute l'information que café est une étape d'un petit-déjeuner
    gr_ex_2_TD = gr_ex_2_TD.ajouter('C', 'D', {'s', '=', 'd', 'e'})
    print('C {0} D'.format(gr_ex_2_TD.getRelations('C', 'D')))
    # On propage cette relation dans le graphe
    gr_ex_2_TD = gr_ex_2_TD.propagation('C', 'D')
    # On voit qu'une relation entre 'J' et 'D' a été mise-à-jour
    print('Relations après la propagation :')
    print('J {0} D'.format(gr_ex_2_TD.getRelations('J', 'D')))
    print('J {0} C'.format(gr_ex_2_TD.getRelations('J', 'C')))
    print('D {0} P'.format(gr_ex_2_TD.getRelations('D', 'P')))
    print('C {0} D'.format(gr_ex_2_TD.getRelations('C', 'D')))
