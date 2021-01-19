from pathlib import Path
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank import Language, FormSpec, Concept
from pylexibank import progressbar

from clldutils.misc import slug
import attr


@attr.s
class CustomLanguage(Language):
    Number = attr.ib(default=None)
    Chinese_Name = attr.ib(default=None)

@attr.s
class CustomConcept(Concept):
    Number = attr.ib(default=None)
    Chinese_Gloss = attr.ib(default=None)

class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "gaotb"
    language_class = CustomLanguage
    concept_class = CustomConcept
    form_spec = FormSpec(
        missing_data=("---",),
        separators="/;",
        replacements=[(" ", "_")]
    )

    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.
        """
        concepts = {}
        for concept in self.conceptlists[0].concepts.values():
            cid = '{0}_{1}'.format(concept.number, slug(concept.english))
            args.writer.add_concept(
                ID=cid,
                Name=concept.english,
                Concepticon_ID=concept.concepticon_id,
                Concepticon_Gloss=concept.concepticon_gloss,
                Number=concept.number
            )
            concepts[concept.number] = cid
        languages = args.writer.add_languages(lookup_factory="Number")
        args.writer.add_sources()
        
        missingL, missingC = set(), set()
        for row in self.raw_dir.read_csv('data.tsv', delimiter='\t', dicts=True):
            lid = languages.get(row['LANGUAGE'])
            cid = concepts.get(row['SID'])
            if lid and cid and row["FORM"] and row["FORM"].strip():
                args.writer.add_forms_from_value(
                    Language_ID=lid,
                    Parameter_ID=cid,
                    Value=row["FORM"],
                    Source='Sun1991'
                )
            if not lid:
                missingL.add(lid)
            if not cid:
                missingC.add(cid)
        for entry in missingL:
            print('missing L {0}'.format(lid))
        for entry in missingC:
            print('missing C {0}'.format(cid))

