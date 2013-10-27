function transform_url() {
  params = $.url().param()
  if (typeof params["i"] === 'array') {
    params["i"] = params["i"].join(",")
  } 
  sanitized =  _.omit(params, function(v) { return v == ""});
  url_params = ""
  _.forIn( sanitized, function(v, k) {
    if (url_params.length > 0) {
      url_params = url_params + "&";
    }
    url_params = url_params + k + "=" + v;
  });
  return "/data/ordered?" + url_params; //$.param(sanitized);
}

function set_default_form_values() {
  if ($.url().param("x") == "zscore") {
    $('#z-score').prop("checked", "checked");
  }
  $('#row-limit').val( $.url().param("c") );
  $('#row-offset').val( $.url().param("s") );
  $('#order').val( $.url().param("o") );
  $('#samples').val( $.url().param("i") );
}

