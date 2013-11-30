var upvotebay = angular.module('upvotebay', []);

upvotebay.controller('UpvoteCtrl', function($scope) {
    $scope.upvotes = [
        {title: 'Title 1'},
        {title: 'Title 2'},
    ];
});
