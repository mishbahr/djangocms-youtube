// the semi-colon before function invocation is a safety net against concatenated
// scripts and/or other plugins which may not be closed properly.
;(function ($, window, document, undefined) {

    var youTubePlayer = 'youTubePlayer',
        defaults = {
            autohide: 2,
            cc_load_policy: 0,
            color: 'white',
            controls: 2,
            dataLayerName: 'dataLayer',
            debug: true,
            disablekb: 1,
            endscreenClose: '.js-endscreen-close',
            endScreenOpacity: 0.85,
            fs: 1,
            gaCategory: 'Videos',
            googleAnalytics: true,
            hl: 'en',
            iv_load_policy: 3,
            modestbranding: 1,
            onErrorMsg: 'We\'re sorry. Something Unexpected Happened. Please Try Again Later.',
            playsinline: 0,
            rel: 0,
            showinfo: 0,
            theme: 'dark',
            videoEndscreen: '.js-video-endscreen',
            videoPoster: '.js-video-poster',
            videoTarget: '.js-video-target',
            videoTrigger: '.js-video-trigger'
        };

    function YTPlayer(el, options) {
        this.el = $(el);
        this.settings = $.extend(true, {}, defaults, options);
        this._defaults = defaults;
        this._name = youTubePlayer;

        this.videoTrigger = $(this.settings.videoTrigger, this.el);
        this.videoPoster = $(this.settings.videoPoster, this.el);
        this.videoTarget = $(this.settings.videoTarget, this.el);
        this.videoEndscreen = $(this.settings.videoEndscreen, this.el);
        this.endscreenClose = $(this.settings.endscreenClose, this.el);

        this.videoId = this.el.data('video-id');
        this.videoTitle = this.el.data('video-title');

        this.isVideoLoaded = false;
        this.trackedEvents = [];
        this.init();
    }

    YTPlayer.prototype = {
        init: function () {
            this.videoTrigger.on('click', function () {
                if (!this.isVideoLoaded) {
                    this.player = new YT.Player(this.videoTarget.get(0), {
                        videoId: this.videoId,
                        width: this.el.outerWidth(true),
                        height: this.el.outerHeight(true),
                        playerVars: {
                            autohide: this.settings.autohide,
                            cc_load_policy: this.settings.cc_load_policy,
                            color: this.settings.color,
                            controls: this.settings.controls,
                            disablekb: this.settings.disablekb,
                            fs: this.settings.fs,
                            hl: this.settings.hl,
                            iv_load_policy: this.settings.iv_load_policy,
                            modestbranding: this.settings.modestbranding,
                            origin: this.getOrigin(),
                            playsinline: this.settings.playsinline,
                            rel: this.settings.rel,
                            showinfo: this.settings.showinfo,
                            theme: this.settings.theme
                        },
                        events: {
                            onReady: $.proxy(this.onPlayerReady, this),
                            onStateChange: $.proxy(this.onPlayerStateChange, this),
                            onError: $.proxy(this.onError, this),
                        }
                    });
                } else {
                    this.playVideo();
                }
            }.bind(this));

            this.endscreenClose.on('click', function () {
                this.fadeInVideoPoster();
                this.fadeOutVideoEndScreen();
            }.bind(this))
        },
        getOrigin: function () {
            return window.location.origin || window.location.protocol + '//' + window.location.hostname + (window.location.port ? ':' + window.location.port : '');
        },
        fadeOutVideoPoster: function () {
            TweenMax.to(this.videoPoster, 0.55, {autoAlpha: 0});
        },
        fadeInVideoPoster: function () {
            TweenMax.to(this.videoPoster, 0.55, {autoAlpha: 1});
        },
        fadeInVideoEndScreen: function () {
            TweenMax.to(this.videoEndscreen, 0.55, {autoAlpha: this.settings.endScreenOpacity});
        },
        fadeOutVideoEndScreen: function () {
            TweenMax.to(this.videoEndscreen, 0.55, {autoAlpha: 0});
        },
        onPlayerReady: function (e) {
            this.isVideoLoaded = true;
            this.videoDuration = this.player.getDuration();
            this.progressMarkers = {
                '10% watched': this.videoDuration * 0.1,
                '25% watched': this.videoDuration * 0.25,
                '50% watched': this.videoDuration * 0.5,
                '75% watched': this.videoDuration * 0.75,
                '90% watched': this.videoDuration * 0.9,
                'Watch to end': this.videoDuration * 0.99
            };
            this.playVideo();
        },
        onPlayerStateChange: function (e) {
            if (e.data == YT.PlayerState.ENDED) {
                this.trackedEvents = [];
                if(this.videoEndscreen.hasClass('js-has-content')) {
                    this.fadeInVideoEndScreen();
                } else {
                    this.fadeInVideoPoster();
                }
            }

            if (e.data == YT.PlayerState.PLAYING && !this.playerTimer) {
                this.playerTimer = setInterval(function () {
                    for (var marker in this.progressMarkers) {
                        if (this.progressMarkers.hasOwnProperty(marker)) {
                            if (Math.floor(this.progressMarkers[marker]) <= this.player.getCurrentTime()) {
                                this.trackEvent(marker);
                            }
                        }
                    }
                }.bind(this), 1000);
            } else {
                clearInterval(this.playerTimer);
                this.playerTimer = false;
            }
        },
        onError: function (e) {
            var errorCode = e.data ? ' - Code ' + e.data : '',
                errorMsg = 'An unknown error occurred.';
            switch (e.data) {
                case 2:
                    errorMsg = 'The request contains an invalid parameter value.';
                    break;
                case 100:
                    errorMsg = 'The video requested was not found.';
                    break;
                case 101:
                case 150:
                    errorMsg = 'The owner of the requested video does not allow it to be played in embedded players.';
                    break;
            }
            this.logError('Youtube Error' + errorCode + ': ' + errorMsg);
        },
        playVideo: function () {
            this.player.playVideo();
            this.trackEvent('Play');
            this.fadeOutVideoPoster();
        },
        trackEvent: function (action) {
            if (!this.settings.googleAnalytics || $.inArray(action, this.trackedEvents) !== -1) {
                return false;
            }
            this.trackedEvents.push(action);

            var trackingData = {
                hitType: 'event',
                eventCategory: this.settings.gaCategory,
                eventLabel: this.videoTitle,
                eventAction: action
            };

            if (typeof window[this.settings.dataLayerName] !== 'undefined') {
                window[this.settings.dataLayerName].push({
                    'event': trackingData.eventCategory,
                    'attributes': {
                        'videoTitle': trackingData.eventLabel,
                        'videoAction': trackingData.eventAction
                    }
                });
            }
            if (typeof window['GoogleAnalyticsObject'] !== 'undefined') {
                var _ga = window['GoogleAnalyticsObject'];
                window[_ga]('send', trackingData);
            }

        },
        logError: function (message) {
            if (this.settings.debug && typeof console !== 'undefined' && typeof console.error !== 'undefined') {
                console.error(arguments.callee.caller, message);
            }
        }
    };

    $.fn[youTubePlayer] = function (options) {
        var tag = document.createElement('script');
        tag.src = 'https://www.youtube.com/iframe_api';
        $('script:first').before(tag);

        window.onYouTubeIframeAPIReady = function () {
            return this.each(function () {
                if (!$.data(this, 'plugin_' + youTubePlayer)) {
                    $.data(this, 'plugin_' + youTubePlayer, new YTPlayer(this, options));
                }
            })
        }.bind(this);
    };
})(jQuery, window, document);


