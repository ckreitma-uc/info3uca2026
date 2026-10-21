$(document).ready(function () {
    var ctx = document.getElementById("myChart").getContext("2d");
    // examine example_data.json for expected response data
    var json_url = "http://127.0.0.1:5500/chart/data/example_data.json";

    // draw empty chart
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: "My First dataset",
                    fill: false,
                    lineTension: 0.2,
                    backgroundColor: "rgba(75,192,192,0.4)",
                    borderColor: "rgba(75,192,192,1)",
                    borderCapStyle: 'butt',
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: 'miter',
                    pointBorderColor: "rgba(75,192,192,1)",
                    pointBackgroundColor: "#fff",
                    pointBorderWidth: 1,
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: "rgba(75,192,192,1)",
                    pointHoverBorderColor: "rgba(220,220,220,1)",
                    pointHoverBorderWidth: 2,
                    pointRadius: 1,
                    pointHitRadius: 10,
                    data: [],
                    spanGaps: false,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            tooltips: {
                mode: 'index',
                intersect: false
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true   // minimum value will be 0.
                    }
                }],
            },
        },
    });

    ajax_chart(myChart, json_url);

    // function to update our chart
    function ajax_chart (chart, url, data) {
        var data = data || {};

        $.getJSON(url, data).done(function (response) {
            chart.data.labels = response.labels;
            chart.data.datasets[0].data = response.data.quantity; // or you can iterate for multiple datasets
            console.log(chart.options.scales);
            chart.update(); // finally update our chart
        });
    }
});
