String.prototype.format = function() {
  var args = arguments;
  return this.replace(/{(\d+)}/g, function(match, number) { 
    return typeof args[number] != 'undefined'
      ? args[number]
      : match
    ;
  });
};

// Handle responses to the ajaxessss
function handler( process ) {

    return function ( e ) {
        if( e.status != 200 )
            return process( e, {} );
        
        data = JSON.parse(e.responseText);
        process(e, data);
        
    };

}