<template>
  <div class="melbourne">
    <div id="map" style="height: 100vh; width: 100%" >
    </div>
  </div>
</template>
<script>
  export default {
    mounted(){
      this.initMap()
    },
    data () {
      return {
        showDialog: false
      }
    },
    methods:{
      initMap() {
        // The location of AU
        let au = {lat: -37.8142176, lng: 144.9631608}
        // The map, centered at Uluru
        let map = new google.maps.Map(
          document.getElementById('map'), {zoom: 9, center: au,styles: [
              {elementType: 'geometry', stylers: [{color: '#242f3e'}]},
              {elementType: 'labels.text.stroke', stylers: [{color: '#242f3e'}]},
              {elementType: 'labels.text.fill', stylers: [{color: '#746855'}]},
              {
                featureType: 'administrative.locality',
                elementType: 'labels.text.fill',
                stylers: [{color: '#d59563'}]
              },
              {
                featureType: 'poi',
                elementType: 'labels.text.fill',
                stylers: [{color: '#d59563'}]
              },
              {
                featureType: 'poi.park',
                elementType: 'geometry',
                stylers: [{color: '#263c3f'}]
              },
              {
                featureType: 'poi.park',
                elementType: 'labels.text.fill',
                stylers: [{color: '#6b9a76'}]
              },
              {
                featureType: 'road',
                elementType: 'geometry',
                stylers: [{color: '#38414e'}]
              },
              {
                featureType: 'road',
                elementType: 'geometry.stroke',
                stylers: [{color: '#212a37'}]
              },
              {
                featureType: 'road',
                elementType: 'labels.text.fill',
                stylers: [{color: '#9ca5b3'}]
              },
              {
                featureType: 'road.highway',
                elementType: 'geometry',
                stylers: [{color: '#746855'}]
              },
              {
                featureType: 'road.highway',
                elementType: 'geometry.stroke',
                stylers: [{color: '#1f2835'}]
              },
              {
                featureType: 'road.highway',
                elementType: 'labels.text.fill',
                stylers: [{color: '#f3d19c'}]
              },
              {
                featureType: 'transit',
                elementType: 'geometry',
                stylers: [{color: '#2f3948'}]
              },
              {
                featureType: 'transit.station',
                elementType: 'labels.text.fill',
                stylers: [{color: '#d59563'}]
              },
              {
                featureType: 'water',
                elementType: 'geometry',
                stylers: [{color: '#17263c'}]
              },
              {
                featureType: 'water',
                elementType: 'labels.text.fill',
                stylers: [{color: '#515c6d'}]
              },
              {
                featureType: 'water',
                elementType: 'labels.text.stroke',
                stylers: [{color: '#17263c'}]
              }
            ]})
        map.data.loadGeoJson('mel_geojson.json')

        // mouse click event: show grid info
        map.data.addListener('click', (event) => {
          let cityName = event.feature.getProperty('SA2_NAME16')
          alert(cityName)
        })

        // mouse over event: highlight color
        map.data.addListener('mouseover', (event) => {
          map.data.overrideStyle(event.feature, {fillColor: 'red'})
        })

        // mouse our event: reset color/info-window
        map.data.addListener('mouseout', (event) => {
          map.data.revertStyle()
        })
      }
    }
  }
</script>

<style lang="scss" scoped>
  .melbourne {
    padding: 20px;

    .student-icon {
      font-size: 28px;
    }
  }
</style>
