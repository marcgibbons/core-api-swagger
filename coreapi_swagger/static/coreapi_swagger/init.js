$(function () {
  // Pre load translate...
  if(window.SwaggerTranslator) {
    window.SwaggerTranslator.translate();
  }
  window.swaggerUi = new SwaggerUi({
    url: window.location.pathname + '?format=openapi',
    dom_id: "swagger-ui-container",
    supportedSubmitMethods: ['get', 'post', 'put', 'delete', 'patch'],
    onComplete: function(swaggerApi, swaggerUi){
      if(typeof initOAuth == "function") {
        initOAuth({
          clientId: "your-client-id",
          clientSecret: "your-client-secret-if-required",
          realm: "your-realms",
          appName: "your-app-name",
          scopeSeparator: ",",
          additionalQueryStringParams: {}
        });
      }

      if(window.SwaggerTranslator) {
        window.SwaggerTranslator.translate();
      }

      $('pre code').each(function(i, e) {
        hljs.highlightBlock(e)
      });

      addApiKeyAuthorization();
      addCsrfTokenAuthorization();
    },
    onFailure: function(data) {
      log("Unable to Load SwaggerUI");
    },
    docExpansion: "none",
    jsonEditor: true,
    apisSorter: "alpha",
    defaultModelRendering: 'schema',
    showRequestHeaders: false
  });

  function addCsrfTokenAuthorization() {
    var csrftoken = $('[name="csrfmiddlewaretoken"]')[0].value;
    if (!csrftoken) {
      return;
    }
    window.swaggerUi.api.clientAuthorizations.add(
      'csrfmiddlewaretoken',
      new SwaggerClient.ApiKeyAuthorization("X-CSRFToken", csrftoken, "header")
    );
  }

  function addApiKeyAuthorization(){
    var key = encodeURIComponent($('#input_apiKey')[0].value);
    if(key && key.trim() != "") {
      var apiKeyAuth = new SwaggerClient.ApiKeyAuthorization("api_key", key, "query");
      window.swaggerUi.api.clientAuthorizations.add("api_key", apiKeyAuth);
      log("added key " + key);
    }
  }

  $('#input_apiKey').change(addApiKeyAuthorization);

  // if you have an apiKey you would like to pre-populate on the page for demonstration purposes...
    /*
  var apiKey = "myApiKeyXXXX123456789";
  $('#input_apiKey').val(apiKey);
  */

  window.swaggerUi.load();

  function log() {
    if ('console' in window) {
      console.log.apply(console, arguments);
    }
  }
});
