var upvotebayControllers = angular.module('upvotebayControllers', []);

upvotebayControllers.controller('MyProfileCtrl', ['$scope', '$http', 'LoginService',
    function($scope, $http, LoginService) {
        $scope.current_user = LoginService.current_user;

        $http.get('/api/v1/my/likes.json').success(function(data) {
            var likes = [];

            angular.forEach(data.likes, function(like, i) {
                like.has_thumbnail = function() {
                    return !!like.thumbnail_url && like.thumbnail_url !== 'self';
                };

                likes.push(like);
            });

            $scope.likes = likes;
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
