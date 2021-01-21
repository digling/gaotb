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
        replacements=[(" ", "_")],
        first_form_only=True,
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
        args.log.info('[i] added concepts')
        languages = args.writer.add_languages(lookup_factory="Number")
        args.log.info('[i] added languages')
        args.writer.add_sources()
        
        missingL, missingC = set(), set()
        missingCog = set()
        cogids = {}
        for row in progressbar(
                self.raw_dir.read_csv('data.tsv', delimiter='\t', dicts=True)):
            lid = languages.get(row['LANGUAGE'])
            cid = concepts.get(row['SID'])
            # take only the first cognate ID if there are several
            cog = row['COGNATE'].split('|')[0]
            if lid and cid and row["FORM"] and row["FORM"].strip():
                lexemes = args.writer.add_forms_from_value(
                    Language_ID=lid,
                    Parameter_ID=cid,
                    Value=row["FORM"],
                    Source='Sun1991'
                )
                if cog.strip():
                    cogid = cid+'-'+cog
                    args.writer.add_cognate(
                            lexeme=lexemes[0],
                            Cognateset_ID=cogid,
                            Cognate_Detection_Method='expert',
                            Source='Gao2020'
                            )
                else:
                    missingCog.add(cogid)

            if not lid:
                missingL.add(lid)
            if not cid:
                missingC.add(cid)
        for entry in missingL:
            print('missing L {0}'.format(entry))
        for entry in missingC:
            print('missing C {0}'.format(entry))
        for entry in missingCog:
            print('missing Cognate {0}'.format(entry))

