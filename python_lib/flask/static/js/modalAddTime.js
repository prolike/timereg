var btn = document.getElementById('timebutton')

// var start = moment('2018-12-08 09:42');
// var remainder = 15 - (start.minute() % 15);

// var dateTime = moment(start).add(remainder, "minutes").format('Y-M-DD[T]HH:mm');

// console.log(dateTime);

var m = (Math.round(moment().minutes()/15) * 15) % 60

var total = moment().minute(m).format('Y-M-DD[T]HH:mm')
console.log(total)

var html = `<h2>Add a date</h2>
<p>Select the date and time where you wanna add you time!</p>
<p>Please input your issue number</p>
<input type='number' id='issueID' required/>
<p>Start time and date:</p>
<div id="picker-start"> </div>
<input type="hidden" id="res1" value="` + total + `">
<p>End time and date:</p>
<div id="picker-end"> </div>
<input type="hidden" id="res2" value="` + total + `">
<br>
<button type='button' id='test'>Click here!</button>`

var modalTinyNoFooter = new tingle.modal({
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

btn.addEventListener('click', function () {
    modalTinyNoFooter.open();
});

modalTinyNoFooter.setContent(html);

var button2 = document.getElementById('test')
var start = document.getElementById('res1')
var end = document.getElementById('res2')
var issueID = document.getElementById('issueID')

button2.onclick = function () {
    if (issueID.value != '') {
        const url = "http://localhost:5000/addtime"
        const other = {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ issue: issueID.value, start_time: res1.value, end_time: res2.value, username: 'davidcarl' })
        }
        fetch(url, other)
            .then(function (response) {
                return response.json();
            })
            .then(function (myJson) {
                clearTable()
                console.log(myJson)
                makeTable(myJson['newdata'])
            });
    } else {
        alert('Please remember to input issue number!')
    }
}

$('#picker-start').dateTimePicker({
    positionShift: { top: 0, left: 0 },
    title: "Select Date and Time",
    buttonTitle: "Select",
    selectData: total
});

$('#picker-end').dateTimePicker({
    positionShift: { top: 0, left: 0 },
    title: "Select Date and Time",
    buttonTitle: "Select",
    selectData: total
});
