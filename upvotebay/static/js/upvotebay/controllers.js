var upvotebayControllers = angular.module('upvotebayControllers', []);

upvotebayControllers.controller('MyProfileCtrl', ['$scope', '$http',
    function($scope, $http) {
        $http.get('/api/v1/my/likes.json').success(function(data) {
            $scope.likes = data['likes'];
        });
    }]
);

upvotebayControllers.controller('UserProfileCtrl', ['$scope', '$routeParams', '$http',
    function($scope, $routeParams, $http) {
        var username = $routeParams.username;

        if (username) {
            $http.get('/api/v1/users/' + username + '/likes.json').success(function(data) {
                $scope.likes = data['likes'];
            });
        }
    }]
);
