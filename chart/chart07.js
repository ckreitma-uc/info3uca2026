$(document).ready(function () {
    var ctx = document.getElementById("myChart").getContext("2d");
    // Repositorio público vega-datasets: 1708 registros (series, year, month, count, rate, date)
    var json_url = "https://raw.githubusercontent.com/vega/vega-datasets/main/data/unemployment-across-industries.json";
    // Series a graficar (122 meses cada una)
    var series = ["Government", "Construction", "Finance", "Information"];
    var colores = [
        "rgba(75,192,192,1)",
        "rgba(200,20,50,1)",
        "rgba(54,88,235,1)",
        "rgba(230,160,40,1)"
    ];

    // draw empty chart
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: []
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            elements: {
                point: { radius: 0, hitRadius: 10 }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: { display: true, text: 'Tasa de desempleo (%)' }
                }
            },
        },
    });

    ajax_chart(myChart, json_url);

    // function to update our chart
    function ajax_chart(chart, url) {
        $.getJSON(url).done(function (response) {
            var total = 0;
            var datasets = series.map(function (nombre, i) {
                var filas = response.filter(function (r) { return r.series === nombre; });
                total += filas.length;
                if (i === 0) {
                    chart.data.labels = filas.map(function (r) { return r.date.substring(0, 7); });
                }
                return {
                    label: nombre,
                    fill: false,
                    tension: 0.2,
                    borderColor: colores[i],
                    backgroundColor: colores[i],
                    data: filas.map(function (r) { return r.rate; })
                };
            });
            chart.data.datasets = datasets;
            console.log("Registros en el JSON: " + response.length + ", puntos graficados: " + total);
            chart.update();
        }).fail(function () {
            console.error("No se pudo cargar " + url);
        });
    }
});
