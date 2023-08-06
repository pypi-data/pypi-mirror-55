# -*- coding: utf-8 -*-
"""Test suite for prance.ResolvingParser ."""

__author__ = 'Jens Finkhaeuser'
__copyright__ = 'Copyright (c) 2016-2018 Jens Finkhaeuser'
__license__ = 'MIT +no-false-attribs'
__all__ = ()

import pytest

from prance import ResolvingParser
from prance import ValidationError

from . import none_of

@pytest.fixture
def petstore_parser():
  return ResolvingParser('tests/specs/petstore.yaml')


@pytest.fixture
def with_externals_parser():
  return ResolvingParser('tests/specs/with_externals.yaml')


@pytest.fixture
def petstore_parser_from_string():
  yaml = None
  with open('tests/specs/petstore.yaml', 'rb') as f:
    x = f.read()
    yaml = x.decode('utf8')
  return ResolvingParser(spec_string = yaml)


@pytest.fixture
def issue_1_parser():
  return ResolvingParser('tests/specs/issue_1.json')


@pytest.mark.skipif(none_of('openapi_spec_validator', 'swagger_spec_validator', 'flex'), reason='Missing backends')
def test_basics(petstore_parser):
  assert petstore_parser.specification, 'No specs loaded!'


@pytest.mark.skipif(none_of('openapi_spec_validator', 'swagger_spec_validator', 'flex'), reason='Missing backends')
def test_petstore_resolve(petstore_parser):
  assert petstore_parser.specification, 'No specs loaded!'

  # The petstore references /definitions/Pet in /definitions/Pets, and uses
  # /definitions/Pets in the 200 response to the /pets path. So let's check
  # whether we can find something of /definitions/Pet there...
  res = petstore_parser.specification['paths']['/pets']['get']['responses']
  assert res['200']['schema']['type'] == 'array', 'Did not resolve right!'


@pytest.mark.skipif(none_of('openapi_spec_validator', 'swagger_spec_validator', 'flex'), reason='Missing backends')
def test_with_externals_resolve(with_externals_parser):
  assert with_externals_parser.specification, 'No specs loaded!'

  # The specs are a simplified version of the petstore example, with some
  # external references.
  # - Test that the list pets call returns the right thing from the external
  #   definitions.yaml
  res = with_externals_parser.specification['paths']['/pets']['get']
  res = res['responses']
  assert res['200']['schema']['type'] == 'array'

  # - Test that the get single pet call returns the right thing from the
  #   remote petstore definition
  res = with_externals_parser.specification['paths']['/pets/{petId}']['get']
  res = res['responses']
  assert 'id' in res['200']['schema']['required']

  # - Test that error responses contain a message from error.json
  res = with_externals_parser.specification['paths']['/pets']['get']
  res = res['responses']
  assert 'message' in res['default']['schema']['required']


@pytest.mark.skipif(none_of('openapi_spec_validator', 'swagger_spec_validator', 'flex'), reason='Missing backends')
def test_relative_urls_from_string(petstore_parser_from_string):
  # This must succeed
  assert petstore_parser_from_string.yaml(), 'Did not get YAML representation of specs!'


@pytest.mark.skipif(none_of('openapi_spec_validator', 'swagger_spec_validator', 'flex'), reason='Missing backends')
def test_issue_1_relative_path_references(issue_1_parser):
  # Must resolve references correctly
  params = issue_1_parser.specification["paths"]["/test"]["parameters"]
  assert 'id' in params[0]['schema']['required']


@pytest.mark.skipif(none_of('openapi_spec_validator'), reason='Missing backends')
def test_issue_39_sequence_indices():
  # Must not fail to parse
  parser = ResolvingParser('tests/specs/issue_39.yaml', backend = 'openapi-spec-validator')
  print(parser.specification)

  # The /useCase path should have two values in its response example.
  example = parser.specification['paths']['/useCase']['get']['responses']['200']['content']['application/json']['examples']['response']
  assert 'value' in example
  assert len(example['value']) == 2

  # However, the /test path should have only one of the strings.
  example = parser.specification['paths']['/test']['get']['responses']['200']['content']['application/json']['example']
  assert example == 'some really long or specific string'
