from lingpy.compare.partial import *
from lingpy.evaluate.acd import bcubes
from lexibank_gaotb import Dataset

part = Partial.from_cldf(Dataset().cldf_dir.joinpath('cldf-metadata.json'), columns=['concept_id', 'concept_name', 'language_id', 'language_name', 'value', 'form', 'segments', 'cogid_cognateset_id'], namespace=(('concept_name', 'concept'), ('language_id', 'doculect'), ('cogid_cognateset_id', 'cog'), ('segments', 'tokens')))
part.renumber('cog')
part.partial_cluster(method='sca', ref='cogids', threshold=0.45, cluster_method='upgma')
part.add_cognate_ids("cogids", "autocogid", idtype="strict")

bcubes(part, "cogid", "autocogid")


part.add_cognate_ids('cogids', 'looseid', idtype='loose')
bcubes(part, "cogid", "looseid")