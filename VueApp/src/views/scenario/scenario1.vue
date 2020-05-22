<template>
  <div id="scenario" style="padding: 20px">
    <el-row>
      <el-col :span="8" v-for="(o, index) in scenarios.length" :key="o" :offset="index > 0 ? scenarios.length: 0">
        <el-card :body-style="{ padding: '0px' }">
          <chart :options="scenarios[index].chart"></chart>
          <div style="padding: 14px;">
            <span>{{scenarios[index].title}}</span>
            <div class="bottom clearfix">
              <time class="time">{{scenarios[index].content}}</time>
              <el-button type="text" class="button">操作按钮</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  import { dataMixin } from '@/common/js/mixin'
  import routes from '@/common/js/config/routes'
  import { queryScenario } from 'api/scenarioAPI'
  import 'echarts/lib/chart/line'
  import 'echarts/lib/component/polar'
  export default {
    name: 'HelloWorld',
    data () {
      return {
        currentDate: new Date(),
        scenarios: [],
        s1Data:{
          x: ["A","B","C"],
          y: [4,6,8]
        },
        s2Data:{
          x: ["A","B","C"],
          y: [4,6,8]
        },
        s3Data:{
          x: ["A","B","C"],
          y: [4,6,8]
        }
      }
    },
    mounted () {
      let scenario1 = {
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
            data: this.s1Data.x,
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
            data: this.s1Data.y
          }
        ]
      }

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
              data: this.s1Data.x,
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
              data: this.s1Data.y
            }
          ]
        }

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
              data: this.s1Data.x,
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
              data: this.s1Data.y
            }
          ]
        }
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
