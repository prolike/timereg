function clearTable() {
    tablesection = document.getElementById('table-section')
    tablesection.innerHTML = ''
}

function makeTable(x) {
    tablesection = document.getElementById('table-section')
    tHTML = ''
    var jsonArray = x
    var tWorked = 0
    for (var k in jsonArray['split_days']) {
        n = 0
        var cHTML = ''
        var tWorkedDay = 0
        cHTML += '<div><p class = "datetime">' + k + '</p></div>' +
            '<div class = "timetable">' +
            '<table>' +
            '<tr>' +
            '<th>Started</th>' +
            '<th>Ended</th>' +
            '<th class = "issue">Issue</th>' +
            '<th class = "worked">Time Worked</th>' +
            '</tr>'
        for (var i in jsonArray['split_days'][k]) {
            if ((n % 2) == 0) {
                var regexDate = /(\d{4}(-\d{2}){2})T/
                var regexTz = /[+-](\d{4})/
                strm1 = jsonArray['split_days'][k][n]['timestamp']
                strm2 = jsonArray['split_days'][k][n + 1]['timestamp']
                dt1 = jsonArray['split_days'][k][n]['timestamp']
                dt2 = jsonArray['split_days'][k][n + 1]['timestamp']
                dt1 = dt1.replace(regexTz, '')
                dt2 = dt2.replace(regexTz, '')
                var d1 = new Date(dt1)
                var d2 = new Date(dt2)
                var worked = new Date(d2.getTime() - d1.getTime())
                cHTML += '<tr onclick="rowClick(this)" data-username=' + JSON.stringify(jsonArray["split_days"][k][n]['user']) + ' data-json-s=' + JSON.stringify(jsonArray["split_days"][k][n]) + ' data-json-e=' + JSON.stringify(jsonArray["split_days"][k][n + 1]) + '>' +
                    '<td class = "center-text timeconvert">' + converttime_print(strm1) + '</td>' +
                    '<td class = "center-text timeconvert">' + converttime_print(strm2) + '</td>' +
                    '<td class = "center-text issue">' + jsonArray["split_days"][k][n]['issue'] + '</td>' +
                    '<td class = "center-text worked">' + writeUTCtime(worked) + '</td>' +
                    '</tr>'
                tWorkedDay += worked.getTime()
            }
            n++
        }
        cHTML += '</table>' +
            '<table>' +
            '<tr>' +
            '<td class = "right-left double-size-table">Time worked this day</td>' +
            '<td class = "center-text worked">' + writeUTCtime(new Date(tWorkedDay)) + '</td>' +
            '</tr>' +
            '</table>' +
            '</div>'
        tWorked += tWorkedDay
        tHTML += cHTML
        cHTML = ''
    }

    cHTML += '<div class = "totalwork">' +
        '<table>' +
        '<tr>' +
        '<td class = "right-left double-size-table">Total time worked</td>' +
        '<td class = "center-text worked">' + writeUTCtime(new Date(tWorked)) + '</td>' +
        '</tr>' +
        '</table>' +
        '</div>'

    tHTML += cHTML
    tablesection.innerHTML = tHTML
}

function writeUTCtime(date) {
    var hour = addZeroBefore(date.getUTCHours())
    var min = addZeroBefore(date.getUTCMinutes())
    var seconds = addZeroBefore(date.getUTCSeconds())
    return hour + ':' + min
}

function addZeroBefore(n) {
    return (n < 10 ? '0' : '') + n;
}

window.onload = function () {
    const url = "http://localhost:5000/getall"
    const other = {
        method: "GET"
    }
    fetch(url, other)
        .then(function (response) {
            return response.json();
        })
        .then(function (myJson) {
            clearTable()
            makeTable(myJson['newdata'])
        });
}