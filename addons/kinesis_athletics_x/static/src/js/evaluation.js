console.log('outside');

openerp.kinesis_athletics_x = function(instance) {

var _t = instance.web._t,
    _lt = instance.web._lt;
var QWeb = instance.web.qweb;

var color_map = {'alert': '#ff3333', 'superior': '#33ccff', 'ideal': '#2de15c', 'none': '#ffffff'}

instance.web_kanban.KinesisMetricWidget = instance.web_kanban.AbstractField.extend({
    className: "kinesis_metric",

    start: function() {
        var self = this;
        var parent = this.getParent();

        var value = this.field.raw_value;
        var test_name = this.getParent().record['test_id'].value;

        var rating_below_minimum_color = color_map['alert'];
        var rating_between = color_map['ideal'];
        var rating_over_maximum_color = color_map['superior'];

        if (this.getParent().record['rating_below_minimum'].raw_value) {
            rating_below_minimum_color = color_map[this.getParent().record['rating_below_minimum'].raw_value];
        }
        if (this.getParent().record['rating_between'].raw_value) {
            rating_between = color_map[this.getParent().record['rating_between'].raw_value];
        }
        if (this.getParent().record['rating_over_maximum'].raw_value) {
            rating_over_maximum_color = color_map[this.getParent().record['rating_over_maximum'].raw_value];
        }

        var tickPositions = [];

        // Set plotband information.
        var plotband_ext_min = null;
        var plotband_val_min = null;
        var plotband_val_max = null;
        var plotband_ext_max = null;

        if (this.getParent().record['plotband_ext_min'] != null && this.getParent().record['result'].raw_value != 0) {
            plotband_ext_min = this.getParent().record['plotband_ext_min'].raw_value;
        }
        tickPositions.push(plotband_ext_min);

        if (this.getParent().record['plotband_val_min'] != null && this.getParent().record['result'].raw_value != 0) {
            plotband_val_min = this.getParent().record['plotband_val_min'].raw_value;
            if (plotband_val_min < plotband_ext_min) {
                plotband_val_min = null;
            } else {
                tickPositions.push(plotband_val_min);
            }
        }


        if (this.getParent().record['plotband_ext_max'] != null && this.getParent().record['result'].raw_value != 0) {
            plotband_ext_max = this.getParent().record['plotband_ext_max'].raw_value;
        }

        if (this.getParent().record['plotband_val_max'] != null && this.getParent().record['result'].raw_value != 0) {
            plotband_val_max = this.getParent().record['plotband_val_max'].raw_value;
            if (plotband_val_max > plotband_ext_max) {
                plotband_val_max = null;
            } else {
                tickPositions.push(plotband_val_max);
            }
        }

        if (this.getParent().record['result'].raw_value == 0) {
            this.getParent().record['state'].raw_value = 'none'
            console.log(this.getParent().record['state'].raw_value)
        }

        tickPositions.push(plotband_ext_max);

        var plotBands = []

        if (plotband_ext_min != null && plotband_val_min != null) {
            plotBands.push({
                from: plotband_ext_min,
                to: plotband_val_min,
                color: rating_below_minimum_color,
                innerRadius: '100%',
                outerRadius: '110%',
            });
        }

        if (plotband_val_min != null && plotband_val_max != null) {
            plotBands.push({
                from: plotband_val_min,
                to: plotband_val_max,
                color: rating_between,
                innerRadius: '100%',
                outerRadius: '110%'
            });
        }

        if (plotband_val_max != null && plotband_ext_max != null) {
            plotBands.push({
                from: plotband_val_max,
                to: plotband_ext_max,
                color: rating_over_maximum_color,
                innerRadius: '100%',
                outerRadius: '110%'
            });
        }

        // Create the series with the value of the test.
        var series = [{
            data: [value],
            yAxis: 0
        }]

        // If the age_avg field is not null add this value to the series.
        if (this.getParent().record['age_avg'] != null && this.getParent().record['result'].raw_value != 0) {
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
                lineColor: '#666666',
                tickColor: '#666666',
                minorTickColor: '#666666',
                minorTickPosition: 'outside',
                tickPosition: 'outside',
                lineWidth: 1,
                tickLength: 19,
                tickWidth: 1,
                tickPositions: tickPositions,
                endOnTick: false,

                labels: {
                    rotation: 'auto',
                    distance: 25,
                    style: {
                        color: '#000000',
                    },
                },
                plotBands: plotBands,
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

instance.web_kanban.KinesisStateWidget = instance.web_kanban.AbstractField.extend({
    className: "kinesis_state",
    template: 'KinesisState',
});

instance.web_kanban.KinesisResultDisplayWidget = instance.web_kanban.AbstractField.extend({
    className: "kinesis_result_display",
    template: 'KinesisResultDisplay',
});

instance.web_kanban.KinesisAgeAvgDisplayWidget = instance.web_kanban.AbstractField.extend({
    className: "kinesis_age_avg_display",
    template: 'KinesisAgeAvgDisplay',
});

instance.web_kanban.fields_registry.add("kinesis_metric", "instance.web_kanban.KinesisMetricWidget");
instance.web_kanban.fields_registry.add("kinesis_state", "instance.web_kanban.KinesisStateWidget");
instance.web_kanban.fields_registry.add("kinesis_result_display", "instance.web_kanban.KinesisResultDisplayWidget");
instance.web_kanban.fields_registry.add("kinesis_age_avg_display", "instance.web_kanban.KinesisAgeAvgDisplayWidget");

};
