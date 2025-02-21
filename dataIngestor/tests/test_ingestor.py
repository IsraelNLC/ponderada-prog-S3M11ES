import pytest
from unittest.mock import patch, MagicMock
from src.dataingestor.ingestor import ingest_data

def test_ingest_data():
    mock_supabase = MagicMock()
    with patch("src.dataingestor.ingestor.supabase", mock_supabase):
        with patch("builtins.open", create=True) as mock_open:
            mock_open.return_value.__enter__.return_value = ["col1,col2\n", "val1,val2\n"]
            with patch("csv.DictReader") as mock_csv:
                mock_csv.return_value = [{"col1": "val1", "col2": "val2"}]
                
                ingest_data("fake_path.csv", "fake_table")
                
                mock_supabase.table.assert_called_with("fake_table")
                mock_supabase.table().insert.assert_called()
