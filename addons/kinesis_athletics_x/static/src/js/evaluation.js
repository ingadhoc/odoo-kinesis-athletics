console.log('outside');

openerp.kinesis_athletics_x = function(instance) {

var _t = instance.web._t,
    _lt = instance.web._lt;
var QWeb = instance.web.qweb;

var color_map = {'alert': '#ff3333', 'superior': '#33ccff', 'ideal': '#66ff66'}

instance.web_kanban.KinesisMetricWidget = instance.web_kanban.AbstractField.extend({
    className: "kinesis_metric",

    start: function() {
        var self = this;
        var parent = this.getParent();

        var value = this.field.raw_value;
        var test_name = this.getParent().record['test_id'].value;

        var plotband_ext_min = 0;
        var plotband_val_min = 50;
        var plotband_val_max = 100;
        var plotband_ext_max = 150;

        if (this.getParent().record['plotband_ext_min'] != null) {
            plotband_ext_min = this.getParent().record['plotband_ext_min'].raw_value;
        }
        if (this.getParent().record['plotband_val_min'] != null) {
            plotband_val_min = this.getParent().record['plotband_val_min'].raw_value;
        }
        if (this.getParent().record['plotband_val_max'] != null) {
            plotband_val_max = this.getParent().record['plotband_val_max'].raw_value;
        }
        if (this.getParent().record['plotband_ext_max'] != null) {
            plotband_ext_max = this.getParent().record['plotband_ext_max'].raw_value;
        }

        var rating_below_minimum_color = color_map['alert'];
        var rating_in_between_color = color_map['ideal'];
        var rating_over_maximum_color = color_map['superior'];

        if (this.getParent().record['rating_below_minimum'] != null) {
            rating_below_minimum_color = color_map[this.getParent().record['rating_below_minimum'].raw_value];
        }
        if (this.getParent().record['rating_over_maximum'] != null) {
            rating_over_maximum_color = color_map[this.getParent().record['rating_over_maximum'].raw_value];
        }

        var series = [{
            data: [value],
            yAxis: 0
        }]

        if (this.getParent().record['age_avg'] != null) {
            series.push({
                data: [this.getParent().record['age_avg'].raw_value],
                backgroundColor: '#ffffff',
                dial: {
                    radius: '105%',
                    backgroundColor: '#999'
                },
                yAxis: 0
            });
        }

        this.$el.highcharts({
            chart: {
                renderTo: 'container',
                type: 'gauge',
                height: 130,
                width: 390
            },
        
            title: {
                text: test_name
            },
            
            pane: [{
                startAngle: -35,
                endAngle: 35,
                background: null,
                center: ['50%', '320%'],
                size: 380    
            }],                     
        
            yAxis: [{
                min: plotband_ext_min,
                max: plotband_ext_max,
                lineColor: '#666',
                tickColor: '#666',
                minorTickColor: '#666',            
                minorTickPosition: 'outside',
                tickPosition: 'outside',
                lineWidth: 1,
                tickLength: 19,
                tickWidth: 1,
                tickInterval: 50,
                endOnTick: false,
                
                labels: {
                    rotation: 'auto',
                    distance: 25,
                    style: {
                        color: '#000',
                    },
                },
                plotBands: [{
                    from: plotband_ext_min,
                    to: plotband_val_min,
                    color: rating_below_minimum_color,
                    innerRadius: '100%',
                    outerRadius: '110%',
                },{
                    from: plotband_val_min,
                    to: plotband_val_max,
                    color: rating_in_between_color,
                    innerRadius: '100%',
                    outerRadius: '110%'
                },{
                    from: plotband_val_max,
                    to: plotband_ext_max,
                    color: rating_over_maximum_color,
                    innerRadius: '100%',
                    outerRadius: '110%',
                }],        
                pane: 0,
            }],
            
            plotOptions: {
                gauge: {
                    dataLabels: {
                        enabled: false
                    },
                    dial: {
                        radius: '105%'
                    }
                }
            },
                
            series: series
        });
    }
});

instance.web_kanban.fields_registry.add("kinesis_metric", "instance.web_kanban.KinesisMetricWidget");

};
