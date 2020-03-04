import gzip
import logging
import os
import pickle
import random
from collections import defaultdict
from typing import Callable, Dict, Iterable, List, Optional, Tuple, TypeVar

from explainer.constants import CONJUNCTIONS, get_error_message
from explainer.core.document_planner import NoInterestingMessagesException
from explainer.core.models import Template
from explainer.core.morphological_realizer import MorphologicalRealizer
from explainer.core.pipeline import NLGPipeline, NLGPipelineComponent
from explainer.core.realize_slots import SlotRealizer
from explainer.core.registry import Registry
from explainer.core.surface_realizer import BodyHTMLListSurfaceRealizer, BodyHTMLOrderedListSurfaceRealizer
from explainer.core.template_reader import read_templates
from explainer.core.template_selector import TemplateSelector
from explainer.english_uralicNLP_morphological_realizer import EnglishUralicNLPMorphologicalRealizer
from explainer.explainer_document_planner import ExplainerDocumentPlanner
from explainer.explainer_message_generator import ExplainerMessageGenerator, NoMessagesForSelectionException
from explainer.explainer_named_entity_resolver import ExplainerEntityNameResolver
from explainer.finnish_uralicNLP_morphological_realizer import FinnishUralicNLPMorphologicalRealizer
from explainer.resources.extract_bigrams_resource import ExtractBigramsResource
from explainer.resources.extract_facets_resource import ExtractFacetsResource
from explainer.resources.extract_words_resource import ExtractWordsResource
from explainer.resources.generate_time_series_resource import GenerateTimeSeriesResource
from explainer.resources.generic_explainer_resource import GenericExplainerResource
from explainer.resources.processor_resource import ProcessorResource

log = logging.getLogger("root")


class ExplainerNlgService(object):

    processor_resources: List[ProcessorResource] = []

    # These are (re)initialized every time run_pipeline is called
    body_pipeline = None
    headline_pipeline = None

    def __init__(self, random_seed: int = None) -> None:
        """
        :param random_seed: seed for random number generation, for repeatability
        """

        # New registry and result importer
        self.registry = Registry()

        # Per-processor resources
        self.processor_resources = [
            GenericExplainerResource(),
            ExtractWordsResource(),
            ExtractBigramsResource(),
            ExtractFacetsResource(),
            GenerateTimeSeriesResource(),
        ]

        # Templates
        self.registry.register(
            "templates",
            self._get_cached_or_compute("../data/templates.cache", self._load_templates, force_cache_refresh=True),
        )

        # Misc language data
        self.registry.register("CONJUNCTIONS", CONJUNCTIONS)

        # PRNG seed
        self._set_seed(seed_val=random_seed)

        # Slot Realizers Components
        self.registry.register("slot-realizers", [])
        for processor_resource in self.processor_resources:
            components = [component(self.registry) for component in processor_resource.slot_realizer_components()]
            self.registry.get("slot-realizers").extend(components)

    T = TypeVar("T")

    def _get_cached_or_compute(
        self, cache: str, compute: Callable[..., T], force_cache_refresh: bool = False, relative_path: bool = True
    ) -> T:  # noqa: F821 -- Needed until https://github.com/PyCQA/pyflakes/issues/427 reaches a release
        if relative_path:
            cache = os.path.abspath(os.path.join(os.path.dirname(__file__), cache))
        if force_cache_refresh:
            log.info("force_cache_refresh is True, deleting previous cache from {}".format(cache))
            if os.path.exists(cache):
                os.remove(cache)
        if not os.path.exists(cache):
            log.info("No cache at {}, computing".format(cache))
            result = compute()
            if not os.path.exists(os.path.dirname(cache)):
                os.makedirs(os.path.dirname(cache))
            with gzip.open(cache, "wb") as f:
                pickle.dump(result, f)
            return result
        else:
            log.info("Found cache at {}, decompressing and loading".format(cache))
            with gzip.open(cache, "rb") as f:
                return pickle.load(f)

    def _load_templates(self) -> Dict[str, List[Template]]:
        log.info("Loading templates")
        templates: Dict[str, List[Template]] = defaultdict(list)
        for resource in self.processor_resources:
            for language, new_templates in read_templates(resource.templates_string())[0].items():
                templates[language].extend(new_templates)
        return templates

    def _get_components(self, realizer: str) -> Iterable[NLGPipelineComponent]:
        yield ExplainerMessageGenerator()
        yield ExplainerDocumentPlanner()
        yield TemplateSelector()
        yield SlotRealizer()
        yield ExplainerEntityNameResolver()

        yield MorphologicalRealizer(
            {"fi": FinnishUralicNLPMorphologicalRealizer(), "en": EnglishUralicNLPMorphologicalRealizer()}
        )

        if realizer == "ol":
            yield BodyHTMLOrderedListSurfaceRealizer()
        else:
            yield BodyHTMLListSurfaceRealizer()

    def run_pipeline(self, language: str, output_format: str, data: str) -> Tuple[str, Optional[str]]:
        log.info("Configuring Body NLG Pipeline")
        self.body_pipeline = NLGPipeline(self.registry, *self._get_components(output_format))
        self.headline_pipeline = NLGPipeline(self.registry, *self._get_components("headline"))

        err = None

        log.info("Running NLG pipeline: language={}".format(language))
        try:
            body = self.body_pipeline.run((data,), language, prng_seed=self.registry.get("seed"))
            log.info("Body pipeline complete")
        except NoMessagesForSelectionException as ex:
            log.error("%s", ex)
            body = get_error_message(language, "no-messages-for-selection")
            err = "NoMessagesForSelectionException"
        except NoInterestingMessagesException as ex:
            log.info("%s", ex)
            err = "NoInterestingMessagesException"
            body = get_error_message(language, "no-interesting-messages-for-selection")
        except Exception as ex:
            log.exception("%s", ex)
            body = get_error_message(language, "general-error")
            err = "{}: {}".format(ex.__class__.__name__, str(ex))

        return body, err

    def _set_seed(self, seed_val: Optional[int] = None) -> None:
        log.info("Selecting seed for NLG pipeline")
        if not seed_val:
            seed_val = random.randint(1, 10000000)
            log.info("No preset seed, using random seed {}".format(seed_val))
        else:
            log.info("Using preset seed {}".format(seed_val))
        self.registry.register("seed", seed_val)

    def get_languages(self) -> List[str]:
        return list(self.registry.get("templates").keys())
