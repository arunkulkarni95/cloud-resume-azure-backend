from unittest.mock import Mock
from function_app import get_visitor_count, update_visitor_count

def test_get_visitor_count():
    mock_table_client = Mock()
    mock_table_client.get_entity.return_value = {'count': 6}
    count = get_visitor_count(mock_table_client)
    assert count == 7

def test_update_visitor_count():
    mock_table_client = Mock()
    update_visitor_count(mock_table_client, 10)

    # Check that upsert_entity is called once with the correct parameters
    mock_table_client.upsert_entity.assert_called_once_with({'PartitionKey': 'visitorCounter', 'RowKey': '0', 'count': 10})

    # Verify that the call was actually made
    assert mock_table_client.upsert_entity.called
