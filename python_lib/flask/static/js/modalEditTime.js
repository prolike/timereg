var btn = document.getElementById('timebutton')

function rowClick(x) {
    var start = JSON.parse(x.dataset.jsonS)
    var end = JSON.parse(x.dataset.jsonE)
    var issue = JSON.parse(x.dataset.jsonS)['issue']
    starttime = converttime(start['timestamp'])
    endtime = converttime(end['timestamp'])
    html = `<h2>Edit time</h2>
    <div class="loader" id="loader" style="display: none;"></div> 
    <h4>Date: ` + start['timestamp'].replace(/T.*/, '') + `</h4>
    <p>Issue number</p>
    <input type='number' id='issueedit' min='0' value='` + JSON.parse(x.dataset.jsonS)['issue'] + `' required/>
    <p>Start time and date:</p>
    <div id="picker-start"> </div>
    <input id='res1' value='` + starttime + `' type='hidden'>
    <p>End time and date:</p>
    <div id="picker-end"> </div>
    <input id='res2' value='` + endtime + `' type='hidden'>
    <br/>
    <button type='button' onclick="edittime('` + x.dataset.username + `', '` + JSON.parse(x.dataset.jsonS)['storage']['issuehash'] + `', '` + JSON.parse(x.dataset.jsonS)['storage']['linehash'] + `', '` + JSON.parse(x.dataset.jsonE)['storage']['issuehash'] + `', '` + JSON.parse(x.dataset.jsonE)['storage']['linehash'] + `', '` + JSON.parse(x.dataset.jsonS)['timestamp'] + `', '` + JSON.parse(x.dataset.jsonE)['timestamp'] + `', '` + JSON.parse(x.dataset.jsonS)['issue'] + `')">Click here!</button>`

    // console.log(JSON.parse(x.dataset.jsonS)['storage'])

    modalTinyNoFooter2.setContent(html);
    makeFields(starttime, endtime)
    modalTinyNoFooter2.open();
}

var modalTinyNoFooter2 = new tingle.modal({
    onClose: function () {
        console.log('close');
    },
    onOpen: function () {
        console.log('open');
    },
    beforeOpen: function () {
        console.log('before open');
    },
    beforeClose: function () {
        console.log('before close');
        return true;
    },
    cssClass: ['class1', 'class2']
});

var button2 = document.getElementById('test')
var start = document.getElementById('res1')
var end = document.getElementById('res2')
// var issueNew = document.getElementById('issue')
function edittime(name, jsonSih, jsonSlh, jsonEih, jsonElh, defstarttime, defendtime, startissue) {
    // console.log(JSON.parse(jsonS))
    var issueedit = document.getElementById('issueedit')
    console.log(issueedit)
    const url = "http://localhost:5000/edittime"
    const other = {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ start_time: res1.value, end_time: res2.value, def_start_time: defstarttime, def_end_time: defendtime, username: name, startih: jsonSih, startlh: jsonSlh, endih: jsonEih, endlh: jsonElh, issue: startissue, newIssue: issueedit.value })
    }

    removeDiv('dtp_modal-win')
    removeDiv('dtp_modal-content')

    document.getElementById("loader").style.display = "inline";
    fetch(url, other)
        .then(function (response) {
            document.getElementById("loader").style.display = "none";
            return response.json();
        })
        .then(function (myJson) {
            modalTinyNoFooter2.close()
            clearTable()
            makeTable(myJson['newdata'])
        });
}

function makeFields(starttime, endtime) {
    // console.log('start: ' + starttime)
    $('#picker-start').dateTimePicker({
        positionShift: { top: 0, left: 0 },
        title: "Select Date and Time",
        buttonTitle: "Select",
        selectData: starttime,
    });

    $('#picker-end').dateTimePicker({
        positionShift: { top: 0, left: 0 },
        title: "Select Date and Time",
        buttonTitle: "Select",
        selectData: endtime
    });
}