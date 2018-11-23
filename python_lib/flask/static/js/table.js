var totalTimeSpent = 0

function clearTable() {
    tablesection = document.getElementById('table-section')
    tablesection.innerHTML = ''
}

function dateDiv(x) {
    var dateTimeDiv = document.createElement('DIV')
    var dateTimeText = document.createElement('P')
    dateTimeText.setAttribute('class', 'datetime')
    var textNode = document.createTextNode('test')
    dateTimeText.appendChild(textNode)
    dateTimeDiv.appendChild(dateTimeText)
    return dateTimeDiv
}

function tableHeader(x) {
    var tableDiv = document.createElement('DIV')
    tableDiv.setAttribute('class', 'timetable')
    var table = document.createElement('TABLE')

    var tr = document.createElement('TR')
    var th1 = document.createElement('TH')
    var th2 = document.createElement('TH')
    var th3 = document.createElement('TH')
    var th4 = document.createElement('TH')

    th3.setAttribute('class', 'issue')
    th4.setAttribute('class', 'worked')

    var t1 = document.createTextNode("Started");
    var t2 = document.createTextNode("Ended");
    var t3 = document.createTextNode("Issue");
    var t4 = document.createTextNode("Time Worked");

    th1.appendChild(t1)
    th2.appendChild(t2)
    th3.appendChild(t3)
    th4.appendChild(t4)

    tr.appendChild(th1)
    tr.appendChild(th2)
    tr.appendChild(th3)
    tr.appendChild(th4)

    table.appendChild(tr)
    // Call tableContent here! and append it
    for (var k in x['split_days']) {
        table.appendChild(tableContent(x['split_days'][k]))
    }
    // THIS IS THE ENDING
    tableDiv.append(table)
    return tableDiv
}

function tableContent(x) {
    console.log(x)
    var tr = document.createElement('TR')
    var td1 = document.createElement('TD')
    var td2 = document.createElement('TD')
    var td3 = document.createElement('TD')
    var td4 = document.createElement('TD')

    td1.setAttribute('class', 'center-text timeconvert')
    td2.setAttribute('class', 'center-text timeconvert')
    td3.setAttribute('class', 'center-text issue')
    td4.setAttribute('class', 'center-text worked')

    var regexTz = /[+-](\d{4})/
    dt1 = x['timestamp_start'].replace(regexTz, '')
    dt2 = x['timestamp_end'].replace(regexTz, '')
    var d1 = new Date(dt1)
    var d2 = new Date(dt2)
    var worked = new Date(d2.getTime() - d1.getTime())

    totalTimeSpent += worked.getTime()

    var t1 = document.createTextNode(converttime_print(x['timestamp_start']));
    var t2 = document.createTextNode(converttime_print(x['timestamp_end']));
    var t3 = document.createTextNode(x['issue']);
    var t4 = document.createTextNode(writeUTCtime(worked));

    td1.appendChild(t1)
    td2.appendChild(t2)
    td3.appendChild(t3)
    td4.appendChild(t4)

    tr.appendChild(td1)
    tr.appendChild(td2)
    tr.appendChild(td3)
    tr.appendChild(td4)

    return tr
}

function totalWork(x) {
    var tableDiv = document.createElement('DIV')
    tableDiv.setAttribute('class', 'totalwork')
    var table = document.createElement('TABLE')
    var tr = document.createElement('TR')
    var td1 = document.createElement('TD')
    var td2 = document.createElement('TD')

    td1.setAttribute('class', 'right-left double-size-table')
    td2.setAttribute('class', 'center-text worked')

    var t1 = document.createTextNode("Total time worked");
    var t2 = document.createTextNode(writeUTCtime(new Date(totalTimeSpent)));

    td1.appendChild(t1)
    td2.appendChild(t2)
    tr.appendChild(td1)
    tr.appendChild(td2)
    table.appendChild(tr)
    tableDiv.appendChild(table)

    return tableDiv
}

function makeTable(x) {
    tablesection = document.getElementById('table-section')

    var outerDiv = document.createElement('DIV')

    var y = dateDiv(x)
    var p = tableHeader(x)
    var z = totalWork(x)

    outerDiv.appendChild(y)
    outerDiv.appendChild(p)
    outerDiv.appendChild(z)
    console.log(outerDiv.children)
    tablesection.appendChild(outerDiv)
}

// function makeTable(x) {
//     tablesection = document.getElementById('table-section')
//     tHTML = ''
//     var jsonArray = x
//     var tWorked = 0
//     for (var k in jsonArray['split_days']) {
//         n = 0
//         var cHTML = ''
//         var tWorkedDay = 0
//         cHTML += '<div><p class = "datetime">' + k + '</p></div>' +
//             '<div class = "timetable">' +
//             '<table>' +
//             '<tr>' +
//             '<th>Started</th>' +
//             '<th>Ended</th>' +
//             '<th class = "issue">Issue</th>' +
//             '<th class = "worked">Time Worked</th>' +
//             '</tr>'
//         for (var i in jsonArray['split_days'][k]) {
//             if ((n % 2) == 0) {
//                 var regexDate = /(\d{4}(-\d{2}){2})T/
//                 var regexTz = /[+-](\d{4})/
//                 strm1 = jsonArray['split_days'][k][n]['timestamp']
//                 strm2 = jsonArray['split_days'][k][n + 1]['timestamp']
//                 dt1 = jsonArray['split_days'][k][n]['timestamp']
//                 dt2 = jsonArray['split_days'][k][n + 1]['timestamp']
//                 dt1 = dt1.replace(regexTz, '')
//                 dt2 = dt2.replace(regexTz, '')
//                 var d1 = new Date(dt1)
//                 var d2 = new Date(dt2)
//                 var worked = new Date(d2.getTime() - d1.getTime())
//                 cHTML += '<tr onclick="rowClick(this)" data-username=' + JSON.stringify(jsonArray["split_days"][k][n]['user']) + ' data-json-s=' + JSON.stringify(jsonArray["split_days"][k][n]) + ' data-json-e=' + JSON.stringify(jsonArray["split_days"][k][n + 1]) + '>' +
//                     '<td class = "center-text timeconvert">' + converttime_print(strm1) + '</td>' +
//                     '<td class = "center-text timeconvert">' + converttime_print(strm2) + '</td>' +
//                     '<td class = "center-text issue">' + jsonArray["split_days"][k][n]['issue'] + '</td>' +
//                     '<td class = "center-text worked">' + writeUTCtime(worked) + '</td>' +
//                     '</tr>'
//                 tWorkedDay += worked.getTime()
//             }
//             n++
//         }
//         cHTML += '</table>' +
//             '<table>' +
//             '<tr>' +
//             '<td class = "right-left double-size-table">Time worked this day</td>' +
//             '<td class = "center-text worked">' + writeUTCtime(new Date(tWorkedDay)) + '</td>' +
//             '</tr>' +
//             '</table>' +
//             '</div>'
//         tWorked += tWorkedDay
//         tHTML += cHTML
//         cHTML = ''
//     }

//     cHTML += '<div class = "totalwork">' +
//         '<table>' +
//         '<tr>' +
//         '<td class = "right-left double-size-table">Total time worked</td>' +
//         '<td class = "center-text worked">' + writeUTCtime(new Date(tWorked)) + '</td>' +
//         '</tr>' +
//         '</table>' +
//         '</div>'

//     tHTML += cHTML
//     tablesection.innerHTML = tHTML
// }

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
    // makeTable({})
}