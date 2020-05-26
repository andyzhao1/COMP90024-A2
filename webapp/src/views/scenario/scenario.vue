<template>
  <div id="scenario" style="padding: 20px">
    <el-tabs type="border-card">
      <el-tab-pane label="Scenario 1">
        <el-container>
          <el-header height="100px"><br/><h1 style="font-size: 50px">{{scenarios[0].title}}</h1><br/></el-header>
          <el-container>
            <el-main style="width: 50%;background-color: #ffffff">
              <h1 style="font-size: 20px">{{scenarios[0].content}}</h1>
            </el-main>
            <el-main width="50%">
              <chart :options="scenarios[1].chart[0]"></chart>
              <p>-------------------------------------------------------------------</p>
              <br/>
              <chart :options="scenarios[0].chart[1]"></chart>
            </el-main>
          </el-container>
        </el-container>
      </el-tab-pane>
      <el-tab-pane label="Scenario 2">
        <el-container>
          <el-header height="150px"><br/><h1 style="font-size: 50px">{{scenarios[1].title}}</h1><br/></el-header>
          <el-container>
            <el-main style="width: 50%;background-color: #ffffff">
              <h1 style="font-size: 20px">{{scenarios[1].content}}</h1>
            </el-main>
            <el-main width="50%">
              <chart :options="scenarios[1].chart[0]"></chart>
              <p>-------------------------------------------------------------------</p>
              <chart :options="scenarios[1].chart[1]"></chart>
            </el-main>
          </el-container>
        </el-container>
      </el-tab-pane>
      <el-tab-pane label="Scenario 3">
        <el-container>
          <el-header height="150px"><br/><h1 style="font-size: 50px">{{scenarios[2].title}}</h1><br/></el-header>
          <el-container>
            <el-main style="height:40vh;width: 50%;background-color: #ffffff">
              <h1 style="font-size: 20px">{{scenarios[2].content}}</h1>
            </el-main>
            <el-main width="50%">
              <chart :options="scenarios[2].chart[0]"></chart>
            </el-main>
          </el-container>
          <el-container>
            <el-main style="width: 50%;background-color: #ffffff">
              <chart :options="scenarios[0].chart[0]"></chart>
            </el-main>
            <el-main width="50%">
              <chart :options="scenarios[2].chart[1]"></chart>
            </el-main>
          </el-container>
        </el-container>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
  import { queryScenario, educationBackground, industryOfEmploymentByOccupation, centrelink, socialBenifit } from 'api/scenarioAPI'
  import 'echarts/lib/chart/line'
  import 'echarts/lib/component/polar'
  export default {
    name: 'HelloWorld',
    data () {
      return {
        currentDate: new Date(),
        scenarios: [],
        s1_1Data: null,
        s1_2Data: null,
        s2_1Data: {
          x: [],
          y: []
        },
        s2_2Data: {
          x: [],
          y: []
        },
        s3_1Data: {
          x: [],
          y: []
        },
        s3_2Data: null
      }
    },
    methods: {
      async getPageData () {
        const res1_1 = await queryScenario({ scenario: 's1' })
        const res1_2 = await socialBenifit()
        const res2_1 = await queryScenario({ scenario: 's2' })
        const res2_2 = await educationBackground()
        const res3_1 = res2_1
        const res3_2 = await industryOfEmploymentByOccupation()
        if (res1_1.isSuccess && res1_2.isSuccess && res2_1.isSuccess && res2_2.isSuccess && res3_1.isSuccess && res3_2.isSuccess) {
          // S1
          this.s1_1Data = res1_1.data
          this.s1_2Data = res1_2.data
          // S2
          this.s2_1Data.x = []
          this.s2_1Data.y = []
          res2_1.data.forEach(item => {
            this.s2_1Data.x.push(item['area'])
            this.s2_1Data.y.push((item['negative'] / (item['negative'] + item['positive'])))
          })
          res2_2.data.forEach(item => {
            this.s2_2Data.x.push(item['cityName'])
            this.s2_2Data.y.push(item['count'])
          })
          // S3
          this.s3_1Data.x = []
          this.s3_1Data.y = []
          res3_1.data.forEach(item => {
            this.s3_1Data.x.push(item['area'])
            this.s3_1Data.y.push((item['negative'] / (item['negative'] + item['positive'])))
          })
          this.s3_2Data = res3_2.data

          let scenario1 = this.createS1()
          let scenario2 = this.createS2()
          let scenario3 = this.createS3()
          this.scenarios.push(
            {
              chart: scenario1,
              title: 'Impacts of social benefits on career attitude',
              content: 'Work is an essential part of people ’s lives, and social benefits have the most direct impact to people. So do people in areas with low social benefits  be pessimistic about work?'
            }
          )
          this.scenarios.push(
            {
              chart: scenario2,
              title: 'The relationship between education level and negative job attitude',
              content: 'Education is a key part of urban construction. A good level of education will create more talents, and life satisfaction will rise accordingly. This scenario make observations and analysis based on education level and people\'s satisfaction with work.'
            }
          )
          this.scenarios.push(
            {
              chart: scenario3,
              title: 'The relationship between different job distribution and occupational satisfaction',
              content: 'Different work distribution have different social status and economic levels. Therefore, the attitudes of people with different jobs towards work will also be affected. This scenario is based on the proportion of jobs between cities to compare with people\'s satisfaction with their work.'
            }
          )
        } else {
          this.getPageData()
        }
      },
      createS1 () {
        // chart 1
        let source = [
          ['Sentiment'],
          ['Positive'],
          ['Negative']
        ]
        let series = []

        let title = []

        let index = 0
        let gap = 0
        let row = 1
        let column = 0
        this.s1_1Data.forEach(item => {
          column += 1
          if (column === 3) {
            row += 1
          }
          if (column === 2) {
            index = 1
          } else {
            index = 0
          }
          if (column > 2) {
            column = 1
          }
          if (row > 1 && column === 1) {
            gap += 12
          }
          item['total'] = item.positive + item.negative
          source[0].push(item.area)
          source[1].push((item.positive * 100 / item.total).toFixed(2))
          source[2].push((item.negative * 100 / item.total).toFixed(2))
          series.push({
            type: 'pie',
            radius: 60,
            center: [(20 * (row) + gap).toString() + '%', (28 * (column) + 15 * (index)).toString() + '%'],
            itemStyle: {
              emphasis: {
                label: {
                  show: true,
                  formatter: '{d}%',
                  position: 'center'
                },
                labelLine: {
                  show: false
                }
              }
            },
            label: {
              normal: {
                position: 'inner',
                show: false
              }
            },
            encode: {
              itemName: 'Sentiment',
              value: item.area
            }
          })
          title.push({
            text: 'User Attitude for Covid',
            x: 'center',
            y: 'bottom',
            textAlign: 'left',
            textStyle: {
              fontStyle: 'normal',
              fontWeight: 'bold',
              fontFamily: 'san-serif',
              fontSize: 18
            }
          })
          title.push({
            text: item.area,
            left: (20 * (row) + gap).toString() + '%',
            top: (44 * (column) + (-2) * (index)).toString() + '%',
            textAlign: 'center',
            textStyle: {
              fontStyle: 'normal',
              fontWeight: 'lighter',
              fontFamily: 'san-serif',
              fontSize: 18
            }
          })
        })
        let scenario1 = []
        scenario1[0] = {
          legend: {
            top: '3.5%'
          },
          tooltip: {
            trigger: 'item',
            formatter: '{b}'
          },
          dataset: {
            source: source
          },
          title: title,
          series: series
        }
        // chart 2
        let source1_2 = []
        let i = 0
        for (let city in this.s1_2Data) {
          if (source1_2.length === 0) {
            source1_2.push(['type'])
            for (let key1 in this.s1_2Data[city]) {
              source1_2[i].push(key1)
            }
            i += 1
            source1_2.push([city])
            for (let key2 in this.s1_2Data[city]) {
              source1_2[i].push(this.s1_2Data[city][key2])
            }
            i += 1
          } else {
            source1_2.push([city])
            for (let key2 in this.s1_2Data[city]) {
              source1_2[i].push(this.s1_2Data[city][key2])
            }
            i += 1
          }
        }
        console.log(source1_2)
        scenario1[1] = {
          title: {
            text: 'Social Benefits',
            x: 'center',
            y: 'bottom',
            textAlign: 'left',
            textStyle: {
              fontStyle: 'normal',
              fontWeight: 'bold',
              fontFamily: 'san-serif',
              fontSize: 18
            }
          },
          legend: {
            top: '5%'
          },
          tooltip: {
            trigger: 'item'
          },
          dataset: {
            source: source1_2
          },
          xAxis: {type: 'category'},
          yAxis: {},
          // Declare several bar series, each will be mapped
          // to a column of dataset.source by default.
          series: [
            {type: 'bar'},
            {type: 'bar'},
            {type: 'bar'}
          ]
        }
        return scenario1
      },
      createS2 () {
        let scenario2 = []
        scenario2[0] = {
          title: {
            text: 'Negative Rate of Job Related Tweets',
            x: 'center',
            y: 'top',
            textAlign: 'left',
            textStyle: {
              fontStyle: 'normal',
              fontWeight: 'bold',
              fontFamily: 'san-serif',
              fontSize: 18
            }
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
            data: this.s2_1Data.x
          },
          yAxis: {
            name: '',
            type: 'value'
          },
          series: [{
            data: this.s2_1Data.y,
            type: 'line',
            areaStyle: {}
          }]
        }
        ///////Chart 2
        scenario2[1] = {
          title: {
            text: 'Education Background (Grade 12+)',
            x: 'center',
            y: 'bottom',
            textAlign: 'left',
            textStyle: {
              fontStyle: 'normal',
              fontWeight: 'bold',
              fontFamily: 'san-serif',
              fontSize: 18
            }
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
            data: this.s2_2Data.x
          },
          yAxis: {
            name: '',
            type: 'value'
          },
          series: [{
            data: this.s2_2Data.y,
            type: 'line',
            areaStyle: {}
          }]
        }
        return scenario2
      },
      createS3 () {
        let scenario3 = []
        scenario3[0] = {
          title: {
            text: 'Negative Rate of Job Related Tweets',
            x: 'center',
            y: 'top',
            textAlign: 'left',
            textStyle: {
              fontStyle: 'normal',
              fontWeight: 'bold',
              fontFamily: 'san-serif',
              fontSize: 18
            }
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
            data: this.s3_1Data.x
          },
          yAxis: {
            name: '',
            type: 'value'
          },
          series: [{
            data: this.s3_1Data.y,
            type: 'line',
            areaStyle: {}
          }]
        }
        ///////Chart 2
        let source = [
          ['Job Type']
        ]
        let series = []

        let title = []

        let index = 0
        let gap = 0
        let row = 1
        let column = 0
        let cityNames = ['Greater Sydney', 'Greater Melbourne', 'Greater Brisbane', 'Greater Adelaide', 'Greater Perth']
        for (let key in this.s3_2Data['Greater Sydney']) {
          source.push([key])
        }
        cityNames.forEach(city => {
          column += 1
          if (column === 3) {
            row += 1
          }
          if (column === 2) {
            index = 1
          } else {
            index = 0
          }
          if (column > 2) {
            column = 1
          }
          if (row > 1 && column === 1) {
            gap += 12
          }
          let total = 0
          for (let key in this.s3_2Data[city]) {
            total += this.s3_2Data[city][key]
          }
          this.s3_2Data[city]['total'] = total
          for (let index = 0; index < source.length; index++) {
            if (index === 0) {
              source[index].push(city)
            } else {
              source[index].push((this.s3_2Data[city][source[index][0]] / this.s3_2Data[city]['total']).toFixed(2))
            }
          }
          series.push({
            type: 'pie',
            radius: 60,
            center: [(20 * (row) + gap).toString() + '%', (25 * (column) + 18* (index)).toString() + '%'],
            itemStyle: {
              emphasis: {
                label: {
                  show: true,
                  formatter: '{d}%',
                  position: 'center'
                },
                labelLine: {
                  show: false
                }
              }
            },
            label: {
              normal: {
                position: 'inner',
                show: false
              }
            },
            encode: {
              itemName: 'Job Type',
              value: city
            }
          })
          title.push({
            text: 'Occupation Distribution',
            x: 'center',
            y: 'bottom',
            textAlign: 'left',
            textStyle: {
              fontStyle: 'normal',
              fontWeight: 'bold',
              fontFamily: 'san-serif',
              fontSize: 18
            }
          })
          title.push({
            text: city.replace('Greater ',''),
            left: (20 * (row) + gap).toString() + '%',
            top: (41* (column) + (1) * (index)).toString() + '%',
            textAlign: 'center',
            textStyle:{
              fontStyle:'normal',
              fontWeight:"lighter",
              fontFamily:"san-serif",
              fontSize:18
            }
          })
        })
        scenario3[1] = {
          legend: {
            type: 'scroll',
            top: 'top'
          },
          tooltip: {
            trigger: 'item',
            formatter: '{b}'
          },
          dataset: {
            source: source
          },
          title: title,
          series: series
        }
        return scenario3
      }
    },
    mounted () {
      this.getPageData()
    }
  }
</script>

<style lang="scss" scoped>
  .scenario {
    padding: 20px;
  }
  @import url("//unpkg.com/element-ui@2.13.2/lib/theme-chalk/index.css");
  .time {
    font-size: 13px;
    color: #999;
  }

  .bottom {
    margin-top: 13px;
    line-height: 12px;
  }

  .button {
    padding: 0;
    float: right;
  }

  .image {
    width: 100%;
    display: block;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }

  .clearfix:after {
    clear: both
  }
</style>
