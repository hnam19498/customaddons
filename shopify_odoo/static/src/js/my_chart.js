setTimeout(function () {
    const ctx = document.getElementById('myChart');
    let list_date = []
    let list_time = []
    let list_money = []
    for (let line of window.parent.data) {
        if (window.parent.bundle_id === line["bundle_id"]) {
            list_date.push(line['date'])
            list_time.push(line['time'])
            list_money.push(line['price_reduce'])
        }
    }
    console.log(list_money)
    new Chart(ctx, {
        data: {
            labels: list_date,
            datasets: [{
                label: 'Time',
                data: list_time,
                borderWidth: 1,
                type: "bar"
            }, {
                label: "Price reduce",
                data: list_money,
                type: "line",
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    text: 'value'
                }
            }
        }
    })
}, 3000)