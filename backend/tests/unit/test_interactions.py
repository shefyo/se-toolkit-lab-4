"""Unit tests for interaction filtering logic."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_all_when_item_id_is_none() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, None)
    assert result == interactions


def test_filter_returns_empty_for_empty_input() -> None:
    result = _filter_by_item_id([], 1)
    assert result == []


def test_filter_returns_interaction_with_matching_ids() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1

def test_filter_excludes_interaction_with_different_learner_id() -> None:
    interactions = [_make_log(1, 2, 1)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1

    def test_filter_returns_only_matching_item_id_when_multiple_present() -> None:
    """KEEP: filters out non-matching item_id when list contains mixed values."""
    interactions = [
        _make_log(1, 1, 1),
        _make_log(2, 1, 2),
        _make_log(3, 2, 1),
        _make_log(4, 3, 3),
        _make_log(5, 4, 1),
    ]
    result = _filter_by_item_id(interactions, 1)
    assert [i.id for i in result] == [1, 3, 5]


def test_filter_preserves_input_order_for_matching_results() -> None:
    """KEEP: stable ordering is useful for predictable API responses/tests."""
    interactions = [
        _make_log(10, 7, 1),
        _make_log(11, 8, 2),
        _make_log(12, 9, 1),
        _make_log(13, 10, 1),
    ]
    result = _filter_by_item_id(interactions, 1)
    assert [i.id for i in result] == [10, 12, 13]


def test_filter_returns_empty_when_item_id_not_present() -> None:
    """KEEP: boundary case where filter value doesn't exist in dataset."""
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 999)
    assert result == []