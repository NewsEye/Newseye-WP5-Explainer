import datetime
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
from explainer.resources.big_collection_resource import BigCollectionResource
from explainer.resources.brute_force_resource import BruteForceResource
from explainer.resources.comparison_resource import ComparisonResource
from explainer.resources.crosslingual_comparison_resource import CrosslingualcomparisonResource
from explainer.resources.expand_query_resource import ExpandQueryResource
from explainer.resources.extract_bigrams_resource import ExtractBigramsResource
from explainer.resources.extract_facets_resource import ExtractFacetsResource
from explainer.resources.extract_names_resource import ExtractNamesResource
from explainer.resources.extract_words_resource import ExtractWordsResource
from explainer.resources.find_best_split_from_timeseries_resource import FindBestSplitFromTimeseriesResource
from explainer.resources.generate_time_series_resource import GenerateTimeSeriesResource
from explainer.resources.global_strategy_resource import GlobalStrategyResource
from explainer.resources.impossible_to_split_resource import ImpossibleToSplitResource
from explainer.resources.initialization_resource import InitializationResource
from explainer.resources.interesting_results_resource import InterestingResultsResource
from explainer.resources.language_resource import LanguageResource
from explainer.resources.new_collection_resource import NewCollectionResource
from explainer.resources.not_enough_data_resource import NotEnoughDataResource
from explainer.resources.nothing_to_compare_resource import NothingToCompareResource
from explainer.resources.path_stop_resource import PathStopResource
from explainer.resources.processor_resource import ProcessorResource, ReasonResource, TaskResource
from explainer.resources.query_topic_model_resource import QueryTopicModelResource
from explainer.resources.same_language_collections_resource import SameLanguageCollectionsResource
from explainer.resources.small_collection_resource import SmallCollectionResource
from explainer.resources.split_by_facet_resource import SplitByFacetResource
from explainer.resources.summarization_resource import SummarizationResource
from explainer.resources.too_big_collection_resource import TooBigCollectionResource
from explainer.resources.topic_model_document_linking_resource import TopicModelDocumentLinkingResource
from explainer.resources.topic_model_document_set_comparison_resource import TopicModelDocumentSetComparisonResource
from explainer.resources.track_name_sentiment_resource import TrackNameSentimentResource
from explainer.resources.unknown_reason_resource import UnknownReasonResource
from explainer.resources.unknown_task_resource import UnknownTaskResource

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
            UnknownTaskResource(),
            UnknownReasonResource(),
            #
            # Reasons
            BigCollectionResource(),
            BruteForceResource(),
            CrosslingualcomparisonResource(),
            GlobalStrategyResource(),
            InitializationResource(),
            ImpossibleToSplitResource(),
            InterestingResultsResource(),
            LanguageResource(),
            NewCollectionResource(),
            NotEnoughDataResource(),
            NothingToCompareResource(),
            PathStopResource(),
            SameLanguageCollectionsResource(),
            SmallCollectionResource(),
            TooBigCollectionResource(),
            #
            # Tasks
            ComparisonResource(),
            ExpandQueryResource(),
            ExtractBigramsResource(),
            ExtractFacetsResource(),
            ExtractNamesResource(),
            ExtractWordsResource(),
            FindBestSplitFromTimeseriesResource(),
            GenerateTimeSeriesResource(),
            QueryTopicModelResource(),
            SplitByFacetResource(),
            SummarizationResource(),
            TopicModelDocumentLinkingResource(),
            TopicModelDocumentSetComparisonResource(),
            TrackNameSentimentResource(),
        ]

        # Templates
        self.registry.register(
            "templates",
            self._get_cached_or_compute("../data/templates.cache", self._load_templates, force_cache_refresh=True),
        )

        # Misc language data
        self.registry.register("CONJUNCTIONS", CONJUNCTIONS)

        # Task and Reason parsers
        self.registry.register("task-parsers", [])
        self.registry.register("reason-parsers", [])
        for resource in self.processor_resources:
            if isinstance(resource, TaskResource):
                self.registry.get("task-parsers").append(resource.parse_task)
            if isinstance(resource, ReasonResource):
                self.registry.get("reason-parsers").append(resource.parse_reason)

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
        log.info("Starting generation")
        start_time = datetime.datetime.now().timestamp()
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

        end_time = datetime.datetime.now().timestamp()
        log.info("Generation complete. Time taken in seconds: {}".format(end_time - start_time))

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
