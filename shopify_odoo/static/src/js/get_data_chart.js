setTimeout(function () {
    if (window.location.href.indexOf("model=bundle.analytic") > -1) {
        let trs = document.getElementsByClassName('o_list_no_open')
        if (trs) {
            let list_count = []
            for (let tr of trs) {
                list_count.push({
                    "bundle_id": parseInt(tr.cells[0].innerText),
                    "time": parseInt(tr.cells[2].innerText),
                    'date': tr.cells[1].innerText,
                    'price_reduce': parseFloat(tr.cells[3].innerText)
                })
            }
            window.data = list_count
            a_hash = document.getElementById('o_field_input_10').hash
            window.bundle_id = parseInt(a_hash.split('&')[0].slice(a_hash.split('&')[0].indexOf("=") + 1))
        }
        document.getElementsByName('bundle_analytic')[0].addEventListener("click", function () {
            setTimeout(function () {
                console.log(window)
                window.location.reload()
            }, 2000)
        })
    }
}, 3000)

