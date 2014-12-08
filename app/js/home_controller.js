angular.module("TrendyWriterApp", []).controller("HomeController", function($scope, $http) {
    $http.get("/query?field=news").success(function(data) {
        console.log(data);
    }).error(function(data) {

    });
});