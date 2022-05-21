from chrono.feature_extractors.all_of_feature_extractor import AllOfFeatureExtractor
from chrono.feature_extractors.feature_extractor import FeatureExtractor
from chrono.feature_extractors.one_of_feature_extractor import OneOfFeatureExtractor
from chrono.feature_extractors.regex_feature_extractor import RegexFeatureExtractor
from chrono.feature_extractors.static_tags_feature_extractor import StaticTagsFeatureExtractor
from chrono.model.feature_extractors_descriptors import FeatureExtractorDescriptors, FeatureExtractorDescriptor, \
    StaticTagsFeatureExtractorDescriptor, RegexFeatureExtractorDescriptor, AllOfFeatureExtractorDescriptor, \
    OneOfFeatureExtractorDescriptor


def build_single_feature_extractor(descriptor: FeatureExtractorDescriptor) -> FeatureExtractor:
    if isinstance(descriptor, StaticTagsFeatureExtractorDescriptor):
        return StaticTagsFeatureExtractor(descriptor)

    if isinstance(descriptor, RegexFeatureExtractorDescriptor):
        return RegexFeatureExtractor(descriptor)

    if isinstance(descriptor, AllOfFeatureExtractorDescriptor):
        return AllOfFeatureExtractor([build_single_feature_extractor(fed) for fed in descriptor.all_of])

    if isinstance(descriptor, OneOfFeatureExtractorDescriptor):
        return OneOfFeatureExtractor([build_single_feature_extractor(fed) for fed in descriptor.one_of])


def build_feature_extractor(feature_extractor_descriptors: FeatureExtractorDescriptors, exhaustive: bool = False) -> FeatureExtractor:
    return OneOfFeatureExtractor(
        [build_single_feature_extractor(fed) for fed in feature_extractor_descriptors.feature_extractors],
        exhaustive=exhaustive
    )
