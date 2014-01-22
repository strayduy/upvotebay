var upvotebayApp = angular.module('upvotebayApp', [
    'ngCookies',
    'ngRoute',
    'upvotebayControllers',
    'upvotebayFilters'
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

upvotebayApp.factory('LoginService', ['$cookieStore', function($cookieStore) {
    var current_user = JSON.parse($cookieStore.get('current_user'));
    $cookieStore.remove('current_user');
    return {current_user: current_user};
}]);
