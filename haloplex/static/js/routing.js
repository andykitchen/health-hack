function transform_url() {
  params = $.url().param()
  if (params["i"]) {
    params["i"] = params["i"].join(",")
  }
  sanitized =  _.omit(params, function(v) { return v == ""});
  
  return "/data/ordered?" + $.param(sanitized);
}

function set_default_form_values() {
  $('#z-score').val( $.url().param("x") );
  $('#row-limit').val( $.url().param("c") );
  $('#row-offset').val( $.url().param("s") );
  $('#order').val( $.url().param("o") );
  $('#samples').val( $.url().param("i") );
}

