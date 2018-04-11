$(function() {
    //var legend="/static/map_plot/images/Legends/zInvis.png";
    //var input = document.getElementById('legend');
    //input.src = legend;
    // Create new Overlay with the #popup element
    var popup = new ol.Overlay({
        element: document.getElementById('popup')
    });

    //function my_callback(points_layer, lines_layer, polygons_layer) {
       //console.log(points_layer);
       //var source=points_layer.getSource();
       //var features=source.getFeatures();
       //console.log(features);

    var map = TETHYS_MAP_VIEW.getMap();
    console.log("hello");
    var select_interaction = TETHYS_MAP_VIEW.getSelectInteraction();
    map.addOverlay(popup);

    select_interaction.getFeatures().on('change:length', function(e)
    {
        var popup_element = popup.getElement();

        if (e.target.getArray().length > 0)
        {
            // this means there is at least 1 feature selected
            var selected_feature = e.target.item(0); // 1st feature in Collection
            // Get coordinates of the point to set position of the popup
            var coordinates = selected_feature.getGeometry().getCoordinates();
            var comID=selected_feature.get('feature_id')
            var popup_content = '<div class="diversion-popup">' +
                                    '<p><b>'+ selected_feature.get('point_name') + '</b></p>' +
                                    '<table class="table  table-condensed">' +
                                        '<tr>' +
                                            '<th>Demand</th>' +
                                            '<td><input type="text" name="demand"></td>' +
                                        '</tr>' +
                                        '<tr>' +
                                            '<th>Piority</th>' +
                                            '<td><input type="text" name="priority"></td>' +
                                        '</tr>' +
                                        '<tr>' +
                                            '<th>Efficiency</th>' +
                                            '<td><input type="text" name="efficeincy"></td>' +
                                        '</tr>' +
                                    '</table>' +
                                '</div>';

            // Clean up last popup and reinitialize
            $(popup_element).popover('destroy');

            // Delay arbitrarily to wait for previous popover to
            // be deleted before showing new popover.
            setTimeout(function() {
                popup.setPosition(coordinates);

                $(popup_element).popover({
                  'placement': 'top',
                  'animation': true,
                  'html': true,
                  'content': popup_content
                });

                $(popup_element).popover('show');
            }, 500);
        } else {
            // remove pop up when selecting nothing on the map
            $(popup_element).popover('destroy');
        }
    });
});