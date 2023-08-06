import pandas as pd
import pytest

import azureml.studio.common.error as error_setting
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.datatable.data_table import DataTableColumnSelectionBuilder
from azureml.studio.core.utils.column_selection import ColumnKind
from azureml.studio.modules.text_analytics.feature_hashing.feature_hashing import FeatureHashingModule


@pytest.fixture
def data_table_with_text():
    df = pd.DataFrame()
    df['text'] = [
        '"Ok~ but I think the Keirsey Temperment Test is more accurate - and cheaper.',
        't describe you at all. This messes up the results, and it did not describe me very well.']
    df['text2'] = [
        '"Ok~ but I think the Keirsey Temperment Test is more accurate',
        't describe you at all. This messes up the results, and it did not describe me very well.']

    return DataTable(df)


@pytest.fixture
def data_table_with_numeric():
    df = pd.DataFrame()
    df['text'] = [1, 2, 3]
    df['text2'] = [2, 3, 4]

    return DataTable(df)


@pytest.fixture
def data_table_with_zero_row():
    df = pd.DataFrame()
    df['text'] = []
    df['text2'] = []

    return DataTable(df)


@pytest.fixture
def data_table_with_zero_column():
    # Test the datatable with zero column
    return DataTable(pd.DataFrame())


def test_dataset_with_zero_row(data_table_with_zero_row):
    # Test the datatable with zero row

    csb = DataTableColumnSelectionBuilder()
    column_selection = csb.include_all().build()

    with pytest.raises(error_setting.TooFewRowsInDatasetError,
                       match='Number of rows in input dataset "Dataset" is 0, less than allowed minimum of 1 row'):
        FeatureHashingModule.run(
            dataset=data_table_with_zero_row,
            target_column=column_selection,
            bits=5,
            ngrams=2)


def test_column_type_not_str(data_table_with_numeric):
    # Test the datatable which has several column types

    csb = DataTableColumnSelectionBuilder()
    column_selection = csb.include_all().build()

    with pytest.raises(error_setting.InvalidColumnTypeError,
                       match='Cannot process column "text,text2" of type int64,int64.'):
        FeatureHashingModule.run(
            dataset=data_table_with_numeric,
            target_column=column_selection,
            bits=5,
            ngrams=2)


def test_run(data_table_with_text):
    # Test the correct datatable

    csb = DataTableColumnSelectionBuilder()
    column_selection = csb.include_all().build()

    output_dt, = FeatureHashingModule.run(
        dataset=data_table_with_text,
        target_column=column_selection,
        bits=2,
        ngrams=2)

    actual_column_names = ['text', 'text2', 'text_HashingFeature.0', 'text_HashingFeature.1', 'text_HashingFeature.2',
                           'text_HashingFeature.3', 'text2_HashingFeature.0', 'text2_HashingFeature.1',
                           'text2_HashingFeature.2', 'text2_HashingFeature.3']
    expected_column_names = output_dt.data_frame.columns.values.tolist()

    assert actual_column_names == expected_column_names


def test_exceeded_hashed_feature_column_size_generated(data_table_with_text):
    # Test the datatable with exceeded hashed feature column size generated

    csb = DataTableColumnSelectionBuilder()
    column_selection = csb.include_all().build()

    with pytest.raises(error_setting.ExceedsColumnLimitError,
                       match="Number of columns in the dataset in 'Dataset' exceeds allowed '100000'"):
        FeatureHashingModule.run(
            dataset=data_table_with_text,
            target_column=column_selection,
            bits=30,
            ngrams=2)


def test_dataset_with_zero_column(data_table_with_zero_column):
    # Test the dataset with zero column
    csb = DataTableColumnSelectionBuilder()
    column_selection = csb.include_all().build()

    with pytest.raises(error_setting.TooFewColumnsInDatasetError,
                       match='Number of columns in input dataset "Dataset" is less than allowed minimum of 1 column'):
        FeatureHashingModule.run(
            dataset=data_table_with_zero_column,
            target_column=column_selection,
            bits=2,
            ngrams=2)


def test_no_hit_column_type(data_table_with_text):
    # Test the dataset with no column which the column type is selected by user
    csb = DataTableColumnSelectionBuilder()
    column_selection = csb.include_col_kinds(ColumnKind.LABEL).build()

    with pytest.raises(error_setting.TooFewColumnsInDatasetError,
                       match='Number of columns in input dataset "Dataset" is less than allowed minimum of 1 column'):
        FeatureHashingModule.run(
            dataset=data_table_with_text,
            target_column=column_selection,
            bits=2,
            ngrams=2)
