angular.module('upvotebayFilters', []).filter('momentFromNow', function() {
    return function(unix_timestamp) {
        return moment.unix(unix_timestamp).fromNow();
    };
});
