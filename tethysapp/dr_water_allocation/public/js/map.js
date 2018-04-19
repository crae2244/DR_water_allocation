function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(function() {

    // Create new Overlay with the #popup element
    var popup = new ol.Overlay({
        element: document.getElementById('popup')
    });


    var map = TETHYS_MAP_VIEW.getMap();
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
            if (selected_feature.get('type') == "dam")
                var popup_content = '<div class="diversion-popup">' +
                                        '<p><b name="name">'+ selected_feature.get('point_name') + '</b></p>' +
                                        '<table class="table  table-condensed">' +
                                            '<tr>' +
                                                '<th>Output</th>' +
                                                '<td><input type="text" name="output" value="'+ selected_feature.get('output') +'"></td>' +
                                            '</tr>' +
                                        '</table>' +
                                        '<div id="wrapper">' +
                                            '<button type="button" class="update-button" ' +
                                            'onclick="update_persistent_store_dam()">Update</button>'+
                                        '</div>'+
                                    '</div>';

            else
                var popup_content = '<div class="diversion-popup">' +
                                        '<p><b name="name">'+ selected_feature.get('point_name') + '</b></p>' +
                                        '<table class="table  table-condensed">' +
                                            '<tr>' +
                                                '<th>Demand</th>' +
                                                '<td><input type="text" name="demand" value="'+ selected_feature.get('demand') +'"></td>' +
                                            '</tr>' +
                                            '<tr>' +
                                                '<th>Priority</th>' +
                                                '<td><select class="priority-select" name="priority" ' +
                                                        'selected="'+ selected_feature.get('priority') +'">  ' +
                                                    '<option value=1>High</option>' +
                                                    '<option value=2>Medium</option>' +
                                                    '<option value=3>Low</option>' +
                                                '</select></td>' +
                                            '</tr>' +
                                            '<tr>' +
                                                '<th>Efficiency</th>' +
                                                '<td><input type="text" name="efficiency" value="'+ selected_feature.get('efficiency') +'"></td>' +
                                            '</tr>' +
                                        '</table>' +
                                        '<div id="wrapper">' +
                                            '<button type="button" class="update-button" ' +
                                            'onclick="update_persistent_store_point()">Update</button>'+
                                        '</div>'+
                                    '</div>';


            // Clean up last popup and reinitialize
            $(popup_element).popover('destroy');

            $(".update-button").click(function(){
                alert("HAndler called");
            });

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

function update_persistent_store_point(){

    //I need to make sure that there are values in these things
    var place_name_new = $('[name="name"]').text();
    var demand_new = $('[name="demand"]').val();
    var priority_new = $('[name="priority"]').val();
    var efficiency_new = $('[name="efficiency"]').val();

    var csrftoken = getCookie('csrftoken');
    $.ajax({
        type:'POST',
        url:'update-persistent-store-point/',
        data: {
            'place_name':place_name_new,
            'demand':demand_new,
            'priority':priority_new,
            'efficiency':efficiency_new,
        },
        headers:{'X-CSRFToken':csrftoken},
        success: function (data) {
            if (!data.error) {
                console.log("this worked")
            }
        },
    })
};

function update_persistent_store_dam(){

    var place_name_new = $('[name="name"]').text();
    var output_new = $('[name="output"]').val();

    var csrftoken = getCookie('csrftoken');
    $.ajax({
        type:'POST',
        url:'update-persistent-store-dam/',
        data: {
            'place_name':place_name_new,
            'output':output_new
        },
        headers:{'X-CSRFToken':csrftoken},
        success: function (data) {
            if (!data.error) {
                console.log("this worked")
            }
        },
    })
};