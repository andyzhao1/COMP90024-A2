<template>
  <div id="scenario" style="padding: 20px">
    <el-tabs type="border-card">
      <el-tab-pane label="Scenario 1">
        <el-container>
          <el-aside style="width: 50%;background-color: #ffffff">
            <h2>{{scenarios[0].title}}</h2>
            <h1>{{scenarios[0].content}}</h1>
          </el-aside>
          <el-main width="50%"><chart :options="scenarios[0].chart"></chart></el-main>
        </el-container>
      </el-tab-pane>
      <el-tab-pane label="Scenario 2">
        <el-container>
          <el-aside style="width: 50%;background-color: #ffffff">
            <h2>{{scenarios[1].title}}</h2>
            <h1>{{scenarios[1].content}}</h1>
          </el-aside>
          <el-main width="50%"><chart :options="scenarios[1].chart"></chart></el-main>
        </el-container>
      </el-tab-pane>
      <el-tab-pane label="Scenario 3">
        <el-container>
          <el-aside style="width: 50%;background-color: #ffffff">
            <h2>{{scenarios[2].title}}</h2>
            <h1>{{scenarios[2].content}}</h1>
          </el-aside>
          <el-main width="50%"><chart :options="scenarios[2].chart"></chart></el-main>
        </el-container>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
  import { queryScenario } from 'api/scenarioAPI'
  import 'echarts/lib/chart/line'
  import 'echarts/lib/component/polar'
  export default {
    name: 'HelloWorld',
    data () {
      return {
        currentDate: new Date(),
        scenarios: [],
        s1Data: null,
        s2Data:{
          x: ["A","B","C"],
          y: [4,6,8]
        },
        s3Data:{
          x: ["D","E","F"],
          y: [8,1,6]
        }
      }
    },
    methods: {
      async getPageData () {
        const res = await queryScenario({ scenario: 's1' })
        if (res.isSuccess) {
          this.s1Data = res.data

          let scenario1 = this.createS1()
          let scenario2 = this.createS2()
          let scenario3 = this.createS3()
          this.scenarios.push(
            {
              chart: scenario1,
              title: 'Scenario 1',
              content: 'This is our scenario1, This is our scenario1, This is our scenario1, This is our scenario1'
            }
          )
          this.scenarios.push(
            {
              chart: scenario2,
              title: 'Scenario 2',
              content: 'This is our scenario2, This is our scenario2, This is our scenario2, This is our scenario2'
            }
          )
          this.scenarios.push(
            {
              chart: scenario3,
              title: 'Scenario 3',
              content: 'asdasdasdasdasdasdasdasdas'
            }
          )
        } else {
          this.getPageData()
        }
      },
      createS1 () {
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
        this.s1Data.forEach(item => {
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
            center: [(20 * (row) + gap).toString() + '%', (20 * (column) + 25 * (index)).toString() + '%'],
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
            text: item.area,
            left: (20 * (row) + gap).toString() + '%',
            top: (40 * (column) + 5 * (index)).toString() + '%',
            textAlign: 'center'
          })
        })
        let scenario1 = {
          legend: {
            bottom: 'bottom',
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
        return scenario1
      },
      createS2 () {
        let scenario2 = {
          color: ['#3398db'],
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: [
            {
              type: 'category',
              data: this.s2Data.x,
              axisTick: {
                alignWithLabel: true
              }
            }
          ],
          yAxis: [
            {
              type: 'value'
            }
          ],
          series: [
            {
              name: '',
              type: 'bar',
              barWidth: '60%',
              data: this.s2Data.y
            }
          ]
        }
        return scenario2
      },
      createS3 () {
        let scenario3 = {
          color: ['#3398DB'],
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: [
            {
              type: 'category',
              data: this.s3Data.x,
              axisTick: {
                alignWithLabel: true
              }
            }
          ],
          yAxis: [
            {
              type: 'value'
            }
          ],
          series: [
            {
              name: '',
              type: 'bar',
              barWidth: '60%',
              data: this.s3Data.y
            }
          ]
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
