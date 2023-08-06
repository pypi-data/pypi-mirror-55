//firebase init
PyDoc_STRVAR(firebaseInit_doc,
	"init the Firebase system \n"\
	"\n"\
	"firebase.init()");

//firebase release
PyDoc_STRVAR(firebaseRelease_doc,
	"release the Firebase system\n"\
	"\n"\
	"firebase.release()");

//firebase testcase
PyDoc_STRVAR(firebaseTestcase_doc,
	"The testcase for firebase\n"\
	"\n"\
	"firebase.testcase()");

//firebase analytics init
PyDoc_STRVAR(firebaseAnalyticsInit_doc,
	"init the Firebase Analytics system \n"\
	"\n"\
	"firebaseAnalytics.init()");

//firebase analytics release
PyDoc_STRVAR(firebaseAnalyticsRelease_doc,
	"release the Firebase Anlytics system\n"\
	"\n"\
	"firebaseAnalytics.release()");

//firebase analytics testcase
PyDoc_STRVAR(firebaseAnalyticsTestcase_doc,
	"The testcase for firebase analytics\n"\
	"\n"\
	"firebaseAnalytics.testcase()");

// firebase analytics setUserProperty
PyDoc_STRVAR(firebaseAnalyticsSetUserProperty_doc,
	"Set a user property to the given value.\n"\
	"\n"\
	"firebaseAnalytics.setUserProperty(name, property)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    name : string\n"\
	"        Name of the user property to set\n"\
	"    property : string\n"\
	"        Value to set the user property to. Set this argument to NULL or nullptr to remove the user property.  The value can be between 1 to 100 characters long.");

// firebase analytics setUserId
PyDoc_STRVAR(firebaseAnalyticsSetUserId_doc,
	"Sets the user ID property.\n"\
	"\n"\
	"firebaseAnalytics.setUserId(user_id)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    user_id : string\n"\
	"        The user ID associated with the user of this app on this device.  The user ID must be non-empty and no more than 256 characters long. Setting user_id to NULL or nullptr removes the user ID.");

// firebase analytics SetCurrentScreen
PyDoc_STRVAR(firebaseAnalyticsSetCurrentScreen_doc,
	"Sets the current screen name and screen class, which specifies the current visual context in your app. This helps identify the areas in your app where users spend their time and how they interact with your app.\n"\
	"\n"\
	"firebaseAnalytics.setCurrentScreen(screen_name, screen_class)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    screen_name : string\n"\
	"        The name of the current screen. Set to nullptr to clear the current screen name. Limited to 100 characters.\n"\
	"    screen_class : string\n"\
	"        The name of the screen class. If you specify nullptr for this, it will use the default. On Android, the default is the class name of the current Activity. On iOS, the default is the class name of the current UIViewController. Limited to 100 characters.");
    
//firebase admob init
PyDoc_STRVAR(firebaseAdmobInit_doc,
	"init the Firebase Admob system \n"\
	"\n"\
	"firebaseAdmob.init(adMobApp, bannerSize, gender, childDirectedTreatment, keywords, birthday, testDevicesIds)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    adMobApp : tuple\n"\
	"        4 Parameters : adMobAppID(char*) | bannerAdUnit(char*) | interstitialAdUnit(char*) | rewardedVideoAdUnit(char*)\n"\
	"    bannerSize : tuple (optional)\n"\
	"        The ads size for the BannerView.\n"\
	"        2 Parameters : width(int) | height(int)\n"\
    "    gender : int (optional)\n"\
	"        If the app is aware of the user's gender, it can be added to the targeting information. Otherwise, 'unknown' should be used.\n"\
	"        kGenderUnknown = 0, kGenderMale = 1, kGenderFemale = 2\n"\
    "    childDirectedTreatment : int (optional)\n"\
	"        Indicates whether an ad request is considered tagged for child-directed treatment.\n"\
	"        kChildDirectedTreatmentStateUnknown = 0, kChildDirectedTreatmentStateTagged = 1, kChildDirectedTreatmentStateNotTagged = 2\n"\
    "    keywords : tuple (optional)\n"\
	"        Keywords to be used in targeting.\n"\
    "    birthday : tuple (optional)\n"\
	"        The user's birthday, if known. Note that months are indexed from one.\n"\
	"        3 Parameters : day(int) | month(int) | year(int)\n"\
    "    testDevicesIds : tuple (optional)\n"\
	"        It's important to register the device IDs associated with any devices that will be used to test the app. This ensures that regardless of the ad unit ID, those devices will always receive test ads in compliance with AdMob policy.\n"\
    "Examples\n"\
	"----------\n"\
	"    fb_admob.init(('YOUR_IOS_ADMOB_APP_ID', 'ca-app-pub-3940256099942544/2934735716', 'ca-app-pub-3940256099942544/4411468910', 'ca-app-pub-3940256099942544/6386090517'), (320, 50), 1, 1, ('game', 'casual', 'hyper casual', 'mobile'), (1, 1, 2020), ('112F1C63CDDE8BAAEE287FDE3BA4C662',));\n"\
    );

//firebase admob release
PyDoc_STRVAR(firebaseAdmobRelease_doc,
	"release the Firebase Admob system\n"\
	"\n"\
	"firebaseAdmob.release()");

//firebase admob testcase
PyDoc_STRVAR(firebaseAdmobTestcase_doc,
	"The testcase for firebase Admob\n"\
	"\n"\
	"firebaseAdmob.testcase()");

