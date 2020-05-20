var myChart = echarts.init(document.getElementById("echart"));
 
        var xAxisData = [];
		var data1 = [];
		var data2 = [];
		for (var i = 0; i < 100; i++) {
			xAxisData.push('class' + i);
			data1.push((Math.sin(i / 5) * (i / 5 -10) + i / 6) * 5);
			data2.push((Math.cos(i / 5) * (i / 5 -10) + i / 6) * 5);
		}

		option = {
			xAxis: {
				type: 'category',
				data: ['Mel', 'Syd', 'Per', 'Bri', 'Ada']
			},
			yAxis: {
				type: 'value'
			},
			series: [{
				data: [120, 200, 150, 80, 70],
				type: 'bar',
				showBackground: true,
				backgroundStyle: {
					color: 'rgba(220, 220, 220, 0.8)'
				}
			}]
		};

 
        myChart.setOption(option);