# -*- coding: utf-8 -*-

from collections import OrderedDict
from unittest import TestCase
from unittest.mock import MagicMock, call, patch

import pytest

from mlblocks.mlblock import MLBlock
from mlblocks.mlpipeline import MLPipeline


def get_mlblock_mock(*args, **kwargs):
    return MagicMock(autospec=MLBlock)


class TestMLPipline(TestCase):

    @patch('mlblocks.mlpipeline.LOGGER')
    @patch('mlblocks.mlpipeline.MLBlock')
    def test___init__(self, mlblock_mock, logger_mock):
        blocks = [
            get_mlblock_mock(),
            get_mlblock_mock(),
            get_mlblock_mock(),
            get_mlblock_mock()
        ]
        last_block = blocks[-1]
        last_block.produce_output = [
            {
                'name': 'y',
                'type': 'array'
            }
        ]
        mlblock_mock.side_effect = blocks

        primitives = [
            'a.primitive.Name',
            'a.primitive.Name',
            'another.primitive.Name',
            'another.primitive.Name',
        ]
        expected_primitives = primitives.copy()

        init_params = {
            'a.primitive.Name': {
                'an_argument': 'value',
            },
            'another.primitive.Name#2': {
                'another': 'argument_value',
            }
        }
        expected_init_params = init_params.copy()
        input_names = {
            'another.primitive.Name#1': {
                'a_name': 'another_name',
            }
        }
        expected_input_names = input_names.copy()

        mlpipeline = MLPipeline(
            primitives=primitives,
            init_params=init_params,
            input_names=input_names
        )

        assert mlpipeline.primitives == expected_primitives
        assert mlpipeline.init_params == expected_init_params
        assert mlpipeline.blocks == OrderedDict((
            ('a.primitive.Name#1', blocks[0]),
            ('a.primitive.Name#2', blocks[1]),
            ('another.primitive.Name#1', blocks[2]),
            ('another.primitive.Name#2', blocks[3])
        ))
        assert mlpipeline.input_names == expected_input_names
        assert mlpipeline.output_names == dict()
        assert mlpipeline._tunable_hyperparameters == {
            'a.primitive.Name#1': blocks[0].get_tunable_hyperparameters.return_value,
            'a.primitive.Name#2': blocks[1].get_tunable_hyperparameters.return_value,
            'another.primitive.Name#1': blocks[2].get_tunable_hyperparameters.return_value,
            'another.primitive.Name#2': blocks[3].get_tunable_hyperparameters.return_value
        }
        assert mlpipeline.outputs == {
            'default': [
                {
                    'name': 'y',
                    'type': 'array',
                    'variable': 'another.primitive.Name#2.y'
                }
            ]
        }
        assert mlpipeline.verbose

        expected_calls = [
            call('a.primitive.Name', an_argument='value'),
            call('a.primitive.Name', an_argument='value'),
            call('another.primitive.Name'),
            call('another.primitive.Name', another='argument_value'),
        ]
        assert mlblock_mock.call_args_list == expected_calls

        logger_mock.warning.assert_called_once_with(
            'Non-numbered init_params are being used for more than one block %s.',
            'a.primitive.Name'
        )

    @patch('mlblocks.mlpipeline.MLBlock', new=get_mlblock_mock)
    def test_get_tunable_hyperparameters(self):
        mlpipeline = MLPipeline(['a_primitive'])
        tunable = dict()
        mlpipeline._tunable_hyperparameters = tunable

        returned = mlpipeline.get_tunable_hyperparameters()

        assert returned == tunable
        assert returned is not tunable

    @patch('mlblocks.mlpipeline.MLBlock', new=get_mlblock_mock)
    def test_get_tunable_hyperparameters_flat(self):
        mlpipeline = MLPipeline(['a_primitive'])
        mlpipeline._tunable_hyperparameters = {
            'block_1': {
                'hp_1': {
                    'type': 'int',
                    'range': [
                        1,
                        10
                    ],
                }
            },
            'block_2': {
                'hp_1': {
                    'type': 'str',
                    'default': 'a',
                    'values': [
                        'a',
                        'b',
                        'c'
                    ],
                },
                'hp_2': {
                    'type': 'bool',
                    'default': True,
                }
            }
        }

        returned = mlpipeline.get_tunable_hyperparameters(flat=True)

        expected = {
            ('block_1', 'hp_1'): {
                'type': 'int',
                'range': [
                    1,
                    10
                ],
            },
            ('block_2', 'hp_1'): {
                'type': 'str',
                'default': 'a',
                'values': [
                    'a',
                    'b',
                    'c'
                ],
            },
            ('block_2', 'hp_2'): {
                'type': 'bool',
                'default': True,
            }
        }
        assert returned == expected

    @patch('mlblocks.mlpipeline.MLBlock', new=get_mlblock_mock)
    def test_get_hyperparameters(self):
        block_1 = get_mlblock_mock()
        block_1.get_hyperparameters.return_value = {
            'a': 'a'
        }
        block_2 = get_mlblock_mock()
        block_2.get_hyperparameters.return_value = {
            'b': 'b',
            'c': 'c',
        }
        blocks = OrderedDict((
            ('a.primitive.Name#1', block_1),
            ('a.primitive.Name#2', block_2),
        ))
        mlpipeline = MLPipeline(['a_primitive'])
        mlpipeline.blocks = blocks

        hyperparameters = mlpipeline.get_hyperparameters()

        assert hyperparameters == {
            'a.primitive.Name#1': {
                'a': 'a',
            },
            'a.primitive.Name#2': {
                'b': 'b',
                'c': 'c',
            },
        }
        block_1.get_hyperparameters.assert_called_once_with()
        block_2.get_hyperparameters.assert_called_once_with()

    @patch('mlblocks.mlpipeline.MLBlock', new=get_mlblock_mock)
    def test_get_hyperparameters_flat(self):
        block_1 = get_mlblock_mock()
        block_1.get_hyperparameters.return_value = {
            'a': 'a'
        }
        block_2 = get_mlblock_mock()
        block_2.get_hyperparameters.return_value = {
            'b': 'b',
            'c': 'c',
        }
        blocks = OrderedDict((
            ('a.primitive.Name#1', block_1),
            ('a.primitive.Name#2', block_2),
        ))
        mlpipeline = MLPipeline(['a_primitive'])
        mlpipeline.blocks = blocks

        hyperparameters = mlpipeline.get_hyperparameters(flat=True)

        assert hyperparameters == {
            ('a.primitive.Name#1', 'a'): 'a',
            ('a.primitive.Name#2', 'b'): 'b',
            ('a.primitive.Name#2', 'c'): 'c',
        }
        block_1.get_hyperparameters.assert_called_once_with()
        block_2.get_hyperparameters.assert_called_once_with()

    @patch('mlblocks.mlpipeline.MLBlock', new=get_mlblock_mock)
    def test_set_hyperparameters(self):
        block_1 = get_mlblock_mock()
        block_2 = get_mlblock_mock()
        blocks = OrderedDict((
            ('a.primitive.Name#1', block_1),
            ('a.primitive.Name#2', block_2),
        ))
        mlpipeline = MLPipeline(['a_primitive'])
        mlpipeline.blocks = blocks

        hyperparameters = {
            'a.primitive.Name#2': {
                'some': 'arg'
            }
        }
        mlpipeline.set_hyperparameters(hyperparameters)

        block_1.set_hyperparameters.assert_not_called()
        block_2.set_hyperparameters.assert_called_once_with({'some': 'arg'})

    @patch('mlblocks.mlpipeline.MLBlock', new=get_mlblock_mock)
    def test_set_hyperparameters_flat(self):
        block_1 = get_mlblock_mock()
        block_2 = get_mlblock_mock()
        blocks = OrderedDict((
            ('a.primitive.Name#1', block_1),
            ('a.primitive.Name#2', block_2),
        ))
        mlpipeline = MLPipeline(['a_primitive'])
        mlpipeline.blocks = blocks

        hyperparameters = {
            ('a.primitive.Name#2', 'some'): 'arg'
        }
        mlpipeline.set_hyperparameters(hyperparameters)

        block_1.set_hyperparameters.assert_not_called()
        block_2.set_hyperparameters.assert_called_once_with({'some': 'arg'})

    @patch('mlblocks.mlpipeline.MLBlock', new=get_mlblock_mock)
    def test__get_block_args(self):
        input_names = {
            'a_block': {
                'arg_3': 'arg_3_alt'
            }
        }
        pipeline = MLPipeline(['a_primitive'], input_names=input_names)

        block_args = [
            {
                'name': 'arg_1',
            },
            {
                'name': 'arg_2',
                'default': 'arg_2_value'
            },
            {
                'name': 'arg_3',
            },
            {
                'name': 'arg_4',
                'required': False
            },
        ]
        context = {
            'arg_1': 'arg_1_value',
            'arg_3_alt': 'arg_3_value'
        }

        args = pipeline._get_block_args('a_block', block_args, context)

        expected = {
            'arg_1': 'arg_1_value',
            'arg_3': 'arg_3_value',
        }
        assert args == expected

    @patch('mlblocks.mlpipeline.MLBlock', new=get_mlblock_mock)
    def test__get_outputs_no_outputs(self):
        self_ = MagicMock(autospec=MLPipeline)

        self_._last_block_name = 'last_block'
        self_._get_block_outputs.return_value = ['some', 'outputs']

        pipeline = dict()
        outputs = None
        returned = MLPipeline._get_outputs(self_, pipeline, outputs)

        expected = {
            'default': ['some', 'outputs']
        }
        assert returned == expected

        self_._get_block_outputs.assert_called_once_with('last_block')

    @patch('mlblocks.mlpipeline.MLBlock', new=get_mlblock_mock)
    def test__get_outputs_defaults(self):
        self_ = MagicMock(autospec=MLPipeline)

        pipeline = dict()
        outputs = {
            'default': ['some', 'outputs']
        }
        returned = MLPipeline._get_outputs(self_, pipeline, outputs)

        expected = {
            'default': ['some', 'outputs']
        }
        assert returned == expected
        self_._get_block_outputs.assert_not_called()

    @patch('mlblocks.mlpipeline.MLBlock', new=get_mlblock_mock)
    def test__get_outputs_additional(self):
        self_ = MagicMock(autospec=MLPipeline)

        pipeline = {
            'outputs': {
                'default': ['some', 'outputs'],
                'additional': ['other', 'outputs']
            }
        }
        outputs = None
        returned = MLPipeline._get_outputs(self_, pipeline, outputs)

        expected = {
            'default': ['some', 'outputs'],
            'additional': ['other', 'outputs']
        }
        assert returned == expected
        self_._get_block_outputs.assert_not_called()

    @patch('mlblocks.mlpipeline.MLBlock', new=get_mlblock_mock)
    def test_get_outputs_str_named(self):
        outputs = {
            'default': [
                {
                    'name': 'a_name',
                    'variable': 'a_variable',
                    'type': 'a_type',
                }
            ],
            'debug': [
                {
                    'name': 'another_name',
                    'variable': 'another_variable',
                }
            ]
        }
        pipeline = MLPipeline(['a_primitive', 'another_primitive'], outputs=outputs)
        returned = pipeline.get_outputs('debug')

        expected = [
            {
                'name': 'another_name',
                'variable': 'another_variable',
            }
        ]

        assert returned == expected

    @patch('mlblocks.mlpipeline.MLBlock', new=get_mlblock_mock)
    def test_get_outputs_str_variable(self):
        pipeline = MLPipeline(['a_primitive', 'another_primitive'])

        pipeline.blocks['a_primitive#1'].produce_output = [
            {
                'name': 'output',
                'type': 'whatever'
            }
        ]

        returned = pipeline.get_outputs('a_primitive#1.output')

        expected = [
            {
                'name': 'output',
                'type': 'whatever',
                'variable': 'a_primitive#1.output'
            }
        ]

        assert returned == expected

    @patch('mlblocks.mlpipeline.MLBlock', new=get_mlblock_mock)
    def test_get_outputs_str_block(self):
        pipeline = MLPipeline(['a_primitive', 'another_primitive'])

        returned = pipeline.get_outputs('a_primitive#1')

        expected = [
            {
                'name': 'a_primitive#1',
                'variable': 'a_primitive#1',
            }
        ]

        assert returned == expected

    @patch('mlblocks.mlpipeline.MLBlock', new=get_mlblock_mock)
    def test_get_outputs_int(self):
        pipeline = MLPipeline(['a_primitive', 'another_primitive'])

        returned = pipeline.get_outputs(-1)

        expected = [
            {
                'name': 'another_primitive#1',
                'variable': 'another_primitive#1',
            }
        ]

        assert returned == expected

    @patch('mlblocks.mlpipeline.MLBlock', new=get_mlblock_mock)
    def test_get_outputs_combination(self):
        outputs = {
            'default': [
                {
                    'name': 'a_name',
                    'variable': 'a_variable',
                    'type': 'a_type',
                }
            ],
            'debug': [
                {
                    'name': 'another_name',
                    'variable': 'another_variable',
                }
            ]
        }
        pipeline = MLPipeline(['a_primitive', 'another_primitive'], outputs=outputs)

        pipeline.blocks['a_primitive#1'].produce_output = [
            {
                'name': 'output',
                'type': 'whatever'
            }
        ]
        pipeline.blocks['another_primitive#1'].produce_output = [
            {
                'name': 'something',
            }
        ]

        returned = pipeline.get_outputs(['default', 'debug', -1, 'a_primitive#1.output'])

        expected = [
            {
                'name': 'a_name',
                'variable': 'a_variable',
                'type': 'a_type'
            },
            {
                'name': 'another_name',
                'variable': 'another_variable',
            },
            {
                'name': 'another_primitive#1',
                'variable': 'another_primitive#1',
            },
            {
                'name': 'output',
                'type': 'whatever',
                'variable': 'a_primitive#1.output'
            }
        ]

        assert returned == expected

    @patch('mlblocks.mlpipeline.MLBlock', new=get_mlblock_mock)
    def test_get_outputs_invalid(self):
        pipeline = MLPipeline(['a_primitive'])

        pipeline.blocks['a_primitive#1'].produce_output = [
            {
                'name': 'output',
                'type': 'whatever'
            }
        ]

        with pytest.raises(ValueError):
            pipeline.get_outputs('a_primitive#1.invalid')

    @patch('mlblocks.mlpipeline.MLBlock', new=get_mlblock_mock)
    def test_get_output_names(self):
        outputs = {
            'default': [
                {
                    'name': 'a_name',
                    'variable': 'a_variable',
                    'type': 'a_type',
                }
            ]
        }
        pipeline = MLPipeline(['a_primitive'], outputs=outputs)

        names = pipeline.get_output_names()

        assert names == ['a_name']

    @patch('mlblocks.mlpipeline.MLBlock', new=get_mlblock_mock)
    def test_get_output_variables(self):
        outputs = {
            'default': [
                {
                    'name': 'a_name',
                    'variable': 'a_variable',
                    'type': 'a_type',
                }
            ]
        }
        pipeline = MLPipeline(['a_primitive'], outputs=outputs)

        names = pipeline.get_output_variables()

        assert names == ['a_variable']

    def test_fit(self):
        pass

    def test_predict(self):
        pass

    def test_to_dict(self):
        pass

    def test_save(self):
        pass

    def test_from_dict(self):
        pass

    def test_load(self):
        pass
