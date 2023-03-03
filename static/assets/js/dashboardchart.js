window.onload = function() {
    //alert ("This is an alert dialog box")
    var LABEL=JSON.parse("{{ChartLabel}}")
    
    
    new Chartist.Line('.line-chart', {
        
        labels: LABEL,//['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        series: [
            [12, 9, 7, 8, 5,20],
            
        ]
        }, {
        fullWidth: true,
        chartPadding: {
            //right: 40
        },
        plugins: [
            Chartist.plugins.tooltip()
        ],
        showArea: true
    });

};

