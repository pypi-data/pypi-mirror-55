#include "FirebaseAnalytics.h"

#include "firebase/analytics/event_names.h"
#include "firebase/analytics/parameter_names.h"
#include "firebase/analytics/user_property_names.h"

namespace analytics = ::firebase::analytics;

FirebaseAnalytics::FirebaseAnalytics()
{
	LOG("FirebaseAnalytics()");
}
FirebaseAnalytics::~FirebaseAnalytics()
{
	LOG("~FirebaseAnalytics()");
}

void FirebaseAnalytics::init()
{	
	analytics::Initialize(*firebase_app);
	analytics::SetAnalyticsCollectionEnabled(true);
	// App session times out after 30 minutes.
	// If the app is placed in the background and returns to the foreground after
	// the timeout is expired analytics will log a new session.
	setSessionTimeoutDuration(1000 * 60 * 30);
}

void FirebaseAnalytics::release()
{
	LOG("FirebaseAnalytics::release()");
	analytics::Terminate();	
}

void FirebaseAnalytics::setSessionTimeoutDuration(int64_t milliseconds)
{
	analytics::SetSessionTimeoutDuration(milliseconds);
}

void FirebaseAnalytics::setUserProperty(const char* name, const char* property)
{
	analytics::SetUserProperty(name, property);
}

void FirebaseAnalytics::setUserId(const char* user_id)
{
	analytics::SetUserId(user_id);
}

void FirebaseAnalytics::setCurrentScreen(const char* screen_name, const char* screen_class)
{
	analytics::SetCurrentScreen(screen_name, screen_class);
}

void FirebaseAnalytics::logEvent(const char* name)
{
	analytics::LogEvent(name);
}

void FirebaseAnalytics::logEvent(const char* name, const char* parameter_name, const double parameter_value)
{
	analytics::LogEvent(name, parameter_name, parameter_value);
}

void FirebaseAnalytics::logEvent(const char* name, const char* parameter_name, const int parameter_value)
{
	analytics::LogEvent(name, parameter_name, parameter_value);
}

void FirebaseAnalytics::logEvent(const char* name, const char* parameter_name, const char* parameter_value)
{
	analytics::LogEvent(name, parameter_name, parameter_value);
}

void FirebaseAnalytics::logEvent(const char* name, const analytics::Parameter* parameters, size_t number_of_parameters)
{
	analytics::LogEvent(name, parameters, number_of_parameters);
}

void FirebaseAnalytics::logEvent(const char* name, const analytics::Parameter* parameters)
{
	analytics::LogEvent(name, parameters, sizeof(parameters) / sizeof(parameters[0]));
}

void FirebaseAnalytics::testcase()
{
	LOG("Get App Instance ID...");
	auto future_result = analytics::GetAnalyticsInstanceId();
	WaitForFutureCompletion(future_result);	

	LOG("Set user properties.");
	// Set the user's sign up method.
	setUserProperty(analytics::kUserPropertySignUpMethod, "Google");
	// Set the user ID.
	setUserId("uber_user_510");

	LOG("Set current screen.");
	// Set the user's current screen.
	setCurrentScreen("Firebase Analytics C++ testapp", "testapp");
	
	LOG("Log login event.");
	// Log an event with no parameters.
	logEvent(analytics::kEventLogin);
	
	LOG("Log progress event.");
	// Log an event with a floating point parameter.
	logEvent("progress", "percent", 0.4f);
	
	LOG("Log post score event.");
	// Log an event with an integer parameter.
	logEvent(analytics::kEventPostScore, analytics::kParameterScore, 42);
		
	LOG("Log group join event.");
	// Log an event with a string parameter.
	logEvent(analytics::kEventJoinGroup, analytics::kParameterGroupID, "spoon_welders");
	
	LOG("Log level up event.");
	// Log an event with multiple parameters.
	{
		const analytics::Parameter kLevelUpParameters[] = {
			analytics::Parameter(analytics::kParameterLevel, 5),
			analytics::Parameter(analytics::kParameterCharacter, "mrspoon"),
			analytics::Parameter("hit_accuracy", 3.14f),
		};
		logEvent(analytics::kEventLevelUp, kLevelUpParameters, sizeof(kLevelUpParameters) / sizeof(kLevelUpParameters[0]));
	}

	LOG("The Firebase Analytics Testcase Complete");
}