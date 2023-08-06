#include "FirebaseAdmob.h"

#include "firebase/admob/interstitial_ad.h"
#include "firebase/admob/rewarded_video.h"
#include "firebase/admob/types.h"
#include "firebase/app.h"
#include "firebase/future.h"

// The AdMob app IDs for the test app.
#if defined(__ANDROID__)
// If you change the AdMob app ID for your Android app, make sure to change it
// in AndroidManifest.xml as well.
const char* kAdMobAppID = "ca-app-pub-1009273426450955~3020262852";
#else
// If you change the AdMob app ID for your iOS app, make sure to change the
// value for "GADApplicationIdentifier" in your Info.plist as well.
const char* kAdMobAppID = "YOUR_IOS_ADMOB_APP_ID";
#endif

// These ad units IDs have been created specifically for testing, and will
// always return test ads.
#if defined(__ANDROID__)
const char* kBannerAdUnit = "ca-app-pub-3940256099942544/6300978111";
const char* kInterstitialAdUnit = "ca-app-pub-3940256099942544/1033173712";
const char* kRewardedVideoAdUnit = "ca-app-pub-3940256099942544/2888167318";
#else
const char* kBannerAdUnit = "ca-app-pub-3940256099942544/2934735716";
const char* kInterstitialAdUnit = "ca-app-pub-3940256099942544/4411468910";
const char* kRewardedVideoAdUnit = "ca-app-pub-3940256099942544/6386090517";
#endif

// Standard mobile banner size is 320x50.
static const int kBannerWidth = 320;
static const int kBannerHeight = 50;

// Sample keywords to use in making the request.
static const char* kKeywords[] = { "AdMob", "C++", "Fun" };

// Sample test device IDs to use in making the request.
static const char* kTestDeviceIDs[] = { "2077ef9a63d2b398840261c8221a0c9b",
									   "098fe087d987c9a878965454a65654d7" };

// Sample birthday value to use in making the request.
static const int kBirthdayDay = 10;
static const int kBirthdayMonth = 11;
static const int kBirthdayYear = 1976;

extern WindowContext FirebaseGetWindowContext();

// A simple listener that logs changes to a BannerView.
class LoggingBannerViewListener : public admob::BannerView::Listener {
public:
	LoggingBannerViewListener() {}
	void OnPresentationStateChanged(
		admob::BannerView* banner_view,
		admob::BannerView::PresentationState state) override {
		LOG("BannerView PresentationState has changed to %d.", state);
	}
	void OnBoundingBoxChanged(admob::BannerView* banner_view,
		admob::BoundingBox box) override {
		LOG(
			"BannerView BoundingBox has changed to (x: %d, y: %d, width: %d, "
			"height %d).",
			box.x, box.y, box.width, box.height);
	}
};

// A simple listener that logs changes to an InterstitialAd.
class LoggingInterstitialAdListener
	: public admob::InterstitialAd::Listener {
public:
	LoggingInterstitialAdListener() {}
	void OnPresentationStateChanged(
		admob::InterstitialAd* interstitial_ad,
		admob::InterstitialAd::PresentationState state) override {
		LOG("InterstitialAd PresentationState has changed to %d.", state);
	}
};

// A simple listener that logs changes to rewarded video state.
class LoggingRewardedVideoListener
	: public admob::rewarded_video::Listener {
public:
	LoggingRewardedVideoListener() {}
	void OnRewarded(admob::rewarded_video::RewardItem reward) override {
		LOG("Rewarding user with %f %s.", reward.amount,
			reward.reward_type.c_str());
	}
	void OnPresentationStateChanged(
		admob::rewarded_video::PresentationState state) override {
		LOG("Rewarded video PresentationState has changed to %d.", state);
	}
};

FirebaseAdmob::FirebaseAdmob()
	: m_AdMobAppID(kAdMobAppID)
	, m_BannerAdUnit(kBannerAdUnit)
	, m_InterstitialAdUnit(kInterstitialAdUnit)
	, m_RewardedVideoAdUnit(kRewardedVideoAdUnit)
	, m_Gender(admob::kGenderUnknown)
	, m_ChildDirectedTreatmentState(admob::kChildDirectedTreatmentStateTagged)
	, m_BannerWidth(kBannerWidth)
	, m_BannerHeight(kBannerHeight)
	, m_Keywords(kKeywords)
	, m_KeywordCount(sizeof(kKeywords) / sizeof(kKeywords[0]))
	, m_TestDeviceIds(kTestDeviceIDs)
	, m_TestDeviceIdCount(sizeof(kTestDeviceIDs) / sizeof(kTestDeviceIDs[0]))
	, m_BirthdayDay(kBirthdayDay)
	, m_BirthdayMonth(kBirthdayMonth)
	, m_BirthdayYear(kBirthdayYear)
	, banner(nullptr)
	, interstitial(nullptr)
	, request()
	, banner_listener(nullptr)
	, interstitial_listener(nullptr)
	, rewarded_listener(nullptr)
{
	LOG("FirebaseAdmob()");
}
FirebaseAdmob::~FirebaseAdmob()
{
	LOG("~FirebaseAdmob()");
}

