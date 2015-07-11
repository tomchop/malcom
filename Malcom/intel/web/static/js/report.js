$(function() {
	$("#edit").click(function() {
		console.log("clicked!");
		edit_table();
	});

	$("#search-btn").click(function(){
		search_entities($('#query').val(), $(this).data('url'))
	});

	$("#associate-btn").click(function(){
		do_associations($(this).data('url'))
	});

	$(".unlink").click(function(){
		unlink($(this).data('url'));
	})

	console.log("report.js loaded");
});

function unlink(url) {
	console.log('unlinking');
	$.ajax({
		url: url,
		method: "DELETE",
	}).success(function(data) {
		console.log('elements succesfully unlinked')
	});

}

function do_associations(url) {
	console.log('associating')
	inputs = $("#associate").serializeArray()
	ids = []
	for (var i in inputs) {
		console.log(inputs[i])
		ids.push(inputs[i].name)
	}
	console.log(ids)
	$.ajax({
		url: url,
		data: $.param({ids: ids}, true),
		method: "POST",
	}).success(function(data) {
		console.log('elements succesfully associated')
	});
}

function search_entities(query, url) {
	$.ajax({
		url: url,
		data: {"query": query},
	}).success(function(data) {
		tbl = $("<table id='search'></table>").addClass('table table-condensed');
		for (var i in data){
			e = data[i];
			tbl.append("<tr><th>"+e['title']+"</th><td>"+e['_type']+"</td><td><input type='checkbox' name='"+e['_id']['$oid']+"' /></td></tr>");
		}
		$("#search table").replaceWith(tbl);
	});
}

function edit_table() {
	tbl = $("#main-table");
	tbl.wrap("<form id='update'></form>")

	$("td", tbl).each(function (index, value){
		text = $(value).text();
		field = $(value).data('field');

		input = '<input type="text" name="'+field+'" value="'+text+'" />';
		$(value).html(input);
	});

	edit = $("#edit")
	edit.text('[save]');
	edit.unbind('click');
	edit.click(function() {
		update_entity();
	});
}

function update_entity() {
	console.log("updating");
	console.log($("#update").serialize())

	$.ajax({
		url: $("#main-table").data('url'),
		data: $("#update").serializeArray(),
	}).success(function(data) {
		$("td", tbl).each(function (index, value){
			text = $('input', value).val();
			$(value).html(text);
		});
		tbl.unwrap();
		edit = $("#edit")
		edit.text('[edit]')
		edit.unbind('click');
		edit.click(function() {
			edit_table();
		});
	});
}