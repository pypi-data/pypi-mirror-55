#pragma once
#include "Firebase.h"
#include "firebase/admob.h"
#include "firebase/admob/banner_view.h"

namespace admob = firebase::admob;
namespace rewarded_video = admob::rewarded_video;
class LoggingBannerViewListener;
class LoggingInterstitialAdListener;
class LoggingRewardedVideoListener;

class IGE_EXPORT FirebaseAdmob : public Firebase
{
public:
	FirebaseAdmob();
	~FirebaseAdmob();
	void init();
	void release();
	void testcase();

	void showBanner(bool reload = true, int timeout = 1000);
	void bannerMoveTo(admob::BannerView::Position position);
	void bannerMoveTo(int x, int y);
	void hideBanner();

	void showInterstitial(bool reload = true, int timeout = 2000);

	void showRewardedVideo(bool reload = true, int timeout = 5000);
	void pauseRewardedVideo();
	void resumeRewardedVideo();

	void setAdMobApp(const char* adMobAppID, const char* bannerAdUnit, const char* interstitialAdUnit, const char* rewardedVideoAdUnit);
	void setBannerSize(uint32_t width, uint32_t height);
	void setGender(admob::Gender gender);
	void setChildDirectedTreatmentState(admob::ChildDirectedTreatmentState state);
	void setKeywords(uint32_t count, const char** keywords);
	void setTestDeviceIds(uint32_t count, const char** testDeviceIds);
	void setBirthday(uint32_t day, uint32_t month, uint32_t year);
private:
	const char* m_AdMobAppID;
	const char* m_BannerAdUnit;
	const char* m_InterstitialAdUnit;
	const char* m_RewardedVideoAdUnit;
	admob::Gender m_Gender;
	admob::ChildDirectedTreatmentState m_ChildDirectedTreatmentState;
	uint32_t m_BannerWidth;
	uint32_t m_BannerHeight;
	const char** m_Keywords;
	uint32_t m_KeywordCount;
	const char** m_TestDeviceIds;
	uint32_t m_TestDeviceIdCount;
	uint32_t m_BirthdayDay;
	uint32_t m_BirthdayMonth;
	uint32_t m_BirthdayYear;

	firebase::admob::BannerView* banner;
	firebase::admob::InterstitialAd* interstitial;
	firebase::admob::AdRequest request;

	LoggingBannerViewListener* banner_listener;
	LoggingInterstitialAdListener* interstitial_listener;
	LoggingRewardedVideoListener* rewarded_listener;
};

