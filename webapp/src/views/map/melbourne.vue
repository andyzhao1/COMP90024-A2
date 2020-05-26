<template>
  <div class="melbourne">
    <div id="map" style="height: 100vh; width: 80%; display: inline-block">
    </div>
    <div style="height: 100vh; width: 20%; display: inline-block" >
      <el-table
        empty-text="Empty"
        ref="multipleTable"
        :data="tableData"
        style="height: 100vh; width: 100%"
        :border=true
        @cell-click="handleMouseClick"
        @cell-mouse-enter="handleMouseEnter"
        @cell-mouse-leave="handleMouseLeave">
        <el-table-column label="rank" type="index" :index="indexMethod" width="55" align="center"></el-table-column>
        <el-table-column label="Zone" prop="cityName" align="center"></el-table-column>
        <el-table-column label="count" prop="negative" align="center"></el-table-column>
        <el-table-column label="rate" prop="rate" align="center"></el-table-column>
      </el-table>
    </div>
  </div>
</template>
<script>
  import popWindowComponent from '../../components/popWindow'
  import Vue from 'vue'
  import { unemploymentRate, jobRelatedTweetsDistribution } from 'api/scenarioAPI'
  export default {
    mounted(){
      this.initMap()
      this.getPageData()
    },
    data () {
      return {
        showDialog: false,
        s4Data: null,
        tableData: null,
        map: null,
        infowindow: null,
        clickSection: false,
        rank: null,
        cityNameMessage: null
      }
    },
    methods: {
      async colorMap () {
        let colors = this.gradient('#ffffff', '#ff9900', 7)
        this.rank.forEach(each => {
          if (each['negative'] > 100) {
            each['color'] = colors[6]
          } else if (each['negative'] > 60) {
            each['color'] = colors[5]
          } else if (each['negative'] > 30) {
            each['color'] = colors[4]
          } else if (each['negative'] > 20) {
            each['color'] = colors[3]
          } else if (each['negative'] > 10) {
            each['color'] = colors[2]
          } else if (each['negative'] > 0) {
            each['color'] = colors[1]
          } else if (each['negative'] === 0) {
            each['color'] = colors[0]
          }
        })
        this.map.data.setStyle((feature) => {
          let cityId = feature.getProperty('SA2_MAIN16')
          let color = '#000000'
          this.rank.forEach(each => {
            if (each['cityId'] === cityId) {
              color = each['color']
            }
          })
          return {
            fillColor: color,
            fillOpacity: 0.5,
            strokeWeight: 2
          }
        })
      },
      gradient (startColor, endColor, step) {
        let sColor = this.hexToRgb(startColor)
        let eColor = this.hexToRgb(endColor)

        let rStep = (eColor[0] - sColor[0]) / step
        let gStep = (eColor[1] - sColor[1]) / step
        let bStep = (eColor[2] - sColor[2]) / step

        let gradientColorArr = []
        for (var i = 0; i < step; i++) {
          gradientColorArr.push(this.rgbToHex(parseInt(rStep * i + sColor[0]), parseInt(gStep * i + sColor[1]), parseInt(bStep * i + sColor[2])))
        }
        return gradientColorArr
      },
      getRandomColor () {
        const letters = '0123456789ABCDEF'
        let color = '#'
        for (let i = 0; i < 6; i++) {
          color += letters[Math.floor(Math.random() * 16)]
        }
        return color
      },
      rgbToHex (r, g, b) {
        var hex = ((r << 16) | (g << 8) | b).toString(16)
        return '#' + new Array(Math.abs(hex.length - 7)).join('0') + hex
      },

      hexToRgb (hex) {
        var rgb = []
        for (var i = 1; i < 7; i += 2) {
          rgb.push(parseInt('0x' + hex.slice(i, i + 2)))
        }
        return rgb
      },
      handleMouseClick: async function (row, column, cell, event) {
        let PopWindow = Vue.extend(popWindowComponent)
        let cityName = row['cityName']
        const res = await unemploymentRate({ sa2_main11: row['cityId'] })
        let unemployment_chart = null
        if (res.isSuccess === true && res.data != null) {
          let x = []
          let y = []
          res.data.forEach(item => {
            x.push(item['year'] + '-' + item['month'])
            y.push(item['value'])
          })
          unemployment_chart = {
            title: {
              text: 'Unemployment Rate',
              x: 'center',
              y: 'top',
              textAlign: 'left'
            },
            tooltip: {
              trigger: 'axis',
              axisPointer: {
                type: 'shadow'
              }
            },
            xAxis: {
              type: 'category',
              boundaryGap: false,
              data: x
            },
            yAxis: {
              name: '%',
              type: 'value'
            },
            series: [{
              data: y,
              type: 'line',
              areaStyle: {}
            }]
          }
        } else {
          this.$message('failed')
        }
        // send data to the view
        let object = new PopWindow({
          propsData: {
            cityName,
            unemployment_chart
          }
        })

        object.$mount()

        let position = null
        this.map.data.forEach(item => {
          if (item.j['SA2_MAIN16'] === row.cityId) {
            position = item.i.i[0].i[0].i[0]
            this.map.data.overrideStyle(item, {fillColor: 'red'})
          }
        })
        this.infowindow.setContent(object.$el)
        this.infowindow.setPosition(position)
        this.infowindow.open(this.map)
      },
      handleMouseEnter: async function (row, column, cell, event) {
        this.map.data.forEach(item => {
          if (item.j['SA2_MAIN16'] === row.cityId) {
            this.map.data.overrideStyle(item, {fillColor: 'red'})
          }
        })
      },
      handleMouseLeave: function (row, column, cell, event) {
        this.map.data.revertStyle()
        //this.infowindow.close()
      },
      async getPageData () {
        const res = await jobRelatedTweetsDistribution()
        if (res.isSuccess) {
          let data = res.data
          for (let item in data) {
            data[item]['rate'] = (data[item]['negative'] / (data[item]['negative'] + data[item]['positive'])).toFixed(2)
            data[item]['total'] = (data[item]['negative'] + data[item]['positive'])
          }
          let countList = Object.keys(data).sort(function (a, b) { return data[a]['negative'] - data[b]['negative'] })
          this.rank = []
          let showRank = []
          for (let item in countList) {
            this.rank.push({ 'cityId': countList[item], 'cityName': data[countList[item]]['name'], 'negative': data[countList[item]]['negative'], 'positive': data[countList[item]]['positive'], 'rate': data[countList[item]]['rate'] })
          }
          this.rank = this.rank.reverse()
          for (let i = 0; i < this.rank.length; i++) {
            if (showRank.length < 10) {
              showRank.push(this.rank[i])
            }
          }
          this.tableData = showRank
          this.colorMap()
        } else {
          this.getPageData()
        }
      },
      initMap () {
        // The location of Melbourne
        let au = { lat: -37.8142176, lng: 144.9631608 }
        this.map = new google.maps.Map(
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
        this.map.data.loadGeoJson('mel_geojson.json')

        // mouse click event: show grid info
        this.infowindow = new google.maps.InfoWindow()
        this.map.data.addListener('click',  async (event) => {
          let cityName = event.feature.getProperty('SA2_NAME16')
          this.clickSection = true
          let PopWindow = Vue.extend(popWindowComponent)
          const res = await unemploymentRate({ sa2_main11: event.feature.getProperty('SA2_MAIN16') })
          let unemployment_chart = null
          if (res.isSuccess === true && res.data != null) {
            let x = []
            let y = []
            res.data.forEach(item => {
              x.push(item['year'] + '-' + item['month'])
              y.push(item['value'])
            })
            unemployment_chart = {
              title: {
                text: 'Unemployment Rate',
                x: 'center',
                y: 'top',
                textAlign: 'left'
              },
              tooltip: {
                trigger: 'axis',
                axisPointer: {
                  type: 'shadow'
                }
              },
              xAxis: {
                type: 'category',
                boundaryGap: false,
                data: x
              },
              yAxis: {
                name: '%',
                type: 'value'
              },
              series: [{
                data: y,
                type: 'line',
                areaStyle: {}
              }]
            }
          } else {
            this.$message('failed')
          }
          // send data to the view
          let object = new PopWindow({
            propsData: {
              cityName,
              unemployment_chart
            }
          })

          object.$mount()

          this.infowindow.setContent(object.$el)
          this.infowindow.setPosition(event.latLng)
          this.infowindow.open(this.map)
        })

        // mouse over event: highlight color
         this.map .data.addListener('mouseover', (event) => {
           this.map .data.overrideStyle(event.feature, { fillColor: 'red' })
           let cityName = event.feature.getProperty('SA2_NAME16')
           this.cityNameMessage = this.$message({
             message: cityName,
             type: 'a',
             center: true
           })
        })

        // mouse our event: reset color/info-window
        this.map .data.addListener('mouseout', (event) => {
          this.cityNameMessage.close()
          this.map .data.revertStyle()
          if (this.clickSection === true) {
            this.clickSection = false
            this.infowindow.close()
          }
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
