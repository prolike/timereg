var totalTimeSpent = 0;
var dayTimeSpent = 0;
var hoursWorked = 0;

function clearTable() {
    tablesection = document.getElementById('table-section');
    tablesection.innerHTML = '';
    totalTimeSpent = 0;
    dayTimeSpent = 0;
}

function dateDiv(x) {
    var dateTimeDiv = document.createElement('DIV');
    var dateTimeText = document.createElement('P');
    dateTimeText.setAttribute('class', 'datetime');
    var textNode = document.createTextNode(x);
    dateTimeText.appendChild(textNode);
    dateTimeDiv.appendChild(dateTimeText);
    return dateTimeDiv;
}

function tableHeader(json) {
    var tableDiv = document.createElement('DIV');
    tableDiv.setAttribute('class', 'timetable');
    var table = document.createElement('TABLE');

    var tr = document.createElement('TR');
    var th1 = document.createElement('TH');
    var th2 = document.createElement('TH');
    var th3 = document.createElement('TH');
    var th4 = document.createElement('TH');

    th3.setAttribute('class', 'issue');
    th4.setAttribute('class', 'worked');

    var t1 = document.createTextNode("Started");
    var t2 = document.createTextNode("Ended");
    var t3 = document.createTextNode("Issue");
    var t4 = document.createTextNode("Time Worked");

    th1.appendChild(t1);
    th2.appendChild(t2);
    th3.appendChild(t3);
    th4.appendChild(t4);

    tr.appendChild(th1);
    tr.appendChild(th2);
    tr.appendChild(th3);
    tr.appendChild(th4);

    table.appendChild(tr);

    for (var k in json) {
        table.appendChild(tableContent(json[k]));
    }

    var twd = todayWork();

    tableDiv.appendChild(table);
    tableDiv.appendChild(twd);
    return tableDiv;
}

function tableContent(x) {
    if(!x.issue){
        x.issue = '-';
        console.log('-');
    }
    
    var tr = document.createElement('TR');
    var td1 = document.createElement('TD');
    var td2 = document.createElement('TD');
    var td3 = document.createElement('TD');
    var td4 = document.createElement('TD');

    td1.setAttribute('class', 'center-text timeconvert');
    td2.setAttribute('class', 'center-text timeconvert');
    td3.setAttribute('class', 'center-text issue');
    td4.setAttribute('class', 'center-text worked'); 
  
    var regexTz = /[+-](\d{4})/;
    dt1 = x.timestamp_start.replace(regexTz, '');
    
    if(x.timestamp_end){
        dt2 = x.timestamp_end.replace(regexTz, '');
        console.log('LOOOP')
        var d1 = new Date(dt1);
        var d2 = new Date(dt2);
        var worked = new Date(d2.getTime() - d1.getTime());
    
        totalTimeSpent += worked.getTime();
        dayTimeSpent += worked.getTime();

        var t2 = document.createTextNode(converttime_print(x.timestamp_end));
        var t4 = document.createTextNode(writeUTCtime(worked));
        tr.setAttribute('data-json-e', x.timestamp_end);
    }else{
        var t2 = document.createTextNode('-');
        var t4 = document.createTextNode('-');
        tr.setAttribute('data-json-e', x.timestamp_start);
        td1.setAttribute('class', 'missing center-text timeconvert');
        td2.setAttribute('class', 'missing center-text timeconvert');
        td3.setAttribute('class', 'missing center-text issue');
        td4.setAttribute('class', 'missing center-text worked');
    }

    var t1 = document.createTextNode(converttime_print(x.timestamp_start));
    var t3 = document.createTextNode(x.issue);

    td1.appendChild(t1);
    td2.appendChild(t2);
    td3.appendChild(t3);
    td4.appendChild(t4);

    tr.setAttribute('onclick', 'rowClick(this)');
    tr.setAttribute('data-hash', x.sha1);
    tr.setAttribute('data-username', x.username);
    tr.setAttribute('data-json-s', x.timestamp_start);
    tr.setAttribute('data-issue', x.issue);
    tr.appendChild(td1);
    tr.appendChild(td2);
    tr.appendChild(td3);
    tr.appendChild(td4);

    return tr;
}

function todayWork() {
    var table = document.createElement('TABLE');
    var tr = document.createElement('TR');
    var td1 = document.createElement('TD');
    var td2 = document.createElement('TD');

    td1.setAttribute('class', 'right-left double-size-table');
    td2.setAttribute('class', 'center-text worked');

    hoursWorked = Math.floor(dayTimeSpent / 3600000);
    minWorked = ((dayTimeSpent % 3600000) / 60000);

    var t1 = document.createTextNode('Time worked this day');
    var t2 = document.createTextNode(addZeroBefore(hoursWorked) + ":" + addZeroBefore(minWorked));

    td1.appendChild(t1);
    td2.appendChild(t2);
    tr.appendChild(td1);
    tr.appendChild(td2);
    table.appendChild(tr);

    dayTimeSpent = 0;

    return table;
}

function totalWork() {
    var tableDiv = document.createElement('DIV');
    tableDiv.setAttribute('class', 'totalwork');
    var table = document.createElement('TABLE');
    var tr = document.createElement('TR');
    var td1 = document.createElement('TD');
    var td2 = document.createElement('TD');

    td1.setAttribute('class', 'right-left double-size-table');
    td2.setAttribute('class', 'center-text worked');

    hoursWorked = Math.floor(totalTimeSpent / 3600000);
    minWorked = ((totalTimeSpent % 3600000) / 60000);

    var t1 = document.createTextNode("Total time worked");
    var t2 = document.createTextNode(addZeroBefore(hoursWorked) + ":" + addZeroBefore(minWorked));

    td1.appendChild(t1);
    td2.appendChild(t2);
    tr.appendChild(td1);
    tr.appendChild(td2);

    table.appendChild(tr);
    tableDiv.appendChild(table);

    return tableDiv;
}

function makeTable(x) {
    tablesection = document.getElementById('table-section');

    var outerDiv = document.createElement('DIV');

    console.log(x)

    for (var date in x.split_days) {
        var y = dateDiv(date);
        var p = tableHeader(x.split_days[date]);
        outerDiv.appendChild(y);
        outerDiv.appendChild(p);
    }

    var z = totalWork();

    outerDiv.appendChild(z);
    tablesection.appendChild(outerDiv);
}

function writeUTCtime(date) {
    var hour = addZeroBefore(date.getUTCHours());
    var min = addZeroBefore(date.getUTCMinutes());
    var seconds = addZeroBefore(date.getUTCSeconds());
    return hour + ':' + min;
}

function addZeroBefore(n) {
    return (n < 10 ? '0' : '') + n;
}

window.onload = function () {
    const url = "http://localhost:5000/v1/all";
    const other = {
        method: "GET"
    }
    fetch(url, other)
        .then(function (response) {
            return response.json();
        })
        .then(function (myJson) {
            clearTable();
            makeTable(myJson.newdata);
        });
};