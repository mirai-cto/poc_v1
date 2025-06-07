from neurmill_poc_py.tool_recommender import ToolRecommender

def test_get_operation_speed_multiplier():
    recommender = ToolRecommender(db=None)  # db is not used in this method
    
    # Test roughing
    result_roughing = recommender._get_operation_speed_multiplier("roughing")
    assert result_roughing == 0.8

    # Test finishing
    result_finishing = recommender._get_operation_speed_multiplier("finishing")
    assert result_finishing == 1.2

    # Test semi-finishing
    result_semi = recommender._get_operation_speed_multiplier("semi-finishing")
    assert result_semi == 1.0

    # Test unknown (should fall back to default 1.0)
    result_unknown = recommender._get_operation_speed_multiplier("unknown-op")
    assert result_unknown == 1.0