void FirebaseAdmob::setAdMobApp(const char* adMobAppID, const char* bannerAdUnit, const char* interstitialAdUnit, const char* rewardedVideoAdUnit)
{
	m_AdMobAppID = adMobAppID;
	m_BannerAdUnit = bannerAdUnit;
	m_InterstitialAdUnit = interstitialAdUnit;
	m_RewardedVideoAdUnit = rewardedVideoAdUnit;
}

void FirebaseAdmob::setBannerSize(uint32_t width, uint32_t height)
{
	m_BannerWidth = width;
	m_BannerHeight = height;
}

void FirebaseAdmob::setGender(admob::Gender gender)
{
	m_Gender = gender;
}

void FirebaseAdmob::setChildDirectedTreatmentState(admob::ChildDirectedTreatmentState state)
{
	m_ChildDirectedTreatmentState = state;
}

void FirebaseAdmob::setKeywords(uint32_t count, const char** keywords)
{
	m_KeywordCount = count;
	m_Keywords = keywords;
}

void FirebaseAdmob::setTestDeviceIds(uint32_t count, const char** testDeviceIds)
{
	m_TestDeviceIdCount = count;
	m_TestDeviceIds = testDeviceIds;
}

void FirebaseAdmob::setBirthday(uint32_t day, uint32_t month, uint32_t year)
{
	m_BirthdayDay = day;
	m_BirthdayMonth = month;
	m_BirthdayYear = year;
}

void FirebaseAdmob::init()
{
	banner_listener = new LoggingBannerViewListener();
	interstitial_listener = new LoggingInterstitialAdListener();
	rewarded_listener = new LoggingRewardedVideoListener();

	LOG("Initializing the AdMob with Firebase API.");
	admob::Initialize(*firebase_app, m_AdMobAppID);
	
	// If the app is aware of the user's gender, it can be added to the targeting
	// information. Otherwise, "unknown" should be used.
	request.gender = m_Gender;

	// This value allows publishers to specify whether they would like the request
	// to be treated as child-directed for purposes of the Children’s Online
	// Privacy Protection Act (COPPA).
	// See http://business.ftc.gov/privacy-and-security/childrens-privacy.
	request.tagged_for_child_directed_treatment = m_ChildDirectedTreatmentState;

	// The user's birthday, if known. Note that months are indexed from one.
	request.birthday_day = m_BirthdayDay;
	request.birthday_month = m_BirthdayMonth;
	request.birthday_year = m_BirthdayYear;

	// Additional keywords to be used in targeting.
	request.keyword_count = m_KeywordCount;
	request.keywords = m_Keywords;

	// This example uses ad units that are specially configured to return test ads
	// for every request. When using your own ad unit IDs, however, it's important
	// to register the device IDs associated with any devices that will be used to
	// test the app. This ensures that regardless of the ad unit ID, those
	// devices will always receive test ads in compliance with AdMob policy.
	//
	// Device IDs can be obtained by checking the logcat or the Xcode log while
	// debugging. They appear as a long string of hex characters.
	request.test_device_id_count = m_TestDeviceIdCount;
	request.test_device_ids = m_TestDeviceIds;

	// Create an ad size for the BannerView.
	admob::AdSize banner_ad_size;
	banner_ad_size.ad_size_type = admob::kAdSizeStandard;
	banner_ad_size.width = m_BannerWidth;
	banner_ad_size.height = m_BannerHeight;

	LOG("Creating the BannerView.");	
	banner = new admob::BannerView();
	auto banner_future_result = banner->Initialize(FirebaseGetWindowContext(), kBannerAdUnit, banner_ad_size);
	WaitForFutureCompletion(banner_future_result);
	if (banner_future_result.status() == ::firebase::kFutureStatusComplete)
	{
		banner->SetListener(banner_listener);
	}

	LOG("Creating the InterstitialAd.");
	interstitial = new admob::InterstitialAd();
	auto interstitial_future_result = interstitial->Initialize(FirebaseGetWindowContext(), kInterstitialAdUnit);
	WaitForFutureCompletion(interstitial_future_result);
	if (interstitial_future_result.status() == ::firebase::kFutureStatusComplete)
	{	
		interstitial->SetListener(interstitial_listener);
	}	

	LOG("Initializing rewarded video.");
	auto rewarded_future_result = rewarded_video::Initialize();

	WaitForFutureCompletion(rewarded_future_result);
	if (rewarded_future_result.status() == ::firebase::kFutureStatusComplete)
	{	
		rewarded_video::SetListener(rewarded_listener);
	}
}

void FirebaseAdmob::release()
{
	LOG("FirebaseAdmob::release()");
	
	// cleanup the listener
	delete banner_listener;
	delete interstitial_listener;
	delete rewarded_listener;

	delete banner;
	delete interstitial;
	rewarded_video::Destroy();
	admob::Terminate();
}

