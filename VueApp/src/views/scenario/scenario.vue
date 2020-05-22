<template>
  <div id="scenario" style="padding: 20px">
    <el-tabs type="border-card">
      <el-tab-pane label="Scenario 1">
        <h1>{{scenarios[0].title}}</h1>
        <p>{{scenarios[0].content}}</p>
        <chart :options="scenarios[0].chart"></chart>
      </el-tab-pane>
      <el-tab-pane label="Scenario 2">
        <h1>{{scenarios[1].title}}</h1>
        <p>{{scenarios[1].content}}</p>
        <chart :options="scenarios[1].chart"></chart>
      </el-tab-pane>
      <el-tab-pane label="Scenario 3">
        <h1>{{scenarios[2].title}}</h1>
        <p>{{scenarios[2].content}}</p>
        <chart :options="scenarios[2].chart"></chart>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
  import {queryScenario} from 'api/scenarioAPI'
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
      async getPageData() {
        const res = await queryScenario({scenario: 's1'})
        if (res.isSuccess) {
          this.s1Data = res.data

          let scenario1 = this.createS1()
          let scenario2 = this.createS2()
          let scenario3 = this.createS3()
          this.scenarios.push(
            {
              chart: scenario1,
              title: 'Scenario 1',
              content: 'asdasdasdasdasdasdasdasdas'
            }
          )
          this.scenarios.push(
            {
              chart: scenario2,
              title: 'Scenario 2',
              content: 'asdasdasdasdasdasdasdasdas'
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

        let title = [{
          text: ''
        }]

        let index = 0
        this.s1Data.forEach(item => {
          index += 1
          item['total'] = item.positive + item.negative
          source[0].push(item.area)
          source[1].push((item.positive * 100 / item.total).toFixed(2))
          source[2].push((item.negative * 100 / item.total).toFixed(2))
          series.push({
            type: 'pie',
            radius: 60,
            center: [(25*(index)).toString()+'%', '40%'],
            label: {
              show: true,
              position: 'center'
            },
            encode: {
              itemName: 'Sentiment',
              value: item.area
            }
          })
          title.push({
            subtext: item.area,
            left: (23*index).toString()+'%',
            top: '45%',
            textAlign: 'center'
          })
        })
        let scenario1 = {
          legend: {},
          tooltip: {
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
              name: '直接访问',
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
              name: '直接访问',
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
