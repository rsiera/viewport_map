(function ($) {
    function LocationTable(elem) {
        this.elem = $(elem);
    }

    LocationTable.prototype.clearTable = function () {
        this.elem.find('tbody').empty();
        this.elem.find('tbody').append('<tr><\/tr>');
    };

    LocationTable.prototype.appendToList = function (point) {
        this.elem.find('tbody').find('tr:last').after(
            '<tr><td>' + point.address + '<\/td>' +
            '<td>' + point.longitude + ',' + point.latitude + '<\/td></tr>'
        );
    };

    LocationTable.prototype.refreshList = function (location_points) {
        if (location_points === undefined) {
            return;
        }
        for (var i = 0; i < location_points.length; i++) {
            this.appendToList(location_points[i]);
        }
    };

    function Map(elem, locationTable, client) {
        this.elem = $(elem);
        this.locationTable = locationTable;
        this.geocoder = new google.maps.Geocoder;
        this.infowindow = new google.maps.InfoWindow;
        this.client = client;
    }

    Map.prototype.init = function () {
        this.map = new google.maps.Map(this.elem[0], {center: {lat: 53, lng: 18}, zoom: 8});
        this.refreshMap();
        this.client.getLocations(this.locationTable);
        var that = this;
        this.map.addListener("click", function (point) {
            that.geocodeLatLng(point);
        });
    };

    Map.prototype.refreshMap = function () {
        var layer = new google.maps.FusionTablesLayer({
            query: {
                select: '*',
                from: '15jQJZ3ZC7LtI9ZtU2r1epPObVyyMnhYngemTG3if'
            }
        });
        layer.setMap(this.map);
    };

    Map.prototype.markLocation = function (results) {
        var marker = new google.maps.Marker({position: results[0].geometry.location, map: this.map});
        this.infowindow.setContent(results[0].formatted_address);
        this.infowindow.open(this.map, marker);
    };

    Map.prototype.geocodeLatLng = function (point) {
        var that = this;
        this.geocoder.geocode({'location': point.latLng}, function (results, status) {
            if (status === google.maps.GeocoderStatus.OK) {
                if (results[0]) {
                    if (results[0].geometry.location_type === "ROOFTOP") {
                        that.client.addLocation(results, that.locationTable);
                        that.markLocation(results);
                        that.refreshMap();
                    }
                    else {
                        window.alert('No real address');
                    }
                } else {
                    window.alert('No results found');
                }
            } else {
                window.alert('Geocoder failed due to: ' + status);
            }
        });
    };

    function Client() {
        this.url = 'api/v1/locations/';
    }

    Client.prototype.addLocation = function (results, locationTable) {
        $.ajax({
            url: this.url,
            type: "post",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({
                "address": results[0].formatted_address,
                "longitude": results[0].geometry.location.lng(),
                "latitude": results[0].geometry.location.lat()
            }),
            success: function (point) {
                locationTable.appendToList(point);
            },

            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    };

    Client.prototype.getLocations = function (locationTable) {
        $.ajax({
            url: this.url,
            type: "GET",
            success: function (points) {
                locationTable.refreshList(points);
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    };

    Client.prototype.bulkDeleteLocations = function (locationTable, map) {
        $.ajax({
            url: this.url,
            type: "DELETE",
            success: function (json) {
                if (json.success === true) {
                    locationTable.clearTable();
                    map.refreshMap();
                }
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    };

    var main = function () {
        var client = new Client();
        var locationTable = new LocationTable('#maptable');
        var map = new Map('#map', locationTable, client);
        map.init();
        $("#delete_data").click(function () {
            client.bulkDeleteLocations(locationTable, map);
        });
    };

    main();
})(jQuery);