void FirebaseAdmob::showBanner(bool reload, int timeout)
{
	if (reload)
	{		
		LOG("Loading a banner ad.");
		banner->LoadAd(request);
		WaitForFutureCompletion(banner->LoadAdLastResult(), timeout);
	}

	LOG("Showing the banner ad.");
	banner->Show();
	WaitForFutureCompletion(banner->ShowLastResult());
}

void FirebaseAdmob::bannerMoveTo(admob::BannerView::Position position)
{
	banner->MoveTo(position);
	WaitForFutureCompletion(banner->MoveToLastResult());
}

void FirebaseAdmob::bannerMoveTo(int x, int y)
{
	banner->MoveTo(x, y);
	WaitForFutureCompletion(banner->MoveToLastResult());
}

void FirebaseAdmob::hideBanner()
{	
	banner->Hide();
	WaitForFutureCompletion(banner->HideLastResult());
}

void FirebaseAdmob::showInterstitial(bool reload, int timeout)
{
	if (reload)
	{
		LOG("Loading an interstitial ad.");
		interstitial->LoadAd(request);

		WaitForFutureCompletion(interstitial->LoadAdLastResult(), timeout);
	}	

	LOG("Showing the interstitial ad.");
	interstitial->Show();
	WaitForFutureCompletion(interstitial->ShowLastResult(), timeout);

	// Wait for the user to close the interstitial.
	while (interstitial->presentation_state() !=
		admob::InterstitialAd::PresentationState::
		kPresentationStateHidden) {
		ProcessEvents(1000);
	}
}

void FirebaseAdmob::showRewardedVideo(bool reload, int timeout)
{
	if (reload)
	{
		LOG("Loading a rewarded video ad.");
		rewarded_video::LoadAd(m_RewardedVideoAdUnit, request);

		WaitForFutureCompletion(rewarded_video::LoadAdLastResult(), timeout);
	}

	if (rewarded_video::LoadAdLastResult().error() == admob::kAdMobErrorNone)
	{
		LOG("Showing a rewarded video ad.");
		rewarded_video::Show(FirebaseGetWindowContext());
	}
	WaitForFutureCompletion(rewarded_video::ShowLastResult(), timeout);
}

void FirebaseAdmob::pauseRewardedVideo()
{
	rewarded_video::Pause();
	WaitForFutureCompletion(rewarded_video::PauseLastResult());
}

void FirebaseAdmob::resumeRewardedVideo()
{
	rewarded_video::Resume();
	WaitForFutureCompletion(rewarded_video::ResumeLastResult());
}

void FirebaseAdmob::testcase()
{
	showBanner();

	WaitForFutureCompletion(banner->ShowLastResult());

	// Move to each of the six pre-defined positions.
	bannerMoveTo(admob::BannerView::kPositionTop);
	WaitForFutureCompletion(banner->MoveToLastResult());

	bannerMoveTo(admob::BannerView::kPositionTopLeft);
	WaitForFutureCompletion(banner->MoveToLastResult());

	bannerMoveTo(admob::BannerView::kPositionTopRight);
	WaitForFutureCompletion(banner->MoveToLastResult());

	bannerMoveTo(admob::BannerView::kPositionBottom);
	WaitForFutureCompletion(banner->MoveToLastResult());

	bannerMoveTo(admob::BannerView::kPositionBottomLeft);
	WaitForFutureCompletion(banner->MoveToLastResult());

	bannerMoveTo(admob::BannerView::kPositionBottomRight);
	WaitForFutureCompletion(banner->MoveToLastResult());

	// Try some coordinate moves.
	bannerMoveTo(100, 300);
	WaitForFutureCompletion(banner->MoveToLastResult());

	bannerMoveTo(100, 400);
	WaitForFutureCompletion(banner->MoveToLastResult());

	// Try hiding and showing the BannerView.
	hideBanner();
	WaitForFutureCompletion(banner->HideLastResult());

	showBanner();
	WaitForFutureCompletion(banner->ShowLastResult());

	// A few last moves after showing it again.
	bannerMoveTo(100, 300);
	WaitForFutureCompletion(banner->MoveToLastResult());

	bannerMoveTo(100, 400);
	WaitForFutureCompletion(banner->MoveToLastResult());

	banner->Hide();
	WaitForFutureCompletion(banner->HideLastResult());
	
	// When the InterstitialAd is initialized, load an ad.
	showInterstitial();
	WaitForFutureCompletion(interstitial->ShowLastResult(), 5000);

	// Wait for the user to close the interstitial.
	while (interstitial->presentation_state() !=
		admob::InterstitialAd::PresentationState::
		kPresentationStateHidden) {
		ProcessEvents(1000);
	}

	// Loading a rewarded video ad.
	showRewardedVideo();

	WaitForFutureCompletion(rewarded_video::LoadAdLastResult(), 10000);

	// Normally Pause and Resume would be called in response to the app pausing
	// or losing focus. This is just a test.
	pauseRewardedVideo();
	WaitForFutureCompletion(rewarded_video::PauseLastResult());

	resumeRewardedVideo();
	WaitForFutureCompletion(rewarded_video::ResumeLastResult());

	LOG("Done!");
}