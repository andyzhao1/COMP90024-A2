<template>
  <div style="max-height:1000px; weight:250px; min-width:250px; text-align:center;">
    <h4>{{cityName}}</h4>
    <chart :options=chart style="width: 300px; height: 200px"></chart>
  </div>
</template>
<script>
  export default {
    name: 'infowindow',
    props: [
      'cityName',
      'chart'
    ]
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
