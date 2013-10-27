function transform_url() {
  sanitized =  _.omit($.url().param(), function(v) { return v == ""});
  return "/data/ordered?" + $.param(sanitized);
}

function set_default_form_values() {
  $('#z-score').val( $.url().param("x") );
  $('#row-limit').val( $.url().param("c") );
  $('#row-offset').val( $.url().param("s") );
  $('#order').val( $.url().param("o") );
  $('#samples').val( $.url().param("i") );
}