// firebase admob showBanner
PyDoc_STRVAR(firebaseAdmobShowBanner_doc,
	"Loading then showing the banner ad.\n"\
	"\n"\
	"firebaseAdmob.showBanner(reload, timeout)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    reload : bool (optional)\n"\
	"        True <- (default)\n"\
	"        When it is True, it need to load an new ads\n"\
	"    timeout : int (optional)\n"\
	"        Value in (msec) to wait for the loading completion. It's helpful only when the reload parameter is True");

// firebase admob bannerMoveTo
PyDoc_STRVAR(firebaseAdmobBannerMoveTo_doc,
	"Moves the @ref BannerView so that its top-left corner is located at (x, y). Coordinates are in pixels from the top-left corner of the screen..\n"\
	"\n"\
	"firebaseAdmob.bannerMoveTo(x, y)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    x : int\n"\
	"        The desired horizontal coordinate.\n"\
	"    y : int\n"\
	"        The desired vertical coordinate.\n"\
    "Moves the @ref BannerView so that it's located at the given pre-defined position.\n"\
	"\n"\
	"firebaseAdmob.bannerMoveTo(position)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    position : int\n"\
	"        Top of the screen, horizontally centered. -> kPositionTop = 0,\n"\
	"        Bottom of the screen, horizontally centered. ->	kPositionBottom,\n"\
	"        Top-left corner of the screen. -> kPositionTopLeft,\n"\
	"        Top-right corner of the screen. -> kPositionTopRight,\n"\
	"        Bottom-left corner of the screen. -> kPositionBottomLeft,\n"\
	"        Bottom-right corner of the screen. -> kPositionBottomRight.");

//firebase admob hideBanner
PyDoc_STRVAR(firebaseAdmobHideBanner_doc,
	"Hides the BannerView.\n"\
	"\n"\
	"firebaseAdmob.hideBanner()");
    
// firebase admob showInterstitial
PyDoc_STRVAR(firebaseAdmobShowInterstitial_doc,
	"Loading then showing the InterstitialAd ad.\n"\
	"\n"\
	"firebaseAdmob.showInterstitial(reload, timeout)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    reload : bool (optional)\n"\
	"        True <- (default)\n"\
	"        When it is True, it need to load an new ads\n"\
	"    timeout : int (optional)\n"\
	"        Value in (msec) to wait for the loading completion.");
    
// firebase admob showRewardedVideo
PyDoc_STRVAR(firebaseAdmobShowRewardedVideo_doc,
	"Loading then showing the RewardedVideo ad.\n"\
	"\n"\
	"firebaseAdmob.showRewardedVideo(reload, timeout)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    reload : bool (optional)\n"\
	"        True <- (default)\n"\
	"        When it is True, it need to load an new ads\n"\
	"    timeout : int (optional)\n"\
	"        Value in (msec) to wait for the loading completion.");
    
//firebase admob pauseRewardedVideo
PyDoc_STRVAR(firebaseAdmobPauseRewardedVideo_doc,
	"Pauses any background processing associated with rewarded video. Should be called whenever the C++ engine pauses or the application loses focus.\n"\
	"\n"\
	"firebaseAdmob.pauseRewardedVideo()");
    
//firebase admob resumeRewardedVideo
PyDoc_STRVAR(firebaseAdmobResumeRewardedVideo_doc,
	"Resumes the rewarded video system after pausing.\n"\
	"\n"\
	"firebaseAdmob.resumeRewardedVideo()");
    
//firebase auth init
PyDoc_STRVAR(firebaseAuthInit_doc,
	"init the Firebase Auth system \n"\
	"\n"\
	"firebaseAuth.init()");

//firebase auth release
PyDoc_STRVAR(firebaseAuthRelease_doc,
	"release the Firebase Auth system\n"\
	"\n"\
	"firebaseAuth.release()");

//firebase auth testcase
PyDoc_STRVAR(firebaseAuthTestcase_doc,
	"The testcase for firebase Auth\n"\
	"\n"\
	"firebaseAuth.testcase()");
    
// firebase auth signInWithEmailAndPassword
PyDoc_STRVAR(firebaseAuthSignInWithEmailAndPassword_doc,
	"Signs in using provided email address and password.\n"\
	"\n"\
	"firebaseAuth.signInWithEmailAndPassword(username, password)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    username : string\n"\
	"    password : string\n"\
    "Returns\n"\
	"-------\n"\
	"    result : bool");
    
// firebase auth signOut
PyDoc_STRVAR(firebaseAuthSignOut_doc,
	"Removes any existing authentication credentials from this client.\n"\
	"\n"\
	"firebaseAuth.signOut()\n"\
	"\n"\
    "Returns\n"\
	"-------\n"\
	"    result : bool");
    
// firebase auth isPlayerAuthenticated
PyDoc_STRVAR(firebaseAuthIsPlayerAuthenticated_doc,
	"return true if the user is signed in, false otherwise.\n"\
	"\n"\
	"firebaseAuth.isPlayerAuthenticated()\n"\
	"\n"\
    "Returns\n"\
	"-------\n"\
	"    result : bool");
    
// firebase auth registerWithEmailAndPassword
PyDoc_STRVAR(firebaseAuthRegisterWithEmailAndPassword_doc,
	"Creates, and on success, logs in a user with the given email address and password..\n"\
    "An error is returned when account creation is unsuccessful (due to another existing account, invalid password, etc.)..\n"\
	"\n"\
	"firebaseAuth.registerWithEmailAndPassword(username, password)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    username : string\n"\
	"    password : string\n"\
    "Returns\n"\
	"-------\n"\
	"    result : bool");