var btn = document.getElementById('timebutton')

function rowClick(x) {
    var start = x.dataset.jsonS
    var end = x.dataset.jsonE
    var issue = x.dataset.issue
    // var issue = JSON.parse(x.dataset.jsonS)['issue']
    starttime = converttime(start)
    endtime = converttime(end)
    html = `<h2>Edit time</h2>
    <div class="loader" id="loader" style="display: none;"></div> 
    <h4>Date: ` + start.replace(/T.*/, '') + `</h4>
    <p>Issue number</p>
    <input type='number' id='issueedit' min='0' value='` + issue + `' required/>
    <p>Start time and date:</p>
    <div id="picker-start"> </div>
    <input id='res1' value='` + starttime + `' type='hidden'>
    <p>End time and date:</p>
    <div id="picker-end"> </div>
    <input id='res2' value='` + endtime + `' type='hidden'>
    <br/>
    <button type='button' onclick="edittime('` + x.dataset.username + `', '` + x.dataset.hash + `')">Click here!</button>
    <div class="trash-solid icon" onclick="deleteEntry('` + x.dataset.hash + `')"></div>
    `

    // console.log(JSON.parse(x.dataset.jsonS)['storage'])

    modalTinyNoFooter2.setContent(html);
    makeFields(starttime, endtime)
    modalTinyNoFooter2.open();
}

var modalTinyNoFooter2 = new tingle.modal({
    onClose: function () {
    },
    onOpen: function () {
    },
    beforeOpen: function () {
    },
    beforeClose: function () {
        removeDiv('dtp_modal-win');
        removeDiv('dtp_modal-content');
        return true;
    },
    cssClass: ['class1', 'class2']
});

var button2 = document.getElementById('test')
var start = document.getElementById('res1')
var end = document.getElementById('res2')
// var issueNew = document.getElementById('issue')

function edittime(username, sha1) {
    // console.log(JSON.parse(jsonS))
    var issueedit = document.getElementById('issueedit')
    console.log(issueedit)
    const url = "http://localhost:5000/v1/edit";
    const other = {
        method: "PUT",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({start_time: res1.value, end_time: res2.value, username: username, issue: issueedit.value, sha1: sha1 })
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

function deleteEntry(sha1) {
    const url = "http://localhost:5000/v1/delete"
    const other = {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({sha1: sha1 })
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