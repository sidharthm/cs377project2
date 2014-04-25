
function cloneAndFillNote(title, content, id, color){
    var cloned = $('#notetemplate').clone(true,true);
    cloned.attr('id',id);
    cloned.children(".note").children('.nano-content').children("p.notetitle").text(title);
    cloned.children(".note").children('.nano-content').children("p.notetitle").attr('name',"testNoteName");
    cloned.children('.note').children('.nano-content').children('p.notecontent').text(content);
    cloned.children('.note').addClass(color);
    cloned.children('.note').attr('color',color);
    return cloned;
}



function displayNotesArray(notesIn, index){
    setTimeout(function(){
	if(index < notesIn.length){
            displayNote(notesIn[index]);
            displayNotesArray(notesIn,index+1);
	}
    },150);
}

var noteDirectives = {
    '@id':'id',
    'div.note':{
	'p.notetitle':'title',
	'center':{
	    'p': 'content'
	}
    }
}
function displayNote(jsonIn){
    console.log(jsonIn);
    if(numNotesDisplayed % 4 == 0){
	$('#notesContainer').append($("<div></div>").addClass("row"));
    }
    
    var cloned=cloneAndFillNote(jsonIn['title'],jsonIn['content'],jsonIn['id'], jsonIn['color']);
    
    if(numNotesDisplayed <= 4){
	console.log("add");
	cloned.addClass("animated slideInDown");
    }else{
	switch(numNotesDisplayed % 4){
	case 0:
	case 1:
	    cloned.addClass("animated slideInLeft");
	    break;
	case 2:
	case 3:
	    cloned.addClass("animated slideInRight");
	    break;
	}
    }
    $('#notesContainer').children('.row:last').append(cloned.show());
    console.log("added note titled: " + jsonIn['title']);
    numNotesDisplayed++;
}
function createNote(){
    //console.log($('#newnotecontent').val());
    $.ajax({
	type: "POST",
	url: newNoteUrl,
	data: { title: $('#newnotetitle').val(), content: $('#newnotecontent').val() }
    })
	.done(function( msg ) {
	    console.log("New note created with ID: " + msg);
	    displayNote({'title':$('#newnotetitle').val(),'content': $('#newnotecontent').val(),'id':msg});
	});
}
var editcolor='';
function showEditNote(note){
    note = $(note);
    console.log(note.parent());
    var editnote = $('#editmodal');
    editcolor = note.parent().parent().children('.note').attr('color');
    $('#editnotetitle').val(note.parent().children('p.notetitle').text());
    $('#editnotecontent').val(note.parent().children('p.notecontent').text());
    $('#editnoteid').val(note.parent().parent().parent().attr('id'))
    editnote.modal('show');
}
function editNote(){
    $.ajax({
	type: "POST",
	url: editNoteUrl,
	data: { title: $('#editnotetitle').val(), content: $('#editnotecontent').val(), id:  $('#editnoteid').val(), color: editcolor}
    })
	.done(function( msg ) {
	    console.log(msg);
	    $($('#editnoteid')).children().children('p.notetitle').text($('#editnotetitle'));
	    location.reload();
	});
}
function deleteNote(){
    $.ajax({
	type: "POST",
	url: deleteNoteUrl,
	data: { id:  $('#editnoteid').val() }
    })
	.done(function( msg ) {
	    console.log(msg);
	    location.reload();
	});
    
}


$(function(){
    //$('.nano').nanoScroller( {} );
});
