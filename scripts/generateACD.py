from lingpy import *
from lingpy.compare.partial import Partial
from lingpy.convert.plot import plot_tree

from lexibank_gaotb import Dataset

columns = columns=['concept_id', 'concept_name', 'language_id', 'language_name', 'value', 'form', 'cogid_cognateset_id']
namespace = (('concept_name', 'concept'), ('language_id', 'doculect'), ('cogid_cognateset_id', 'cog'))
wl = Wordlist.from_cldf(Dataset().cldf_dir.joinpath('cldf-metadata.json'), columns=columns, namespace=namespace)
wl.renumber("cog")
wl.calculate('distances')
wl.output('dst', filename='expertCognates')
wl.calculate('tree', ref='cogid', tree_calc='upgma')
plot_tree(str(wl.tree), filename="treeEXP-UPGMA", fileformat="png")
wl.calculate('tree', ref='cogid', tree_calc='neighbor', force=True)
plot_tree(str(wl.tree), filename="treeEXP-NEI", fileformat="png")

#get our cldf data
partSCA = Partial.from_cldf(Dataset().cldf_dir.joinpath('cldf-metadata.json'))
#generate the acd cluster
partSCA.partial_cluster(threshold=0.45, ref="cogids", cluster_method="upgma")
#align the cluster and save it
almsSCA = Alignments(partSCA, ref='cogids')
almsSCA.align()
almsSCA.output('tsv', filename='autoCognatesSCA', ignore='all', prettify=False)

#add missing ids for the tree
partSCA.add_cognate_ids('cogids', 'cogid', idtype='strict')
#plot
partSCA.calculate('tree', ref='cogid', tree_calc='upgma')
plot_tree(str(partSCA.tree), filename="treeSCA-UPGMA", fileformat="png")
partSCA.calculate('tree', ref='cogid', tree_calc='neighbor', force=True)
plot_tree(str(partSCA.tree), filename="treeSCA-NEI", fileformat="png")



#get our cldf data
partLEX = Partial.from_cldf(Dataset().cldf_dir.joinpath('cldf-metadata.json'))
#generate cluster
partLEX.get_partial_scorer(runs=1000)
partLEX.partial_cluster(method='lexstat', threshold=0.55, cluster_method='upgma', ref="lexstatids")
partLEX.output('tsv', filename='autoCognatesLEX', ignore='all', prettify=False)

#plot
partLEX.calculate('tree', ref='lexstatids', tree_calc='upgma')
plot_tree(str(partLEX.tree), filename="treeLEX-UPGMA", fileformat="png")
partLEX.calculate('tree', ref='lexstatids', tree_calc='neighbor', force=True)
plot_tree(str(partLEX.tree), filename="treeLEX-NEI", fileformat="png")

part = Partial.from_cldf(Dataset().cldf_dir.joinpath('cldf-metadata.json'))
print('Dataset has {0} concepts, {1} languages and {2} words.'.format(part.height, part.width, len(part)))