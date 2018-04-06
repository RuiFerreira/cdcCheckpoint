<template>
  <div>
    <div id='map'></div>
  </div>
</template>
<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js'></script>
<script>
import mapboxgl from 'mapbox-gl'
import axios from 'axios'
require('../../node_modules/mapbox-gl/dist/mapbox-gl.css')
var $ = require('jQuery')
var geojsonPOIs = {
  type: 'FeatureCollection',
  features: []
}
export default {
  data () {
    return {
      map: null,
      pois: [],
      geoJSONPOIs: geojsonPOIs,
      apiKey: 'pk.eyJ1IjoiaWNsaW8iLCJhIjoiY2l2bnByem9pMDAwajJucDh5MWFiOTUwdCJ9.RNHNU1MujwhDoHknx31_OQ'
    }
  },
  created () {
    this.getPOIs()
  },
  methods: {
    getPOIs () {
      this.pois = this.getPOIsFromBackend()
    },
    getPOIsFromBackend () {
      const path = `http://localhost:5000/pois`
      axios.get(path)
        .then(response => {
          this.pois = response.data // nao guarda resposta
          this.createMap()
        })
        .catch(error => {
          console.log(error)
        })
    },
    createMap () {
      mapboxgl.accessToken = this.apiKey
      // init the map
      this.map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/iclio/cjf8bwvxt4wlg2rqp3a9e9xid',
        center: [-8.422, 40.223], // coimbra
        zoom: 8
      })
      this.map.on('load', this.updateMap.bind(this))
      },
    updateMap () {
      for (var i = 0; i < this.pois.length; i++) {
        this.geoJSONPOIs.features.push({
          type: 'Feature',
          geometry: {
            type: 'Point',
            coordinates: [this.pois[i].geoLong, this.pois[i].geoLat]
          },
          properties: {
            description: this.pois[i].POIName // need to add prediction to choose color of icon from the historical records max value of timestamp
          }
        })
      }
      var _this = this
      this.geoJSONPOIs.features.forEach(function (orangemarker) {
        var el = document.createElement('div')
        el.className = 'orangemarker'
        // need to make an if statement to choose color of icon for each point of interest based on the property set before
        new mapboxgl.Marker(el)
          .setLngLat(orangemarker.geometry.coordinates)
          .setPopup(new mapboxgl.Popup({ offset: 25 }) // add popups
          .setHTML('<h4>' + orangemarker.properties.description + '</h4>'))
          .addTo(_this.map)
      })
      var start = [this.pois[3].geoLong , this.pois[3].geoLat]
      var end = [this.pois[4].geoLong , this.pois[4].geoLat]
      var directionsRequest = 'https://api.mapbox.com/directions/v5/mapbox/walking/' + start[0] + ',' + start[1] + ';' + end[0] + ',' + end[1] + '?geometries=geojson&access_token=' + mapboxgl.accessToken;
      $.ajax({
        method: 'GET',
        url: directionsRequest,
      }).done(function(data) {
        var route = data.routes[0].geometry
        _this.map.addLayer({
          id: 'route',
          type: 'line',
          source: {
            type: 'geojson',
            data: {
              type: 'Feature',
              geometry: route
            }
          },
          paint: {
            'line-width': 2
          }
        })
        _this.map.addLayer({
          id: 'start',
          type: 'circle',
          source: {
            type: 'geojson',
            data: {
              type: 'Feature',
              geometry: {
                type: 'Point',
                coordinates: start
              }
            }
          }
        })
        _this.map.addLayer({
          id: 'end',
          type: 'circle',
          source: {
            type: 'geojson',
            data: {
              type: 'Feature',
              geometry: {
                type: 'Point',
                coordinates: end
              }
            }
          }
        })
      })
    }
  }
}
</script>

<style>
#map {
  display: flex;
  width: 100%;
  height: 600px;
}
.orangemarker {
  background-image: url('../assets/orangepin.png');
  background-size: cover;
  width: 25px;
  height: 25px;
  border-radius: 50%;
  cursor: pointer;
}
.mapboxgl-popup {
  max-width: 200px;
}
.mapboxgl-popup-content {
  text-align: center;
  font-family: 'Open Sans', sans-serif
}
</style>
