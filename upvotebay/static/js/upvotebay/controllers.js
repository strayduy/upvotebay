var upvotebay = angular.module('upvotebay', []);

upvotebay.controller('UpvoteCtrl', ['$scope', '$http',
    function($scope, $http) {
        $http.get('/api/v1/my/likes.json').success(function(data) {
            $scope.likes = data['likes'];
        });
    }]
);
