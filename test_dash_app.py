import pytest
from dash.testing.application_runners import import_app


def test_header_present(dash_duo):
    app = import_app("dash_app")
    dash_duo.start_server(app)
    
    dash_duo.wait_for_element("h1", timeout=10)
    
    header = dash_duo.find_element("h1")
    assert header.text == "Pink Morsel Sales Dashboard", "Header text does not match expected value"
    
    print("✓ Header test passed: 'Pink Morsel Sales Dashboard' is present")


def test_visualization_present(dash_duo):
    app = import_app("dash_app")
    dash_duo.start_server(app)
    
    dash_duo.wait_for_element("#sales-chart", timeout=10)
    
    graph = dash_duo.find_element("#sales-chart")
    assert graph is not None, "Sales chart visualization is not present"
    
    assert "plotly" in graph.get_attribute("class").lower() or \
           dash_duo.find_element(".js-plotly-plot") is not None, \
           "Element is not a Plotly graph"
    
    print("✓ Visualization test passed: Sales chart is present")


def test_region_picker_present(dash_duo):
    app = import_app("dash_app")
    dash_duo.start_server(app)
    
    dash_duo.wait_for_element("#region-filter", timeout=10)
    
    region_filter = dash_duo.find_element("#region-filter")
    assert region_filter is not None, "Region picker is not present"
    
    radio_inputs = dash_duo.find_elements("input[type='radio']")
    assert len(radio_inputs) == 5, f"Expected 5 radio buttons, found {len(radio_inputs)}"
    
    region_filter_text = region_filter.text
    expected_regions = ['All Regions', 'North', 'East', 'South', 'West']
    
    for expected_region in expected_regions:
        assert expected_region in region_filter_text, f"Radio button label for '{expected_region}' is missing"
    
    print("✓ Region picker test passed: All 5 radio buttons are present")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
