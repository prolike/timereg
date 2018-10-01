function clearTable(){
    console.log('Clearing')
    tablesection = document.getElementById('table-section')
    tablesection.innerHTML = ''    
}

function makeTable(x) {
    console.log('Called!')
    tablesection = document.getElementById('table-section')
    tHTML = ''
    // const url = "http://localhost:5000/getall"
    // const other = {
    //     method: "GET",
    // }
    // fetch(url, other)
    //     .then(function (response) {
    //         return response.json();
    //     })
    //     .then(function (myJson) {
    //         jsonArray = myJson;
    //     });

    var jsonArray = x

    // for (var k in jsonArray){
    //     console.log(jsonArray[k])
    //     tHTML += jsonArray[k]
    // }

    console.log(x)

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
            '<th class = "worked">Time Worked</th>' +
            '</tr>'
        for (var i in jsonArray['split_days'][k]) {
            if ((n % 2) == 0) {
                var regexDate = /(\d{4}(-\d{2}){2})T/
                var regexTz = /[+-](\d{4})/

                strm1 = jsonArray['split_days'][k][n]['timestamp'].replace(regexDate, '')
                strm2 = jsonArray['split_days'][k][n + 1]['timestamp'].replace(regexDate, '')

                dt1 = jsonArray['split_days'][k][n]['timestamp']
                dt2 = jsonArray['split_days'][k][n + 1]['timestamp']
                dt1 = dt1.replace(regexTz, '')
                dt2 = dt2.replace(regexTz, '')
                var d1 = new Date(dt1)
                var d2 = new Date(dt2)
                var worked = new Date(d2.getTime() - d1.getTime())
                console.log(jsonArray["split_days"][k][n])
                cHTML += '<tr onclick="rowClick(this)" data-username=' + JSON.stringify(jsonArray['username']) + ' data-json-s=' + JSON.stringify(jsonArray["split_days"][k][n]) + ' data-json-e=' + JSON.stringify(jsonArray["split_days"][k][n + 1]) + '>' +
                    '<td class = "center-text timeconvert">' + strm1 + '</td>' +
                    '<td class = "center-text timeconvert">' + strm2 + '</td>' +
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
    return hour + ':' + min + ':' + seconds
}

function addZeroBefore(n) {
    return (n < 10 ? '0' : '') + n;
}