var upvotebayApp = angular.module('upvotebayApp', [
    'ngRoute',
    'upvotebayControllers'
]);

upvotebayApp.config(['$routeProvider', '$locationProvider',
    function($routeProvider, $locationProvider) {
        $locationProvider.html5Mode(true);
        $routeProvider.
            when('/', {
                templateUrl: '/static/partials/my-profile.html',
                controller: 'MyProfileCtrl'
            }).
            when('/u/:username', {
                templateUrl: '/static/partials/user-profile.html',
                controller: 'UserProfileCtrl'
            }).
            otherwise({
                redirectTo: '/404'
            });
    }
]);
